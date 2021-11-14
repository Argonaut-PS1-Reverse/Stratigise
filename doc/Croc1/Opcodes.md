# *Croc: Legend of the Gobbos* Bytecode Instructions

This file compares the Croc DE and Croc PSX demo bytecodes. They seem to be mostly the same.

***NOTE**: Blank opcode spots are unknown.*

| Opcode | EU PSX Demo | Final and Croc DE |
| --- | --- | --- |
| `0x00` | stCommandError | stCommandError |
| `0x01` | stLoadObject | stLoadObject |
| `0x02` | stLoadSprite | stLoadSprite |
| `0x03` | stLoadAnim | stLoadAnim |
| `0x04` | stLoadSample | stLoadSample |
| `0x05` | stLoadAnimFlag | stLoadAnimFlag |
| `0x06` | stTurnTowardX |  |
| `0x07` | stTurnTowardY |  |
| `0x08` | stTurnTowardWaypointX |  |
| `0x09` | stPlaySound |  |
| `0x0A` | stStopSound |  |
| `0x0B` | stPlayAnim |  |
| `0x0C` | stStopAnim |  |
| `0x0D` | stWaitAnimend | stWaitAnimend |
| `0x0E` | stPrint | stPrint |
| `0x0F` | stSpecialFXOn |  |
| `0x10` | stWait |  |
| `0x11` | stRepeat |  |
| `0x12` | stUntil |  |
| `0x13` | stWhile |  |
| `0x14` | stEndWhile |  |
| `0x15` | stIf |  |
| `0x16` | stElse |  |
| `0x17` | stIfAnimend |  |
| `0x18` | stFor |  |
| `0x19` | stNext |  |
| `0x1A` | stSwitch |  |
| `0x1B` | stEndCase |  |
| `0x1C` | stProcCall |  |
| `0x1D` | stResetPosition |  |
| `0x1E` | stGoto |  |
| `0x1F` | stScaleX | stScaleX |
| `0x20` | stScaleY | stScaleY |
| `0x21` | stScaleZ | stScaleZ |
| `0x22` | stJump |  |
| `0x23` | stFall |  |
| `0x24` | stMoveBackward |  |
| `0x25` | stMoveForward |  |
| `0x26` | stMoveRight |  |
| `0x27` | stMoveDown |  |
| `0x28` | stMoveLeft |  |
| `0x29` | stMoveUp |  |
| `0x2A` | stTurnRight |  |
| `0x2B` | stTurnLeft |  |
| `0x2C` | stTiltBackward |  |
| `0x2D` | stTiltForward |  |
| `0x2E` | stTiltRight |  |
| `0x2F` | stTiltLeft |  |
| `0x30` | stSpawn |  |
| `0x31` | stCreateTrigger |  |
| `0x32` | stKillTrigger |  |
| `0x33` | stCommandError |  |
| `0x34` | stEndTrigger |  |
| `0x35` | stRemove |  |
| `0x36` | stLetGVar |  |
| `0x37` | stLetPGVar |  |
| `0x38` | stLetAVar |  |
| `0x39` | stEndProc |  |
| `0x3A` | stSetModel | stSetModel |
| `0x3B` | stFileEnd |  |
| `0x3C` | stBlink |  |
| `0x3D` | stHoldTrigger |  |
| `0x3E` | stReleaseTrigger |  |
| `0x3F` | stSetAnim |  |
| `0x40` | stTurnTowardXY |  |
| `0x41` | stCommandError |  |
| `0x42` | stHold |  |
| `0x43` | stRelease |  |
| `0x44` | stInc |  |
| `0x45` | stPlayerAttackOn |  |
| `0x46` | stPlayerAttackOff |  |
| `0x47` | stCamWobble |  |
| `0x48` | stLookAtMe |  |
| `0x49` | stShadowSize |  |
| `0x4A` | stShadowType |  |
| `0x4B` | stClearAnim |  |
| `0x4C` | stStopFall |  |
| `0x4D` | stSetPlayerPosRel |  |
| `0x4E` | stCollectKey |  |
| `0x4F` | stRemoveKey |  |
| `0x50` | stCommandError |  |
| `0x51` | stCommandError |  |
| `0x52` | stCollisionOn |  |
| `0x53` | stCollisionOff |  |
| `0x54` | stPauseTriggers |  |
| `0x55` | stUnpauseTriggers |  |
| `0x56` | stSetPosition |  |
| `0x57` | stIsPlayer |  |
| `0x58` | stIfJumping |  |
| `0x59` | stIfFalling |  |
| `0x5A` | stScale | stScale |
| `0x5B` | stTurnTowardWaypointY |  |
| `0x5C` | stHide |  |
| `0x5D` | stUnhide |  |
| `0x5E` | stLetXGVar |  |
| `0x5F` | stSetCamHeight |  |
| `0x60` | stSetLevel |  |
| `0x61` | stShadowOn |  |
| `0x62` | stShadowOff |  |
| `0x63` | stAccelerate |  |
| `0x64` | stDecelerate |  |
| `0x65` | stSetAnimSpeed |  |
| `0x66` | stSetCamDist |  |
| `0x67` | stUserTrigger |  |
| `0x68` | stWaitEvent |  |
| `0x69` | stPlayerCollisionOn |  |
| `0x6A` | stAnimCtrlSpdOn |  |
| `0x6B` | stAnimCtrlSpdOff |  |
| `0x6C` | stLetParam |  |
| `0x6D` | stTurnTowardPosX |  |
| `0x6E` | stSpecialFXOff |  |
| `0x6F` | stOpenEyes |  |
| `0x70` | stCloseEyes |  |
| `0x71` | stJumpCtrlOn |  |
| `0x72` | stJumpCtrlOff |  |
| `0x73` | stStomp |  |
| `0x74` | stPushCamera |  |
| `0x75` | stPullCamera |  |
| `0x76` | stFloat |  |
| `0x77` | stSpawnChild |  |
| `0x78` | stSetCamera |  |
| `0x79` | stNextImm |  |
| `0x7A` | stAddPickup |  |
| `0x7B` | stLosePickups |  |
| `0x7C` | stReverse |  |
| `0x7D` | stPlayerCollisionOff |  |
| `0x7E` | stSetCollPoint |  |
| `0x7F` | stSetCollPoints |  |
| `0x80` | stPushingOn |  |
| `0x81` | stPushingOff |  |
| `0x82` | stPushableOn |  |
| `0x83` | stPushableOff |  |
| `0x84` | stPushWaypoint |  |
| `0x85` | stPullWaypoint |  |
| `0x86` | stEndWhileImm |  |
| `0x87` | stNextWaypoint |  |
| `0x88` | stPrevWaypoint |  |
| `0x89` | stTurnTowardWaypointXY |  |
| `0x8A` | stTurnTowardPosXY |  |
| `0x8B` | stNearestWaypointNext |  |
| `0x8C` | stNearestWaypointPrev |  |
| `0x8D` | stDeleteWaypoint |  |
| `0x8E` | stCommandError |  |
| `0x8F` | stMoveForwardAngle |  |
| `0x90` | stTurnTowardPosY |  |
| `0x91` | stMovePlayerForward |  |
| `0x92` | stMovePlayerBackward |  |
| `0x93` | stLoopSound |  |
| `0x94` | stWobble |  |
| `0x95` | stCamHold |  |
| `0x96` | stSpeedUp |  |
| `0x97` | stSlowDown |  |
| `0x98` | stSmoothSpeed |  |
| `0x99` | stAccelerateAngle |  |
| `0x9A` | stDecelerateAngle |  |
| `0x9B` | stMovePosition |  |
| `0x9C` | stRemoveFromMap |  |
| `0x9D` | stInitCrystal |  |
| `0x9E` | stCrystal |  |
| `0x9F` | stEndLevel |  |
| `0xA0` | stStopDead |  |
| `0xA1` | stPitchShift |  |
| `0xA2` | stActivated |  |
| `0xA3` | stHangOn |  |
| `0xA4` | stHangOff |  |
| `0xA5` | stCreateDeath |  |
| `0xA6` | stDoDeath |  |
| `0xA7` | stEndCrystal |  |
| `0xA8` | stPausePlayer |  |
| `0xA9` | stUnpausePlayer |  |
| `0xAA` | stPlayerDead |  |
| `0xAB` | stSlideOn |  |
| `0xAC` | stSlideOff |  |
| `0xAD` | stFirstWaypoint |  |
| `0xAE` | stUntilImm |  |
| `0xAF` | stCollected |  |
| `0xB0` | stDec |  |
| `0xB1` | stSpawnFrom |  |
| `0xB2` | stLetXParam |  |
| `0xB3` | stRemoveCrystal |  |
| `0xB4` | stCollectJigsaw |  |
| `0xB5` | stBonus |  |
| `0xB6` | stNextLevel |  |
| `0xB7` | stLookAtMe |  |
| `0xB8` | stNoHang |  |
| `0xB9` | stVibrate |  |
| `0xBA` | stPlayerNoStood |  |
| `0xBB` | stRemoveGobbo |  |
| `0xBC` | stPauseTriggersNoAnim |  |
| `0xBD` | stShowBonus |  |
| `0xBE` | stLookAtMeMap |  |
| `0xBF` | stPlayerMove |  |
| `0xC0` | stPlayerTurn |  |
| `0xC1` | stSetEnvelope |  |
| `0xC2` | stTurnTowardPlayerX |  |
| `0xC3` | stTurnTowardPlayerY |  |
| `0xC4` | stTurnTowardPlayerXY |  |
| `0xC5` | stForceDoor |  |
| `0xC6` | stLevelStats |  |
| `0xC7` | stReSeed |  |
| `0xC8` | stShowBonusOn |  |
| `0xC9` | stShowBonusOff |  |
| `0xCA` | stRemoveModel |  |
| `0xCB` | stQuickPlayer |  |
| `0xCC` | stGobboON |  |
| `0xCD` | stGobboOFF |  |
| `0xCE` | stUnActivated |  |
| `0xCF` | stEndSubLevel |  |
| `0xD0` | stTurnOffLookAtMe |  |
| `0xD1` | stHeightFloat |  |
| `0xD2` | stFlashOn |  |
| `0xD3` | stFlashOff |  |
| `0xD4` | stCommandError |  |
| `0xD5` | stCommandError |  |
| `0xD6` | stCommandError |  |
| `0xD7` | stCommandError | stCommandError |
| `0xD8` | stCommandError | stCommandError |
| `0xD9` | stCommandError | stCommandError |
| `0xDA` | stCommandError | stCommandError |
| `0xDB` | stCommandError | stCommandError |
| `0xDC` | stCommandError | stCommandError |
| `0xDD` | stCommandError | stCommandError |
| `0xDE` | stCommandError | stCommandError |
| `0xDF` | stCommandError | stCommandError |
| `0xE0` | stCommandError | stCommandError |
| `0xE1` | stCommandError | stCommandError |
| `0xE2` | stCommandError | stCommandError |
| `0xE3` | stCommandError | stCommandError |
| `0xE4` | stCommandError | stCommandError |
| `0xE5` | stCommandError | stCommandError |
| `0xE6` | stCommandError | stCommandError |
| `0xE7` | stCommandError | stCommandError |
| `0xE8` | stCommandError | stCommandError |
| `0xE9` | stCommandError | stCommandError |
| `0xEA` | stCommandError | stCommandError |
| `0xEB` | stCommandError | stCommandError |
| `0xEC` | stCommandError | stCommandError |
| `0xED` | stCommandError | stCommandError |
| `0xEE` | stCommandError | stCommandError |
| `0xEF` | stCommandError | stCommandError |
| `0xF0` | stCommandError | stCommandError |
| `0xF1` | stCommandError | stCommandError |
| `0xF2` | stCommandError | stCommandError |
| `0xF3` | stCommandError | stCommandError |
| `0xF4` | stCommandError | stCommandError |
| `0xF5` | stCommandError | stCommandError |
| `0xF6` | stCommandError | stCommandError |
| `0xF7` | stCommandError | stCommandError |
| `0xF8` | stCommandError | stCommandError |
| `0xF9` | stCommandError | stCommandError |
| `0xFA` | stCommandError | stCommandError |
| `0xFB` | stCommandError | stCommandError |
| `0xFC` | stCommandError | stCommandError |
| `0xFD` | stCommandError | stCommandError |
| `0xFE` | stTonyTest | stTonyTest |
| `0xFF` | stLewisTest | stLewisTest |
