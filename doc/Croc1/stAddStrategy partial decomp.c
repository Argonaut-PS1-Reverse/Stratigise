
stStrat * stAddStrategy(char *strat_name,uint32_t *base_memory,void *stream,stStrat *child_strat,
                       int param_5,int32_t *parent,stStratType type,int32_t flags)

{
  stStrat **ppsVar1;
  bool bVar2;
  char cVar3;
  byte bVar4;
  ushort uVar5;
  undefined2 uVar6;
  uint32_t *puVar7;
  int iVar8;
  int *piVar9;
  stStrat *psVar10;
  undefined *puVar11;
  int index;
  byte *strat_memory;
  char *pcVar12;
  byte *pbVar13;
  uint uVar14;
  undefined4 local_60 [14];
  stStrat *strat;
  StratBaseRef *strat_base;
  
  if (base_memory == (uint32_t *)0x0) {
    uVar14 = *(uint *)(&QuickStratTable + (uint)(byte)*strat_name * 4);
    strat_base = ::strat_base + uVar14;
    for (; iVar8 = 0, uVar14 < max_strat_index; uVar14 = uVar14 + 1) {
      iVar8 = 0;
      index = 0;
      do {
        if (strat_name[index] == '\0') break;
        if (strat_base->name[index] != strat_name[index]) {
          iVar8 = -1;
          break;
        }
        index = index + 1;
        iVar8 = iVar8 + 1;
      } while (index < 0x18);
      if (iVar8 == index) break;
      strat_base = strat_base + 1;
    }
    if (iVar8 == 0) {
      return (stStrat *)0x0;
    }
    local_60[0] = s_STRATS\_80073bc8._0_4_;
    local_60[1] = s_STRATS\_80073bc8._4_4_;
    index = 0;
    iVar8 = strlen((char *)local_60);
    pcVar12 = (char *)((int)local_60 + iVar8);
    do {
      if (strat_base->name[index + 0x18] == '\0') break;
      *pcVar12 = strat_base->name[index + 0x18];
      index = index + 1;
      pcVar12 = pcVar12 + 1;
    } while (index < 8);
    *pcVar12 = '\0';
    strcat((char *)local_60,&DAT_80073bd0);
    strat_memory = (byte *)SearchForEntry((char *)local_60);
    if (strat_memory == (byte *)0x0) {
      hang();
    }
  }
  else {
    strat_memory = (byte *)*base_memory;
    strat_base = ::strat_base;
  }
  strat = EmptyFirstStrat;
  ppsVar1 = &EmptyFirstStrat->previous;
  bVar2 = EmptyFirstStrat != (stStrat *)0x0;
  psVar10 = (stStrat *)0x0;
  EmptyFirstStrat = *ppsVar1;
  if (bVar2) {
    QuickReset(strat);
    strat->field329_0x18c = (uint32_t *)flags;
    strat->flags2 = (uint32_t *)0x1;
    if (stream != (void *)0x0) {
      puVar7 = *(uint32_t **)((int)stream + 8);
      *(uint32_t **)&strat->field_0x3a0 = puVar7;
      strat->field_0x370_ = puVar7;
      puVar7 = *(uint32_t **)((int)stream + 0xc);
      *(uint32_t **)&strat->field_0x3a4 = puVar7;
      strat->field794_0x374 = puVar7;
      puVar7 = *(uint32_t **)((int)stream + 0x10);
      *(uint32_t **)&strat->field_0x3a8 = puVar7;
      strat->field795_0x378 = puVar7;
                    /* WARNING: Load size is inaccurate */
      uVar5 = *stream;
      *(ushort *)&strat->field_0x398 = uVar5;
      strat->field790_0x368 = uVar5;
      uVar5 = *(ushort *)((int)stream + 2);
      *(ushort *)&strat->field_0x39a = uVar5;
      strat->field791_0x36a = uVar5;
      uVar6 = *(undefined2 *)((int)stream + 4);
      *(undefined2 *)&strat->field_0x39c = uVar6;
      *(undefined2 *)&strat->field792_0x36c = uVar6;
    }
    strat->name[3] = -1;
    strat->name[2] = -1;
    RotMatrixYXZ((SVECTOR *)&strat->field790_0x368,(MATRIX *)&strat->field_0x3b0);
    *(uint32_t **)&strat->field_0x3c4 = strat->field_0x370_;
    *(uint32_t **)&strat->field_0x3c8 = strat->field794_0x374;
    strat->field873_0x3cc = strat->field795_0x378;
    ModelRelight(strat);
    strat->field330_0x190 = parent;
    *(int32_t **)&strat->parent = parent;
    strat->field335_0x198 = (int)parent;
    if (parent != (int32_t *)0x0) {
      iVar8 = *parent;
      while (iVar8 != 0) {
        piVar9 = *(int **)strat->field335_0x198;
        strat->field335_0x198 = (int)piVar9;
        iVar8 = *piVar9;
      }
    }
    if (type == ST_CHILD_STRAT) {
      child_strat->field8_0x14 = strat;
      strat->flags2 = (uint32_t *)((uint)strat->flags2 | 0x4000000);
    }
    strat->someVars = (uint32_t *)child_strat;
    strat->instructionStreamMemory = strat_memory;
    if (base_memory == (uint32_t *)0x0) {
      strat->instructionStream =
           strat_memory +
           (uint)*(byte *)&strat_base->resume +
           (uint)*(byte *)((int)&strat_base->resume + 1) * 0x100;
      cVar3 = strat_base->field_0x23;
    }
    else {
      strat->instructionStream = strat_memory + *(ushort *)(base_memory + 1);
      cVar3 = *(char *)((int)base_memory + 6);
    }
    if (cVar3 == '\0') {
      *(undefined4 *)&strat->field_0xc = 0;
    }
    else {
      switch(cVar3) {
      case '\x01':
        piVar9 = &global_s;
        iVar8 = 0;
LAB_800265e0:
        if (*piVar9 != 0) goto code_r0x800265f0;
        puVar11 = &global_list_s;
        iVar8 = iVar8 << 4;
LAB_80026768:
        strat->stratGlobals = (uint32_t *)(puVar11 + iVar8);
        *(int **)&strat->field_0xc = piVar9;
        *piVar9 = *piVar9 + 1;
        break;
      case '\x02':
        piVar9 = &global_m;
        iVar8 = 0;
        do {
          if (*piVar9 == 0) {
            puVar11 = &global_list_m;
            iVar8 = iVar8 << 5;
            goto LAB_80026768;
          }
          iVar8 = iVar8 + 1;
          piVar9 = piVar9 + 1;
        } while (iVar8 < 0x1c);
        break;
      case '\x03':
        piVar9 = &global_l;
        iVar8 = 0;
        do {
          if (*piVar9 == 0) {
            puVar11 = &global_list_l;
            iVar8 = iVar8 << 6;
            goto LAB_80026768;
          }
          iVar8 = iVar8 + 1;
          piVar9 = piVar9 + 1;
        } while (iVar8 < 0xe);
        break;
      case '\x04':
        piVar9 = &global_xl;
        iVar8 = 0;
        do {
          if (*piVar9 == 0) {
            puVar11 = &global_list_xl;
            iVar8 = iVar8 << 7;
            goto LAB_80026768;
          }
          iVar8 = iVar8 + 1;
          piVar9 = piVar9 + 1;
        } while (iVar8 < 6);
        break;
      case '\x05':
        piVar9 = &global_xxl;
        iVar8 = 0;
        do {
          if (*piVar9 == 0) {
            puVar11 = &global_list_xxl;
            iVar8 = iVar8 << 8;
            goto LAB_80026768;
          }
          iVar8 = iVar8 + 1;
          piVar9 = piVar9 + 1;
        } while (iVar8 < 1);
        break;
      case '\x06':
        piVar9 = &global_sxxl;
        iVar8 = 0;
        do {
          if (*piVar9 == 0) {
            iVar8 = iVar8 * 0x300;
            puVar11 = &global_list_sxxl;
            goto LAB_80026768;
          }
          iVar8 = iVar8 + 1;
          piVar9 = piVar9 + 1;
        } while (iVar8 < 1);
      }
    }
switchD_800265cc_caseD_6:
    iVar8 = 0;
    if (param_5 == 0) {
      index = 0;
      do {
        *(undefined4 *)(&strat->field_0x154 + index) = 0;
        iVar8 = iVar8 + 1;
        index = iVar8 * 4;
      } while (iVar8 < 8);
    }
    else {
      index = 0;
      do {
        *(undefined4 *)(&strat->field_0x154 + index) = *(undefined4 *)(index + param_5);
        iVar8 = iVar8 + 1;
        index = iVar8 * 4;
      } while (iVar8 < 8);
    }
    strcpy(strat->name + 4,strat_name);
    if (type == ST_CHILD_STRAT) {
      if (strat->someVars != (uint32_t *)0x0) {
        *(undefined4 *)&strat->field_0x28 = *(undefined4 *)&child_strat->field_0x28;
        *(undefined4 *)&strat->field_0x2c = *(undefined4 *)&child_strat->field_0x2c;
        *(undefined4 *)&strat->field_0x30 = *(undefined4 *)&child_strat->field_0x30;
        *(undefined4 *)&strat->field_0x34 = *(undefined4 *)&child_strat->field_0x34;
      }
    }
    else {
      iVar8 = (uint)strat_memory[2] + (uint)strat_memory[3] * 0x100;
      pbVar13 = strat_memory + iVar8 + 2;
      for (uVar14 = (uint)strat_memory[iVar8]; uVar14 != 0; uVar14 = uVar14 - 1) {
        if (*pbVar13 == 0) {
          bVar4 = pbVar13[1];
          pbVar13 = pbVar13 + 2;
          iVar8 = 0;
          if (bVar4 != 0) {
            do {
              *(byte *)((int)local_60 + iVar8) = *pbVar13;
              iVar8 = iVar8 + 1;
              pbVar13 = pbVar13 + 1;
            } while (iVar8 < (int)(uint)bVar4);
          }
          *(undefined *)((int)local_60 + iVar8) = 0;
          iVar8 = 0;
          index = 0;
          do {
            iVar8 = iVar8 + 1;
            if (*(int *)((int)&DAT_8007aa04 + index) == 0) {
              strcpy(&DAT_8007aa08 + index,(char *)local_60);
              *(stStrat **)((int)&extern_area + index) = strat;
              *(int *)((int)&DAT_8007aa04 + index) = *(int *)((int)&DAT_8007aa04 + index) + 1;
              break;
            }
            index = iVar8 * 0x20;
          } while (iVar8 < 0x20);
        }
        else {
          pbVar13 = pbVar13 + 3;
        }
      }
      if (type == ST_BIRTH_STRAT) {
        stResolveReferences();
      }
    }
    strat->previous = FirstStrat;
    if (FirstStrat != (stStrat *)0x0) {
      FirstStrat->next = strat;
    }
    FirstStrat = strat;
    psVar10 = strat;
    if (type == ST_PLAYER_STRAT) {
      PlayerStrat = strat;
      strat->flags2 = (uint32_t *)((uint)strat->flags2 | 0x2000800);
    }
  }
  return psVar10;
code_r0x800265f0:
  iVar8 = iVar8 + 1;
  piVar9 = piVar9 + 1;
  if (0x3b < iVar8) goto switchD_800265cc_caseD_6;
  goto LAB_800265e0;
}

