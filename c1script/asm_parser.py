"""
Converting assemply input into internal representation

Very poor implementation but enough for current needs
"""

import re
from c1script.tokenizer import TokenType

class Insn:
    def __init__(self, op, args, loc, text):
        self.op = op
        self.args = args
        self.loc = loc
        self.text = text

class Label:
    def __init__(self, name, loc, text):
        self.name = name
        self.loc = loc
        self.proc = False
        self.trigger = False
        self.strat = None
        self.jumps = []
        self.nosplit = False
        self.text = text

class StratAttrs:
    def __init__(self):
        self.name = None
        self.pc = None
        self.vars = None

class LabelRef:
    def __init__(self, label):
        self.label = label

class Eval:
    def __init__(self, eval_insns):
        self.eval_insns = eval_insns

class EvalInsn:
    def __init__(self, op, args):
        self.op = op
        self.args = args

class AsmParser:
    def __init__(self, tokens, lines):
        self.tokens = list(tokens)
        self.tokens_read = 0
        self.strat_attrs = {}
        self.preloads = []
        self.lines = lines

    def parse(self):
        self.insns = []

        while True:
            tokens = self.read_line_tokens()
            if tokens is None:
                break

            if tokens[0].kind == TokenType.ATTRIBUTE:
                self.parse_attribute(tokens)
            elif len(tokens) == 2 and tokens[1].kind == TokenType.COLON:
                self.parse_label(tokens)
            elif tokens[0].kind == TokenType.IDENTIFIER:
                self.parse_insn(tokens)
            elif tokens[0].kind == TokenType.EOF:
                return self.insns, self.strat_attrs.values(), self.preloads
            else:
                raise Exception(f"Cannot understand the line from tokens: {[t.__format__(None) for t in tokens]}")
            
        return self.insns, self.strat_attrs.values(), self.preloads
            
    def parse_attribute(self, tokens):
        if len(tokens) != 3:
            raise Exception(f"Invalid number of tokens in line: {[t.__format__(None) for t in tokens]}")

        attr = tokens[1].data
        val = tokens[2].data

        if attr == "entry":
            return

        if attr == "preload":
            self.preloads.append(val)
            return

        mo = re.match("^strat(\d+)_(\w+)$", attr)
        if not mo:
            raise Exception(f"Invalid attribute: {attr}")

        index = int(mo.group(1))
        if index not in self.strat_attrs:
            self.strat_attrs[index] = StratAttrs()

        match mo.group(2):
            case "name": self.strat_attrs[index].name = val
            case "pc": self.strat_attrs[index].pc = val
            case "vars": self.strat_attrs[index].vars = val
            case _: raise Exception(f"Invalid attribute: {attr}")

    def parse_label(self, tokens):
        if len(tokens) != 2:
            raise Exception(f"Invalid number of tokens in line: {[t.__format__(None) for t in tokens]}")

        self.insns.append(Label(tokens[0].data, self.line, self.lines[self.line - 1]))

    def parse_insn(self, tokens):
        op = tokens[0].data

        i = 1
        args = []
        while i < len(tokens):
            arg, i = self.parse_expr(tokens, i)
            args.append(arg)

        self.insns.append(Insn(op, args, self.line, self.lines[self.line - 1]))

    def parse_expr(self, tokens, i):
        match tokens[i].kind:
            case TokenType.INTEGER:
                return int(tokens[i].data), i + 1
            case TokenType.DECIMAL:
                return int(tokens[i].data), i + 1
            case TokenType.STRING:
                return tokens[i].data, i + 1
            case TokenType.IDENTIFIER:
                return LabelRef(tokens[i].data), i + 1
            case TokenType.OPEN_BRACE:
                return self.parse_eval(tokens, i)
            case TokenType.OPERATOR: # special case of minus recognized as operator
                if tokens[i].data == "-" and tokens[i + 1].kind in [TokenType.INTEGER, TokenType.DECIMAL]:
                    return -int(tokens[i + 1].data), i + 2
                else:
                    raise Exception(f"Unexpected token {tokens[i]} in {[t.__format__(None) for t in tokens]}")
            case _:
                raise Exception(f"Unexpected token {tokens[i]} in {[t.__format__(None) for t in tokens]}")
            
    def parse_eval(self, tokens, i):
        i += 1
        insns = []

        while tokens[i].kind != TokenType.CLOSE_BRACE:
            if tokens[i].kind != TokenType.IDENTIFIER:
                raise Exception(f"Unexpected token at index {i} in {[t.__format__(None) for t in tokens]}")
            
            op = tokens[i].data
            i += 1

            args = []
            while tokens[i].kind in [TokenType.INTEGER, TokenType.DECIMAL, TokenType.OPERATOR, TokenType.STRING, TokenType.OPEN_BRACE]:
                arg, i = self.parse_expr(tokens, i)
                args.append(arg)

            insns.append(EvalInsn(op, args))

        i += 1
        
        return Eval(insns), i

    def read_line_tokens(self):
        if self.tokens_read >= len(self.tokens):
            return
        
        self.line = self.tokens[self.tokens_read].line
        tokens = []

        while self.tokens_read < len(self.tokens) and self.tokens[self.tokens_read].line == self.line:
            tokens.append(self.tokens[self.tokens_read])
            self.tokens_read += 1

        return tokens
