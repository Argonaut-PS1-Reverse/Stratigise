from stratigise.common import BinaryReadStream
import enum

class TokenType(Enum):
	"""
	The type of token
	"""
	
	INVALID = 0
	SYMBOL = 1
	STRING = 2
	NUMBER = 3
	
	COLON = 4
	OPEN_BRACKET = 5
	CLOSE_BRACKET = 6
	ATTRIBUTE = 7 # '@'

class Token:
	"""
	A token 
	"""
	
	def __init__(self, kind, data):
		self.kind = kind
		self.data = data

def isAlpha(c):
	"""
	Returns if a char is alphabetic
	"""
	
	c = ord(c)
	
	return (c > 0x40) and (c < 0x5B or c > 0x60) and (c < 0x7B or c > 0x7F)

def isNumeric(c):
	"""
	Returns if the char is numeric
	"""
	
	c = ord(c)
	
	return (c >= 0x30 and c <= 0x39)

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
	
	stream = source.getBytes(source.getLength()).decode('latin-1')
	
	tokens = []
	
	i = 0
	while (i < len(stream)):
		c = stream[i]
		
		match (c):
			# Whitespace
			case (c in '\t\r '):
				pass
			
			# Symbols
			case (isAlpha(c)):
				string = ""
				
				while (True):
					c = stream[i]
					
					if (not isAlphaNumeric(c)):
						break
					
					string += c
					
					i += 1
				
				i -= 1
				
				tokens.append(Token(TokenType.STRING, string))
			
			# Strings
			case (c == '"'):
				i += 1
				
				while (True):
					
		
		i += 1

if (__name__ == "__main__"):
	import sys
	
	print(tokenise(sys.argv[1]))
