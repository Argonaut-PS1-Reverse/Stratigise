def formathex(n):
	"""
	Format 32-bit integer as hexidecimal
	"""
	return "0x" + '{:02X}'.format(n)

cmds = """
CommandError
LoadObject
LoadSprite
LoadAnim
LoadSample
LoadAnimFlag
TurnTowardX
TurnTowardY
TurnTowardWaypointX
PlaySound
StopSound
PlayAnim
StopAnim
WaitAnimend
Print
SpecialFXOn
Wait
Repeat
Until
While
EndWhile
If
Else
IfAnimend
For
Next
Switch
EndCase
ProcCall
ResetPosition
Goto
ScaleX
ScaleY
ScaleZ
Jump
Fall
MoveBackward
MoveForward
MoveRight
MoveDown
MoveLeft
MoveUp
TurnRight
TurnLeft
TiltBackward
TiltForward
TiltRight
TiltLeft
Spawn
CreateTrigger
KillTrigger
CommandError
EndTrigger
Remove
LetGVar
LetPGVar
LetAVar
EndProc
SetModel
FileEnd
Blink
HoldTrigger
ReleaseTrigger
SetAnim
TurnTowardXY
CommandError
Hold
Release
Inc
PlayerAttackOn
PlayerAttackOff
CamWobble
LookAtMe
ShadowSize
ShadowType
ClearAnim
StopFall
SetPlayerPosRel
CollectKey
RemoveKey
CommandError
CommandError
CollisionOn
CollisionOff
PauseTriggers
UnpauseTriggers
SetPosition
IsPlayer
IfJumping
IfFalling
Scale
TurnTowardWaypointY
Hide
Unhide
LetXGVar
SetCamHeight
SetLevel
ShadowOn
ShadowOff
Accelerate
Decelerate
SetAnimSpeed
SetCamDist
UserTrigger
WaitEvent
PlayerCollisionOn
AnimCtrlSpdOn
AnimCtrlSpdOff
LetParam
TurnTowardPosX
SpecialFXOff
OpenEyes
CloseEyes
JumpCtrlOn
JumpCtrlOff
Stomp
PushCamera
PullCamera
Float
SpawnChild
SetCamera
NextImm
AddPickup
LosePickups
Reverse
PlayerCollisionOff
SetCollPoint
SetCollPoints
PushingOn
PushingOff
PushableOn
PushableOff
PushWaypoint
PullWaypoint
EndWhileImm
NextWaypoint
PrevWaypoint
TurnTowardWaypointXY
TurnTowardPosXY
NearestWaypointNext
NearestWaypointPrev
DeleteWaypoint
CommandError
MoveForwardAngle
TurnTowardPosY
MovePlayerForward
MovePlayerBackward
LoopSound
Wobble
CamHold
SpeedUp
SlowDown
SmoothSpeed
AccelerateAngle
DecelerateAngle
MovePosition
RemoveFromMap
InitCrystal
Crystal
EndLevel
StopDead
PitchShift
Activated
HangOn
HangOff
CreateDeath
DoDeath
EndCrystal
PausePlayer
UnpausePlayer
PlayerDead
SlideOn
SlideOff
FirstWaypoint
UntilImm
Collected
Dec
SpawnFrom
LetXParam
RemoveCrystal
CollectJigsaw
Bonus
NextLevel
LookAtMe
NoHang
Vibrate
PlayerNoStood
RemoveGobbo
PauseTriggersNoAnim
ShowBonus
LookAtMeMap
PlayerMove
PlayerTurn
SetEnvelope
TurnTowardPlayerX
TurnTowardPlayerY
TurnTowardPlayerXY
ForceDoor
LevelStats
ReSeed
ShowBonusOn
ShowBonusOff
RemoveModel
QuickPlayer
GobboON
GobboOFF
UnActivated
EndSubLevel
TurnOffLookAtMe
HeightFloat
FlashOn
FlashOff
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
CommandError
TonyTest
LewisTest
"""

a = cmds.split("\n")
s = 0

for i in range(len(a)):
	if (not a[i]): s += 1; continue;
	print(f"\t{formathex(i - s)}: ['{a[i]}'],")
