"""
Syntax tree node types
"""

import decimal
from types import NoneType
import c1script.mappings

class NodeLocation:
    def __init__(self, line, pos):
        self.line = line
        self.pos = pos

class NodeException(Exception):
    def __init__(self, message, loc):
        super().__init__(message)
        self.message = message
        self.loc = loc

    def __str__(self):
        return f"{self.message} at line {self.loc.line}, pos {self.loc.pos}"
    
class TriggerRef:
    def __init__(self, trigger):
        self.trigger = trigger

    def __formet__(self, _unused):
        return f"trigger:{self.trigger}"

    def __str__(self):
        return f"trigger:{self.trigger}"

class NodeBase:
    def __init__(self, loc):
        self.loc = loc
        self.result = self.eval()

    def children(self):
        return []

    def description(self):
        raise Exception("Not implemented")
    
    def eval(self):
        return None

    def assert_type(self, value, klass):
        if not issubclass(value.__class__, klass):
            raise Exception(f"Expected {value} to be {klass.__name__}")

        return value

    def assert_list_type(self, array, klass):
        for value in array:
            if not issubclass(value.__class__, klass):
                raise Exception(f"Expected {value} to be {klass.__name__}")

        return array
    
    def assert_string(self, string, allowed):
        if string not in allowed:
            raise Exception(f"Expected {string} to be in {allowed}")

        return string
    
    def format_tree(self, parent_prefix = "", last = True):
        if (last):
            prefix = parent_prefix + "└── "
            prefix_for_child = parent_prefix + "    "
        else:
            prefix = parent_prefix + "├── "
            prefix_for_child = parent_prefix + "│   "
        
        text = prefix + self.description()
        if self.result != None:
            text += f" (raw result = {self.result})"
        text += "\n"
        children = self.children()
        for i in range(len(children)):
            text += children[i].format_tree(prefix_for_child, i == len(children) - 1)

        return text

class NodeFile(NodeBase):
    def __init__(self, loc, units):
        super().__init__(loc)
        self.units = self.assert_list_type(units, NodeUnit)

    def children(self):
        return self.units

    def description(self):
        return "Strat file"

class NodeUnit(NodeBase):
    pass

class NodeConst(NodeUnit):
    def __init__(self, loc, name, expr):
        super().__init__(loc)
        self.name = self.assert_type(name, NodeIdentifier)
        self.expr = self.assert_type(expr, NodeExpr)

    def children(self):
        return [self.name, self.expr]

    def description(self):
        return "const"
    
class NodePreload(NodeUnit):
    def __init__(self, loc, strat):
        super().__init__(loc)
        self.strat = self.assert_type(strat, NodeString)

    def description(self):
        return f"preload '{self.strat}'"

class NodeUse(NodeUnit):
    def __init__(self, loc, kind, index, alias, comment = None):
        super().__init__(loc)
        self.kind = self.assert_type(kind, NodeIdentifier)
        self.index = self.assert_type(index, NodeInteger)
        self.alias = self.assert_type(alias, NodeIdentifier)
        self.comment = self.assert_type(comment, str | NoneType)

    def children(self):
        return [self.kind, self.index, self.alias]

    def description(self):
        return "use"
    
class NodeGlobalVar(NodeUnit):
    def __init__(self, loc, name):
        super().__init__(loc)
        self.name = self.assert_type(name, NodeIdentifier)

    def children(self):
        return [self.name]

    def description(self):
        return "Global var"

class NodeProc(NodeUnit):
    def __init__(self, loc, name, block):
        super().__init__(loc)
        self.name = self.assert_type(name, NodeIdentifier)
        self.block = self.assert_type(block, NodeBlock)

    def children(self):
        return [self.name, self.block]

    def description(self):
        return "Proc"

class NodeTrigger(NodeUnit):
    def __init__(self, loc, name, block):
        super().__init__(loc)
        self.name = self.assert_type(name, NodeIdentifier)
        self.block = self.assert_type(block, NodeBlock)

    def children(self):
        return [self.name, self.block]

    def description(self):
        return "Trigger"

class NodeStrat(NodeUnit):
    def __init__(self, loc, name, block):
        super().__init__(loc)
        self.name = self.assert_type(name, NodeIdentifier)
        self.block = self.assert_type(block, NodeBlock)

    def children(self):
        return [self.name, self.block]

    def description(self):
        return "Strat"

class NodeBlock(NodeBase):
    def __init__(self, loc, statements):
        super().__init__(loc)
        self.statements = self.assert_list_type(statements, NodeStatement)

    def children(self):
        return self.statements

    def description(self):
        return "Block"

class NodeStatement(NodeBase):
    pass

class NodeCommand(NodeStatement):
    def __init__(self, loc, name, args):
        super().__init__(loc)
        self.name = self.assert_type(name, NodeIdentifier)
        self.args = self.assert_type(args, NodeArgs)

    def children(self):
        return [self.name, self.args]

    def description(self):
        return "Command"

class NodeProcCall(NodeStatement):
    def __init__(self, loc, name):
        super().__init__(loc)
        self.name = self.assert_type(name, NodeIdentifier)

    def children(self):
        return [self.name]

    def description(self):
        return "Proc Call"

class NodeAssignment(NodeStatement):
    def __init__(self, loc, name, operator, expr):
        super().__init__(loc)
        self.name = self.assert_type(name, NodeIdentifier)
        self.operator = self.assert_string(operator, ["=", "+=", "-=", "*=", "/="])
        self.expr = self.assert_type(expr, NodeExpr)

    def children(self):
        return [self.name, self.expr]

    def description(self):
        return f"Assignment {self.operator}"
    
class NodeVar(NodeStatement):
    def __init__(self, loc, name, expr):
        super().__init__(loc)
        self.name = self.assert_type(name, NodeIdentifier)
        self.expr = self.assert_type(expr, NodeExpr)

    def children(self):
        return [self.name, self.expr]

    def description(self):
        return "Local var"

class NodeControl(NodeStatement):
    pass

class NodeIf(NodeControl):
    def __init__(self, loc, condition, block, else_part = None):
        super().__init__(loc)
        self.condition = self.assert_type(condition, NodeExpr | NodeSpecialCondition)
        self.block = self.assert_type(block, NodeBlock)
        self.else_part = self.assert_type(else_part, NodeBlock | NodeIf | NoneType)

    def children(self):
        return [c for c in [self.condition, self.block, self.else_part] if c is not None]

    def description(self):
        return "if"

class NodeWhile(NodeControl):
    def __init__(self, loc, condition, imm, block):
        super().__init__(loc)
        self.condition = self.assert_type(condition, NodeExpr)
        self.imm = self.assert_type(imm, bool)
        self.block = self.assert_type(block, NodeBlock)

    def children(self):
        return [self.condition, self.block]

    def description(self):
        return "while"

class NodeRepeatUntil(NodeControl):
    def __init__(self, loc, condition, imm, block):
        super().__init__(loc)
        self.condition = self.assert_type(condition, NodeExpr)
        self.imm = self.assert_type(imm, bool)
        self.block = self.assert_type(block, NodeBlock)

    def children(self):
        return [self.condition, self.block]

    def description(self):
        return "repeat-until"

class NodeFor(NodeControl):
    def __init__(self, loc, var, start_value, end_value, imm, block):
        super().__init__(loc)
        self.var = self.assert_type(var, NodeIdentifier)
        self.start_value = self.assert_type(start_value, NodeExpr)
        self.end_value = self.assert_type(end_value, NodeExpr)
        self.imm = self.assert_type(imm, bool)
        self.block = self.assert_type(block, NodeBlock)

    def children(self):
        return [self.var, self.start_value, self.end_value, self.block]

    def description(self):
        return "for"

class NodeSwitch(NodeControl):
    def __init__(self, loc, expr, cases, default = None):
        super().__init__(loc)
        self.expr = self.assert_type(expr, NodeExpr)
        self.cases = self.assert_list_type(cases, NodeCase)
        self.default = self.assert_type(default, NodeBlock | NoneType)

    def children(self):
        return [c for c in [self.expr] + self.cases + [self.default] if c is not None]

    def description(self):
        return "switch"

class NodeCase(NodeBase):
    def __init__(self, loc, expr, block):
        super().__init__(loc)
        self.expr = self.assert_type(expr, NodeExpr)
        self.block = self.assert_type(block, NodeBlock)

    def children(self):
        return [self.expr, self.block]

    def description(self):
        return "case"

class NodeExpr(NodeBase):
    def assert_operand_result_type(self, operator, node, klass):
        if not issubclass(node.result.__class__, klass):
            raise NodeException(f"Unsupported operand `{node.result}` for {operator}", node.loc)

class NodeBinaryExpr(NodeExpr):
    def __init__(self, loc, left, right, operator):
        self.left = self.assert_type(left, NodeExpr)
        self.right = self.assert_type(right, NodeExpr)
        self.operator = self.assert_string(
            operator,
            ["and", "or", "&", "|", ">", "<", ">=", "<=", "==", "!=", "+", "-", "*", "/", ">>", "<<"]
        )
        super().__init__(loc)

    def children(self):
        return [self.left, self.right]

    def description(self):
        return f"operator {self.operator}"
    
    def eval(self):
        if self.left.result == None or self.right.result == None:
            return
        
        if self.operator == "+" and isinstance(self.left.result, str):
            self.assert_operand_result_type(self.operator, self.right, str)
            return self.left.result + self.right.result

        self.assert_operand_result_type(self.operator, self.left, int)
        self.assert_operand_result_type(self.operator, self.right, int)

        match self.operator:
            case "and": return int(bool(self.left.result) and bool(self.right.result)) * c1script.mappings.MAGIC_VALUE
            case "or": return int(bool(self.left.result) or bool(self.right.result)) * c1script.mappings.MAGIC_VALUE
            case "|": return self.left.result | self.right.result
            case "&": return self.left.result & self.right.result
            case ">": return int(self.left.result > self.right.result) * c1script.mappings.MAGIC_VALUE
            case "<": return int(self.left.result < self.right.result) * c1script.mappings.MAGIC_VALUE
            case ">=": return int(self.left.result >= self.right.result) * c1script.mappings.MAGIC_VALUE
            case "<=": return int(self.left.result <= self.right.result) * c1script.mappings.MAGIC_VALUE
            case "==": return int(self.left.result == self.right.result) * c1script.mappings.MAGIC_VALUE
            case "!=": return int(self.left.result != self.right.result) * c1script.mappings.MAGIC_VALUE
            case "+": return self.left.result + self.right.result
            case "-": return self.left.result - self.right.result
            case "*": return self.left.result * self.right.result / c1script.mappings.MAGIC_VALUE
            case "/": return self.left.result * c1script.mappings.MAGIC_VALUE / self.right.result
            case "<<": return self.left.result << (self.right.result / c1script.mappings.MAGIC_VALUE)
            case ">>": return self.left.result >> (self.right.result / c1script.mappings.MAGIC_VALUE)

class NodeUnaryExpr(NodeExpr):
    def __init__(self, loc, expr, operator):
        self.expr = self.assert_type(expr, NodeExpr)
        self.operator = self.assert_string(operator, ["+", "-", "!"])
        super().__init__(loc)

    def children(self):
        return [self.expr]

    def description(self):
        return f"operator {self.operator} (unary)"

    def eval(self):
        if self.expr.result == None:
            return

        self.assert_operand_result_type(self.operator, self.expr, int)

        match self.operator:
            case "+": return self.expr.result
            case "-": return -self.expr.result
            case "!": return int(self.expr.result == 0) * c1script.mappings.MAGIC_VALUE

class NodeFuncCall(NodeExpr):
    def __init__(self, loc, name, args):
        super().__init__(loc)
        self.name = self.assert_type(name, NodeIdentifier)
        self.args = self.assert_type(args, NodeArgs)

    def children(self):
        return [self.name, self.args]

    def description(self):
        return "Function call"

class NodeArgs(NodeStatement):
    def __init__(self, loc, args):
        super().__init__(loc)
        self.args = self.assert_list_type(args, NodeExpr)

    def children(self):
        return self.args

    def description(self):
        return "Arguments"

class NodeIdentifier(NodeExpr):
    def __init__(self, loc, identifier, value = None):
        super().__init__(loc)
        self.identifier = self.assert_type(identifier, str)
        self.result = value

    def description(self):
        return f"`{self.identifier}` (identifier)"

class NodeNumber(NodeExpr):
    def __init__(self, loc, value):
        self.value = self.assert_type(value, int | decimal.Decimal)
        super().__init__(loc)

    def description(self):
        return f"{self.value} (number)"
    
    def eval(self):
        return int(self.value * c1script.mappings.MAGIC_VALUE)

class NodeInteger(NodeExpr):
    def __init__(self, loc, value):
        self.value = self.assert_type(value, int)
        super().__init__(loc)

    def description(self):
        return f"{self.value} (number)"
    
    def eval(self):
        return self.value * c1script.mappings.MAGIC_VALUE

class NodeString(NodeExpr):
    def __init__(self, loc, value):
        self.value = self.assert_type(value, str)
        super().__init__(loc)

    def description(self):
        return f"\"{self.value}\" (string)"
    
    def eval(self):
        return self.value
    
class NodeRawInteger(NodeExpr):
    def __init__(self, loc, expr):
        self.expr = self.assert_type(expr, NodeExpr)
        self.assert_type(expr.result, int)
        super().__init__(loc)

    def description(self):
        return f"raw integer, (value = {self.expr.result})"
    
    def children(self):
        return [self.expr]
    
    def eval(self):
        return int(self.expr.result / c1script.mappings.MAGIC_VALUE)
    
class NodeBoolean(NodeExpr):
    def __init__(self, loc, value):
        self.value = self.assert_type(value, bool)
        super().__init__(loc)

    def description(self):
        return f"\"{self.value}\" (boolean)"
    
    def eval(self):
        return int(self.value) * c1script.mappings.MAGIC_VALUE
    
class NodeSpecialCondition(NodeBase):
    def __init__(self, loc, name, invert = False):
        self.name = self.assert_type(name, str)
        self.invert = self.assert_type(invert, bool)
        super().__init__(loc)

    def description(self):
        return f"Special condition \"{self.name}\""

class NodeUnhandled(NodeStatement):
    def __init__(self, loc, line, comment = None):
        self.line = self.assert_type(line, str)
        self.comment = self.assert_type(comment, str | NoneType)
        super().__init__(loc)

    def description(self):
        return f"Unhandled statement `{self.line}`"
