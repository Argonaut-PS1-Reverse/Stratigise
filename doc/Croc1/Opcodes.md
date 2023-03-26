# *Croc: Legend of the Gobbos* ASL Bytecode

In Croc 1, stratigies control many things, like the player's movement.

***Note**: PSX is the demo version and PC is Croc DE, unless otherwise noted.*

## All bytecodes, ordered by opcode number

### `stCommandError`

Indicates that the command being called doesn't exist or isn't implemented in this version.

### `stLoadObject`

Either halt and catch fire or nop, depending on the platform.

### `stLoadSprite`

Either halt and catch fire or nop, depending on the platform.

### `stLoadAnim`

Either halt and catch fire or nop, depending on the platform.

### `stLoadSample`

Either halt and catch fire or nop, depending on the platform.

### `stLoadAnimFlag`

Either halt and catch fire or nop, depending on the platform.

### `stTurnTowardX`

```
stTurnTowardX [int16: ] [eval: ]
```

### `stTurnTowardY`

```
stTurnTowardY [int16: ] [eval: ]
```

### `stTurnTowardWaypointX`

```
stTurnTowardWaypointX [eval: ]
```

### `stPlaySound`

```
stPlaySound [int8: ] [eval: ] [varargs: ]
```

### `stStopSound`

```
stStopSound [eval: ]
```

### `stPlayAnim`

```
stPlayAnim [eval: ]
```

### `stStopAnim`

```
stStopAnim
```

### `stWaitAnimend`

```
stWaitAnimend
```

### `stPrint`

```
stPrint [string: message]
```

Prints `message` to the console, if available.

### `stSpecialFXOn`

```
stSpecialFXOn [eval: ]
```

### `stWait`

```
stWait [eval: ]
```

### `stRepeat`

```
stRepeat
```

### `stUntil`

```
stUntil [eval: ]
```

### `stWhile`

```
stWhile [eval: ] [int16: ]
```

### `stEndWhile`

```
stEndWhile
```

### `stIf`

```
stIf [stEvaluate: expression] [int16: offset]
```

If `expression` is equal to `0`, then jump `offset` bytes ahead. `offset` is relative to the instruction after the current `stIf` instruction.

```c
void stIf(stStrat *strat) {
	short offset;
	uint32_t expression;
	
	// Skip instruction byte
	strat->instructionStream = strat->instructionStream + 1;
	
	// Get expression and offset from instruction stream
	expression = stEvaluate(strat);
	offset = getPCword(strat);
	
	// Jump if expression is zero
	if (expression == 0) {
		strat->instructionStream = strat->instructionStream + offset;
	}
	
	return;
}
```

### `stElse`

```
stElse [int16: offset]
```

Add `offset` to the instruction pointer. `offset` is relative to the instruction after the current `stElse` instruction.

Note: `stElse` is sometimes used for relative jumps. It does not need a proceeding `stIf` instruction.

```c
void stElse(stStrat *strat) {
	short offset;
	
	// Skip instruction byte
	strat->instructionStream = strat->instructionStream + 1;
	
	// Get relative address from instruction stream
	offset = getPCword(strat);
	
	// Go to relative address
	strat->instructionStream = strat->instructionStream + (int) offset;
	
	return;
}
```

### `stIfAnimend`

```
stIfAnimend [int16: ]
```

### `stFor`

```
stFor [int8: ] [int16: ] [eval: ] [eval: ]
```

### `stNext`

```
stNext
```

### `stSwitch`

```
stSwitch [eval: ] [int16: ] [address16: ] [varargs: ]
```

### `stEndCase`

```
stEndCase [address16: ]
```

### `stProcCall`

```
stProcCall [address16: ]
```

### `stResetPosition`

```
stResetPosition
```

### `stGoto`

```
stGoto [address16: ]
```

### `stScaleX`

```
stScaleX [eval: ]
```

### `stScaleY`

```
stScaleY [eval: ]
```

### `stScaleZ`

```
stScaleZ [eval: ]
```

### `stJump`

```
stJump [eval: ]
```

### `stFall`

```
stFall
```

### `stMoveBackward`

```
stMoveBackward [eval: ]
```

### `stMoveForward`

```
stMoveForward [eval: ]
```

### `stMoveRight`

```
stMoveRight [eval: ]
```

### `stMoveDown`

```
stMoveDown [eval: ]
```

### `stMoveLeft`

```
stMoveLeft [eval: ]
```

### `stMoveUp`

```
stMoveUp [eval: ]
```

### `stTurnRight`

```
stTurnRight [eval: ]
```

### `stTurnLeft`

```
stTurnLeft [eval: ]
```

### `stTiltBackward`

```
stTiltBackward [eval: ]
```

### `stTiltForward`

```
stTiltForward [eval: ]
```

### `stTiltRight`

```
stTiltRight [eval: ]
```

### `stTiltLeft`

```
stTiltLeft [eval: ]
```

### `stSpawn`

```
stSpawn [int32: ] [int16: ] [int8: ] [int8: ] [int8: ] [varargs: ]
```

### `stCreateTrigger`

```
stCreateTrigger [int8: ] [varargs: ] [int16: ]
```

### `stKillTrigger`

```
stKillTrigger [int16: ]
```

### `stCommandError`

```
stCommandError
```

### `stEndTrigger`

```
stEndTrigger
```

### `stRemove`

```
stRemove
```

### `stLetGVar`

```
stLetGVar [int16: ] [eval: ]
```

### `stLetPGVar`

```
stLetPGVar [int16: ] [eval: ]
```

### `stLetAVar`

```
stLetAVar [int16: ] [eval: ]
```

### `stEndProc`

```
stEndProc
```

### `stSetModel`

```
stSetModel [eval: ]
```

### `stFileEnd`

```
stFileEnd
```

### `stBlink`

```
stBlink [int8: ] [varargs: ]
```

### `stHoldTrigger`

```
stHoldTrigger
```

### `stReleaseTrigger`

```
stReleaseTrigger
```

### `stSetAnim`

```
stSetAnim [eval: ]
```

### `stTurnTowardXY`

```
stTurnTowardXY [int16: ] [eval: ] [eval: ]
```

### `stCommandError`

```
stCommandError
```

### `stHold`

```
stHold
```

### `stRelease`

```
stRelease [string: ]
```

### `stInc`

```
stInc [int8: ] [int16: ]
```

### `stPlayerAttackOn`

```
stPlayerAttackOn
```

### `stPlayerAttackOff`

```
stPlayerAttackOff
```

### `stCamWobble`

```
stCamWobble [eval: ]
```

### `stLookAtMe_0`

```
stLookAtMe_0
```

### `stShadowSize`

```
stShadowSize [eval: ]
```

### `stShadowType`

```
stShadowType
```

### `stClearAnim`

```
stClearAnim
```

### `stStopFall`

```
stStopFall
```

### `stSetPlayerPosRel`

```
stSetPlayerPosRel [eval: ] [eval: ] [eval: ]
```

### `stCollectKey`

```
stCollectKey
```

### `stRemoveKey`

```
stRemoveKey
```

### `stCommandError`

```
stCommandError
```

### `stCommandError`

```
stCommandError
```

### `stCollisionOn`

```
stCollisionOn [eval: ]
```

### `stCollisionOff`

```
stCollisionOff [eval: ]
```

### `stPauseTriggers`

```
stPauseTriggers
```

### `stUnpauseTriggers`

```
stUnpauseTriggers
```

### `stSetPosition`

```
stSetPosition
```

### `stIsPlayer`

```
stIsPlayer
```

### `stIfJumping`

```
stIfJumping [int16: ]
```

### `stIfFalling`

```
stIfFalling [int16: ]
```

### `stScale`

```
stScale [eval: ]
```

### `stTurnTowardWaypointY`

```
stTurnTowardWaypointY [eval: ]
```

### `stHide`

```
stHide
```

### `stUnhide`

```
stUnhide
```

### `stLetXGVar`

```
stLetXGVar [int16: ] [eval: ]
```

### `stSetCamHeight`

```
stSetCamHeight [eval: ]
```

### `stSetLevel`

```
stSetLevel [eval: ] [eval: ]
```

### `stShadowOn`

```
stShadowOn
```

### `stShadowOff`

```
stShadowOff
```

### `stAccelerate`

```
stAccelerate
```

### `stDecelerate`

```
stDecelerate
```

### `stSetAnimSpeed`

```
stSetAnimSpeed [eval: ]
```

### `stSetCamDist`

```
stSetCamDist [eval: ]
```

### `stUserTrigger`

```
stUserTrigger [int16: ] [eval: ]
```

### `stWaitEvent`

```
stWaitEvent
```

### `stPlayerCollisionOn`

```
stPlayerCollisionOn
```

### `stAnimCtrlSpdOn`

```
stAnimCtrlSpdOn
```

### `stAnimCtrlSpdOff`

```
stAnimCtrlSpdOff
```

### `stLetParam`

```
stLetParam [int16: ] [eval: ]
```

### `stTurnTowardPosX`

```
stTurnTowardPosX [eval: ]
```

### `stSpecialFXOff`

```
stSpecialFXOff [eval: ]
```

### `stOpenEyes`

```
stOpenEyes
```

### `stCloseEyes`

```
stCloseEyes [int8: ] [varargs: ]
```

### `stJumpCtrlOn`

```
stJumpCtrlOn
```

### `stJumpCtrlOff`

```
stJumpCtrlOff
```

### `stStomp`

```
stStomp
```

### `stPushCamera`

```
stPushCamera
```

### `stPullCamera`

```
stPullCamera
```

### `stFloat`

```
stFloat
```

### `stSpawnChild`

```
stSpawnChild [int32: ] [int16: ]
```

### `stSetCamera`

```
stSetCamera [eval: ]
```

### `stNextImm`

```
stNextImm
```

### `stAddPickup`

```
stAddPickup [eval: ]
```

### `stLosePickups`

```
stLosePickups
```

### `stReverse`

```
stReverse
```

### `stPlayerCollisionOff`

```
stPlayerCollisionOff
```

### `stSetCollPoint`

```
stSetCollPoint [eval: ] [eval: ] [eval: ] [eval: ]
```

### `stSetCollPoints`

```
stSetCollPoints [eval: ]
```

### `stPushingOn`

```
stPushingOn
```

### `stPushingOff`

```
stPushingOff
```

### `stPushableOn`

```
stPushableOn
```

### `stPushableOff`

```
stPushableOff
```

### `stPushWaypoint`

```
stPushWaypoint
```

### `stPullWaypoint`

```
stPullWaypoint
```

### `stEndWhileImm`

```
stEndWhileImm
```

### `stNextWaypoint`

```
stNextWaypoint
```

### `stPrevWaypoint`

```
stPrevWaypoint
```

### `stTurnTowardWaypointXY`

```
stTurnTowardWaypointXY [eval: ] [eval: ]
```

### `stTurnTowardPosXY`

```
stTurnTowardPosXY [eval: ]
```

### `stNearestWaypointNext`

```
stNearestWaypointNext
```

### `stNearestWaypointPrev`

```
stNearestWaypointPrev
```

### `stDeleteWaypoint`

```
stDeleteWaypoint
```

### `stCommandError`

```
stCommandError
```

### `stMoveForwardAngle`

```
stMoveForwardAngle [eval: ] [eval: ]
```

### `stTurnTowardPosY`

```
stTurnTowardPosY [eval: ]
```

### `stMovePlayerForward`

```
stMovePlayerForward [eval: ]
```

### `stMovePlayerBackward`

```
stMovePlayerBackward [eval: ]
```

### `stLoopSound`

```
stLoopSound [eval: ] [eval: ]
```

### `stWobble`

```
stWobble [int16: ]
```

### `stCamHold`

```
stCamHold [eval: ]
```

### `stSpeedUp`

```
stSpeedUp [eval: ]
```

### `stSlowDown`

```
stSlowDown [eval: ]
```

### `stSmoothSpeed`

```
stSmoothSpeed [eval: ]
```

### `stAccelerateAngle`

```
stAccelerateAngle [eval: ]
```

### `stDecelerateAngle`

```
stDecelerateAngle [eval: ]
```

### `stMovePosition`

```
stMovePosition [int16: ] [int16: ] [int16: ] [eval: ] [eval: ]
```

### `stRemoveFromMap`

```
stRemoveFromMap
```

### `stInitCrystal`

```
stInitCrystal
```

### `stCrystal`

```
stCrystal
```

### `stEndLevel`

```
stEndLevel
```

### `stStopDead`

```
stStopDead
```

### `stPitchShift`

```
stPitchShift [eval: ] [eval: ]
```

### `stActivated`

```
stActivated
```

### `stHangOn`

```
stHangOn
```

### `stHangOff`

```
stHangOff
```

### `stCreateDeath`

```
stCreateDeath
```

### `stDoDeath`

```
stDoDeath
```

### `stEndCrystal`

```
stEndCrystal
```

### `stPausePlayer`

```
stPausePlayer
```

### `stUnpausePlayer`

```
stUnpausePlayer
```

### `stPlayerDead`

```
stPlayerDead
```

### `stSlideOn`

```
stSlideOn
```

### `stSlideOff`

```
stSlideOff
```

### `stFirstWaypoint`

```
stFirstWaypoint
```

### `stUntilImm`

```
stUntilImm [eval: ]
```

### `stCollected`

```
stCollected
```

### `stDec`

```
stDec [int8: ] [int16: ]
```

### `stSpawnFrom`

```
stSpawnFrom [int32: ] [int16: ] [eval: ]
```

### `stLetXParam`

```
stLetXParam
```

### `stRemoveCrystal`

```
stRemoveCrystal
```

### `stCollectJigsaw`

```
stCollectJigsaw [eval: ]
```

### `stBonus`

```
stBonus [int32: ]
```

### `stNextLevel`

```
stNextLevel
```

### `stLookAtMe_1`

```
stLookAtMe_1
```

### `stNoHang`

```
stNoHang
```

### `stVibrate`

```
stVibrate [eval: ]
```

### `stPlayerNoStood`

```
stPlayerNoStood
```

### `stRemoveGobbo`

```
stRemoveGobbo
```

### `stPauseTriggersNoAnim`

```
stPauseTriggersNoAnim
```

### `stShowBonus`

```
stShowBonus
```

### `stLookAtMeMap`

```
stLookAtMeMap
```

### `stPlayerMove`

```
stPlayerMove
```

### `stPlayerTurn`

```
stPlayerTurn
```

### `stSetEnvelope`

```
stSetEnvelope [eval: ] [eval: ] [eval: ] [eval: ] [eval: ] [eval: ]
```

### `stTurnTowardPlayerX`

```
stTurnTowardPlayerX [eval: ]
```

### `stTurnTowardPlayerY`

```
stTurnTowardPlayerY [eval: ]
```

### `stTurnTowardPlayerXY`

```
stTurnTowardPlayerXY [eval: ]
```

### `stForceDoor`

```
stForceDoor [eval: ]
```

### `stLevelStats`

```
stLevelStats
```

### `stReSeed`

```
stReSeed
```

### `stShowBonusOn`

```
stShowBonusOn
```

### `stShowBonusOff`

```
stShowBonusOff
```

### `stRemoveModel`

```
stRemoveModel
```

### `stQuickPlayer`

```
stQuickPlayer
```

### `stGobboON`

```
stGobboON
```

### `stGobboOFF`

```
stGobboOFF
```

### `stUnActivated`

```
stUnActivated
```

### `stEndSubLevel`

```
stEndSubLevel
```

### `stTurnOffLookAtMe`

```
stTurnOffLookAtMe
```

### `stHeightFloat`

```
stHeightFloat
```

### `stFlashOn`

```
stFlashOn
```

### `stFlashOff`

```
stFlashOff
```

### `st_Light_0xd4`

```
st_Light_0xd4 [eval: ]
```

### `st_Light_0xd5`

```
st_Light_0xd5 [eval: ]
```

### `st_Light_0xd6`

```
st_Light_0xd6 [eval: ] [eval: ] [eval: ]
```

### `stTonyTest`

```
stTonyTest
```

### `stLewisTest`

```
stLewisTest [int8: ] [eval: ]
```

## PC and PSX comparison

The PC and PSX opcodes are the same except for `0xD4`, `0xD5` and `0xD6`, which are mapped to `stCommandError` in PSX and are lighting related on PC.
