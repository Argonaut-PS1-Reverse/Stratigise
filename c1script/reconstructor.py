"""
Reconstruction of script syntax tree base on assembly input
"""

import enum, decimal, copy
from c1script.asm_parser import *
from c1script.nodes import *
import c1script.mappings

LOADER_HINTS = {
    "loadObject": "model",
	"loadAsset0": "model",
	"loadAnim": "anim",
	"loadAsset1": "sound",
	"loadAsset2": "anim",
	"loadAsset3": "sound",
	"loadAsset4": "sound",
	"loadAsset5": "anim"
}

class SectionType(enum.Enum):
    UNKNOWN = 0
    PROC = 1
    TRIGGER = 2
    STRAT = 3

class Section:
    def __init__(self, type, name, start, end):
        self.type = type
        self.name = name
        self.start = start
        self.end = end
        self.insns = []
        self.vars = {}
        self.deps = []
        self.var_hints = {}

    def __str__(self):
        match self.type:
            case SectionType.PROC: return f"{self.start}-{self.end} -- Proc `{self.name}`"
            case SectionType.TRIGGER: return f"{self.start}-{self.end} -- Trigger `{self.name}`"
            case SectionType.STRAT: return f"{self.start}-{self.end} -- Strat `{self.name}`"
            case _: return f"{self.start}-{self.end} -- Unknown"

class ProcessStatementError(Exception):
    def __init__(self, comment):
        self.comment = comment

class Reconstructor:
    def __init__(self, insns, strat_attrs, preloads):
        self.insns = insns
        self.strat_attrs = strat_attrs
        self.preloads = preloads
        self.strats = {}
        self.strat_trees = {}
        self.failed_strats = []
        self.labels = {}
        self.insns_count = len(insns)
        self.unhandled_count = 0

    def reconstruct(self):
        print("Starting reconstruction...")

        self.check_labels()
        self.split()

        for section in self.sections:
            section.trees = self.process_section(section)

        self.generate_strats_trees()

        print("\nReconstruction finished!")

        percentage = (self.insns_count - self.unhandled_count) / float(self.insns_count) * 100
        print(f"  {percentage:.1f}% of lines have been processed ({self.insns_count - self.unhandled_count}/{self.insns_count})")

        if len(self.failed_strats) > 0:
            print("\n!!! WARNING !!! Failed to process the following strats, they might be broken!")
            for strat in self.failed_strats:
                print(f"  {strat}")

        return self.strat_trees

    def check_labels(self):
        print("\nAnalysing labels...")
        for insn in self.insns:
            if isinstance(insn, Label):
                self.labels[insn.name] = insn

        for strat in self.strat_attrs:
            if strat.pc in self.labels:
                self.labels[strat.pc].strat = strat.name
            else:
                print(f"WARNING! Broken strat {strat.name} (invalid address)")
                self.failed_strats.append(strat.name)
    
        for insn in self.insns:
            if isinstance(insn, Label):
                continue

            match insn.op:
                case "ProcCall":
                    self.labels[insn.args[0].label].proc = True
                case "CreateTrigger":
                    self.labels[insn.args[-1].label].trigger = True
                case _:
                    for arg in insn.args:
                        if isinstance(arg, LabelRef):
                            self.labels[arg.label].jumps.append(insn.loc)

        strats_count = 0
        procs_count = 0
        triggers_count = 0

        for label in self.labels.values():
            if label.proc:
                procs_count += 1
            if label.trigger:
                triggers_count += 1
            if label.strat is not None:
                strats_count += 1

        print(f"  Labels found: {len(self.labels)}")
        print(f"  Strats: {strats_count}")
        print(f"  Procs: {procs_count}")
        print(f"  Triggers: {triggers_count}")

    def split(self):
        print("\nSplitting into sections...")

        self.sections = []
        cur_section = None
        prev_insn = None

        if len(self.insns) > 0 and isinstance(self.insns[0], Insn):
            cur_section = Section(SectionType.UNKNOWN, None, self.insns[0].loc, None)

        for i in range(len(self.insns)):
            insn = self.insns[i]

            if isinstance(insn, Insn) and insn.op == "FileEnd":
                break

            if isinstance(insn, Label) and (insn.proc or insn.trigger or insn.strat is not None):
                if cur_section is not None:
                    if insn.strat:
                        if prev_insn.op not in ["EndProc", "EndTrigger", "Remove", None]:
                            self.ignore_split_label(insn)

                    if not insn.nosplit:
                        cur_section.end = prev_insn.loc
                        print(f"  section {cur_section}")
                        self.sections.append(cur_section)

                if not insn.nosplit:
                    if insn.proc:
                        cur_section = Section(SectionType.PROC, insn.name, insn.loc, None)
                    elif insn.trigger:
                        cur_section = Section(SectionType.TRIGGER, insn.name, insn.loc, None)
                    elif insn.strat is not None:
                        cur_section = Section(SectionType.STRAT, insn.strat, insn.loc, None)
                        self.strats[insn.strat] = len(self.sections)

            if cur_section is not None:
                cur_section.insns.append(insn)

            if isinstance(insn, Insn):
                prev_insn = insn

        if cur_section is not None:
            match cur_section.type:
                case SectionType.PROC:
                    if prev_insn is None or prev_insn.op != "EndProc":
                        print(f"WARNING! Expected `EndProc` before `FileEnd`!")
                case SectionType.TRIGGER:
                    if prev_insn is None or prev_insn.op != "EndTrigger":
                        print(f"WARNING! Expected `EndTrigger` before `FileEnd`!")
                case SectionType.STRAT:
                    if prev_insn is None or prev_insn.op != "Remove":
                        print(f"WARNING! Expected `Remove` before `FileEnd`!")

            cur_section.end = prev_insn.loc
            print(f"  section {cur_section}")
            self.sections.append(cur_section)

    def ignore_split_label(self, label):
        if label.strat:
            print(f"WARNING! Not splitting at strat label {label.name}! This can be a broken strat, ignoring it")
            self.failed_strats.append(label.strat)
            label.strat = None
        else:
            print(f"WARNING! Not splitting at label {label.name} because `{expected}` was expected before it!")

        label.nosplit = True

    def process_section(self, section):
        print(f"\nProcessing section `{section}`...")

        self.process_statements(section)
        self.process_control(section)

        nodes = []
        cur_type = self.section_type_from_insn(section.insns[-1])
        i = len(section.insns) - 2
        end = len(section.insns) - 1
        type = None

        while i >= 1:
            type = self.section_type_from_insn(section.insns[i])
            if type != SectionType.UNKNOWN:
                if i == end - 1 and type == SectionType.STRAT:
                    type = SectionType.UNKNOWN
                    i -= 1
                    continue

                insn = section.insns[i + 1]
                if isinstance(insn, Label) and insn.nosplit:
                    insn.nosplit = False

                statements = [s for s in [self.finalize_statement(insn) for insn in section.insns[i + 1:end]] if s is not None]
                match cur_type:
                    case SectionType.PROC:
                        print(f"  found unused proc at {section.insns[i].loc + 1} -- {section.insns[end].loc}")
                        nodes.append(NodeProc(None, NodeIdentifier(None, f"__unused_proc_at_{section.insns[i].loc + 1}"), NodeBlock(None, statements)))
                    case SectionType.TRIGGER:
                        print(f"  found unused trigger at {section.insns[i].loc + 1} -- {section.insns[end].loc}")
                        nodes.append(NodeTrigger(None, NodeIdentifier(None, f"__unused_trigger_at_{section.insns[i].loc + 1}"), NodeBlock(None, statements)))
                    case SectionType.STRAT:
                        print(f"  found unused strat at {section.insns[i].loc + 1} -- {section.insns[end].loc}")
                        nodes.append(NodeStrat(None, NodeIdentifier(None, f"__unused_strat_at_{section.insns[i].loc + 1}"), NodeBlock(None, statements)))

                end = i
                cur_type = type

            i -= 1

        if type == SectionType.STRAT and section.type != SectionType.STRAT:
            end += 1 # Including `Remove` insn

        statements = [s for s in [self.finalize_statement(insn) for insn in section.insns[:end]] if s is not None]

        match section.type:
            case SectionType.PROC:
                print(f"  creating proc unit at {section.insns[0].loc} -- {section.insns[end].loc}")
                nodes.append(NodeProc(None, NodeIdentifier(None, section.name), NodeBlock(None, statements)))
            case SectionType.TRIGGER:
                print(f"  creating trigger unit at {section.insns[0].loc} -- {section.insns[end].loc}")
                nodes.append(NodeTrigger(None, NodeIdentifier(None, section.name), NodeBlock(None, statements)))
            case SectionType.STRAT:
                print(f"  creating strat unit at {section.insns[0].loc} -- {section.insns[end].loc}")
                nodes.append(NodeStrat(None, NodeIdentifier(None, section.name), NodeBlock(None, statements)))
            case SectionType.UNKNOWN:
                print(f"  creating unknown unit at {section.insns[0].loc} -- {section.insns[end].loc}")
                nodes.append(NodeProc(None, NodeIdentifier(None, f"__unknown_section_{hex(section.start)}"), NodeBlock(None, statements)))

        return list(reversed(nodes))
    
    def section_type_from_insn(self, insn):
        if isinstance(insn, Insn):
            if insn.op == "EndProc":
                return SectionType.PROC
            elif insn.op == "EndTrigger":
                return SectionType.TRIGGER
            elif insn.op == "Remove":
                return SectionType.STRAT
            
        return SectionType.UNKNOWN

    def process_statements(self, section):
        fail_count = 0
        for i in range(len(section.insns)):
            try:
                result = self.process_statement(section, section.insns[i])

                if result is None:
                    del section.insns[i]
                    i -= 1
                else:
                    section.insns[i] = result
            except ProcessStatementError as e:
                section.insns[i] = self.unhandled_line(section.insns[i], e.comment)
                fail_count += 1

        print(f"  processed commands ({fail_count} failures)")

    def process_statement(self, section, insn):
        if not isinstance(insn, Insn):
            return insn
        
        if insn.op in c1script.mappings.VAR_SETTERS:
            if len(insn.args) != 2:
                raise ProcessStatementError(f"Wrong arguments count for `{insn.op}`")
            
            index = self.process_arg(section, insn.args[0], "int16", insn.op)
            expr = self.process_arg(section, insn.args[1], "eval", insn.op)

            for vk, vd in c1script.mappings.VAR_MAP.items():
                if vd["let"] == insn.op:
                    var_name = vd["name_pfx"] + str(index.value)
                    if vk == "alien_vars" and index.value in c1script.mappings.ALIEN_VARS:
                        var_name = c1script.mappings.ALIEN_VARS[index.value]
                    self.use_var(section, vk, index.value, True)

                    return self.create_assignment(section, var_name, expr)
            
        if insn.op == "ProcCall":
            if len(insn.args) != 1:
                raise ProcessStatementError(f"Wrong arguments count for `{insn.op}`")

            label = self.process_arg(section, insn.args[0], "label", insn.op)

            return NodeProcCall(None, label)
        
        if insn.op in ["Inc", "Dec"]:
            if len(insn.args) != 2:
                raise ProcessStatementError(f"Wrong arguments count for `{insn.op}`")
            
            kind = self.process_arg(section, insn.args[0], "int8", insn.op)
            index = self.process_arg(section, insn.args[1], "int16", insn.op)
            op = ("+=" if insn.op == "Inc" else "-=")

            for vk, vd in c1script.mappings.VAR_MAP.items():
                if vd["kind_int"] == kind.value:
                    var_name = vd["name_pfx"] + str(index.value)
                    if vk == "alien_vars" and index.value in c1script.mappings.ALIEN_VARS:
                        var_name = c1script.mappings.ALIEN_VARS[index.value]
                    self.use_var(section, vk, index.value)

                    return NodeAssignment(None, NodeIdentifier(None, var_name), op, NodeInteger(None, 1))
                
        if insn.op == "Remove":
            return insn # Ignore for now
        
        for sign in c1script.mappings.COMMAND_SIGNATURES:
            if sign.insn == insn.op:
                args = self.process_args(section, insn.args, sign)

                return NodeCommand(None, NodeIdentifier(None, sign.name), args)

        return insn
    
    def process_args(self, section, args, sign):
        arg_types = [a for a in sign.signature if a != "stack"]

        if "varargs" in arg_types:
            varargs_pos = arg_types.index("varargs")
            varargs_count = len(args) - len(arg_types) + 1

            if varargs_count < 0:
                raise ProcessStatementError(f"Too few arguments for {sign.insn}, expected at least {len(arg_types) - 1}, given {len(args)}")
            
            arg_types = arg_types[:varargs_pos] + ["eval"] * varargs_count + arg_types[varargs_pos + 1:]

        if "varargs_int" in arg_types:
            varargs_pos = arg_types.index("varargs_int")
            varargs_count = len(args) - len(arg_types) + 1

            if varargs_count < 0:
                raise ProcessStatementError(f"Too few arguments for {sign.insn}, expected at least {len(arg_types) - 1}, given {len(args)}")
            
            arg_types = arg_types[:varargs_pos] + ["int16"] * varargs_count + arg_types[varargs_pos + 1:]

        if len(args) != len(arg_types):
            raise ProcessStatementError(f"Wrong number of arguments for {sign.insn}, expected {len(arg_types)}, given {len(args)}")

        result_args = []
        for i in range(len(arg_types)):
            result_args.append(self.process_arg(section, args[i], arg_types[i], sign.insn))

        return NodeArgs(None, result_args)
    
    def process_arg(self, section, arg, type, op):
        match type:
            case "string":
                if isinstance(arg, str):
                    return NodeString(None, arg)
                else:
                    raise ProcessStatementError(f"Wrong argument type for {op}, expected `{type}`, given {arg}")

            case "int8" | "int16" | "int32":
                if isinstance(arg, int):
                    return NodeInteger(None, arg)
                else:
                    raise ProcessStatementError(f"Wrong argument type for {op}, expected `{type}`, given {arg}")
                
            case "eval":
                if isinstance(arg, Eval):
                    return self.process_eval(section, arg)
                else:
                    raise ProcessStatementError(f"Wrong argument type for {op}, expected `{type}`, given {arg}")
                
            case "trigger" | "label":
                if isinstance(arg, LabelRef):
                    self.make_dependency(section, arg.label)

                    return NodeIdentifier(None, arg.label)
                else:
                    raise ProcessStatementError(f"Wrong argument type for {op}, expected `{type}`, given {arg}")
                
            case _:
                raise ProcessStatementError(f"Unsupported arg type for {op} `{type}`, given {arg}")
            
    def process_eval(self, section, eval):
        stack = []

        for insn in eval.eval_insns:
            if insn.op == "ReturnTop":
                if len(stack) != 1:
                    raise ProcessStatementError(f"Stack length should be 1 for {insn.op}")
                
                return stack[-1]

            elif insn.op == "ReturnZero":
                if len(stack) != 0:
                    raise ProcessStatementError(f"Stack length should be 0 for {insn.op}")
                
                return NodeInteger(None, 0)

            elif insn.op in c1script.mappings.BINARY_OPERATOR_MAP.values():
                if len(stack) < 2:
                    raise ProcessStatementError(f"Not enough variables in stack for {insn.op}")
                
                op = list(reversed(c1script.mappings.BINARY_OPERATOR_MAP.keys()))[list(reversed(c1script.mappings.BINARY_OPERATOR_MAP.values())).index(insn.op)]

                if op in ["==", "!="]:
                    rval = self.get_const_by_value(stack[-2], stack[-1])
                elif op in ["&", "|"]:
                    rval = self.get_const_flags_by_value(stack[-2], stack[-1])
                else:
                    rval = stack[-1]

                stack = stack[:-2] + [NodeBinaryExpr(None, stack[-2], rval, op)]

            elif insn.op in c1script.mappings.UNARY_OPERATOR_MAP.values():
                if len(stack) < 1:
                    raise ProcessStatementError(f"Not enough variables in stack for {insn.op}")
                
                op = list(c1script.mappings.UNARY_OPERATOR_MAP.keys())[list(c1script.mappings.UNARY_OPERATOR_MAP.values()).index(insn.op)]

                stack = stack[:-1] + [NodeUnaryExpr(None, stack[-1], op)]

            elif insn.op == "PushInt32":
                if len(insn.args) != 1 or not isinstance(insn.args[0], int):
                    raise ProcessStatementError(f"Wrong arguments for `PushInt32`: {insn.args}")

                val = insn.args[0]
                if val > 0 and val < 32:
                    stack.append(NodeRawInteger(None, NodeInteger(None, val)))
                elif val % c1script.mappings.MAGIC_VALUE == 0:
                    stack.append(NodeInteger(None, int(val / c1script.mappings.MAGIC_VALUE)))
                else:
                    stack.append(NodeNumber(None, val / decimal.Decimal(c1script.mappings.MAGIC_VALUE)))

            elif insn.op in c1script.mappings.VAR_GETTERS:
                if len(insn.args) != 1:
                    raise ProcessStatementError(f"Wrong arguments count for `{insn.op}`")
                
                index = self.process_arg(section, insn.args[0], "int16", insn.op)

                for vk, vd in c1script.mappings.VAR_MAP.items():
                    if vd["push"] == insn.op:
                        var_name = vd["name_pfx"] + str(index.value)
                        if vk == "alien_vars" and index.value in c1script.mappings.ALIEN_VARS:
                            var_name = c1script.mappings.ALIEN_VARS[index.value]
                        self.use_var(section, vk, index.value, True)

                        stack.append(NodeIdentifier(None, var_name))

            else:
                node = None
                for sign in c1script.mappings.FUNCTION_SIGNATURES:
                    if sign.insn == insn.op:
                        stack_count = sign.signature.count("stack")
                        if len(stack) < stack_count:
                            raise ProcessStatementError(f"Stack length should be {stack_count} for {insn.op}")

                        args = self.process_args(section, insn.args, sign)

                        if stack_count > 0:
                            i = 0
                            for type in sign.signature:
                                if type == "stack":
                                    arg = stack[-stack_count + i]
                                    args.args.append(arg)
                                    i += 1

                            stack = stack[:-stack_count]

                        node = NodeFuncCall(None, NodeIdentifier(None, sign.name), args)
                    
                if node is None:
                    raise ProcessStatementError(f"Unhandled eval operation {insn.op}")
                
                stack.append(node)

    def process_control(self, section):
        print("  reconstructing control flow statements...")

        self.process_control_body(section, 0)

    def process_control_body(self, section, index, until_insns = [], until_labels = []):
        while index < len(section.insns):
            insn = section.insns[index]
            if isinstance(insn, Label):
                if insn.name in until_labels:
                    return index  
                else:
                    if len(insn.jumps) > 0:
                        index = self.process_label_with_jump(section, index)
                    else:
                        index += 1
            elif isinstance(insn, Insn):
                if insn.op in until_insns:
                    return index
                elif insn.op in (["If"] + list(c1script.mappings.SPECIAL_CONDITIONS.values())):
                    index = self.process_if(section, index)
                elif insn.op == "While":
                    index = self.process_while(section, index)
                elif insn.op == "Repeat":
                    index = self.process_repeat_until(section, index)
                elif insn.op == "For":
                    index = self.process_for(section, index)
                elif insn.op == "Switch":
                    index = self.process_switch(section, index)
                elif insn.op in ["Else", "EndWhile", "EndWhileImm", "Until", "UntilImm", "Next", "NextImm", "EndCase"]:
                    index += 1
                elif insn.op in ["EndProc", "EndTrigger", "Remove"]:
                    index += 1
                else:
                    section.insns[index] = self.unhandled_line(insn, "Unexpected instruction")
                    index += 1
            else:
                index += 1

        return index

    def process_if(self, section, index):
        insn = section.insns[index]
        op = insn.op

        if op == "If":
            if len(insn.args) != 2:
                section.insns[index] = self.unhandled_line(insn, f"Wrong arguments count for `{op}`")
                return index + 1

            try:
                condition = self.process_arg(section, insn.args[0], "eval", op)
                label = self.process_arg(section, insn.args[1], "label", op)
            except ProcessStatementError as e:
                section.insns[index] = self.unhandled_line(insn, e.comment)
                return index + 1
        else:
            if len(insn.args) != 1:
                section.insns[index] = self.unhandled_line(insn, f"Wrong arguments count for `{op}`")
                return index + 1

            try:
                name = list(c1script.mappings.SPECIAL_CONDITIONS.keys())[list(c1script.mappings.SPECIAL_CONDITIONS.values()).index(op)]
                condition = NodeSpecialCondition(None, name)
                label = self.process_arg(section, insn.args[0], "label", op)
            except ProcessStatementError as e:
                section.insns[index] = self.unhandled_line(insn, e.comment)
                return index + 1

        i = self.process_control_body(section, index + 1, [], [label.identifier])

        if i >= len(section.insns):
            section.insns[index] = self.unhandled_line(insn, f"No corresponding label found inside the section")
            return index + 1

        insn = section.insns[i]

        if not (isinstance(section.insns[i - 1], Insn) and section.insns[i - 1].op == "Else"):
            # Create `if` structure`
            insn.jumps.remove(section.insns[index].loc)

            statements = [s for s in [self.finalize_statement(insn) for insn in section.insns[index + 1:i]] if s is not None]
            node = NodeIf(None, condition, NodeBlock(None, statements))

            print(f"  wrapped {section.insns[index].loc}-{insn.loc} in `if`")
            section.insns = section.insns[:index] + [node] + section.insns[i:]
            return index + 1
            
        else_index = i - 1
        else_insn = section.insns[else_index]
        skip_else = False

        if len(else_insn.args) != 1:
            section.insns[else_index] = self.unhandled_line(else_insn, f"Wrong arguments count for `{else_insn.op}`")
            skip_else = True

        if not skip_else:
            try:
                else_label = self.process_arg(section, else_insn.args[0], "label", else_insn.op)
            except ProcessStatementError as e:
                section.insns[else_index] = self.unhandled_line(else_insn, e.comment)
                skip_else = True

        if not skip_else:
            insn.jumps.remove(section.insns[index].loc)
            i = self.process_control_body(section, i, [], [else_label.identifier])

            if i >= len(section.insns):
                section.insns[else_index] = self.unhandled_line(else_insn, f"No corresponding label found inside the section")
                skip_else = True
            else:   
                insn2 = section.insns[i]
        
        if skip_else:
            # Ignore `else``end create `if` structure
            statements = [s for s in [self.finalize_statement(insn) for insn in section.insns[index + 1:i]] if s is not None]
            node = NodeIf(None, condition, NodeBlock(None, statements))

            print(f"  wrapped {section.insns[index].loc}-{insn.loc} in `if` but couldn't handle `Else`")
            section.insns = section.insns[:index] + [node] + section.insns[i:]
            return index + 1

        # Create `if-else` construction
        if section.insns[index].loc in insn.jumps:
            insn.jumps.remove(section.insns[index].loc)
        insn2.jumps.remove(section.insns[else_index].loc)

        statements_then = [s for s in [self.finalize_statement(insn) for insn in section.insns[index + 1:else_index]] if s is not None]
        statements_else = [s for s in [self.finalize_statement(insn) for insn in section.insns[else_index + 1:i]] if s is not None]
        node = NodeIf(None, condition, NodeBlock(None, statements_then), NodeBlock(None, statements_else))

        print(f"  wrapped {section.insns[index].loc}-{insn2.loc} in `if-else`")
        section.insns = section.insns[:index] + [node] + section.insns[i:]
        return index + 1
        
    def process_while(self, section, index):
        insn = section.insns[index]
        if len(insn.args) != 2:
            section.insns[index] = self.unhandled_line(insn, f"Wrong arguments count for `{insn.op}`")
            return index + 1

        try:
            condition = self.process_arg(section, insn.args[0], "eval", insn.op)
            label = self.process_arg(section, insn.args[1], "label", insn.op)
        except ProcessStatementError as e:
            section.insns[index] = self.unhandled_line(insn, e.comment)
            return index + 1

        i = self.process_control_body(section, index + 1, [], [label.identifier])

        if i >= len(section.insns):
            section.insns[index] = self.unhandled_line(insn, f"No corresponding label found inside the section")
            return index + 1

        if not (isinstance(section.insns[i - 1], Insn) and section.insns[i - 1].op in ["EndWhile", "EndWhileImm"]):
            section.insns[index] = self.unhandled_line(insn, f"Didn't find `EndWhile` before the ending label")
            return index + 1

        insn = section.insns[i]
        imm = section.insns[i - 1].op == "EndWhileImm"

        # Create `while` structure`
        insn.jumps.remove(section.insns[index].loc)

        statements = [s for s in [self.finalize_statement(insn) for insn in section.insns[index + 1:i - 1]] if s is not None]
        node = NodeWhile(None, condition, imm, NodeBlock(None, statements))

        print(f"  wrapped {section.insns[index].loc}-{insn.loc} in `while`")
        section.insns = section.insns[:index] + [node] + section.insns[i:]
        return index + 1
    
    def process_repeat_until(self, section, index):
        insn = section.insns[index]
        if len(insn.args) != 0:
            section.insns[index] = self.unhandled_line(insn, f"Wrong arguments count for `{insn.op}`")
            return index + 1

        i = self.process_control_body(section, index + 1, ["Until", "UntilImm"], [])

        if i >= len(section.insns):
            section.insns[index] = self.unhandled_line(insn, f"No corresponding `Until` found inside the section")
            return index + 1

        insn = section.insns[i]
        imm = insn.op == "UntilImm"

        if len(insn.args) != 1:
            section.insns[index] = self.unhandled_line(section.insns[index], f"Wrong arguments count for `Until`")
            section.insns[i] = self.unhandled_line(insn, f"Wrong arguments count for `{insn.op}`")
            return index + 1
        
        try:
            condition = self.process_arg(section, insn.args[0], "eval", insn.op)
        except ProcessStatementError as e:
            section.insns[index] = self.unhandled_line(section.insns[index], e.comment)
            section.insns[i] = self.unhandled_line(insn, e.comment)
            return index + 1

        # Create `repeat-until` structure`
        statements = [s for s in [self.finalize_statement(insn) for insn in section.insns[index + 1:i]] if s is not None]
        node = NodeRepeatUntil(None, condition, imm, NodeBlock(None, statements))

        print(f"  wrapped {section.insns[index].loc}-{insn.loc} in `repeat-until`")
        section.insns = section.insns[:index] + [node] + section.insns[i + 1:]
        return index + 1
    
    def process_for(self, section, index):
        insn = section.insns[index]
        if len(insn.args) != 4:
            section.insns[index] = self.unhandled_line(insn, f"Wrong arguments count for `{insn.op}`")
            return index + 1

        try:
            var_type = self.process_arg(section, insn.args[0], "int8", insn.op)
            var_index = self.process_arg(section, insn.args[1], "int16", insn.op)
            start_value = self.process_arg(section, insn.args[2], "eval", insn.op)
            end_value = self.process_arg(section, insn.args[3], "eval", insn.op)
        except ProcessStatementError as e:
            section.insns[index] = self.unhandled_line(insn, e.comment)
            return index + 1
        
        var_kind = None
        var_data = None
        for vk, vd in c1script.mappings.VAR_MAP.items():
            if vd["kind_int"] == var_type.value:
                var_kind = vk
                var_data = vd
                break

        var_name = var_data["name_pfx"] + str(var_index.value)

        if vk is None:
            section.insns[index] = self.unhandled_line(insn, f"Unknown counter variable kind `{var_type}`")
            return index + 1

        i = self.process_control_body(section, index + 1, ["Next", "NextImm"], [])

        if i >= len(section.insns):
            section.insns[index] = self.unhandled_line(insn, f"No corresponding `Next` found inside the section")
            return index + 1

        insn = section.insns[i]
        imm = insn.op == "NextImm"

        # Create `for` structure`
        var = NodeIdentifier(None, var_name)
        statements = [s for s in [self.finalize_statement(insn) for insn in section.insns[index + 1:i]] if s is not None]
        node = NodeFor(None, var, start_value, end_value, imm, NodeBlock(None, statements))
        self.use_var(section, var_kind, var_index.value, True)

        print(f"  wrapped {section.insns[index].loc}-{insn.loc} in `for`")
        section.insns = section.insns[:index] + [node] + section.insns[i + 1:]
        return index + 1
    
    def process_switch(self, section, index):
        insn = section.insns[index]
        if len(insn.args) < 3:
            section.insns[index] = self.unhandled_line(insn, f"Too few arguments for `{insn.op}`")
            return index + 1

        try:
            expr = self.process_arg(section, insn.args[0], "eval", insn.op)
            cases_count = self.process_arg(section, insn.args[1], "int16", insn.op)
            label_default = self.process_arg(section, insn.args[2], "label", insn.op)

            if len(insn.args) != 3 + 2 * cases_count.value:
                section.insns[index] = self.unhandled_line(insn, f"Wrong arguments count for `{insn.op}`")
                return index + 1

            cases = []
            labels = []
            for c in range(cases_count.value):
                case = {
                    "label": self.process_arg(section, insn.args[3 + 2 * c], "label", insn.op),
                    "value": self.get_const_by_value(
                        expr,
                        self.process_arg(section, insn.args[3 + 2 * c + 1], "eval", insn.op)
                    ),
                    "block": None
                }

                if case["label"].identifier not in labels:
                    labels.append(case["label"].identifier)

                cases.append(case)

        except ProcessStatementError as e:
            section.insns[index] = self.unhandled_line(insn, e.comment)
            return index + 1
        
        i = index + 1
        end_case_locs = []
        label_end = label_default
        default = None

        until_labels = labels
        for c in range(len(labels)):
            insn = section.insns[i]
            if not isinstance(insn, Label):
                section.insns[index] = self.unhandled_line(section.insns[index], "Expected label after `Switch`")
                return index + 1

            if insn.name not in until_labels:
                section.insns[index] = self.unhandled_line(section.insns[index], f"Unexpected label `{insn.name}`")
                return index + 1
            
            until_labels.remove(insn.name)
            insn.jumps = [j for j in insn.jumps if j != section.insns[index].loc] # removing all jumps
            
            start_index = i

            i = self.process_control_body(section, i, [], until_labels + [label_default.identifier])

            if i >= len(section.insns):
                section.insns[index] = self.unhandled_line(section.insns[index], f"Not found some case labels inside the section")
                return index + 1
            
            if isinstance(section.insns[i - 1], Insn) and section.insns[i - 1].op == "EndCase":
                end_case_insn = section.insns[i - 1]
                if len(end_case_insn.args) != 1:
                    section.insns[index] = self.unhandled_line(section.insns[index], f"Wrong number of args for `EndCase` before `{section.insns[i].name}`")
                    return index + 1

                try:
                    label_end = self.process_arg(section, end_case_insn.args[0], "label", end_case_insn.op)
                except ProcessStatementError as e:
                    section.insns[index] = self.unhandled_line(insn, e.comment)
                    return index + 1

                end_case_locs.append(section.insns[i - 1].loc)

                statements = [s for s in [self.finalize_statement(insn) for insn in section.insns[start_index:i - 1]] if s is not None]
            else:
                print(f"WARNING!!! Expected `EndCase` before `{section.insns[i].name}`, handling the case as if it was there")
                statements = [s for s in [self.finalize_statement(insn) for insn in section.insns[start_index:i]] if s is not None]

            block = NodeBlock(None, statements)

            for case in cases:
                if case["label"].identifier == insn.name:
                    case["block"] = block

        insn = section.insns[i]
        if not (isinstance(insn, Label) and insn.name in [label_default.identifier]):
            section.insns[index] = self.unhandled_line(section.insns[index], "Expected ending or default label after the last case")
            return index + 1
        
        if label_default.identifier != label_end.identifier:
            start_index = i

            insn.jumps.remove(section.insns[index].loc)

            i = self.process_control_body(section, i, [], [label_end.identifier])

            if i >= len(section.insns):
                section.insns[index] = self.unhandled_line(section.insns[index], f"Not found ending labels inside the section")
                return index + 1
            
            if not (isinstance(section.insns[i - 1], Insn) and section.insns[i - 1].op == "EndCase"):
                section.insns[index] = self.unhandled_line(section.insns[index], f"Expected `EndCase` before `{section.insns[i].name}`")
                return index + 1
            
            end_case_insn = section.insns[i - 1]
            if len(end_case_insn.args) != 1:
                section.insns[index] = self.unhandled_line(section.insns[index], f"Wrong number of args for `EndCase` before `{section.insns[i].name}`")
                return index + 1

            try:
                label_end = self.process_arg(section, end_case_insn.args[0], "label", end_case_insn.op)
            except ProcessStatementError as e:
                section.insns[index] = self.unhandled_line(insn, e.comment)
                return index + 1

            end_case_locs.append(section.insns[i - 1].loc)

            statements = [s for s in [self.finalize_statement(insn) for insn in section.insns[start_index:i - 1]] if s is not None]
            default = NodeBlock(None, statements)

        insn = section.insns[i]
        if not (isinstance(insn, Label) and insn.name == label_end.identifier):
            section.insns[index] = self.unhandled_line(section.insns[index], "Expected ending label after the last case")
            return index + 1

        # Create `switch` structure`
        if default is None:
            insn.jumps.remove(section.insns[index].loc)

        for loc in end_case_locs:
            insn.jumps.remove(loc)
        node = NodeSwitch(None, expr, [NodeCase(None, case["value"], case["block"]) for case in cases], default)

        print(f"  wrapped {section.insns[index].loc}-{insn.loc} in `switch`")
        section.insns = section.insns[:index] + [node] + section.insns[i:]
        return index + 1
    
    def process_label_with_jump(self, section, index):
        label_insn = section.insns[index]
        i = index

        while True:
            i = self.process_control_body(section, i + 1, ["Goto"], [])

            if i >= len(section.insns):
                return index + 1
            
            insn = section.insns[i]

            if len(insn.args) != 1:
                section.insns[i] = self.unhandled_line(insn, f"Wrong arguments count for `{insn.op}`")
                i += 1
                continue

            try:
                label = self.process_arg(section, insn.args[0], "label", insn.op)
            except ProcessStatementError as e:
                section.insns[i] = self.unhandled_line(insn, e.comment)
                i += 1
                continue

            if label.identifier == label_insn.name:
                break

            i += 1

        # Create `while (true)` structure`
        label_insn.jumps.remove(section.insns[i].loc)

        statements = [s for s in [self.finalize_statement(insn) for insn in section.insns[index + 1:i]] if s is not None]
        node = NodeWhile(None, NodeBoolean(None, True), False, NodeBlock(None, statements))

        print(f"  wrapped {section.insns[index].loc}-{insn.loc} in `while (true)`")
        section.insns = section.insns[:index] + [node] + section.insns[i + 1:]
        return index

    def finalize_statement(self, insn):
        if isinstance(insn, NodeBase):
            return insn
        
        if isinstance(insn, Label):
            if insn.nosplit:
                if insn.strat:
                    return self.unhandled_line(insn, f"Unhandled strat `{insn.strat}` (probably broken)")
                elif insn.proc:
                    return self.unhandled_line(insn, "Unhandled proc")
                elif insn.trigger:
                    return self.unhandled_line(insn, "Unhandled trigger")
            
            if len(insn.jumps) > 0:
                return self.unhandled_line(insn, "Some unhandled jumps refer to this")
            
            return
        
        # Now we can replace it
        if isinstance(insn, Insn) and insn.op == "Remove":
            return NodeCommand(None, NodeIdentifier(None, "remove"), NodeArgs(None, []))
        
        return self.unhandled_line(insn)
    
    def create_assignment(self, section, var_name, expr):
        if var_name not in section.var_hints:
            section.var_hints[var_name] = None

            if isinstance(expr, NodeFuncCall) and expr.name.identifier in LOADER_HINTS:
                hint = None
                res_name = "unknown"
                if len(expr.args.args) > 0 and isinstance(expr.args.args[0], NodeString):
                    res_name = expr.args.args[0].value.split(".")[0].replace("-", "_")
                mo = re.match("([^\d_]+)[^\d]+(\d+)", var_name)
                if mo:
                    hint = mo.group(1) + "_" + LOADER_HINTS[expr.name.identifier] + "_" + res_name

                if hint not in section.var_hints.values():
                    section.var_hints[var_name] = hint

            if (
                isinstance(expr, NodeFuncCall) and expr.name.identifier == "checkAnimFlag32" and
                len(expr.args.args) > 0 and isinstance(expr.args.args[0], NodeFuncCall) and
                expr.args.args[0].name.identifier in LOADER_HINTS
            ):
                hint = None
                res_name = "unknown"
                if len(expr.args.args[0].args.args) > 0 and isinstance(expr.args.args[0].args.args[0], NodeString):
                    res_name = expr.args.args[0].args.args[0].value.split(".")[0].replace("-", "_")
                mo = re.match("([^\d_]+)[^\d]+(\d+)", var_name)
                if mo:
                    hint = mo.group(1) + "_" + LOADER_HINTS[expr.args.args[0].name.identifier] + "_" + res_name

                if hint not in section.var_hints.values():
                    section.var_hints[var_name] = hint
        else:
            section.var_hints[var_name] = None

        if (
            isinstance(expr, NodeBinaryExpr) and expr.operator in ["+", "-", "*", "/"] and
            isinstance(expr.left, NodeIdentifier) and expr.left.identifier == var_name
        ):
            return NodeAssignment(None, NodeIdentifier(None, var_name), expr.operator + "=", expr.right)

        return NodeAssignment(None, NodeIdentifier(None, var_name), "=", expr)

    def use_var(self, section, kind, index, init = False):
        if kind not in section.vars:
            section.vars[kind] = {}

        if index not in section.vars[kind]:
            section.vars[kind][index] = {"init": init}

    def get_const_by_value(self, var, node):
        if not isinstance(var, NodeIdentifier):
            return node
        if not isinstance(node, NodeInteger | NodeNumber | NodeRawInteger):
            return node
        if var.identifier not in c1script.mappings.ALIEN_VARS_CONSTANTS:
            return node

        consts = c1script.mappings.ALIEN_VARS_CONSTANTS[var.identifier]
        raw_value = node.result

        if raw_value in consts:
            return NodeIdentifier(node.loc, consts[raw_value])

        return node
    
    def get_const_flags_by_value(self, var, node):
        if not isinstance(var, NodeIdentifier):
            return node

        if not isinstance(node, NodeInteger | NodeNumber | NodeRawInteger):
            return node
        if var.identifier not in c1script.mappings.ALIEN_VARS_CONSTANTS:
            return node

        consts = c1script.mappings.ALIEN_VARS_CONSTANTS[var.identifier]
        raw_value = node.result
        flags = []
        rest = raw_value
        for i in range(32):
            const = 1 << i
            if const in consts and (rest & const) != 0:
                flags.append(consts[const])
                rest = rest & ~const

        if len(flags) == 0:
            return node
        
        result = NodeIdentifier(node.loc, flags[0])

        for flag in flags[1:]:
            result = NodeBinaryExpr(node.loc, result, NodeIdentifier(node.loc, flag), "|")

        if rest != 0:
            result = NodeBinaryExpr(node.loc, result,  NodeRawInteger(node.loc, rest), "|")

        return result

    def make_dependency(self, section, label_name):
        label = self.labels[label_name]
        
        if label.loc >= section.start and label.loc <= section.end:
            return
        
        for i in range(len(self.sections)):
            s = self.sections[i]

            if label.loc >= s.start and label.loc <= s.end:
                if i not in section.deps:
                    section.deps.append(i)

                return

    def generate_strats_trees(self):
        print("\nGenerating trees for strats...")

        unused_sections = set(range(len(self.sections)))
        refs = {k: [] for k in range(len(self.sections))}

        for strat, section in self.strats.items():
            sections_indexes = self.get_all_deps(self.sections[section]) + [section]
            for i in sections_indexes:
                if i != section:
                    refs[i].append(section)
            sections = [self.sections[i] for i in sections_indexes]

            units, vars_count = self.generate_usages(sections)
            for s in sections:
                units += s.trees

            self.apply_var_hints(units, sections)

            self.strat_trees[strat] = NodeFile(None, units)
            print(f"  generated {strat} with {len(sections_indexes)} sections, {vars_count} variables")

            unused_sections = unused_sections.difference(set(sections_indexes))

        for section, strats in refs.items():
            if len(strats) > 1:
                joined = ", ".join([f"`{self.sections[strat].name}`" for strat in strats])
                print(f"WARNING!!! Section `{self.sections[section].name}` used in multiple strats: {joined}. Pasting it to each file")

        if len(unused_sections) > 0:
            sections = [self.sections[i] for i in unused_sections]
            units, vars_count = self.generate_usages(sections)
            for s in sections:
                units += s.trees
            strat = "__unused"

            self.apply_var_hints(units, sections)

            self.strat_trees[strat] = NodeFile(None, units)
            print(f"  generated {strat} with {len(unused_sections)} sections, {vars_count} variables")
            
    def get_all_deps(self, section):
        deps = set(section.deps)
        prev_deps = set()

        while deps != prev_deps:
            prev_deps = deps

            for dep in prev_deps:
                deps = deps.union(set(self.sections[dep].deps))

        return sorted(list(deps))
    
    def generate_usages(self, sections):
        preloads = [NodePreload(None, NodeString(None, p)) for p in self.preloads]

        all_vars = {vk: {} for vk in c1script.mappings.VAR_MAP.keys()}

        for section in sections:
            for vk, vars in section.vars.items():
                for index, data in vars.items():
                    if index not in all_vars[vk]:
                        all_vars[vk][index] = {"local": data["init"] and vk in ["vars", "params"]}
                    else:
                        all_vars[vk][index]["local"] = False

        usages = []
        vars_count = 0
        
        for vk, vars in all_vars.items():
            for index in sorted(vars.keys()):
                vars_count += 1

                comment = None
                if vars[index]["local"]:
                    comment = "local"

                name = c1script.mappings.VAR_MAP[vk]["name_pfx"] + str(index)
                if vk == "alien_vars" and index in c1script.mappings.ALIEN_VARS:
                        name = c1script.mappings.ALIEN_VARS[index]
                usages.append(NodeUse(None, NodeIdentifier(None, vk), NodeInteger(None, index), NodeIdentifier(None, name), comment))

        return preloads + usages, vars_count

    def apply_var_hints(self, units, sections):
        hints = {}
        for s in sections:
            for var, hint in s.var_hints.items():
                if var in hints:
                    hints[var] = None
                else:
                    hints[var] = hint

        for unit in units:
            for node in unit.walk():
                if isinstance(node, NodeIdentifier) and node.identifier in hints and hints[node.identifier] is not None:
                    node.identifier = hints[node.identifier]

    def unhandled_line(self, insn, comment = None):
        self.unhandled_count += 1

        return NodeUnhandled(None, insn.text, comment)
