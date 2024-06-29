"""
Splits c1s source into tokens
"""

import enum, re, decimal

class TokenType(enum.Enum):
	"""
	The type of token
	"""
	
	INVALID = 0
	KEYWORD = 1
	IDENTIFIER = 2 # abcdefg, Label_230 ...
	STRING = 3 # "abcedefg", "CROC.MOD", "Croc!!" ...
	INTEGER = 4 # 293 0x7FFF
	DECIMAL = 5 # 50.0
	
	OPEN_PARENT = 6 # '('
	CLOSE_PARENT = 7 # ')'
	OPEN_BRACE = 8 # '{'
	CLOSE_BRACE = 9 # '}'
	OPEN_BRACKET = 10 # '['
	CLOSE_BRACKET = 11 # ']'
	COMMA = 12 # ','
	OPERATOR = 13 # '+', '>=', 'and', etc.
	ATTRIBUTE = 14 # `@``
	COLON = 15 # `:`
	EOF = 16

class Token:
	"""
	A token 
	"""
	
	def __init__(self, kind, data = None, line = None, pos = None):
		self.kind = kind
		self.data = data
		self.line = line
		self.pos = pos
	
	def __format__(self, _unused):
		match (self.kind):
			case TokenType.KEYWORD: return f"Keyword {self.data}"
			case TokenType.IDENTIFIER: return f"Identifier {self.data}"
			case TokenType.STRING: return f"String {self.data}"
			case TokenType.INTEGER: return f"Integer {self.data}"
			case TokenType.DECIMAL: return f"Number {self.data}"
			
			case TokenType.OPEN_PARENT: return "Open Parent"
			case TokenType.CLOSE_PARENT: return "Close Parent"
			case TokenType.OPEN_BRACE: return "Open Brace"
			case TokenType.CLOSE_BRACE: return "Close Brace"
			case TokenType.OPEN_BRACKET: return "Open Bracket"
			case TokenType.CLOSE_BRACKET: return "Close Bracket"
			case TokenType.COMMA: return "Comma"
			case TokenType.OPERATOR: return f"Operator {self.data}"
			case TokenType.ATTRIBUTE: return "Attribute"
			case TokenType.COLON: return "Colon"
			case TokenType.EOF: return "End of file"
			
			case _: return f"Invalid Token : {self.data}"

class TokenizerException(Exception):
	def __init__(self, message, line, pos):
		super().__init__(message)
		self.message = message
		self.line = line
		self.pos = pos

	def __str__(self):
		return f"{self.message} at line {self.line}, pos {self.pos}"

KEYWORDS = [
	"const",
	"preload",
	"use",
	"as",
	"global",
	"proc",
	"trigger",
	"strat",
	"if",
	"else",
	"unless",
	"while",
	"repeat",
	"until",
	"for",
	"from",
	"to",
	"immediately",
	"switch",
	"case",
	"default",
	"true",
	"false",
	"and",
	"or",
	"jumping",
	"falling",
	"animend",
	"raw"
]

def print_tokens(tokens):
	"""
	Print a list of tokens (for debugging)
	"""
	
	for t in tokens:
		print(f"{t}")

def is_alpha(c):
	"""
	Returns if a char is alphabetic
	"""
	
	c = ord(c)
	
	return ((c > 0x40) and (c < 0x5B or c > 0x60) and (c < 0x7B or c > 0x7F)) or (c == ord("_"))

def is_numeric(c):
	"""
	Returns if the char is numeric
	"""
	
	c = ord(c)
	
	return (c >= 0x30 and c <= 0x39)

def is_alpha_numeric(c):
	"""
	Returns if a char is alphanumeric
	"""
	
	return is_alpha(c) or is_numeric(c)

def tokens(text):
	"""
	Load a file and tokenise it
	"""
	
	i = 0
	line = 1 # starting from 1
	line_start = 0

	while (i < len(text)):
		c = text[i]
		start = i
		
		# Whitespace
		if (c in '\t\r '):
			pass

	    # Newline
		elif (c == "\n"):
			line += 1
			line_start = i + 1
		
		# Symbols
		elif (is_alpha(c)):
			string = ""
			
			while (i < len(text)):
				c = text[i]
				
				if (not is_alpha_numeric(c)):
					break
				
				string += c
				
				i += 1
			
			i -= 1
			
			if string in KEYWORDS:
				yield Token(TokenType.KEYWORD, string, line, start - line_start)
			else:
				yield Token(TokenType.IDENTIFIER, string, line, start - line_start)
		
		# Numbers
		elif (is_numeric(c) or c == "."):
			string = ""
			
			while (i < len(text)):
				c = text[i]
				
				if (not (is_numeric(c) or is_alpha(c) or c == ".")):
					break
				
				string += c
				
				i += 1
			
			i -= 1
			
			# What kind of number though?
			if (re.match("^0x[\da-fA-F]+$", string)):
				yield Token(TokenType.INTEGER, int(string, 0), line, start - line_start)
			elif (re.match("^[+\-]?\d*\.\d+$", string)):
				yield Token(TokenType.DECIMAL, decimal.Decimal(string), line, start - line_start)
			elif (re.match("^[+\-]?[0-9]+$", string)):
				yield Token(TokenType.INTEGER, int(string), line, start - line_start)
			elif (string == "+" or string == "-"):
				yield Token(TokenType.OPERATOR, string, line, start - line_start)
			else:
				raise TokenizerException(f"Warning: Unexpected token '{string}'", line, start - line_start)
		
		# Strings
		elif (c == '"'):
			i += 1
			
			string = ""
			
			while (i < len(text)):
				c = text[i]

				if (c == "\n"):
					raise TokenizerException("Unexpected newline inside string literal", line, start - line_start)
				
				if (c == '"'):
					break
				
				string += c
				
				i += 1
			
			yield Token(TokenType.STRING, string, line, start - line_start)
		
		elif (c == "("):
			yield Token(TokenType.OPEN_PARENT, c, line, start - line_start)

		elif (c == ")"):
			yield Token(TokenType.CLOSE_PARENT, c, line, start - line_start)
		
		elif (c == "{"):
			yield Token(TokenType.OPEN_BRACE, c, line, start - line_start)
		
		elif (c == "}"):
			yield Token(TokenType.CLOSE_BRACE, c, line, start - line_start)
		
		elif (c == "["):
			yield Token(TokenType.OPEN_BRACKET, c, line, start - line_start)
		
		elif (c == "]"):
			yield Token(TokenType.CLOSE_BRACKET, c, line, start - line_start)
		
		elif (c == ","):
			yield Token(TokenType.COMMA, c, line, start - line_start)

		elif (c == "@"):
			yield Token(TokenType.ATTRIBUTE, c, line, start - line_start)
		
		elif (c == ":"):
			yield Token(TokenType.COLON, c, line, start - line_start)

		elif (c in "+-*/=<>!"):
			i += 1
				
			if (text[i] == "="):
				yield Token(TokenType.OPERATOR, c + text[i], line, start - line_start)
				i += 1
			elif (c == ">" and text[i] == ">") or (c == "<" and text[i] == "<"):
				yield Token(TokenType.OPERATOR, c + text[i], line, start - line_start)
				i += 1
			else:
				yield Token(TokenType.OPERATOR, c, line, start - line_start)

			i -= 1

		elif (c in "&|"):
			yield Token(TokenType.OPERATOR, c, line, start - line_start)
		
		# Comments
		elif (c in ["#", ";"]):
			while (i < len(text)):
				i += 1
				
				c = text[i]
				
				if (c == '\n'):
					break
			i -= 1
		
		else:
			raise TokenizerException(f"Warning: Unknown char '{c}'", line, start - line_start)
		
		i += 1

	yield Token(TokenType.EOF, None, line, len(text) - line_start)

	return tokens

if (__name__ == "__main__"):
	import sys
	
	text = open(sys.argv[1]).read()
	print_tokens(tokens(text))
