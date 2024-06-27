"""
Splits c1s source into tokens
"""

import enum, copy

from c1script.nodes import *
from c1script.tokenizer import TokenType
import c1script.mappings

class ParserException(Exception):
    def __init__(self, message, loc):
        super().__init__(message)
        self.message = message
        self.loc = loc

    def __str__(self):
        return f"{self.message} at line {self.loc.line}, pos {self.loc.pos}"
    
class IdentifierType(enum.Enum):
    INVALID = 0
    CONST = 1
    VARIABLE = 2
    COMMAND = 3
    PROC = 4
    TRIGGER = 5
    STRAT = 6
    FUNCTION = 7
    
class IdentifierData:
    def __init__(self, kind, value = None):
        self.kind = kind
        self.value = value

    def __format__(self, _unused):
        match (self.kind):
            case IdentifierType.CONST: return f"Constant = {self.value}"
            case IdentifierType.VARIABLE: return f"Variable {self.value}"
            case IdentifierType.COMMAND: return "Command"
            case IdentifierType.PROC: return "Proc"
            case IdentifierType.TRIGGER: return "Trigger"
            case IdentifierType.STRAT: return "Strat"
            case IdentifierType.FUNCTION: return "Function"

            case _: return f"Invalid Identifier"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.init_identifiers()
        self.next()
        self.cur_id_data = None
        self.strat_defined = False
        self.uses_forbidden = False

    def parse(self):
        return self.parse_file()

    def parse_file(self):
        loc = self.loc()

        units = []

        while not self.is_a(TokenType.EOF):
            units.append(self.parse_unit())

        return NodeFile(loc, units)
    
    def parse_unit(self):
        # if self.strat_defined:
        #     self.error("Nothing should be placed after the strat body")

        self.expect(
            TokenType.KEYWORD,
            "Expected `const`, `preload`, `use`, `global`, `proc`, `trigger`, or `strat` keyword",
            ["const", "preload", "use", "global", "proc", "trigger", "strat"]
        )

        if self.value() not in ["const", "use", "preload"]:
            self.uses_forbidden = True
        
        match self.value():
            case "const": return self.parse_const()
            case "preload": return self.parse_preload()
            case "use": return self.parse_use()
            case "global": return self.parse_global_var()
            case "proc": return self.parse_proc()
            case "trigger": return self.parse_trigger()
            case "strat": return self.parse_strat()

    def parse_const(self):
        loc = self.loc()

        self.expect(TokenType.KEYWORD, "Expected `const` keyword", ["const"])
        self.next()

        name = self.parse_identifier(error = "Expected name of a constant")

        self.expect(TokenType.OPERATOR, "Expected `=` after constant name", ["="])
        self.next()

        expr = self.parse_expr()

        if expr.result is None:
            self.error("Unable to evaluate expression for constant at compile time", expr.loc)

        name.result = expr.result

        self.define(name, IdentifierType.CONST, expr.result)

        return NodeConst(loc, name, expr)
    
    def parse_preload(self):
        loc = self.loc()

        self.expect(TokenType.KEYWORD, "Expected `preload` keyword", ["preload"])
        self.next()

        strat = self.parse_expr()

        if not isinstance(strat.result, str):
            self.error("Expected a string for `preload`", strat.loc)

        return NodePreload(loc, strat)

    def parse_use(self):
        loc = self.loc()

        if self.uses_forbidden:
            self.error("All the `use` statements have to be placed above any var/proc definitions")

        self.expect(TokenType.KEYWORD, "Expected `use` keyword", ["use"])
        self.next()

        kind = self.parse_identifier(error = "Expected name of a variables array")

        if kind.identifier not in c1script.mappings.VAR_MAP.keys():
            self.error(
                f"Wrong variables array `{kind.identifier}`, should be one of {c1script.mappings.VAR_MAP.keys()}",
                kind.loc
            )

        self.expect(TokenType.OPEN_BRACKET, "Expected `[`")
        self.next()

        self.expect(TokenType.INTEGER, "Expected integer index")
        index = self.parse_const_expr()

        if index.result >= c1script.mappings.VAR_MAP[kind.identifier]["limit"]:
            self.error(
                f"Variable index `{index.result}` is too big",
                index.loc
            )

        self.expect(TokenType.CLOSE_BRACKET, "Expected `]`")
        self.next()

        self.expect(TokenType.KEYWORD, "Expected `as` keyword", ["as"])
        self.next()

        alias = self.parse_identifier(error = "Expected identifier for alias")

        self.define(alias, IdentifierType.VARIABLE)

        return NodeUse(loc, kind, index, alias)
    
    def parse_global_var(self):
        loc = self.loc()

        self.expect(TokenType.KEYWORD, "Expected `global` keyword", ["global"])
        self.next()

        name = self.parse_identifier(error = "Expected name of a variable or `[`")
        self.define(name, IdentifierType.VARIABLE)

        return NodeGlobalVar(loc, name)
    
    def parse_proc(self):
        loc = self.loc()

        self.expect(TokenType.KEYWORD, "Expected `proc` keyword", ["proc"])
        self.next()

        name = self.parse_identifier(error = "Expected name of a proc")
        self.define(name, IdentifierType.PROC)

        block = self.parse_block()

        return NodeProc(loc, name, block)
    
    def parse_trigger(self):
        loc = self.loc()

        self.expect(TokenType.KEYWORD, "Expected `trigger` keyword", ["trigger"])
        self.next()

        name = self.parse_identifier(error = "Expected name of a trigger")
        self.define(name, IdentifierType.TRIGGER)

        block = self.parse_block()

        return NodeTrigger(loc, name, block)
    
    def parse_strat(self):
        loc = self.loc()

        self.expect(TokenType.KEYWORD, "Expected `strat` keyword", "strat")
        self.next()

        name = self.parse_identifier(error = "Expected name of a strat")
        self.define(name, IdentifierType.STRAT)

        block = self.parse_block()

        self.strat_defined = True

        return NodeStrat(loc, name, block)
    
    def parse_block(self):
        loc = self.loc()

        self.expect(TokenType.OPEN_BRACE, "Expected `{`")
        self.next()

        identifiers = copy.deepcopy(self.identifiers)

        statements = []

        while not self.is_a(TokenType.CLOSE_BRACE):
            statements.append(self.parse_statement())

        self.identifiers = identifiers

        self.expect(TokenType.CLOSE_BRACE, "Expected `}`")
        self.next()

        return NodeBlock(loc, statements)
    
    def parse_statement(self):
        if self.is_a(TokenType.KEYWORD):
            return self.parse_control()

        elif self.is_a(TokenType.IDENTIFIER):
            if self.cur_id_data is None:
                return self.parse_var()
            else:
                if self.identifier_is_a(IdentifierType.COMMAND):
                    return self.parse_command()
                if self.identifier_is_a(IdentifierType.PROC):
                    return self.parse_proc_call()
                if self.identifier_is_a(IdentifierType.VARIABLE):
                    return self.parse_assignment()
                else:
                    self.error("Expected assignment (`=`, `+=`, etc.), command, or proc call")

        else:
            self.error("Expected assignment, command, proc call, or control flow operator")

    def parse_command(self):
        loc = self.loc()
        
        self.expect_defined_identifier()
        if not self.identifier_is_a(IdentifierType.COMMAND):
            self.error("Expected command")

        identifier = self.parse_identifier()

        self.expect(TokenType.OPEN_PARENT, "Expected `(`")
        self.next()

        args = self.parse_args()

        self.expect(TokenType.CLOSE_PARENT, "Expected `)` or `,` after command argument")
        self.next()

        signature = c1script.mappings.COMMAND_MAP[identifier.identifier]
        self.check_args(args, signature)

        return NodeCommand(loc, identifier, args)

    def parse_proc_call(self):
        loc = self.loc()
        
        self.expect_defined_identifier()
        if not self.identifier_is_a(IdentifierType.PROC):
            self.error("Expected proc name")

        identifier = self.parse_identifier()

        self.expect(TokenType.OPEN_PARENT, "Expected `(`")
        self.next()

        self.expect(TokenType.CLOSE_PARENT, "Expected `)` immediately after `(`")
        self.next()

        return NodeProcCall(loc, identifier)
    
    def parse_assignment(self):
        loc = self.loc()

        self.expect_defined_identifier()
        if not self.identifier_is_a(IdentifierType.VARIABLE):
            self.error("Expected variable")

        identifier = self.parse_identifier()

        self.expect(
            TokenType.OPERATOR,
            "Only assignment operators are allowed in top level statements (`=`, `+=`, etc.)",
            ["=", "+=", "-=", "*=", "/="]
        )
        operator = self.take()
        rvalue = self.parse_expr()

        return NodeAssignment(loc, identifier, operator, rvalue)
    
    def parse_var(self):
        loc = self.loc()

        identifier = self.parse_identifier()
        self.define(identifier, IdentifierType.VARIABLE)

        self.expect(
            TokenType.OPERATOR,
            "Newly declared local variables must be immediately initialized with `=`",
            ["="]
        )
        self.next()
        rvalue = self.parse_expr()

        return NodeVar(loc, identifier, rvalue)
    
    def parse_control(self):
        loc = self.loc()

        match self.value():
            case "if": return self.parse_if()
            case "unless": return self.parse_unless()
            case "while": return self.parse_while()
            case "repeat": return self.parse_repeat_until()
            case "for": return self.parse_for()
            case "switch": return self.parse_switch()
            case _: self.error(f"Unexpected keyword {self.value()}, only `if`, `unless`, `while`, `repeat`, `for`, and `switch` are supported")

    def parse_if(self):
        loc = self.loc()

        self.expect(TokenType.KEYWORD, "Expected `if`", ["if"])
        self.next()
        self.expect(TokenType.OPEN_PARENT, "Expected a `(` after `if`")
        self.next()
        
        condition = self.parse_if_condition()

        self.expect(TokenType.CLOSE_PARENT, "Expected a `)` after condition")
        self.next()

        block = self.parse_block()

        if self.is_a(TokenType.KEYWORD, "else"):
            else_part = self.parse_else()
            return NodeIf(loc, condition, block, else_part)
        else:
            return NodeIf(loc, condition, block)
        
    def parse_if_condition(self):
        loc = self.loc()

        invert_locs = []

        while self.is_a(TokenType.OPERATOR, "!"):
            invert_locs.append(self.loc)
            self.next()

        if self.is_a(TokenType.KEYWORD, list(c1script.mappings.SPECIAL_CONDITIONS.keys())):
            name = self.take()
            self.expect(TokenType.OPEN_PARENT, "Expected a `(`")
            self.next()
            self.expect(TokenType.CLOSE_PARENT, "Expected a `)`")
            self.next()

            return NodeSpecialCondition(loc, name, len(invert_locs) % 2 == 1)
        
        condition = self.parse_expr()

        for invert_loc in reversed(invert_locs):
            condition = NodeUnaryExpr(invert_loc, condition, "!")

        return condition
        
    def parse_else(self):
        self.expect(TokenType.KEYWORD, "Expected `else`", ["else"])
        self.next()

        if self.is_a(TokenType.KEYWORD, "if"):
            return self.parse_if()
        elif self.is_a(TokenType.OPEN_BRACE):
            return self.parse_block()
        else:
            self.error("Expected a block or another `if` after `else`")

    def parse_unless(self):
        loc = self.loc()

        self.expect(TokenType.KEYWORD, "Expected `unless`", ["unless"])
        self.next()
        self.expect(TokenType.OPEN_PARENT, "Expected a `(` after `unless`")
        self.next()
        
        condition = self.parse_expr()

        self.expect(TokenType.CLOSE_PARENT, "Expected a `)` after condition")
        self.next()

        block = self.parse_block()

        if self.is_a(TokenType.KEYWORD, "else"):
            self.error("`else` is not supported for `unless`")
        else:
            return NodeUnless(loc, condition, block)
        
    def parse_while(self):
        loc = self.loc()

        self.expect(TokenType.KEYWORD, "Expected `while`", ["while"])
        self.next()
        self.expect(TokenType.OPEN_PARENT, "Expected a `(` after `while`")
        self.next()
        
        condition = self.parse_expr()

        self.expect(TokenType.CLOSE_PARENT, "Expected a `)` after condition")
        self.next()

        imm = False
        if self.is_a(TokenType.KEYWORD, "immediately"):
            imm = True
            self.next()
        else:
            self.expect(TokenType.OPEN_BRACE, "Expected `{` of `immediately`")

        block = self.parse_block()

        return NodeWhile(loc, condition, imm, block)
    
    def parse_repeat_until(self):
        loc = self.loc()

        self.expect(TokenType.KEYWORD, "Expected `repeat`", ["repeat"])
        self.next()

        imm = False
        if self.is_a(TokenType.KEYWORD, "immediately"):
            imm = True
            self.next()
        else:
            self.expect(TokenType.OPEN_BRACE, "Expected `{` of `immediately`")

        block = self.parse_block()

        self.expect(TokenType.KEYWORD, "Expected `until` after `repeat` block", ["until"])
        self.next()
        self.expect(TokenType.OPEN_PARENT, "Expected a `(` after `until`")
        self.next()
        
        condition = self.parse_expr()

        self.expect(TokenType.CLOSE_PARENT, "Expected a `)` after condition")
        self.next()

        return NodeRepeatUntil(loc, condition, imm, block)
    
    def parse_for(self):
        loc = self.loc()

        self.expect(TokenType.KEYWORD, "Expected `for`", ["for"])
        self.next()

        self.expect(TokenType.IDENTIFIER, "Expected a counter variable name")
        identifiers = copy.deepcopy(self.identifiers)

        var = self.parse_identifier()

        if var.identifier not in self.identifiers:
            self.define(var, IdentifierType.VARIABLE)

        self.expect(TokenType.KEYWORD, "Expected `from`", ["from"])
        self.next()
        
        start_value = self.parse_expr()

        self.expect(TokenType.KEYWORD, "Expected `to`", ["to"])
        self.next()

        end_value = self.parse_expr()

        imm = False
        if self.is_a(TokenType.KEYWORD, "immediately"):
            imm = True
            self.next()
        else:
            self.expect(TokenType.OPEN_BRACE, "Expected `{` of `immediately`")

        block = self.parse_block()

        self.identifiers = identifiers

        return NodeFor(loc, var, start_value, end_value, imm, block)
    
    def parse_switch(self):
        loc = self.loc()

        self.expect(TokenType.KEYWORD, "Expected `switch`", ["switch"])
        self.next()
        self.expect(TokenType.OPEN_PARENT, "Expected a `(` after `switch`")
        self.next()
        
        value = self.parse_expr()

        self.expect(TokenType.CLOSE_PARENT, "Expected a `)` after `switch` value")
        self.next()
        self.expect(TokenType.OPEN_BRACE, "Expected a `{` before case statements")
        self.next()

        cases = []
        default = None

        while not self.is_a(TokenType.CLOSE_BRACE):
            if self.is_a(TokenType.KEYWORD, ["case"]):
                cases.append(self.parse_case())
            elif self.is_a(TokenType.KEYWORD, ["default"]):
                if default is not None:
                    self.error("Redefinition of `default` case")

                self.next()
                default = self.parse_block()
            else:
                self.error("Expected `case` of `default`")


        self.expect(TokenType.CLOSE_BRACE, "Expected a `}` after case statements")
        self.next()

        return NodeSwitch(loc, value, cases, default)
    
    def parse_case(self):
        loc = self.loc()

        self.expect(TokenType.KEYWORD, "Expected `case`", ["case"])
        self.next()
        self.expect(TokenType.OPEN_PARENT, "Expected a `(` after `case`")
        self.next()
        
        expression = self.parse_expr()

        self.expect(TokenType.CLOSE_PARENT, "Expected a `)` after case expression")
        self.next()

        block = self.parse_block()

        return NodeCase(loc, expression, block)
    
    def parse_expr(self):
        return self.parse_or_expr()
    
    def parse_or_expr(self):
        loc = self.loc()

        acc = self.parse_and_expr()

        while self.is_a(TokenType.KEYWORD, "or"):
            operator = self.take()
            right = self.parse_and_expr()
            acc = NodeBinaryExpr(loc, acc, right, operator)

        return acc
    
    def parse_and_expr(self):
        loc = self.loc()

        acc = self.parse_xor_expr()

        while self.is_a(TokenType.KEYWORD, "and"):
            operator = self.take()
            right = self.parse_xor_expr()
            acc = NodeBinaryExpr(loc, acc, right, operator)

        return acc
    
    def parse_xor_expr(self):
        loc = self.loc()

        acc = self.parse_comparison_expr()

        while self.is_a(TokenType.KEYWORD, "xor"):
            operator = self.take()
            right = self.parse_comparison_expr()
            acc = NodeBinaryExpr(loc, acc, right, operator)

        return acc
    
    def parse_comparison_expr(self):
        loc = self.loc()

        acc = self.parse_bit_shift_expr()

        if self.is_a(TokenType.OPERATOR, ["==", "!=", "<", ">", "<=", ">="]):
            operator = self.take()
            right = self.parse_bit_shift_expr()
            acc = NodeBinaryExpr(loc, acc, right, operator)

        if self.is_a(TokenType.OPERATOR, ["==", "!=", "<", ">", "<=", ">="]):
            self.error("Comparison chaining is not supported")

        return acc
    
    def parse_bit_shift_expr(self):
        loc = self.loc()

        acc = self.parse_add_sub_expr()

        while self.is_a(TokenType.OPERATOR, [">>", "<<"]):
            operator = self.take()
            right = self.parse_add_sub_expr()
            acc = NodeBinaryExpr(loc, acc, right, operator)

        return acc
    
    def parse_add_sub_expr(self):
        loc = self.loc()

        acc = self.parse_mul_div_expr()

        while self.is_a(TokenType.OPERATOR, ["+", "-"]):
            operator = self.take()
            right = self.parse_mul_div_expr()
            acc = NodeBinaryExpr(loc, acc, right, operator)

        return acc
    
    def parse_mul_div_expr(self):
        loc = self.loc()

        acc = self.parse_unary_expr()

        while self.is_a(TokenType.OPERATOR, ["*", "/"]):
            operator = self.take()
            right = self.parse_unary_expr()
            acc = NodeBinaryExpr(loc, acc, right, operator)

        return acc
    
    def parse_unary_expr(self):
        loc = self.loc()

        if self.is_a(TokenType.OPERATOR, ["+", "-", "!"]):
            operator = self.take()
            expr = self.parse_unary_expr()
            return NodeUnaryExpr(loc, expr, operator)
        else:
            return self.parse_value_expr()
        
    def parse_value_expr(self):
        loc = self.loc()

        if self.is_a(TokenType.IDENTIFIER):
            self.expect_defined_identifier()

            if self.identifier_is_a(IdentifierType.FUNCTION):
                return self.parse_func_call()

            elif self.identifier_is_a([IdentifierType.CONST, IdentifierType.VARIABLE]):
                return self.parse_identifier()

            elif self.identifier_is_a([IdentifierType.TRIGGER]):
                return self.parse_identifier()
            
            else:
                self.error("Cannot call command/proc from here")

        elif self.is_a(TokenType.OPEN_PARENT):
            self.next()
            expr = self.parse_expr()

            self.expect(TokenType.CLOSE_PARENT, "Expected matching `)`")
            self.next()

            return expr

        else:
            return self.parse_const_expr()
        
    def parse_func_call(self):
        loc = self.loc()

        if not self.identifier_is_a(IdentifierType.FUNCTION):
            self.error("Expected function name")

        identifier = self.parse_identifier()

        self.expect(TokenType.OPEN_PARENT, "Expected `(` after function call")
        self.next()

        args = self.parse_args()

        self.expect(TokenType.CLOSE_PARENT, "Expected `)` or `,` after function argument")
        self.next()

        signature = c1script.mappings.FUNCTION_MAP[identifier.identifier]
        self.check_args(args, signature)

        return NodeFuncCall(loc, identifier, args)
        
    def parse_args(self):
        loc = self.loc()

        if self.is_a(TokenType.CLOSE_PARENT):
            return NodeArgs(loc, [])
        
        args = [self.parse_expr()]

        while self.is_a(TokenType.COMMA):
            self.next()
            args.append(self.parse_expr())

        return NodeArgs(loc, args)
        
    def parse_const_expr(self):
        loc = self.loc()

        if self.is_a(TokenType.INTEGER):
            return NodeInteger(loc, self.take())
        elif self.is_a(TokenType.DECIMAL):
            return NodeNumber(loc, self.take())
        elif self.is_a(TokenType.STRING):
            return NodeString(loc, self.take())
        elif self.is_a(TokenType.KEYWORD, ["true", "false"]):
            return NodeBoolean(loc, self.take() == "true")
        elif self.is_a(TokenType.KEYWORD, ["raw"]):
            return self.parse_raw_int()
        else:
            self.error(f"Unexpected token `{self.value()}` in expression")

    def parse_raw_int(self):
        loc = self.loc()

        self.expect(TokenType.KEYWORD, "Expected `raw`", ["raw"])
        self.next()
        self.expect(TokenType.OPEN_PARENT, "Expected a `(` after `raw`")
        self.next()

        value = self.parse_expr()
        if not isinstance(value.result, int):
            self.error(f"Expected const integer value", value.loc)

        self.expect(TokenType.CLOSE_PARENT, "Expected a `)` after `raw` value")
        self.next()

        return NodeRawInteger(loc, value)
    
    def parse_identifier(self, error = "Expected identifier"):
        loc = self.loc()

        self.expect(TokenType.IDENTIFIER, error = error)

        if self.identifier_is_a(IdentifierType.CONST):
            value = self.cur_id_data.value
            return NodeIdentifier(loc, self.take(), value)
        elif self.identifier_is_a(IdentifierType.TRIGGER):
            name = self.take()
            return NodeIdentifier(loc, name, TriggerRef(name))
        elif self.identifier_is_a(IdentifierType.VARIABLE):
            return NodeIdentifier(loc, self.take())
        else:
            return NodeIdentifier(loc, self.take())
    
    def next(self):
        self.token = next(self.tokens)
        self.cur_id_data = None

        if self.token.kind == TokenType.IDENTIFIER and self.token.data in self.identifiers:
            self.cur_id_data = self.identifiers[self.token.data]
        
    def take(self):
        data = self.token.data
        self.next()

        return data
    
    def value(self):
        return self.token.data

    def loc(self):
        return NodeLocation(self.token.line, self.token.pos)
    
    def expect(self, kind, error = "Unexpected token", allowed = None):
        if self.token.kind != kind:
            raise ParserException(error, self.loc())
        if allowed != None and self.token.data not in allowed:
            raise ParserException(error, self.loc())
        
    def expect_defined_identifier(self):
        self.expect(TokenType.IDENTIFIER)

        if self.cur_id_data == None:
            self.error(f"Unknown identifier `{self.value()}`")
    
    def is_a(self, kind, value = None):
        if self.token.kind != kind:
            return False
        if value != None:
            if isinstance(value, list):
                if self.token.data not in value:
                    return False
            else:
                if self.token.data != value:
                    return False
        
        return True
    
    def identifier_is_a(self, kind):
        if self.cur_id_data == None:
            return False

        if isinstance(kind, list):
            return self.cur_id_data.kind in kind
        else:
            return self.cur_id_data.kind == kind
    
    def error(self, message, loc = None):
        if loc is None:
            loc = self.loc()

        raise ParserException(message, loc)
    
    def define(self, id, type, value = None):
        if id.identifier in self.identifiers:
            self.error(f"Redefinition of `{id.identifier}` identifier", id.loc)

        self.identifiers[id.identifier] = IdentifierData(type, value)

    def define_command(self, signature):
        name = signature[0]
        name = name[0].lower() + name[1:]
        self.identifiers[name] = IdentifierData( IdentifierType.COMMAND, signature[1:])

    def define_function(self, name):
        name = name[0].lower() + name[1:]
        self.identifiers[name] = IdentifierData( IdentifierType.FUNCTION)

    def init_identifiers(self):
        self.identifiers = {}

        for name in c1script.mappings.COMMAND_MAP.keys():
            self.identifiers[name] = IdentifierData(IdentifierType.COMMAND)

        for name in c1script.mappings.FUNCTION_MAP.keys():
            self.identifiers[name] = IdentifierData(IdentifierType.FUNCTION)

        for consts in c1script.mappings.ALIEN_VARS_CONSTANTS.values():
            for value, name in consts.items():
                self.identifiers[name] = IdentifierData(IdentifierType.CONST, value)

    def check_args(self, args, signature):
        sign = signature.signature

        if "varargs" in sign:
            varargs_pos = sign.index("varargs")
            varargs_count = len(args.args) - len(sign) + 1

            if varargs_count < 0:
                self.error(
                    f"Too few arguments for {signature}, expected at least {len(sign) - 1}, given {len(args.args)}",
                    args.loc
                )
            
            sign = sign[:varargs_pos] + ["eval"] * varargs_count + sign[varargs_pos + 1:]

        if "varargs_int" in sign:
            varargs_pos = sign.index("varargs_int")
            varargs_count = len(args.args) - len(sign) + 1

            if varargs_count < 0:
                self.error(
                    f"Too few arguments for {signature}, expected at least {len(sign) - 1}, given {len(args.args)}",
                    args.loc
                )
            
            sign = sign[:varargs_pos] + ["int16"] * varargs_count + sign[varargs_pos + 1:]

        if len(args.args) != len(sign):
            self.error(
                f"Wrong number of arguments for {signature}, expected {len(sign)}, given {len(args.args)}",
                args.loc
            )

        for i in range(len(sign)):
            type = sign[i]
            arg = args.args[i]

            match type:
                case "int8":
                    if not isinstance(arg.result, int):
                        self.error(f"Expected constant integer argument for {signature}", arg.loc)
                    if arg.result < 0 or arg.result >= 256:
                        self.error(f"Expected integer argument between 0 and 255 for {signature}", arg.loc)

                case "int16":
                    if not isinstance(arg.result, int):
                        self.error(f"Expected constant integer argument for {signature}", arg.loc)

                case "int32":
                    if not isinstance(arg.result, int):
                        self.error(f"Expected constant integer argument for {signature}", arg.loc)

                case "string":
                    if not isinstance(arg.result, str):
                        self.error(f"Expected constant string argument for {signature}", arg.loc)

                case "trigger":
                    if not isinstance(arg.result, TriggerRef):
                        self.error(f"Expected trigger name argument for {signature}", arg.loc)

                case "eval":
                    if arg.result != None and not isinstance(arg.result, int | decimal.Decimal):
                        self.error(f"Expected numeric expression argument for {signature}", arg.loc)

                case "stack":
                    if arg.result != None and not isinstance(arg.result, int | decimal.Decimal):
                        self.error(f"Expected numeric expression argument for {signature}", arg.loc)

                case _:
                    self.error(f"Invalid argument type `{type}` in signature {signature}", arg.loc)

if (__name__ == "__main__"):
    import sys
    import tokenizer
	
    text = open(sys.argv[1]).read()
    tokens = tokenizer.tokens(text)
    tree = Parser(tokens).parse()
    print(tree.format_tree())
