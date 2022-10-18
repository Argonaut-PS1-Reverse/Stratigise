"""
Croc 1 strat spec - opcodes and unevalute
"""

"""
Read an opcode - for Croc 1 is is one byte.
"""
def readOpcode(strat):
	return strat.readInt8()

"""
Processes the section data
"""
def processSections(strat):
	from stratigise.common import SectionInfo
	
	# Read size of strat, audio upper number and audio start position
	size = strat.readInt32LE()
	audio_upper = strat.readInt16LE()
	audio_start = strat.readInt16LE()
	
	# Find sizes
	audio_size = size - audio_start
	code_size = size - audio_size - 4
	
	return [
		SectionInfo('code', 8, code_size, ".DIS", params = {"original_size": size, "original_audio_start": audio_start, "audio_upper": audio_upper}),
		SectionInfo('data', 8 + code_size, audio_size, ".AXX"),
	]

"""
NOTE: This is based on the PSX list of opcodes, NOT those in Croc DE. They are
still being found out and might be different from those. They seem to be the 
same except for three extra opcodes in Croc DE.

Instruction notes:

  * hcf: halt and catch fire (breaks strat)
  * nop: no operation
"""
opcodes = {
	0x00: ['CommandError'], # hcf
	0x01: ['LoadObject'], # nop/hcf
	0x02: ['LoadSprite'], # nop/hcf
	0x03: ['LoadAnim'], # nop/hcf
	0x04: ['LoadSample'], # nop/hcf
	0x05: ['LoadAnimFlag'], # nop/hcf
	0x06: ['TurnTowardX', 'int16', 'eval'],
	0x07: ['TurnTowardY', 'int16', 'eval'],
	0x08: ['TurnTowardWaypointX', 'eval'],
	0x09: ['PlaySound', 'int8', 'eval', 'varargs'],
	0x0A: ['StopSound', 'eval'],
	0x0B: ['PlayAnim', 'eval'],
	0x0C: ['StopAnim'],
	0x0D: ['WaitAnimend'],
	0x0E: ['Print', 'string'], # Note: Croc DE is different
	0x0F: ['SpecialFXOn', 'eval'],
	0x10: ['Wait', 'eval'],
	0x11: ['Repeat'],
	0x12: ['Until', 'eval'],
	0x13: ['While', 'eval', 'int16'],
	0x14: ['EndWhile'],
	0x15: ['If', 'eval', 'offset16'],
	0x16: ['Else', 'offset16'],
	0x17: ['IfAnimend', 'int16'],
	0x18: ['For', 'int8', 'int16', 'eval', 'eval'],
	0x19: ['Next'],
	0x1A: ['Switch', 'eval', 'int16', 'address16', 'varargs'],
	0x1B: ['EndCase', 'address16'],
	0x1C: ['ProcCall', 'address16'],
	0x1D: ['ResetPosition'],
	0x1E: ['Goto', 'address16'],
	0x1F: ['ScaleX', 'eval'],
	0x20: ['ScaleY', 'eval'],
	0x21: ['ScaleZ', 'eval'],
	0x22: ['Jump', 'eval'],
	0x23: ['Fall'],
	0x24: ['MoveBackward', 'eval'],
	0x25: ['MoveForward', 'eval'],
	0x26: ['MoveRight', 'eval'],
	0x27: ['MoveDown', 'eval'],
	0x28: ['MoveLeft', 'eval'],
	0x29: ['MoveUp', 'eval'],
	0x2A: ['TurnRight', 'eval'],
	0x2B: ['TurnLeft', 'eval'],
	0x2C: ['TiltBackward', 'eval'],
	0x2D: ['TiltForward', 'eval'],
	0x2E: ['TiltRight', 'eval'],
	0x2F: ['TiltLeft', 'eval'],
	0x30: ['Spawn', 'int32', 'int16', 'int8', 'int8', 'int8', 'varargs'],
	0x31: ['CreateTrigger', 'int8', 'varargs', 'int16'],
	0x32: ['KillTrigger', 'int16'], # hcf
	0x33: ['CommandError'],
	0x34: ['EndTrigger'],
	0x35: ['Remove'],
	0x36: ['LetGVar', 'int16', 'eval'],
	0x37: ['LetPGVar', 'int16', 'eval'],
	0x38: ['LetAVar', 'int16', 'eval'],
	0x39: ['EndProc'],
	0x3A: ['SetModel', 'eval'],
	0x3B: ['FileEnd'], # hcf
	0x3C: ['Blink', 'int8', 'varargs'], # Warning: Variable arguments based on strat runtime variable, though first byte seems to align with the number of arguments
	0x3D: ['HoldTrigger'],
	0x3E: ['ReleaseTrigger'],
	0x3F: ['SetAnim', 'eval'],
	0x40: ['TurnTowardXY', 'int16', 'eval', 'eval'],
	0x41: ['CommandError'],
	0x42: ['Hold'],
	0x43: ['Release', 'string'],
	0x44: ['Inc', 'int8', 'int16'],
	0x45: ['PlayerAttackOn'],
	0x46: ['PlayerAttackOff'],
	0x47: ['CamWobble', 'eval'],
	0x48: ['LookAtMe'],
	0x49: ['ShadowSize', 'eval'],
	0x4A: ['ShadowType'],
	0x4B: ['ClearAnim'],
	0x4C: ['StopFall'],
	0x4D: ['SetPlayerPosRel', 'eval', 'eval', 'eval'],
	0x4E: ['CollectKey'],
	0x4F: ['RemoveKey'],
	0x50: ['CommandError'],
	0x51: ['CommandError'],
	0x52: ['CollisionOn', 'eval'],
	0x53: ['CollisionOff', 'eval'],
	0x54: ['PauseTriggers'],
	0x55: ['UnpauseTriggers'],
	0x56: ['SetPosition'],
	0x57: ['IsPlayer'],
	0x58: ['IfJumping', 'int16'],
	0x59: ['IfFalling', 'int16'],
	0x5A: ['Scale', 'eval'],
	0x5B: ['TurnTowardWaypointY', 'eval'],
	0x5C: ['Hide'],
	0x5D: ['Unhide'],
	0x5E: ['LetXGVar', 'int16', 'eval'],
	0x5F: ['SetCamHeight', 'eval'],
	0x60: ['SetLevel', 'eval', 'eval'],
	0x61: ['ShadowOn'],
	0x62: ['ShadowOff'],
	0x63: ['Accelerate'],
	0x64: ['Decelerate'],
	0x65: ['SetAnimSpeed', 'eval'],
	0x66: ['SetCamDist', 'eval'],
	0x67: ['UserTrigger', 'int16', 'eval'],
	0x68: ['WaitEvent'],
	0x69: ['PlayerCollisionOn'],
	0x6A: ['AnimCtrlSpdOn'],
	0x6B: ['AnimCtrlSpdOff'],
	0x6C: ['LetParam', 'int16', 'eval'],
	0x6D: ['TurnTowardPosX', 'eval'],
	0x6E: ['SpecialFXOff', 'eval'],
	0x6F: ['OpenEyes'],
	0x70: ['CloseEyes', 'int8', 'varargs'], # Warning: See Blink
	0x71: ['JumpCtrlOn'],
	0x72: ['JumpCtrlOff'],
	0x73: ['Stomp'],
	0x74: ['PushCamera'],
	0x75: ['PullCamera'],
	0x76: ['Float'],
	0x77: ['SpawnChild', 'int32', 'int16'], # Warning: Variable arguments, cannot yet properly disassemble
	0x78: ['SetCamera', 'eval'],
	0x79: ['NextImm'],
	0x7A: ['AddPickup', 'eval'],
	0x7B: ['LosePickups'],
	0x7C: ['Reverse'],
	0x7D: ['PlayerCollisionOff'],
	0x7E: ['SetCollPoint', 'eval', 'eval', 'eval', 'eval'],
	0x7F: ['SetCollPoints', 'eval'],
	0x80: ['PushingOn'],
	0x81: ['PushingOff'],
	0x82: ['PushableOn'],
	0x83: ['PushableOff'],
	0x84: ['PushWaypoint'],
	0x85: ['PullWaypoint'],
	0x86: ['EndWhileImm'],
	0x87: ['NextWaypoint'],
	0x88: ['PrevWaypoint'],
	0x89: ['TurnTowardWaypointXY', 'eval', 'eval'],
	0x8A: ['TurnTowardPosXY', 'eval'],
	0x8B: ['NearestWaypointNext'],
	0x8C: ['NearestWaypointPrev'],
	0x8D: ['DeleteWaypoint'],
	0x8E: ['CommandError'],
	0x8F: ['MoveForwardAngle', 'eval', 'eval'],
	0x90: ['TurnTowardPosY', 'eval'],
	0x91: ['MovePlayerForward', 'eval'],
	0x92: ['MovePlayerBackward', 'eval'],
	0x93: ['LoopSound', 'eval', 'eval'],
	0x94: ['Wobble', 'int16'],
	0x95: ['CamHold', 'eval'],
	0x96: ['SpeedUp', 'eval'],
	0x97: ['SlowDown', 'eval'],
	0x98: ['SmoothSpeed', 'eval'],
	0x99: ['AccelerateAngle', 'eval'],
	0x9A: ['DecelerateAngle', 'eval'],
	0x9B: ['MovePosition', 'int16', 'int16', 'int16', 'eval', 'eval'],
	0x9C: ['RemoveFromMap'],
	0x9D: ['InitCrystal'],
	0x9E: ['Crystal'],
	0x9F: ['EndLevel'],
	0xA0: ['StopDead'],
	0xA1: ['PitchShift', 'eval', 'eval'],
	0xA2: ['Activated'],
	0xA3: ['HangOn'],
	0xA4: ['HangOff'],
	0xA5: ['CreateDeath'],
	0xA6: ['DoDeath'],
	0xA7: ['EndCrystal'],
	0xA8: ['PausePlayer'],
	0xA9: ['UnpausePlayer'],
	0xAA: ['PlayerDead'],
	0xAB: ['SlideOn'],
	0xAC: ['SlideOff'],
	0xAD: ['FirstWaypoint'],
	0xAE: ['UntilImm', 'eval'],
	0xAF: ['Collected'],
	0xB0: ['Dec', 'int8', 'int16'],
	0xB1: ['SpawnFrom', 'int32', 'int16', 'eval'], # Warning: Variable arguments, cannot yet properly disassemble
	0xB2: ['LetXParam'],
	0xB3: ['RemoveCrystal'],
	0xB4: ['CollectJigsaw', 'eval'],
	0xB5: ['Bonus', 'int32'],
	0xB6: ['NextLevel'],
	0xB7: ['LookAtMe'],
	0xB8: ['NoHang'],
	0xB9: ['Vibrate', 'eval'],
	0xBA: ['PlayerNoStood'],
	0xBB: ['RemoveGobbo'],
	0xBC: ['PauseTriggersNoAnim'],
	0xBD: ['ShowBonus'],
	0xBE: ['LookAtMeMap'],
	0xBF: ['PlayerMove'],
	0xC0: ['PlayerTurn'],
	0xC1: ['SetEnvelope', 'eval', 'eval', 'eval', 'eval', 'eval', 'eval'],
	0xC2: ['TurnTowardPlayerX', 'eval'],
	0xC3: ['TurnTowardPlayerY', 'eval'],
	0xC4: ['TurnTowardPlayerXY', 'eval'],
	0xC5: ['ForceDoor', 'eval'],
	0xC6: ['LevelStats'],
	0xC7: ['ReSeed'],
	0xC8: ['ShowBonusOn'],
	0xC9: ['ShowBonusOff'],
	0xCA: ['RemoveModel'],
	0xCB: ['QuickPlayer'],
	0xCC: ['GobboON'],
	0xCD: ['GobboOFF'],
	0xCE: ['UnActivated'],
	0xCF: ['EndSubLevel'],
	0xD0: ['TurnOffLookAtMe'],
	0xD1: ['HeightFloat'],
	0xD2: ['FlashOn'],
	0xD3: ['FlashOff'],
	0xD4: ['_Light_0xd4', 'eval'],
	0xD5: ['_Light_0xd5', 'eval'],
	0xD6: ['_Light_0xd6', 'eval', 'eval', 'eval'],
	0xD7: ['CommandError'],
	0xD8: ['CommandError'],
	0xD9: ['CommandError'],
	0xDA: ['CommandError'],
	0xDB: ['CommandError'],
	0xDC: ['CommandError'],
	0xDD: ['CommandError'],
	0xDE: ['CommandError'],
	0xDF: ['CommandError'],
	0xE0: ['CommandError'],
	0xE1: ['CommandError'],
	0xE2: ['CommandError'],
	0xE3: ['CommandError'],
	0xE4: ['CommandError'],
	0xE5: ['CommandError'],
	0xE6: ['CommandError'],
	0xE7: ['CommandError'],
	0xE8: ['CommandError'],
	0xE9: ['CommandError'],
	0xEA: ['CommandError'],
	0xEB: ['CommandError'],
	0xEC: ['CommandError'],
	0xED: ['CommandError'],
	0xEE: ['CommandError'],
	0xEF: ['CommandError'],
	0xF0: ['CommandError'],
	0xF1: ['CommandError'],
	0xF2: ['CommandError'],
	0xF3: ['CommandError'],
	0xF4: ['CommandError'],
	0xF5: ['CommandError'],
	0xF6: ['CommandError'],
	0xF7: ['CommandError'],
	0xF8: ['CommandError'],
	0xF9: ['CommandError'],
	0xFA: ['CommandError'],
	0xFB: ['CommandError'],
	0xFC: ['CommandError'],
	0xFD: ['CommandError'],
	0xFE: ['TonyTest'],
	0xFF: ['LewisTest', 'int8', 'eval'],
}

"""
Unevalute names are now in a table so it's easier to reassemble strats
"""
EVALUATE_NAMES = {
	0x00: None,
	0x01: "PushPGVar",
	0x02: "PushGVar",
	0x03: "PushAVar",
	0x04: "PushInt32",
	0x05: None,
	0x06: "Add",
	0x07: "Subtract",
	0x08: "Divide",
	0x09: "Multiply",
	0x0A: "BitAnd",
	0x0B: "BitOr",
	0x0C: "Equal",
	0x0D: "NotEqual",
	0x0E: "TopLess",
	0x0F: "TopGreater",
	0x10: "TopNotLess",
	0x11: "TopNotGreater",
	0x12: "ReturnTop",
	0x13: {
		0x01: "LoadObject",
		0x02: "LoadAsset0",
		0x03: "LoadAnim",
		0x04: "LoadAsset1",
		0x05: "LoadAsset2",
		0x09: "LoadSound",
		0x50: "LoadAsset3",
		0x51: "LoadAsset4",
		0x8E: "LoadAsset5",
	},
	0x14: "Sine",
	0x15: "Cosine",
	0x17: "SquareRoot",
	0x18: "AbsoluteValue",
	0x19: "RandomNumber",
	0x1A: "FloorNumber",
	0x1B: "PlayerIsWithinRadius2D",
	0x1C: "PushExternGlobal",
	0x1D: "PushValueFromIPAndOffset154",
	0x1E: "Negate",
	0x1F: "IsZero",
	0x20: "TopPairNotZero",
	0x21: "VelocityLessThan",
	0x22: "DistanceFromPoint",
	0x23: "CheckAnimFlag32",
	0x26: "ReturnZero",
}

def unevaluate(strat):
	"""
	Croc 1 eval type handling
	"""
	
	# This should be here so the reassembler doesn't try to import this
	from stratigise.common import Symbol
	
	operations = []
	
	while (True):
		op = strat.readInt8()
		
		# Break on none
		if (op == None): break
		
		# Assume that A and B are the top and second-to-top of the stack.
		
		# 0x01 - Get a PGVar (procedure global?)
		elif (op == 0x01):
			operations.append(Symbol(EVALUATE_NAMES[op]))
			operations.append(strat.readInt16LE())
		
		# 0x02 - Get strat global value
		elif (op == 0x02):
			operations.append(Symbol(EVALUATE_NAMES[op]))
			operations.append(strat.readInt16LE())
		
		# 0x03 - Load alien var (?)
		elif (op == 0x03):
			operations.append(Symbol(EVALUATE_NAMES[op]))
			pp = strat.readInt16LE()
			operations.append(pp)
		
		# 0x04 - Read a long value
		elif (op == 0x04):
			operations.append(Symbol(EVALUATE_NAMES[op]))
			operations.append(strat.readInt32LE())
		
		# 0x06 - Add between top values (A + B)
		elif (op == 0x06):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x07 - Subtract between top values (B - A)
		elif (op == 0x07):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x08 - Divide between top values
		elif (op == 0x08):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x09 - Multiply between top values
		elif (op == 0x09):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x0A - Bitwise AND between top values
		elif (op == 0x0A):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x0B - Bitwise OR between top values
		elif (op == 0x0B):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x0C - Unknown but usually followed by string litral
		elif (op == 0x0C):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x0D - Unknown but usually followed by string literal
		elif (op == 0x0D):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x0E - Compare A < B
		elif (op == 0x0E):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x0F - Compare B < A (A > B)
		elif (op == 0x0F):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x10 - Compare A < B then XOR 1
		elif (op == 0x10):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x11 - Compare B < A then XOR 1 ((A > B) ^ 1)
		elif (op == 0x11):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x12 - Pop top stack value and return
		elif (op == 0x12):
			operations.append(Symbol(EVALUATE_NAMES[op]))
			break
		
		# 0x13 - Load assets
		elif (op == 0x13):
			pp = strat.readInt8()
			
			# 0x01, 0x02 - These try to find if the asset is already loaded in memory first
			if (pp == 0x01 or pp == 0x02):
				operations.append(Symbol(EVALUATE_NAMES[op][pp]))
				operations.append(strat.readInt32LE())
				strat.readInt8() # ignore value
				operations.append(strat.readString())
			
			# 0x03, 0x04, 0x05 - These just seem to directly load the asset
			elif (pp == 0x03 or pp == 0x04 or pp == 0x05):
				operations.append(Symbol(EVALUATE_NAMES[op][pp]))
				operations.append(strat.readInt32LE())
				sz = strat.readInt8()
				operations.append(strat.readBytes(sz).decode('latin-1'))
			
			# 0x09 - Seems to play sounds effects based on a distance to a camera
			# Just saying LoadSound since 13 XX seem to be related to asset loading
			elif (pp == 0x09):
				operations.append(Symbol(EVALUATE_NAMES[op][pp]))
				a = strat.readInt8()
				operations.append(a)
				operations.append(unevaluate(strat))
				
				if (a > 1):
					operations.append(unevaluate(strat))
				
				if (a > 3):
					operations.append(unevaluate(strat))
					operations.append(unevaluate(strat))
			
			# 0x50 - Read int32 which is then shifted left 16 (0x10)
			elif (pp == 0x50):
				operations.append(Symbol(EVALUATE_NAMES[op][pp]))
				operations.append(strat.readInt32LE() >> 0x10)
				sz = strat.readInt8()
				operations.append(strat.readBytes(sz).decode('latin-1'))
			
			# I did not actually check what exactly these do yet, since they
			# both seem to do the broing "load a 32-bit" integer routine
			# like most things here seem to do...
			elif (pp == 0x51 or pp == 0x8E):
				operations.append(Symbol(EVALUATE_NAMES[op][pp]))
				operations.append(strat.readInt32LE())
		
		# NOTE: Assume the following math functions replace the top of the stack
		# with their resulting value unless otherwise noted.
		
		# 0x14 - Sine(top value on the stack << 16)
		elif (op == 0x14):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x15 - Cosine(top value on the stack << 16)
		elif (op == 0x15):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x17 - Square root of the top stack value
		elif (op == 0x17):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x18 - Absolute value of the top stack value
		elif (op == 0x18):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x19 - (Random number) % top of stack
		elif (op == 0x19):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x1A - Floor the top of the stack (for fixed point numbers)
		elif (op == 0x1A):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x1B - Check if the player is within the given radius (disregarding height) at the top of the stack
		elif (op == 0x1B):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x1C - Push extern global to the stack
		elif (op == 0x1C):
			operations.append(Symbol(EVALUATE_NAMES[op]))
			operations.append(strat.readInt16LE())
		
		# 0x1D - Load value from (instructionPointer + offset + 0x154)
		elif (op == 0x1D):
			operations.append(Symbol(EVALUATE_NAMES[op]))
			operations.append(strat.readInt16LE())
		
		# 0x1E - Negate top value on the stack
		elif (op == 0x1E):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x1F - Compare to zero, push 1 if is zero and 0 otherwise (A == 0)
		elif (op == 0x1F):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x20 - Pop the first two stack values, check are not zero and place
		# result in second down stack value
		elif (op == 0x20):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x21 - Check if the strat's velocity is under the value on top of stack (unsure)
		elif (op == 0x21):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x22 - Pop top three values as point and push distance to that point
		elif (op == 0x22):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x23 - Check if higest bit on strat anim flags is set and decrement 
		# the stack pointer if so (seems very sepcific so not confident in this)
		# Flag32 referes to 32nd flag, not 32-bit integer
		elif (op == 0x23):
			operations.append(Symbol(EVALUATE_NAMES[op]))
		
		# 0x26 - Push zero and stop eval
		elif (op == 0x26):
			operations.append(Symbol(EVALUATE_NAMES[op]))
			break
		
		# Unknown eval opcode
		else:
			operations.append(Symbol("__unknown_operation_" + hex(op)))
			break
	
	return operations

def varargs(strat, op, args, instructions):
	"""
	Variable arguments handling
	"""
	
	from stratigise.common import Symbol, getLabelString
	
	# Play sound
	if (op == 0x09):
		mode = args[0]
		
		if (mode == 2):
			args.append(unevaluate(strat))
		
		elif (mode == 4):
			args.append(unevaluate(strat))
			args.append(unevaluate(strat))
			args.append(unevaluate(strat))
	
	# Switch statement
	elif (op == 0x1A):
		for i in range(args[1]):
			# Get the label
			address = (strat.readInt16LE() or 1) + 0x4
			instructions.addLabel(address)
			args.append(Symbol(getLabelString(address)))
			
			# Evaluate expression
			args.append(unevaluate(strat))
	
	# Spawn
	elif (op == 0x30):
		# Read string
		args.append(strat.readBytes(strat.readInt8()).decode('latin-1'))
		
		# something else should go here probably
		
		# Read evals
		for i in range(args[4] - 1):
			args.append(unevaluate(strat))
	
	# Create trigger
	elif (op == 0x31):
		mode = args[0]
		
		if (mode in [0x1, 0x8, 0x9, 0xB]):
			pass
		else:
			args.append(unevaluate(strat))
	
	# Blink, CloseEyes
	elif (op == 0x3c or op == 0x70):
		count = args[0]
		
		for i in range(count):
			args.append(strat.readInt16LE())
	
	return []

def after(op):
	"""
	String to append after the opcode output
	"""
	
	if (op == 0x39):
		return "\n\n; -------------------------------------------------------------------\n "
	
	return ""
