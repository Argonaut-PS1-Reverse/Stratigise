"""
Splits disassembler output into tokens
"""

from common import BinaryReadStream
import enum

class TokenType(enum.Enum):
	"""
	The type of token
	"""
	
	INVALID = 0
	SYMBOL = 1 # abcdefg, Label_230 ...
	STRING = 2 # "abcedefg", "CROC.MOD", "Croc!!" ...
	NUMBER = 3 # 293 0x7FFF 50.0
	
	COLON = 4 # ':'
	OPEN_BRACKET = 5 # '{'
	CLOSE_BRACKET = 6 # '}'
	ATTRIBUTE = 7 # '@'

class Token:
	"""
	A token 
	"""
	
	def __init__(self, kind, data = None, location = None):
		self.kind = kind
		self.data = data
		self.location = location
	
	def __format__(self, _unused):
		match (self.kind):
			case TokenType.SYMBOL: return f"Symbol {self.data}"
			case TokenType.STRING: return f"String {self.data}"
			case TokenType.NUMBER: return f"Number {self.data}"
			
			case TokenType.COLON: return "Colon"
			case TokenType.OPEN_BRACKET: return "Open Bracket"
			case TokenType.CLOSE_BRACKET: return "Close Bracket"
			case TokenType.ATTRIBUTE: return "Attribute"
			
			case _: return f"Invalid Token : {self.data}"

def print_tokens(tokens):
	"""
	Print a list of tokens (for debugging)
	"""
	
	for t in tokens:
		print(f"{t}")

def isAlpha(c):
	"""
	Returns if a char is alphabetic
	"""
	
	c = ord(c)
	
	return ((c > 0x40) and (c < 0x5B or c > 0x60) and (c < 0x7B or c > 0x7F)) or (c == ord("_"))

def isNumeric(c):
	"""
	Returns if the char is numeric
	"""
	
	c = ord(c)
	
	return (c >= 0x30 and c <= 0x39) or (ord(".") == c)

def isAlphaNumeric(c):
	"""
	Returns if a char is alphanumeric
	"""
	
	return isAlpha(c) or isNumeric(c)

def tokenise(path):
	"""
	Load a file and tokenise it
	"""
	
	source = BinaryReadStream(path)
	
	stream = source.readBytes(source.getLength()).decode('latin-1')
	
	tokens = []
	
	i = 0
	while (i < len(stream)):
		c = stream[i]
		
		# Whitespace
		if (c in '\t\r '):
			pass
		
		# Symbols
		elif (isAlpha(c)):
			string = ""
			
			while (True):
				c = stream[i]
				
				if (not isAlphaNumeric(c)):
					break
				
				string += c
				
				i += 1
			
			i -= 1
			
			tokens.append(Token(TokenType.SYMBOL, string, i))
		
		# Numbers
		elif (isNumeric(c)):
			string = ""
			
			while (True):
				c = stream[i]
				
				if (not isNumeric(c)):
					break
				
				string += c
				
				i += 1
			
			i -= 1
			
			# What kind of number though?
			if ("." in string):
				string = float(string)
			else:
				string = int(string)
			
			tokens.append(Token(TokenType.NUMBER, string, i))
		
		# Strings
		elif (c == '"'):
			i += 1
			
			string = ""
			
			while (True):
				c = stream[i]
				
				if (c == '"'):
					break
				
				string += c
				
				i += 1
			
			tokens.append(Token(TokenType.STRING, string, i))
		
		elif (c == ":"):
			tokens.append(Token(TokenType.COLON, location = i))
		
		elif (c == "{"):
			tokens.append(Token(TokenType.OPEN_BRACKET, location = i))
		
		elif (c == "}"):
			tokens.append(Token(TokenType.CLOSE_BRACKET, location = i))
		
		elif (c == "@"):
			tokens.append(Token(TokenType.ATTRIBUTE, location = i))
		
		else:
			print(f"Warning: Unknown char '{c}' at {i}")
		
		i += 1
	
	return tokens

if (__name__ == "__main__"):
	import sys
	
	print_tokens(tokenise(sys.argv[1]))
