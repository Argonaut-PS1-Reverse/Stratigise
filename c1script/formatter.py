"""
Generation of script output from syntax tree
"""

import decimal
import c1script.mappings
from c1script.nodes import *

class VarData:
    def __init__(self, name, kind, index):
        self.name = name
        self.kind = kind
        self.index = index

class Formatter:
    INDENT = "    "

    BINARY_PRIORITIES = {
        "or": 1,
        "and": 2,
        "|": 3,
        "&": 4,
        ">": 5,
        "<": 5,
        ">=": 5,
        "<=": 5,
        "==": 5,
        "!=": 5,
        "<<": 6,
        ">>": 6,
        "+": 7,
        "-": 7,
        "*": 8,
        "/": 8
    }

    def __init__(self, tree, title_comment = "Generated from a syntax tree"):
        self.tree = tree
        self.title_comment = title_comment
        self.code = ""
        self.indent = 0

    def format(self):
        self.comment("=" * 78)
        self.comment("")
        self.comment(self.title_comment)
        self.comment("")
        self.comment("=" * 78)
        self.newline()

        self.format_file(self.tree)

        self.newline()

        return self.code

    def format_file(self, node):
        self.assert_type(node, NodeFile)

        for unit in node.units:
            self.format_unit(unit)

        self.newline()

    def format_unit(self, node):
        self.assert_type(node, NodeUnit)

        if isinstance(node, NodeConst):
            self.format_const(node)
        elif isinstance(node, NodePreload):
            self.format_preload(node)
        elif isinstance(node, NodeUse):
            self.format_use(node)
        elif isinstance(node, NodeGlobalVar):
            self.format_global_var(node)
        elif isinstance(node, NodeProc):
            self.format_proc(node)
        elif isinstance(node, NodeTrigger):
            self.format_trigger(node)
        elif isinstance(node, NodeStrat):
            self.format_strat(node)
        else:
            raise Exception(f"Unknown unit type for #{node}")
        
    def format_const(self, node):
        self.assert_type(node, NodeConst)

        self.write_line(f"const {node.name.identifier} = {self.formatted_expr(node.expr)}")

    def format_preload(self, node):
        self.assert_type(node, NodePreload)

        self.write_line(f"preload \"{node.strat.result}\"")

    def format_use(self, node):
        self.assert_type(node, NodeUse)

        self.start_line(f"use {node.kind.identifier}[{self.formatted_expr(node.index)}] as {node.alias.identifier}")
        if node.comment is not None:
            self.comment(node.comment)
        else:
            self.newline()

    def format_global_var(self, node):
        self.assert_type(node, NodeGlobalVar)

        self.write_line(f"global {node.name.identifier}")

    def format_proc(self, node):
        self.assert_type(node, NodeProc)

        self.separate()
        self.start_line(f"proc {node.name.identifier} ")

        self.format_block(node.block)

    def format_trigger(self, node):
        self.assert_type(node, NodeTrigger)

        self.separate()
        self.start_line(f"trigger {node.name.identifier} ")

        self.format_block(node.block)

    def format_strat(self, node):
        self.assert_type(node, NodeStrat)

        self.separate()
        self.start_line(f"strat {node.name.identifier} ")

        self.format_block(node.block)

    def format_block(self, node, no_newline = False):
        self.assert_type(node, NodeBlock)

        self.append_line("{")
        self.newline()
        self.indent += 1

        for statement in node.statements:
            self.format_statement(statement)

        self.indent -= 1
        if no_newline:
            self.start_line("}")
        else:
            self.write_line("}")

    def format_statement(self, node):
        self.assert_type(node, NodeStatement)

        if isinstance(node, NodeCommand):
            self.format_command(node)
        elif isinstance(node, NodeProcCall):
            self.format_proc_call(node)
        elif isinstance(node, NodeAssignment):
            self.format_assignment(node)
        elif isinstance(node, NodeVar):
            self.format_var(node)
        elif isinstance(node, NodeControl):
            self.format_control(node)
        elif isinstance(node, NodeUnhandled):
            self.format_unhandled(node)
        else:
            raise Exception(f"Unknown statement type for #{node}")
        
    def format_command(self, node):
        self.assert_type(node, NodeCommand)

        self.write_line(f"{node.name.identifier}({self.formatted_args(node.args)})")

    def format_proc_call(self, node):
        self.assert_type(node, NodeProcCall)

        self.write_line(f"{node.name.identifier}()")

    def format_assignment(self, node):
        self.assert_type(node, NodeAssignment)
        
        self.write_line(f"{node.name.identifier} {node.operator} {self.formatted_expr(node.expr)}")

    def format_var(self, node):
        self.assert_type(node, NodeVar)

        self.write_line(f"{node.name.identifier} = {self.formatted_expr(node.expr)}")

    def format_control(self, node):
        self.assert_type(node, NodeControl)

        if isinstance(node, NodeIf):
            self.format_if(node)
        elif isinstance(node, NodeUnless):
            self.format_unless(node)
        elif isinstance(node, NodeWhile):
            self.format_while(node)
        elif isinstance(node, NodeRepeatUntil):
            self.format_repeat_until(node)
        elif isinstance(node, NodeFor):
            self.format_for(node)
        elif isinstance(node, NodeSwitch):
            self.format_switch(node)
        else:
            raise Exception(f"Unknown control statement type for #{node}")
        
    def format_if(self, node, after_else = False):
        self.assert_type(node, NodeIf)

        if after_else:
            self.append_line(f"if ({self.formatted_if_condition(node.condition)}) ")
        else:
            self.start_line(f"if ({self.formatted_if_condition(node.condition)}) ")

        self.format_block(node.block)

        if node.else_part is not None:
            self.start_line("else ")

            if isinstance(node.else_part, NodeIf):
                self.format_if(node.else_part, True)
            else:
                self.format_block(node.else_part)

    def format_unless(self, node):
        self.assert_type(node, NodeUnless)

        self.start_line(f"unless ({self.formatted_expr(node.condition)}) ")

        self.format_block(node.block)
        
    def format_while(self, node):
        self.assert_type(node, NodeWhile)

        self.start_line(f"while ({self.formatted_expr(node.condition)}) ")

        if node.imm:
            self.append_line("immediately ")

        self.format_block(node.block)
        
    def format_repeat_until(self, node):
        self.assert_type(node, NodeRepeatUntil)

        self.start_line("repeat ")

        if node.imm:
            self.append_line("immediately ")

        self.format_block(node.block, True)

        self.append_line(f" until ({self.formatted_expr(node.condition)})")
        self.newline()
        
    def format_for(self, node):
        self.assert_type(node, NodeFor)

        self.start_line(f"for {node.var.identifier} from {self.formatted_expr(node.start_value)} to {self.formatted_expr(node.end_value)} ")

        if node.imm:
            self.append_line("immediately ")

        self.format_block(node.block)
        
    def format_switch(self, node):
        self.assert_type(node, NodeSwitch)

        self.start_line(f"switch ({self.formatted_expr(node.expr)}) ")

        self.append_line("{")
        self.newline()
        self.indent += 1

        for case in node.cases:
            self.start_line(f"case ({self.formatted_expr(case.expr)}) ")
            self.format_block(case.block)

        if node.default is not None:
            self.start_line(f"default ")
            self.format_block(node.default)

        self.indent -= 1
        self.write_line("}")

    def format_unhandled(self, node):
        self.assert_type(node, NodeUnhandled)

        self.start_line(f"??? {node.line}")
        if node.comment is not None:
            self.append_line(f" # {node.comment}")
        self.newline()

    def formatted_args(self, node):
        return ", ".join([self.formatted_expr(arg) for arg in node.args])
    
    def formatted_if_condition(self, node):
        self.assert_type(node, NodeExpr | NodeSpecialCondition)

        if isinstance(node, NodeSpecialCondition):
            if node.invert:
                return f"!{node.name}()"
            else:
                return f"{node.name}()"
            
        return self.formatted_expr(node)

    def formatted_expr(self, node, parent = None, left = True):
        self.assert_type(node, NodeExpr)

        if isinstance(node, NodeBinaryExpr):
            return self.formatted_binary_expr(node, parent)
        elif isinstance(node, NodeUnaryExpr):
            return self.formatted_unary_expr(node, parent)
        elif isinstance(node, NodeFuncCall):
            return self.formatted_func_call(node)
        elif isinstance(node, NodeIdentifier):
            return self.formatted_identifier(node)
        elif isinstance(node, NodeInteger):
            return self.formatted_integer(node)
        elif isinstance(node, NodeNumber):
            return self.formatted_number(node)
        elif isinstance(node, NodeRawInteger):
            return self.formatted_raw_integer(node)
        elif isinstance(node, NodeBoolean):
            return self.formatted_boolean(node)
        elif isinstance(node, NodeString):
            return self.formatted_string(node)
        else:
            raise Exception(f"Unknown expression node type for #{node}")

    def formatted_binary_expr(self, node, parent = None, left = True):
        self.assert_type(node, NodeBinaryExpr)

        wrap = isinstance(parent, NodeUnaryExpr)
        if isinstance(parent, NodeBinaryExpr):
            priority = self.BINARY_PRIORITIES[node.operator]
            parent_priority = self.BINARY_PRIORITIES[parent.operator]

            if left:
                wrap = priority < parent_priority
            else:
                wrap = priority <= parent_priority

        result = ""
        if wrap:
            result += "("

        result += self.formatted_expr(node.left, node, True)
        result += f" {node.operator} "
        result += self.formatted_expr(node.right, node, False)
        
        if wrap:
            result += ")"

        return result

    def formatted_unary_expr(self, node, parent = None):
        self.assert_type(node, NodeUnaryExpr)

        return f"{node.operator}{self.formatted_expr(node.expr, node)}"

    def formatted_func_call(self, node):
        self.assert_type(node, NodeFuncCall)

        return f"{node.name.identifier}({self.formatted_args(node.args)})"

    def formatted_identifier(self, node):
        self.assert_type(node, NodeIdentifier)

        return node.identifier

    def formatted_integer(self, node):
        self.assert_type(node, NodeInteger)

        return str(node.value)

    def formatted_number(self, node):
        self.assert_type(node, NodeNumber)

        if node.value == 0:
            return "0"

        r = decimal.Decimal(node.value)
        rounded = r.quantize(decimal.Decimal(10) ** -3)
        if abs(r - rounded) < (decimal.Decimal(10) ** -5):
            s = str(r.quantize(decimal.Decimal(10) ** -4))
        else:
            s = str(r.quantize(decimal.Decimal(10) ** -16))

        return s.rstrip('0').rstrip('.') if '.' in s else s

    def formatted_raw_integer(self, node):
        self.assert_type(node, NodeRawInteger)

        return f"raw({self.formatted_expr(node.expr)})"
    
    def formatted_boolean(self, node):
        self.assert_type(node, NodeBoolean)

        if node.value:
            return "true"
        else:
            return "false"

    def formatted_string(self, node):
        self.assert_type(node, NodeString)

        return f"\"{node.value}\""
        
    def assert_type(self, node, type):
        if not isinstance(node, type):
            raise Exception(f"Expected #{type} node type for #{node}")
        
    def newline(self):
        self.code += "\n"

    def separate(self):
        self.code += "\n#-----------------------------------------------------------------\n\n"

    def start_line(self, line = None):
        if line is None:
            self.code += self.INDENT * self.indent
        else:
            self.code += self.INDENT * self.indent + line

    def append_line(self, line):
        self.code += f"{line}"

    def write_line(self, line):
        self.start_line(line)
        self.newline()
        
    def comment(self, comment):
        if len(self.code) == 0 or self.code[-1] in ["\n", "\t", " "]:
            self.code += f"# {comment}\n"
        else:
            self.code += f" # {comment}\n"