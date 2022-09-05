
uint32_t stEvaluate(stStrat *strat)

{
  short *psVar1;
  bool bVar2;
  short offset;
  uint32_t uVar3;
  undefined2 extraout_var;
  uint uVar4;
  stStrat *psVar5;
  uint32_t *puVar6;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  byte **ppbVar7;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  undefined2 extraout_var_04;
  int iVar8;
  int tempResultVar;
  byte *instructionStream;
  byte *pbVar9;
  uint32_t **ppuVar10;
  uint32_t *puVar11;
  uint32_t *puVar12;
  ushort *puVar13;
  uint32_t **evsp_;
  uint32_t **ppuVar14;
  uint32_t *puVar15;
  ushort *puVar16;
  int returnValuesCount;
  uint32_t tempValue;
  undefined auStack72 [8];
  uint32_t *local_40;
  uint32_t *local_3c;
  uint32_t *local_38;
  uint32_t *result;
  undefined2 local_2c [2];
  uint32_t *local_28;
  short local_24 [2];
  byte resource_type;
  
  returnValuesCount = 0;
  tempValue = 0;
  evsp = &evalstack;
  do {
    instructionStream = strat->instructionStream;
    strat->instructionStream = instructionStream + 1;
    evsp_ = (uint32_t **)evsp;
    if (false) {
switchD_8002e9b4_caseD_5:
      strat->flags2 = (uint32_t *)((uint)strat->flags2 | 6);
                    /* WARNING: Subroutine does not return */
      printf(&s_Error_in_evaluate_s,strat->name + 4);
    }
    switch(*instructionStream) {
    case 1:
                    /* Get an XGVar */
      offset = getPCword(strat);
      tempResultVar = CONCAT22(extraout_var_04,offset);
      puVar15 = (uint32_t *)strat->someVars[2];
      evsp_ = (uint32_t **)evsp;
      goto LAB_8002f630;
    case 2:
                    /* Get a strat global variable */
      offset = getPCword(strat);
      tempResultVar = CONCAT22(extraout_var_02,offset);
      puVar15 = strat->stratGlobals;
      evsp_ = (uint32_t **)evsp;
LAB_8002f630:
      evsp = (int32_t **)(evsp_ + 1);
      *evsp_ = (uint32_t *)puVar15[tempResultVar];
      goto LAB_8002fe5c;
    case 3:
                    /* Get an alien variable */
      offset = getPCword(strat);
      local_28 = (uint32_t *)0x0;
      if (false) goto switchD_8002ed90_caseD_55;
      break;
    case 4:
                    /* Push a 32-bit integer on top of the stack.
                        */
      puVar15 = (uint32_t *)getPClong(strat);
LAB_8002ed4c:
      evsp_ = (uint32_t **)evsp + 1;
      *evsp = (int32_t *)puVar15;
      evsp = (int32_t **)evsp_;
      goto LAB_8002fe5c;
    default:
      goto switchD_8002e9b4_caseD_5;
    case 6:
      evsp_ = (uint32_t **)evsp + -1;
                    /* Add the values on the top of the stack */
      local_28 = ((uint32_t **)evsp)[-2];
      ppuVar10 = (uint32_t **)evsp + -2;
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      *ppuVar10 = (uint32_t *)((int)*evsp_ + (int)local_28);
      goto LAB_8002fe5c;
    case 7:
      evsp_ = (uint32_t **)evsp + -1;
                    /* Subtract the values on the top of the stack ([top-1] - top) */
      local_28 = ((uint32_t **)evsp)[-2];
      ppuVar10 = (uint32_t **)evsp + -2;
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      *ppuVar10 = (uint32_t *)((int)local_28 - (int)*evsp_);
      goto LAB_8002fe5c;
    case 8:
                    /* Divide the two variables on the top of the stack */
      puVar15 = ((uint32_t **)evsp)[-1];
      local_28 = ((uint32_t **)evsp)[-2];
      evsp_ = (uint32_t **)evsp + -2;
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      *evsp_ = (uint32_t *)
               (((int)local_28 % (int)puVar15) / (int)((uint)puVar15 >> 0x10) & 0xffffU |
               (int)local_28 / (int)puVar15 << 0x10);
      goto LAB_8002fe5c;
    case 9:
      evsp_ = (uint32_t **)evsp + -1;
                    /* Multiply the two variables on the top of the stack */
      local_28 = ((uint32_t **)evsp)[-2];
      ppuVar10 = (uint32_t **)evsp + -2;
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      *ppuVar10 = (uint32_t *)
                  ((uint)((longlong)(int)*evsp_ * (longlong)(int)local_28) >> 0x10 |
                  (int)((ulonglong)((longlong)(int)*evsp_ * (longlong)(int)local_28) >> 0x20) <<
                  0x10);
      goto LAB_8002fe5c;
    case 10:
      evsp_ = (uint32_t **)evsp + -1;
                    /* Bitwise AND with the two varaibles on the top of the stack. */
      local_28 = ((uint32_t **)evsp)[-2];
      ppuVar10 = (uint32_t **)evsp + -2;
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      *ppuVar10 = (uint32_t *)((uint)*evsp_ & (uint)local_28);
      goto LAB_8002fe5c;
    case 0xb:
                    /* Bitwise OR with the two variables on top of the stack */
      evsp_ = (uint32_t **)evsp + -1;
      local_28 = ((uint32_t **)evsp)[-2];
      ppuVar10 = (uint32_t **)evsp + -2;
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      *ppuVar10 = (uint32_t *)((uint)*evsp_ | (uint)local_28);
      goto LAB_8002fe5c;
    case 0xc:
                    /* Check the variables on top of the stack for equality */
      evsp_ = (uint32_t **)evsp + -1;
      local_28 = ((uint32_t **)evsp)[-2];
      ppuVar10 = (uint32_t **)evsp + -2;
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      *ppuVar10 = (uint32_t *)(uint)(local_28 == *evsp_);
      goto LAB_8002fe5c;
    case 0xd:
                    /* Check the two values on top of the stack for inqeuality */
      evsp_ = (uint32_t **)evsp + -1;
      local_28 = ((uint32_t **)evsp)[-2];
      ppuVar10 = (uint32_t **)evsp + -2;
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      *ppuVar10 = (uint32_t *)(uint)(local_28 != *evsp_);
      goto LAB_8002fe5c;
    case 0xe:
                    /* Less than */
      evsp_ = (uint32_t **)evsp + -1;
      local_28 = ((uint32_t **)evsp)[-2];
      ppuVar10 = (uint32_t **)evsp + -2;
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      *ppuVar10 = (uint32_t *)(uint)((int)*evsp_ < (int)local_28);
      goto LAB_8002fe5c;
    case 0xf:
      evsp_ = (uint32_t **)evsp + -1;
                    /* Greater than */
      local_28 = ((uint32_t **)evsp)[-2];
      ppuVar10 = (uint32_t **)evsp + -2;
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      *ppuVar10 = (uint32_t *)(uint)((int)local_28 < (int)*evsp_);
      goto LAB_8002fe5c;
    case 0x10:
                    /* Less than or equal to */
      local_28 = ((uint32_t **)evsp)[-2];
      bVar2 = (int)local_28 < (int)((uint32_t **)evsp)[-1];
      goto LAB_8002fa30;
    case 0x11:
      local_28 = ((uint32_t **)evsp)[-2];
      bVar2 = (int)((uint32_t **)evsp)[-1] < (int)local_28;
LAB_8002fa30:
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      evsp_[-2] = (uint32_t *)(bVar2 ^ 1);
      goto LAB_8002fe5c;
    case 0x12:
                    /* Pop the value at the top of the stack and return it
                        */
      tempValue = (uint32_t)((uint32_t **)evsp)[-1];
      returnValuesCount = returnValuesCount + 1;
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      goto LAB_8002fe5c;
    case 0x13:
      instructionStream = strat->instructionStream;
      strat->instructionStream = instructionStream + 1;
      resource_type = *instructionStream;
      if (resource_type == 5) {
                    /* Read an Int32 and push it on the eval stack */
        puVar15 = (uint32_t *)getPClong(strat);
        instructionStream = strat->instructionStream;
        pbVar9 = instructionStream + 1;
        strat->instructionStream = pbVar9;
        strat->instructionStream = pbVar9 + *instructionStream;
        result = puVar15;
        goto LAB_8002ed4c;
      }
      if (resource_type < 6) {
        if (resource_type == 3) {
                    /* Seems to be the exact same as 13 05: read an int32 and push to stack. */
          puVar15 = (uint32_t *)getPClong(strat);
          instructionStream = strat->instructionStream;
          pbVar9 = instructionStream + 1;
          strat->instructionStream = pbVar9;
          strat->instructionStream = pbVar9 + *instructionStream;
          result = puVar15;
          goto LAB_8002ed4c;
        }
        if (resource_type < 4) {
          if (resource_type != 0) {
            result = (uint32_t *)getPClong(strat);
            if (result == (uint32_t *)0x0) {
              result = (uint32_t *)SearchForEntry((char *)(strat->instructionStream + 1));
              if (result == (uint32_t *)0x0) {
                    /* WARNING: Subroutine does not return */
                printf(&DAT_800109e4,strat->name + 4,strat->instructionStream);
              }
              evsp_ = (uint32_t **)evsp + 1;
              *evsp = (int32_t *)result;
              evsp = (int32_t **)evsp_;
            }
            else {
              evsp_ = (uint32_t **)evsp + 1;
              *evsp = (int32_t *)result;
              evsp = (int32_t **)evsp_;
            }
            instructionStream = strat->instructionStream;
            pbVar9 = instructionStream + 1;
            strat->instructionStream = pbVar9;
            strat->instructionStream = pbVar9 + *instructionStream;
            if (resource_type == 2) {
              strat->flags2 = (uint32_t *)((uint)strat->flags2 | 0x80);
            }
            else {
              strat->flags2 = (uint32_t *)((uint)strat->flags2 & 0xffffff7f);
            }
          }
        }
        else {
          result = (uint32_t *)getPClong(strat);
          instructionStream = strat->instructionStream;
          pbVar9 = instructionStream + 1;
          strat->instructionStream = pbVar9;
          strat->instructionStream = pbVar9 + *instructionStream;
          if (result != (uint32_t *)0x0) {
            puVar15 = (uint32_t *)((int)result + -1);
            ppuVar10 = (uint32_t **)evsp;
            goto code_r0x8002ece0;
          }
        }
      }
      else {
        if (resource_type == 0x50) {
          puVar15 = (uint32_t *)getPClong(strat);
          instructionStream = strat->instructionStream;
          pbVar9 = instructionStream + 1;
          strat->instructionStream = pbVar9;
          strat->instructionStream = pbVar9 + *instructionStream;
          ppuVar10 = (uint32_t **)evsp;
joined_r0x8002ecb8:
          result = puVar15;
          if (puVar15 != (uint32_t *)0x0) {
            puVar15 = (uint32_t *)((int)puVar15 + -1);
            result = puVar15;
          }
code_r0x8002ece0:
          evsp = (int32_t **)(ppuVar10 + 1);
          puVar15 = (uint32_t *)((int)puVar15 << 0x10);
          goto LAB_8002ece4;
        }
        if (resource_type < 0x51) {
          if (resource_type == 9) {
            instructionStream = strat->instructionStream;
            strat->instructionStream = instructionStream + 1;
            resource_type = *instructionStream;
            uVar3 = stEvaluate(strat);
            local_28 = (uint32_t *)((int)uVar3 >> 0x10);
            tempResultVar = 100;
            if (1 < resource_type) {
              uVar3 = stEvaluate(strat);
              tempResultVar = (int)uVar3 >> 0x10;
            }
            iVar8 = 0;
            if (3 < resource_type) {
              uVar3 = stEvaluate(strat);
              iVar8 = (int)uVar3 >> 0x10;
              stEvaluate(strat);
            }
            CameraDistAng(&strat->field790_0x368,&result,local_2c);
            if (RunD != 2) {
              puVar15 = (uint32_t *)SFXPlay(local_28,tempResultVar,iVar8,result,local_2c[0]);
              goto LAB_8002ed4c;
            }
            evsp_ = (uint32_t **)evsp + 1;
            *evsp = (int32_t *)0x0;
            evsp = (int32_t **)evsp_;
          }
        }
        else {
          if (resource_type == 0x51) {
            puVar15 = (uint32_t *)getPClong(strat);
            ppuVar10 = (uint32_t **)evsp;
            goto joined_r0x8002ecb8;
          }
          if (resource_type == 0x8e) {
            puVar15 = (uint32_t *)getPClong(strat);
            result = puVar15;
            goto LAB_8002ed4c;
          }
        }
      }
      goto LAB_8002fe5c;
    case 0x14:
                    /* Get sine of top of stack */
      psVar1 = (short *)((int)evsp + -2);
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      tempResultVar = rsin((int)*psVar1 & 0xfff);
      goto LAB_8002fc9c;
    case 0x15:
                    /* Get cosine of top of stack */
      psVar1 = (short *)((int)evsp + -2);
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      tempResultVar = rcos((int)*psVar1 & 0xfff);
      goto LAB_8002fc9c;
    case 0x17:
                    /* Get square root of top of stack */
      evsp_ = (uint32_t **)evsp + -1;
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      tempResultVar = SquareRoot((int)*evsp_ >> 4);
LAB_8002fc9c:
      evsp_ = (uint32_t **)evsp + 1;
      *evsp = (int32_t *)(tempResultVar << 4);
      evsp = (int32_t **)evsp_;
      goto LAB_8002fe5c;
    case 0x18:
                    /* Get the absolute value of the top of the stack */
      puVar15 = ((uint32_t **)evsp)[-1];
      if ((int)puVar15 < 0) {
        puVar15 = (uint32_t *)-(int)puVar15;
      }
      ((uint32_t **)evsp)[-1] = puVar15;
      goto LAB_8002fe5c;
    case 0x19:
                    /* Get a random number (stack top is max value) */
      tempResultVar = rand();
      iVar8 = rand();
      random_number = tempResultVar + iVar8 * 0x20000 + random_number;
      puVar15 = (uint32_t *)(random_number % (uint)((uint32_t **)evsp)[-1]);
      if (((uint32_t **)evsp)[-1] == (uint32_t *)0x0) {
        trap(0x1c00);
      }
      goto LAB_8002fad0;
    case 0x1a:
                    /* Floor the value (fixed point only) */
      puVar15 = (uint32_t *)((uint)((uint32_t **)evsp)[-1] & 0xffff0000);
LAB_8002fad0:
      ((uint32_t **)evsp)[-1] = puVar15;
      goto LAB_8002fe5c;
    case 0x1b:
                    /* Get if player is within the specified radius of this strat */
      evsp_ = (uint32_t **)evsp + -1;
      puVar15 = ((uint32_t **)evsp)[-1];
      local_28 = (uint32_t *)0x0;
      evsp = (int32_t **)evsp_;
      if (PlayerStrat != (stStrat *)0x0) {
        ObjectDistNoY(&PlayerStrat->field790_0x368,&strat->field790_0x368,&result);
        bVar2 = (uint32_t *)((int)result << 4) < puVar15;
LAB_8002fd40:
        puVar15 = (uint32_t *)0xffffffff;
        if (bVar2) goto LAB_8002fd48;
      }
      goto switchD_8002ed90_caseD_55;
    case 0x1c:
                    /* Push an external global variable to the stack */
      offset = getPCword(strat);
      evsp_ = (uint32_t **)evsp + 1;
      *evsp = (int32_t *)*(uint32_t **)(&extern_globals + CONCAT22(extraout_var_03,offset) * 4);
      evsp = (int32_t **)evsp_;
      goto LAB_8002fe5c;
    case 0x1d:
                    /* Load a value from the instruction stream (pc+offset+0x154) */
      offset = getPCword(strat);
      ppbVar7 = &strat->instructionStream + CONCAT22(extraout_var_00,offset);
      evsp_ = (uint32_t **)evsp;
      goto LAB_8002f5a8;
    case 0x1e:
                    /* Negate the value on the top of the stack */
      ((uint32_t **)evsp)[-1] = (uint32_t *)-(int)((uint32_t **)evsp)[-1];
      goto LAB_8002fe5c;
    case 0x1f:
                    /* Check that the value on the stack equals zero */
      if (((uint32_t **)evsp)[-1] == (uint32_t *)0x0) {
        ((uint32_t **)evsp)[-1] = (uint32_t *)0x1;
      }
      else {
        ((uint32_t **)evsp)[-1] = (uint32_t *)0x0;
      }
      goto LAB_8002fe5c;
    case 0x20:
                    /* Check if top two stack values are not zero */
      ppuVar14 = (uint32_t **)evsp + -1;
      evsp_ = (uint32_t **)evsp + -1;
      ppuVar10 = (uint32_t **)evsp + -2;
      local_28 = ((uint32_t **)evsp)[-2];
      puVar15 = (uint32_t *)0x0;
      evsp = (int32_t **)ppuVar14;
      if (*evsp_ != (uint32_t *)0x0) {
        puVar15 = (uint32_t *)(uint)(local_28 != (uint32_t *)0x0);
      }
LAB_8002ece4:
      *ppuVar10 = puVar15;
      goto LAB_8002fe5c;
    case 0x21:
                    /* Check that the magnitude of the velocity is less than the top of the stack.
                        */
      ppuVar10 = (uint32_t **)evsp + -1;
      evsp_ = (uint32_t **)evsp + -1;
      local_28 = (uint32_t *)0x0;
      evsp = (int32_t **)ppuVar10;
      if (PlayerStrat != (stStrat *)0x0) {
        bVar2 = (int)(strat->velocityMagintude << 4) < (int)*evsp_;
        goto LAB_8002fd40;
      }
      goto switchD_8002ed90_caseD_55;
    case 0x22:
                    /* Pop the top three values from the stack as a vector and push the distance
                       from the point to the vector onto the stack. */
      local_38 = ((uint32_t **)evsp)[-1];
      local_3c = ((uint32_t **)evsp)[-2];
      local_40 = ((uint32_t **)evsp)[-3];
      evsp = (int32_t **)((uint32_t **)evsp + -3);
      ObjectDist(auStack72,&strat->field790_0x368,&local_28);
      local_28 = (uint32_t *)((int)local_28 << 4);
      evsp_ = (uint32_t **)evsp + 1;
      *evsp = (int32_t *)local_28;
      evsp = (int32_t **)evsp_;
      goto LAB_8002fe5c;
    case 0x23:
                    /* See if a flag is set and decrement the eval stack pointer if so. */
      if (((uint)strat->flags2 & 0x8000000) == 0) {
        evsp = (int32_t **)((uint32_t **)evsp + -1);
      }
      goto LAB_8002fe5c;
    case 0x24:
      psVar1 = (short *)((int)evsp + -2);
      local_28 = ((uint32_t **)evsp)[-2];
      evsp_ = (uint32_t **)evsp + -2;
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      *evsp_ = (uint32_t *)((int)local_28 >> ((int)*psVar1 & 0x1fU));
      goto LAB_8002fe5c;
    case 0x25:
      psVar1 = (short *)((int)evsp + -2);
      local_28 = ((uint32_t **)evsp)[-2];
      evsp_ = (uint32_t **)evsp + -2;
      evsp = (int32_t **)((uint32_t **)evsp + -1);
      *evsp_ = (uint32_t *)((int)local_28 << ((int)*psVar1 & 0x1fU));
      goto LAB_8002fe5c;
    case 0x26:
      tempValue = 0;
      returnValuesCount = returnValuesCount + 1;
      goto LAB_8002fe5c;
    case 0x27:
      puVar15 = strat->someVars;
      local_28 = (uint32_t *)
                 ((int)*(short *)(*(short *)((int)evsp + -2) * 0x18 +
                                  *(int *)(puVar15[0x50] * 4 + *(int *)(puVar15[9] + 0x1c)) + 0x12)
                 + puVar15[0xdc]);
      goto LAB_8002fc14;
    case 0x28:
      puVar15 = strat->someVars;
      local_28 = (uint32_t *)
                 ((int)*(short *)(*(short *)((int)evsp + -2) * 0x18 +
                                  *(int *)(puVar15[0x50] * 4 + *(int *)(puVar15[9] + 0x1c)) + 0x14)
                 + puVar15[0xdd]);
      goto LAB_8002fc14;
    case 0x29:
      puVar15 = strat->someVars;
      local_28 = (uint32_t *)
                 ((int)*(short *)(*(short *)((int)evsp + -2) * 0x18 +
                                  *(int *)(puVar15[0x50] * 4 + *(int *)(puVar15[9] + 0x1c)) + 0x16)
                 + puVar15[0xde]);
LAB_8002fc14:
      ((uint32_t **)evsp)[-1] = local_28;
      goto LAB_8002fe5c;
    case 0x2a:
    case 0x2b:
    case 0x2c:
      ((uint32_t **)evsp)[-1] = (uint32_t *)0x0;
      goto LAB_8002fe5c;
    case 0x2d:
      offset = getPCword(strat);
      ppbVar7 = (byte **)(strat->someVars + CONCAT22(extraout_var_01,offset));
      evsp_ = (uint32_t **)evsp;
LAB_8002f5a8:
      evsp = (int32_t **)(evsp_ + 1);
      *evsp_ = (uint32_t *)ppbVar7[0x55];
      goto LAB_8002fe5c;
    case 0x2e:
      *evsp = (int32_t *)(&JigsawPieces)[(int)*evsp];
      goto LAB_8002fe5c;
    }
                    /* IMPORTANT: This is a different switch-case from the one above, which seems to
                       handle some strat properties. */
    switch(CONCAT22(extraout_var,offset)) {
    case 0:
      local_28 = strat->field29_0x38;
      goto switchD_8002ed90_caseD_55;
    case 1:
      local_28 = (uint32_t *)(uint)strat->field30_0x3c;
      goto switchD_8002ed90_caseD_55;
    case 2:
      local_28 = strat->field_0x370_;
      goto switchD_8002ed90_caseD_55;
    case 3:
      local_28 = strat->field794_0x374;
      goto switchD_8002ed90_caseD_55;
    case 4:
      local_28 = strat->field795_0x378;
      goto switchD_8002ed90_caseD_55;
    case 5:
      uVar4 = strat->field790_0x368 & 0xfff;
      goto LAB_8002f508;
    case 6:
      uVar4 = strat->field791_0x36a & 0xfff;
      goto LAB_8002f508;
    case 7:
      uVar4 = *(ushort *)&strat->field792_0x36c & 0xfff;
      goto LAB_8002f508;
    case 8:
      puVar15 = (uint32_t *)((int)strat->field143_0xb4 << 4);
      break;
    case 9:
      puVar15 = (uint32_t *)(*(int *)&strat->field_0xb8 << 4);
      break;
    case 10:
      puVar15 = (uint32_t *)((int)strat->field143_0xb4 << 4);
      break;
    case 0xb:
      ObjectDistNoY(&strat->field790_0x368,&strat->field_0x380,&local_28);
      goto LAB_8002f2c4;
    case 0xc:
      if (PlayerPaused != 0) goto switchD_8002ed90_caseD_53;
      local_28 = PlayerPad;
      goto switchD_8002ed90_caseD_55;
    case 0xd:
      if (PlayerPaused != 0) goto switchD_8002ed90_caseD_53;
      local_28 = PlayerPadPush;
      goto switchD_8002ed90_caseD_55;
    case 0xe:
      if (PlayerPaused != 0) goto switchD_8002ed90_caseD_53;
      local_28 = PlayerPadPull;
      goto switchD_8002ed90_caseD_55;
    case 0xf:
      psVar5 = PlayerStrat;
      goto code_r0x8002eef4;
    case 0x10:
      psVar5 = PlayerStrat;
      goto code_r0x8002ef0c;
    case 0x11:
      psVar5 = PlayerStrat;
      goto code_r0x8002ef24;
    case 0x12:
      uVar4 = PlayerStrat->field790_0x368 & 0xfff;
      goto LAB_8002f508;
    case 0x13:
      uVar4 = PlayerStrat->field791_0x36a & 0xfff;
      goto LAB_8002f508;
    case 0x14:
      uVar4 = *(ushort *)&PlayerStrat->field792_0x36c & 0xfff;
      goto LAB_8002f508;
    case 0x15:
      puVar15 = (uint32_t *)(accval << 0x10);
      break;
    case 0x16:
      puVar15 = (uint32_t *)((int)strat->field83_0x74 << 0x10);
      break;
    case 0x17:
      puVar15 = (uint32_t *)((uint)strat->field84_0x76 << 0x10);
      break;
    case 0x18:
      puVar15 = (uint32_t *)((uint)strat->flags2 & 0x200);
      break;
    case 0x19:
      puVar15 = (uint32_t *)((uint)strat->flags2 & 0x400);
      break;
    case 0x1a:
      puVar15 = (uint32_t *)((uint)strat->flags2 & 8);
      break;
    case 0x1b:
      local_28 = (uint32_t *)(uint)strat->field31_0x3d;
      goto switchD_8002ed90_caseD_55;
    case 0x1c:
      puVar15 = (uint32_t *)(strat->velocityMagintude << 4);
      break;
    case 0x1d:
      puVar13 = (ushort *)(strat->field330_0x190 + 8);
      puVar16 = &strat->field790_0x368;
LAB_8002f2bc:
      ObjectDist(puVar13,puVar16,&local_28);
LAB_8002f2c4:
      puVar15 = (uint32_t *)((int)local_28 << 4);
      break;
    case 0x1e:
      local_28 = (uint32_t *)strat->field330_0x190[10];
      goto switchD_8002ed90_caseD_55;
    case 0x1f:
      local_28 = (uint32_t *)strat->field330_0x190[0xb];
      goto switchD_8002ed90_caseD_55;
    case 0x20:
      local_28 = (uint32_t *)strat->field330_0x190[0xc];
      goto switchD_8002ed90_caseD_55;
    case 0x21:
      local_28 = (uint32_t *)strat->field330_0x190[0xe];
      goto switchD_8002ed90_caseD_55;
    case 0x22:
      local_28 = (uint32_t *)0x0;
      if (*strat->field330_0x190 == 0) {
        local_28 = (uint32_t *)0x10000;
      }
      if (strat->field330_0x190[1] == 0) {
        puVar15 = (uint32_t *)((uint)local_28 | 0x20000);
        break;
      }
      goto switchD_8002ed90_caseD_55;
    case 0x23:
      local_28 = strat->field82_0x70;
      goto switchD_8002ed90_caseD_55;
    case 0x24:
      puVar15 = (uint32_t *)((uint)strat->flags2 & 0x400000);
      break;
    case 0x25:
      local_28 = CamLookOffset;
      goto switchD_8002ed90_caseD_55;
    case 0x26:
      local_28 = DAT_8007dbdc;
      goto switchD_8002ed90_caseD_55;
    case 0x27:
      local_28 = DAT_8007dbe0;
      goto switchD_8002ed90_caseD_55;
    case 0x28:
      puVar15 = (uint32_t *)((uint)*(ushort *)(CurrentMap + 0x6e) << 0x10);
      break;
    case 0x29:
      puVar15 = (uint32_t *)(PickUpCount << 0x10);
      break;
    case 0x2a:
      local_28 = DAT_8006b348;
      goto switchD_8002ed90_caseD_55;
    case 0x2b:
      local_28 = DAT_8006b34c;
      goto switchD_8002ed90_caseD_55;
    case 0x2c:
      local_28 = DAT_8006b350;
      goto switchD_8002ed90_caseD_55;
    case 0x2d:
      uVar4 = cam._2_2_ & 0xfff;
      goto LAB_8002f508;
    case 0x2e:
      puVar15 = (uint32_t *)(GobboCount << 0x10);
      break;
    case 0x2f:
      puVar15 = (uint32_t *)(strat->model_related & 0x200);
      break;
    case 0x30:
      if (strat->field329_0x18c == (uint32_t *)0x0) goto switchD_8002ed90_caseD_53;
      puVar15 = (uint32_t *)(strat->field329_0x18c[5] & 2);
      break;
    case 0x31:
      puVar15 = (uint32_t *)((uint)PlayerStrat->flags2 & 0x200);
      break;
    case 0x32:
      puVar15 = (uint32_t *)((uint)PlayerStrat->flags2 & 0x400);
      break;
    case 0x33:
      psVar5 = (stStrat *)strat->someVars;
code_r0x8002eef4:
      local_28 = psVar5->field_0x370_;
      goto switchD_8002ed90_caseD_55;
    case 0x34:
      psVar5 = (stStrat *)strat->someVars;
code_r0x8002ef0c:
      local_28 = psVar5->field794_0x374;
      goto switchD_8002ed90_caseD_55;
    case 0x35:
      psVar5 = (stStrat *)strat->someVars;
code_r0x8002ef24:
      local_28 = psVar5->field795_0x378;
      goto switchD_8002ed90_caseD_55;
    case 0x36:
      uVar4 = *(ushort *)(strat->someVars + 0xda) & 0xfff;
      goto LAB_8002f508;
    case 0x37:
      uVar4 = *(ushort *)((int)strat->someVars + 0x36a) & 0xfff;
      goto LAB_8002f508;
    case 0x38:
      uVar4 = *(ushort *)(strat->someVars + 0xdb) & 0xfff;
      goto LAB_8002f508;
    case 0x39:
      puVar15 = (uint32_t *)(KeyCollected << 0x10);
      break;
    case 0x3a:
      local_28 = DoorType;
      goto switchD_8002ed90_caseD_55;
    case 0x3b:
      puVar11 = PlayerStrat->field_0x370_;
      puVar15 = strat->field_0x370_;
      puVar12 = PlayerStrat->field795_0x378;
      puVar6 = strat->field795_0x378;
      local_24[0] = -strat->field791_0x36a;
      tempResultVar = rsin((int)local_24[0]);
      iVar8 = rcos((int)local_24[0]);
      tempResultVar =
           ((int)puVar12 - (int)puVar6) * tempResultVar + ((int)puVar11 - (int)puVar15) * iVar8;
      goto LAB_8002f030;
    case 0x3c:
      puVar15 = (uint32_t *)((int)PlayerStrat->field794_0x374 - (int)strat->field794_0x374);
      break;
    case 0x3d:
      puVar11 = PlayerStrat->field_0x370_;
      puVar15 = strat->field_0x370_;
      puVar12 = PlayerStrat->field795_0x378;
      puVar6 = strat->field795_0x378;
      local_24[0] = -strat->field791_0x36a;
      tempResultVar = rcos((int)local_24[0]);
      iVar8 = rsin((int)local_24[0]);
      tempResultVar =
           ((int)puVar12 - (int)puVar6) * tempResultVar - ((int)puVar11 - (int)puVar15) * iVar8;
LAB_8002f030:
      puVar15 = (uint32_t *)(tempResultVar >> 0xc);
      break;
    case 0x3e:
      ObjectAng(strat->field330_0x190 + 8,&strat->field790_0x368,local_24);
      puVar15 = (uint32_t *)((int)local_24[0] << 0x10);
      break;
    case 0x3f:
      if (PlayerStrat == (stStrat *)0x0) goto switchD_8002ed90_caseD_53;
      ObjectAng(&PlayerStrat->field790_0x368,&strat->field790_0x368,local_24);
      puVar15 = (uint32_t *)((int)local_24[0] << 0x10);
      break;
    case 0x40:
      puVar13 = &PlayerStrat->field790_0x368;
      if (PlayerStrat != (stStrat *)0x0) {
        puVar16 = (ushort *)(strat->field330_0x190 + 8);
        goto LAB_8002f2bc;
      }
    case 0x53:
switchD_8002ed90_caseD_53:
      local_28 = (uint32_t *)0x0;
      goto switchD_8002ed90_caseD_55;
    case 0x41:
      puVar15 = (uint32_t *)(strat->model_related & 2);
      break;
    case 0x42:
      puVar15 = (uint32_t *)(light_timer << 0x10);
      break;
    case 0x43:
      puVar15 = (uint32_t *)0x1;
      if (BonusCollected == 0x1f) break;
      local_28 = (uint32_t *)0x0;
      goto switchD_8002ed90_caseD_55;
    case 0x44:
      puVar15 = (uint32_t *)(LittleKeysCollected << 0x10);
      break;
    case 0x45:
      puVar15 = (uint32_t *)(level_number << 0x10);
      break;
    case 0x46:
      puVar15 = (uint32_t *)(sublevel_number << 0x10);
      break;
    case 0x47:
      puVar15 = (uint32_t *)0x10000;
      break;
    case 0x48:
      local_28 = move_state;
      goto switchD_8002ed90_caseD_55;
    case 0x49:
      local_28 = turn_speed;
      goto switchD_8002ed90_caseD_55;
    case 0x4a:
      puVar15 = (uint32_t *)((int)strat->field143_0xb4 << 4);
      break;
    case 0x4b:
      puVar15 = (uint32_t *)((int)*(short *)&strat->field_0xb8 << 4);
      break;
    case 0x4c:
      puVar15 = (uint32_t *)((int)strat->field146_0xba << 4);
      break;
    case 0x4d:
      puVar15 = (uint32_t *)0x1;
      break;
    case 0x4e:
      puVar15 = (uint32_t *)(strat->model_related & 0x800);
      break;
    case 0x4f:
      puVar15 = (uint32_t *)(strat->someVars[0x5e] & 0x800);
      break;
    case 0x50:
      local_28 = NewLevelSelected;
      NewLevelSelected = (uint32_t *)0x0;
      goto switchD_8002ed90_caseD_55;
    case 0x51:
      local_28 = (uint32_t *)((level_number_order % 10) * 0x10000);
      goto switchD_8002ed90_caseD_55;
    case 0x52:
      local_28 = CameraThere;
      goto switchD_8002ed90_caseD_55;
    case 0x54:
      if ((PlayerStrat->field30_0x3c & 0x80) == 0) goto switchD_8002ed90_caseD_53;
      local_28 = WaterDoorCount;
    default:
      goto switchD_8002ed90_caseD_55;
    case 0x56:
      local_28 = *(uint32_t **)(CurrentMap + 0x10);
      goto switchD_8002ed90_caseD_55;
    case 0x57:
      puVar15 = (uint32_t *)(IslandSecret << 0x10);
      break;
    case 0x58:
      uVar4 = IslandSecret;
LAB_8002f508:
      puVar15 = (uint32_t *)(uVar4 << 0x10);
      break;
    case 0x59:
      if ((sublevel_number != 0) || (GameState == 3)) goto switchD_8002ed90_caseD_53;
      local_28 = BirdDoor;
      BirdDoor = (uint32_t *)0x0;
      goto switchD_8002ed90_caseD_55;
    }
LAB_8002fd48:
    local_28 = puVar15;
switchD_8002ed90_caseD_55:
    evsp_ = (uint32_t **)evsp + 1;
    *evsp = (int32_t *)local_28;
    evsp = (int32_t **)evsp_;
LAB_8002fe5c:
                    /* Check if there are any value to return and terminate if there are more than
                       zero. */
    if (returnValuesCount != 0) {
      return (uint32_t)(uint32_t *)tempValue;
    }
  } while( true );
}

