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
### `stTurnTowardY`
### `stTurnTowardWaypointX`
### `stPlaySound`
### `stStopSound`
### `stPlayAnim`
### `stStopAnim`
### `stWaitAnimend`
### `stPrint`

```
stPrint [string: message]
```

Prints `message` to the console, if available.

### `stSpecialFXOn`
### `stWait`
### `stRepeat`
### `stUntil`
### `stWhile`
### `stEndWhile`
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
### `stFor`
### `stNext`
### `stSwitch`
### `stEndCase`
### `stProcCall`
### `stResetPosition`
### `stGoto`
### `stScaleX`
### `stScaleY`
### `stScaleZ`
### `stJump`
### `stFall`
### `stMoveBackward`
### `stMoveForward`
### `stMoveRight`
### `stMoveDown`
### `stMoveLeft`
### `stMoveUp`
### `stTurnRight`
### `stTurnLeft`
### `stTiltBackward`
### `stTiltForward`
### `stTiltRight`
### `stTiltLeft`
### `stSpawn`
### `stCreateTrigger`
### `stKillTrigger`
### `stCommandError`
### `stEndTrigger`
### `stRemove`
### `stLetGVar`
### `stLetPGVar`
### `stLetAVar`
### `stEndProc`
### `stSetModel`
### `stFileEnd`
### `stBlink`
### `stHoldTrigger`
### `stReleaseTrigger`
### `stSetAnim`
### `stTurnTowardXY`
### `stCommandError`
### `stHold`
### `stRelease`
### `stInc`
### `stPlayerAttackOn`
### `stPlayerAttackOff`
### `stCamWobble`
### `stLookAtMe`
### `stShadowSize`
### `stShadowType`
### `stClearAnim`
### `stStopFall`
### `stSetPlayerPosRel`
### `stCollectKey`
### `stRemoveKey`
### `stCommandError`
### `stCommandError`
### `stCollisionOn`
### `stCollisionOff`
### `stPauseTriggers`
### `stUnpauseTriggers`
### `stSetPosition`
### `stIsPlayer`
### `stIfJumping`
### `stIfFalling`
### `stScale`
### `stTurnTowardWaypointY`
### `stHide`
### `stUnhide`
### `stLetXGVar`
### `stSetCamHeight`
### `stSetLevel`
### `stShadowOn`
### `stShadowOff`
### `stAccelerate`
### `stDecelerate`
### `stSetAnimSpeed`
### `stSetCamDist`
### `stUserTrigger`
### `stWaitEvent`
### `stPlayerCollisionOn`
### `stAnimCtrlSpdOn`
### `stAnimCtrlSpdOff`
### `stLetParam`
### `stTurnTowardPosX`
### `stSpecialFXOff`
### `stOpenEyes`
### `stCloseEyes`
### `stJumpCtrlOn`
### `stJumpCtrlOff`
### `stStomp`
### `stPushCamera`
### `stPullCamera`
### `stFloat`
### `stSpawnChild`
### `stSetCamera`
### `stNextImm`
### `stAddPickup`
### `stLosePickups`
### `stReverse`
### `stPlayerCollisionOff`
### `stSetCollPoint`
### `stSetCollPoints`
### `stPushingOn`
### `stPushingOff`
### `stPushableOn`
### `stPushableOff`
### `stPushWaypoint`
### `stPullWaypoint`
### `stEndWhileImm`
### `stNextWaypoint`
### `stPrevWaypoint`
### `stTurnTowardWaypointXY`
### `stTurnTowardPosXY`
### `stNearestWaypointNext`
### `stNearestWaypointPrev`
### `stDeleteWaypoint`
### `stCommandError`
### `stMoveForwardAngle`
### `stTurnTowardPosY`
### `stMovePlayerForward`
### `stMovePlayerBackward`
### `stLoopSound`
### `stWobble`
### `stCamHold`
### `stSpeedUp`
### `stSlowDown`
### `stSmoothSpeed`
### `stAccelerateAngle`
### `stDecelerateAngle`
### `stMovePosition`
### `stRemoveFromMap`
### `stInitCrystal`
### `stCrystal`
### `stEndLevel`
### `stStopDead`
### `stPitchShift`
### `stActivated`
### `stHangOn`
### `stHangOff`
### `stCreateDeath`
### `stDoDeath`
### `stEndCrystal`
### `stPausePlayer`
### `stUnpausePlayer`
### `stPlayerDead`
### `stSlideOn`
### `stSlideOff`
### `stFirstWaypoint`
### `stUntilImm`
### `stCollected`
### `stDec`
### `stSpawnFrom`
### `stLetXParam`
### `stRemoveCrystal`
### `stCollectJigsaw`
### `stBonus`
### `stNextLevel`
### `stLookAtMe`
### `stNoHang`
### `stVibrate`
### `stPlayerNoStood`
### `stRemoveGobbo`
### `stPauseTriggersNoAnim`
### `stShowBonus`
### `stLookAtMeMap`
### `stPlayerMove`
### `stPlayerTurn`
### `stSetEnvelope`
### `stTurnTowardPlayerX`
### `stTurnTowardPlayerY`
### `stTurnTowardPlayerXY`
### `stForceDoor`
### `stLevelStats`
### `stReSeed`
### `stShowBonusOn`
### `stShowBonusOff`
### `stRemoveModel`
### `stQuickPlayer`
### `stGobboON`
### `stGobboOFF`
### `stUnActivated`
### `stEndSubLevel`
### `stTurnOffLookAtMe`
### `stHeightFloat`
### `stFlashOn`
### `stFlashOff`
### `stTonyTest`
### `stLewisTest`

## PC and PSX comparison

The PC and PSX opcodes are the same except for `0xD4`, `0xD5` and `0xD6`, which are mapped to `stCommandError` in PSX and are lighting related on PC.
