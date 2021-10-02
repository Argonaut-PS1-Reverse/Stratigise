{
	0x00000000: ['CommandError'], # This should never be decompiled in an offical wad.
	0x00000001: ['Local', 'int32'], # Push local variable onto the stack
	0x00000002: ['Global', 'int32'], # Push global variable onto the stack
	0x00000003: ['WorldGlobal', 'int32'], # Push world global variable onto the stack
	0x00000004: ['AlienVar', 'int32'], # Push alien variable onto the stack
}
