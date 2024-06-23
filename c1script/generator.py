"""
Generation of assembly output from syntax tree
"""

import math, copy
from c1script.nodes import *
import c1script.mappings
import decimal

class VarData:
    def __init__(self, name, kind, index):
        self.name = name
        self.kind = kind
        self.index = index

class Generator:
    MAGIC_VALUE = 65536

    def __init__(self, tree, strat_index = 0, skip_entry = False, skip_end = False):
        self.tree = tree
        self.asm = ""
        self.labels = {}
        self.cur_strat_index = strat_index
        self.skip_entry = skip_entry
        self.skip_end = skip_end
        self.init_vars()

    def generate(self):
        self.comment("=" * 78)
        self.comment("")
        self.comment("Strat file <STRAT_NAME_PLACEHOLDER>")
        self.comment("")
        self.comment("=" * 78)
        self.newline()

        self.generate_file(self.tree)

        self.newline()

        return self.asm, self.cur_strat_index

    def generate_file(self, node):
        self.assert_type(node, NodeFile)

        if not self.skip_entry:
            self.asm += "@entry 4\n\n"

        for unit in node.units:
            self.generate_unit(unit)

        if not self.skip_end:
            self.newline()
            self.write_line("FileEnd")

        self.write_var_size()

    def generate_unit(self, node):
        self.assert_type(node, NodeUnit)

        if isinstance(node, NodeConst):
            self.generate_const(node)
        elif isinstance(node, NodePreload):
            self.generate_preload(node)
        elif isinstance(node, NodeUse):
            self.generate_use(node)
        elif isinstance(node, NodeGlobalVar):
            self.generate_global_var(node)
        elif isinstance(node, NodeProc):
            self.generate_proc(node)
        elif isinstance(node, NodeTrigger):
            self.generate_trigger(node)
        elif isinstance(node, NodeStrat):
            self.generate_strat(node)
        else:
            raise Exception(f"Unknown unit type for #{node}")

    def generate_const(self, node):
        self.assert_type(node, NodeConst)

        self.comment(f"constant {node.name.identifier} evaluated to {node.name.result}")

    def generate_preload(self, node):
        self.assert_type(node, NodePreload)

        self.asm += f"@preload {node.strat.result}\n"

    def generate_use(self, node):
        self.assert_type(node, NodeUse)

        self.allocate_var(node.alias.identifier, node.kind.identifier, node.index.result)
        self.comment(f"using {node.kind.identifier}[{node.index.result}] as {node.alias.identifier}")

    def generate_global_var(self, node):
        self.assert_type(node, NodeGlobalVar)

        kind, index = self.allocate_var(node.name.identifier)
        self.comment(f"global var {node.name.identifier} ({kind}[{index}])")

    def generate_proc(self, node):
        self.assert_type(node, NodeProc)

        self.separate()
        self.set_label(f"proc_{node.name.identifier}", node.name.identifier)

        self.generate_block(node.block)

        self.write_line("EndProc")

    def generate_trigger(self, node):
        self.assert_type(node, NodeTrigger)

        self.separate()
        self.set_label(f"trigger_{node.name.identifier}", node.name.identifier)

        self.generate_block(node.block)

        self.write_line("EndTrigger")

    def generate_strat(self, node):
        self.assert_type(node, NodeStrat)

        self.separate()
        self.newline()

        label = f"strat_{node.name.identifier}"
        self.asm += f"@strat{self.cur_strat_index}_name {node.name.identifier}\n"
        self.asm += f"@strat{self.cur_strat_index}_pc {label}\n"
        self.asm += f"@strat{self.cur_strat_index}_vars <STRAT_VARS_PLACEHOLDER>\n" # To be rewritten
        self.cur_strat_index += 1

        self.asm = self.asm.replace("<STRAT_NAME_PLACEHOLDER>", node.name.identifier)
        
        self.set_label(label)

        self.generate_block(node.block)

        self.write_line("Remove")

    def generate_block(self, node):
        self.assert_type(node, NodeBlock)

        var_locs = copy.deepcopy(self.var_locs)

        for statement in node.statements:
            self.generate_statement(statement)

        self.var_locs = var_locs

    def generate_statement(self, node):
        self.assert_type(node, NodeStatement)

        if isinstance(node, NodeCommand):
            self.generate_command(node)
        elif isinstance(node, NodeProcCall):
            self.generate_proc_call(node)
        elif isinstance(node, NodeAssignment):
            self.generate_assignment(node)
        elif isinstance(node, NodeVar):
            self.generate_var(node)
        elif isinstance(node, NodeControl):
            self.generate_control(node)
        else:
            raise Exception(f"Unknown statement type for #{node}")
        
    def generate_command(self, node):
        self.assert_type(node, NodeCommand)

        signature = c1script.mappings.COMMAND_MAP[node.name.identifier]

        self.start_line()
        self.generate_insn(node, signature)
        self.newline()

    def generate_proc_call(self, node):
        self.assert_type(node, NodeProcCall)

        self.write_line(f"ProcCall {self.labels[node.name.identifier]}")

    def generate_assignment(self, node):
        self.assert_type(node, NodeAssignment)

        if node.name.identifier not in self.var_locs:
            raise Exception(f"Unknown variable `{node.name.identifier}`")
        
        var_data = self.var_locs[node.name.identifier]
        
        self.start_line(c1script.mappings.VAR_MAP[var_data.kind]["let"])
        self.append_line(f"{var_data.index}")

        if node.operator == "=":
            self.generate_eval(node.expr)
        else:
            self.generate_eval(
                node.expr,
                prepend = f"{c1script.mappings.VAR_MAP[var_data.kind]['push']} {var_data.index}",
                append = c1script.mappings.BINARY_OPERATOR_MAP[node.operator[0]]
            )

        self.newline()

    def generate_var(self, node):
        self.assert_type(node, NodeVar)

        kind, index = self.allocate_var(node.name.identifier)
        self.start_line(c1script.mappings.VAR_MAP[kind]["let"])
        self.append_line(f"{index}")

        self.generate_eval(node.expr)

        self.comment(f"declaration of {node.name.identifier}")

    def generate_control(self, node):
        self.assert_type(node, NodeControl)

        if isinstance(node, NodeIf):
            self.generate_if(node)
        elif isinstance(node, NodeUnless):
            self.generate_unless(node)
        elif isinstance(node, NodeWhile):
            self.generate_while(node)
        elif isinstance(node, NodeRepeatUntil):
            self.generate_repeat_until(node)
        elif isinstance(node, NodeFor):
            self.generate_for(node)
        elif isinstance(node, NodeSwitch):
            self.generate_switch(node)
        else:
            raise Exception(f"Unknown control statement type for #{node}")
        
    def generate_if(self, node):
        self.assert_type(node, NodeIf)

        condition = node.condition
        block = node.block
        else_part = node.else_part
        insn = "If"

        if isinstance(node.condition, NodeSpecialCondition):
            insn = c1script.mappings.SPECIAL_CONDITIONS[node.condition.name]
            if node.condition.invert:
                block, else_part = else_part, block
                if block is None:
                    block = NodeBlock(None, [])

        if else_part is None:
            label_end = f"if_{node.loc.line}_{node.loc.pos}_end"

            self.start_line(insn)
            if insn == "If":
                self.generate_eval(condition)
            self.append_line(label_end)
            self.newline()

            self.generate_block(block)

            self.set_label(label_end)
        
        else:
            label_else = f"if_{node.loc.line}_{node.loc.pos}_else"
            label_end = f"if_{node.loc.line}_{node.loc.pos}_end"

            self.start_line(insn)
            if insn == "If":
                self.generate_eval(condition)
            self.append_line(label_else)
            self.newline()

            self.generate_block(block)
            
            self.start_line("Else")
            self.append_line(label_end)
            self.newline()

            self.set_label(label_else)

            if isinstance(else_part, NodeIf):
                self.generate_if(else_part)
            else:
                self.generate_block(else_part)

            self.set_label(label_end)
        
    def generate_unless(self, node):
        self.assert_type(node, NodeUnless)

        label_end = f"unless_{node.loc.line}_{node.loc.pos}_end"

        self.start_line("If")
        self.generate_eval(node.condition)
        self.append_line(label_end)
        self.newline()

        self.generate_block(node.block)

        self.set_label(label_end)
        
    def generate_while(self, node):
        self.assert_type(node, NodeWhile)

        label_end = f"while_{node.loc.line}_{node.loc.pos}_end"

        self.start_line("While")
        self.generate_eval(node.condition)
        self.append_line(label_end)
        self.newline()

        self.generate_block(node.block)

        self.write_line("EndWhileImm" if node.imm else "EndWhile")

        self.set_label(label_end)
        
    def generate_repeat_until(self, node):
        self.assert_type(node, NodeRepeatUntil)

        self.write_line("Repeat")

        self.generate_block(node.block)

        self.start_line("UntilImm" if node.imm else "Until")
        self.generate_eval(node.condition)
        self.newline()
        
    def generate_for(self, node):
        self.assert_type(node, NodeFor)

        var_locs = copy.deepcopy(self.var_locs)

        if node.var.identifier in self.var_locs:
            vl = self.var_locs[node.var.identifier]
            kind = vl.kind
            index = vl.index
        else:
            kind, index = self.allocate_var(node.var.identifier)

        self.start_line(f"For {c1script.mappings.VAR_MAP[kind]['kind_int']} {index}")
        self.generate_eval(node.start_value)
        self.generate_eval(node.end_value)
        self.newline()

        self.generate_block(node.block)

        self.var_locs = var_locs

        self.write_line("NextImm" if node.imm else "Next")
        
    def generate_switch(self, node):
        self.assert_type(node, NodeSwitch)

        self.start_line("Switch")
        self.generate_eval(node.expr)
        self.append_line(f"{len(node.cases)}")

        label_end = f"switch_{node.loc.line}_{node.loc.pos}_end"
        self.append_line(label_end)

        case_labels = []
        for case in node.cases:
            label = f"switch_{node.loc.line}_{node.loc.pos}_case_{case.loc.line}_{case.loc.pos}"
            case_labels.append(label)

            self.append_line(label)
            self.generate_eval(case.expr)
        self.newline()

        for i in range(len(node.cases)):
            case = node.cases[i]

            self.set_label(case_labels[i])

            self.generate_block(case.block)

            self.write_line(f"EndCase {label_end}")

        self.set_label(label_end)

    def generate_insn(self, node, signature):
        self.assert_type(node, NodeCommand | NodeFuncCall)

        sign = signature.signature

        if "varargs" in sign:
            varargs_pos = sign.index("varargs")
            varargs_count = len(node.args.args) - len(sign) + 1

            if varargs_count < 0:
                raise Exception("Signature mismatch")
            
            sign = sign[:varargs_pos] + ["eval"] * varargs_count + sign[varargs_pos + 1:]

        if "varargs_int" in sign:
            varargs_pos = sign.index("varargs_int")
            varargs_count = len(node.args.args) - len(sign) + 1

            if varargs_count < 0:
                raise Exception("Signature mismatch")
            
            sign = sign[:varargs_pos] + ["int16"] * varargs_count + sign[varargs_pos + 1:]

        if len(node.args.args) != len(sign):
            raise Exception("Signature mismatch")

        for i in range(len(sign)):
            type = sign[i]
            arg = node.args.args[i]

            if type == "stack":
                self.generate_expr(arg)

        self.append_line(signature.insn)

        for i in range(len(sign)):
            type = sign[i]
            arg = node.args.args[i]

            match type:
                case "int8": self.append_line(f"{arg.result}")
                case "int16": self.append_line(f"{arg.result}")
                case "int32": self.append_line(f"{arg.result}")
                case "string": self.append_line(f"\"{arg.result}\"")
                case "trigger": self.append_line(f"{self.labels[arg.result.trigger]}")
                case "eval": self.generate_eval(arg)

    def generate_eval(self, node, *, prepend = None, append = None):
        self.assert_type(node, NodeExpr)

        self.append_line("{")

        if prepend != None:
            self.append_line(prepend)

        self.generate_expr(node)

        if append != None:
            self.append_line(append)

        self.append_line("ReturnTop")
        self.append_line("}")

    def generate_expr(self, node):
        self.assert_type(node, NodeExpr)

        if isinstance(node, NodeBinaryExpr):
            self.generate_binary_expr(node)
        elif isinstance(node, NodeUnaryExpr):
            self.generate_unary_expr(node)
        elif isinstance(node, NodeFuncCall):
            self.generate_func_call(node)
        else:
            self.generate_value(node)

    def generate_binary_expr(self, node):
        self.assert_type(node, NodeBinaryExpr)

        self.generate_expr(node.left)
        self.generate_expr(node.right)
        
        insn = c1script.mappings.BINARY_OPERATOR_MAP[node.operator]
        self.append_line(insn)

    def generate_unary_expr(self, node):
        self.assert_type(node, NodeUnaryExpr)

        self.generate_expr(node.expr)
        
        insn = c1script.mappings.UNARY_OPERATOR_MAP[node.operator]
        self.append_line(insn)

    def generate_func_call(self, node):
        self.assert_type(node, NodeFuncCall)

        signature = c1script.mappings.FUNCTION_MAP[node.name.identifier]

        self.generate_insn(node, signature)

    def generate_value(self, node):
        self.assert_type(node, NodeExpr)

        if node.result != None:
            if isinstance(node.result, int):
                self.append_line(f"PushInt32 {node.result * self.MAGIC_VALUE}")
            elif isinstance(node.result, decimal.Decimal):
                self.append_line(f"PushInt32 {int(math.floor(node.result * self.MAGIC_VALUE))}")
            elif isinstance(node.result, bool):
                if node.result:
                    self.append_line(f"PushInt32 {self.MAGIC_VALUE}")
                else:
                    self.append_line(f"PushZero")
            else:
                raise Exception(f"Unsupported value `{node.result}` in expression")
        elif isinstance(node, NodeRawInteger):
            self.append_line(f"PushInt32 {node.expr.result}")
        else:
            self.assert_type(node, NodeIdentifier)
            if node.identifier not in self.var_locs:
                raise Exception(f"Unknown variable {node.identifier}")

            var_data = self.var_locs[node.identifier]
            
            self.append_line(c1script.mappings.VAR_MAP[var_data.kind]["push"])
            self.append_line(f"{var_data.index}")

    def assert_type(self, node, type):
        if not isinstance(node, type):
            raise Exception(f"Expected #{type} node type for #{node}")

    def set_label(self, name, key = None):
        if key != None:
            self.labels[key] = name

        self.asm += f"\n{name}:\n"
        
    def newline(self):
        self.asm += "\n"

    def separate(self):
        self.asm += "\n; ----------------------------------------------------------------\n"

    def start_line(self, line = None):
        if line is None:
            self.asm += f"\t"
        else:
            self.asm += f"\t{line}"

    def append_line(self, line):
        if line is None:
            return
        
        if self.asm[-1] == "\t":
            self.asm += f"{line}"
        else:
            self.asm += f" {line}"

    def write_line(self, line):
        self.asm += f"\t{line}\n"
        
    def comment(self, comment):
        if len(self.asm) == 0 or self.asm[-1] in ["\n", "\t"]:
            self.asm += f"; {comment}\n"
        else:
            self.asm += f" ; {comment}\n"

    def init_vars(self):
        self.var_locs = {}
        self.var_slots = {}

        for name, data in c1script.mappings.VAR_MAP.items():
            self.var_slots[name] = [False] * data["limit"]

    def allocate_var(self, name, kind = None, index = None):
        if name in self.var_locs:
            raise Exception(f"Redefinition of variable `{name}`")
        if kind is None:
            for k in ["params", "vars"]:
                try:
                    index = self.var_slots[k].index(False)
                    kind = k
                    break
                except ValueError:
                    pass
            if kind is None:
                raise Exception("No more params and vars available")

        else:
            if self.var_slots[kind][index]:
                raise Exception(f"Variable `{kind}` with index `{index}` is already used")

        self.var_slots[kind][index] = True
        self.var_locs[name] = VarData(name, kind, index)

        return kind, index
    
    def write_var_size(self):
        vars_count = 0
        if True in self.var_slots["vars"]:
            vars_count = len(self.var_slots["vars"]) - self.var_slots["vars"][::-1].index(True)
        try:
            vars_size = next(filter(lambda v: v["size"] >= vars_count, c1script.mappings.VAR_SIZES))["index"]
        except StopIteration:
            raise Exception("Out of variables")

        self.asm = self.asm.replace("<STRAT_VARS_PLACEHOLDER>", str(vars_size))
