{
	# NOTE: While the opcodes are fairly well known, the arguments are not very
	# well known and are still in research.
	'InstructionSize': 1,
	0x00: ['CommandError'], # This should never normally appear.
	0x01: ['LoadObject', 'string'],
	0x02: ['LoadSprite'],
	0x03: ['LoadAnim'],
	0x04: ['LoadSample'],
	0x05: ['LoadAnimFlag'],
	0x06: ['TurnTowardX', 'int16', 'eval'],
	0x06: ['TurnTowardY', 'int16', 'eval'],
	0x07: ['TurnTowardWaypointX', 'eval'],
	0x08: ['PlaySound', 'int8', 'eval'], # for arg[0]==2
	0x09: ['StopSound', 'eval'],
	0x0C: ['PlayAnim', 'eval'],
	0x0D: ['StopAnim', 'string', 'eval'],
	0x0E: ['WaitAnimend'],
	0x0F: ['Print'],
	0x10: ['SpecialFXOn'],
	0x11: ['Wait'],
	0x12: ['Repeat'],
	0x13: ['Until'],
	0x14: ['While'],
	0x15: ['EndWhile'],
	0x16: ['If'],
	0x17: ['Else'],
	0x18: ['IfAnimend'],
	0x19: ['For'],
	0x1A: ['Next'],
	0x1B: ['Switch'],
	0x1C: ['EndCase'],
	0x1D: ['ProcCall'],
	0x1E: ['ResetPosition'],
	0x1F: ['ScaleX'],
	0x20: ['ScaleY'],
	0x21: ['ScaleZ'],
	0x22: ['Jump'],
	0x23: ['Fall'],
	0x24: ['MoveBackward'],
	0x25: ['MoveForward'],
	0x26: ['MoveRight'],
	0x27: ['MoveDown'],
	0x28: ['MoveLeft'],
	0x29: ['MoveUp'],
	0x2A: ['TurnRight'],
	0x2B: ['TurnLeft'],
	0x2C: ['TiltBackward'],
	0x2D: ['TiltForward'],
	0x2E: ['TiltRight'],
	0x2F: ['TiltLeft'],
	0x30: ['Spawn'],
	0x31: ['CreateTrigger'],
	0x32: ['KillTrigger'],
	0x33: ['EndTrigger'],
	0x34: ['Remove'],
	0x35: ['LetGVar'],
	0x36: ['LetPGVar'],
	0x37: ['LetAVar'],
	0x38: ['EndProc'],
	0x39: ['SetModel'],
	0x3A: ['FileEnd'],
	0x3B: ['Blink'],
	0x3C: ['HoldTrigger'],
	0x3D: ['ReleaseTrigger'],
	0x3E: ['SetAnim'],
	0x3F: ['TurnTowardXY'],
	0x40: ['CommandError'],
	0x41: ['__Operation_41'],
	0x42: ['Relase'],
	0x43: ['Inc'],
	0x44: ['__Operation_44'],
	0x45: ['__Operation_45'],
	0x46: ['CamWobble'],
	0x47: ['LookAtMe'],
	0x48: ['ShadowSize'],
	0x49: ['__Operation_49'],
	0x4A: ['__Operation_4a'],
	0x4B: ['__Operation_4b'],
	0x4C: ['SetPlayerPosRel'],
	0x4D: ['__Operation_4d'],
	0x4E: ['__Operation_4e'],
	0x4F: ['CommandError'],
	0x50: ['CommandError'],
	0x51: ['CollisionOn'],
	0x52: ['CollisionOff'],
}
