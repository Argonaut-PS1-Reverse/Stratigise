#!/usr/bin/env python
"""
Compare two compiled strats and check for difference
"""

import sys
from stratigise.common import BinaryReadStream

def check_diff(strat1_path, strat2_path):
    strat1 = BinaryReadStream(strat1_path)
    strat2 = BinaryReadStream(strat2_path)

    size1 = strat1.readInt32LE()
    entry1 = strat1.readInt16LE()
    axx_start1 = strat1.readInt16LE() + 4
	
    size2 = strat2.readInt32LE()
    entry2 = strat2.readInt16LE()
    axx_start2 = strat2.readInt16LE() + 4

    if entry1 != entry2:
        print(f"Entry mismatch: {hex(entry1)} != {hex(entry2)}")

    axx1, str_locs1, preloads1 = read_axx(strat1, axx_start1)
    axx2, str_locs2, preloads2 = read_axx(strat2, axx_start2)

    if preloads1 != preloads2:
        print("Preloads mismatch:")
        print("1: ", preloads1)
        print("2: ", preloads2)

    # There is one case when one string is missing from the initial strat
    if len(axx1) != len(axx2) and len(axx1) + 1 != len(axx2):
        print(f"AXX entry counts mismatch: {len(axx1)} != {len(axx2)}")
        print("AXX 1: ", axx1)
        print("AXX 2: ", axx2)
    else:
        for i in range(len(axx1)):
            if axx1[i]["kind"] != axx2[i]["kind"]:
                print(f"AXX entries mismatch at index {i}: {axx1[i]} != {axx2[i]}")
                print("AXX 1: ", axx1)
                print("AXX 2: ", axx2)
                break
    
    strat1.setPos(8)
    strat2.setPos(8)

    prev = []

    while True:
        pos1 = strat1.getPos()
        pos2 = strat2.getPos()

        if pos1 in str_locs1 and pos2 in str_locs2:
            string1 = read_string(strat1)
            string2 = read_string(strat2)

            if string1 != string2:
                print(f"Code mismatch: string `{string1}` vs string `{string2}` at {hex(pos1)} - {hex(pos2)}")
                break

        elif pos1 not in str_locs1 and pos2 not in str_locs2:
            byte1 = strat1.readInt8()
            byte2 = strat2.readInt8()

            if byte1 != byte2:
                # Handling special cases

                # Spawn* + old-fashioned 32-bit placeholder vk. 64-bit one
                if len(prev) >= 5 and prev[-5] in [0x30, 0x77, 0xb1] and prev[-4:] == [0, 0, 0, 0]:
                    bytes = strat2.readBytes(3)
                    if byte2 == 0 and bytes == b"\x00\x00\x00":
                        strat1.setPos(strat1.getPos() - 1)
                        continue

                    strat2.setPos(strat2.getPos() - 3)

                # CreateTrigger 1 Label + 4 extra zero bytes
                if len(prev) >= 4 and prev[-4] == 0x31 and prev[-3] == 1:
                    bytes = strat1.readBytes(3)
                    if byte1 == 0 and bytes == b"\x00\x00\x00":
                        strat2.setPos(strat2.getPos() - 1)
                        continue

                    strat1.setPos(strat1.getPos() - 3)

                # Wrong opcode for PushPGVar
                if byte1 == 0x1b and byte2 == 0x1:
                    continue

                # Maybe these are labels - let's check what they're pointing at is
                byte12 = strat1.readInt8()
                byte22 = strat2.readInt8()
                label1 = byte1 + 256 * byte12
                label2 = byte2 + 256 * byte22

                op1 = read_byte_at(strat1, strat1.getPos() + label1)
                op2 = read_byte_at(strat2, strat2.getPos() + label2)

                if op1 is not None and op1 == op2:
                    prev.append(byte1)
                    prev.append(byte12)
                    continue

                op1 = read_byte_at(strat1, label1 + 4)
                op2 = read_byte_at(strat2, label2 + 4)

                if op1 is not None and op1 == op2:
                    prev.append(byte1)
                    prev.append(byte12)
                    continue

                strat1.setPos(strat1.getPos() - 1)
                strat2.setPos(strat2.getPos() - 1)

                print(f"Code mismatch: byte {hex(byte1)} vs byte {hex(byte2)} at {hex(pos1)} - {hex(pos2)}")
                break

            if byte1 == 0x3b:
                break

            prev.append(byte1)

        elif pos1 in str_locs1:
            print(f"Code mismatch: string `{read_string(strat1)}` vs byte {hex(strat2.readInt8())} at {hex(pos1)} - {hex(pos2)}")
            break

        else:
            string2 = read_string(strat2)

            sz = strat1.readInt8()

            # Case when string isn't presented in original AXX
            if sz == len(string2) or sz == len(string2) + 1:
                strat1.setPos(strat1.getPos() - 1)
                string1 = read_string(strat1)

                if string1 != string2:
                    print(f"Code mismatch: string `{string1}` vs string `{string2}` at {hex(pos1)} - {hex(pos2)}")
                    break
            else:
                print(f"Code mismatch: byte {hex(sz)} vs string `{string2}` at {hex(pos1)} - {hex(pos2)}")
                break

def read_axx(strat, start):
    strat.setPos(start)

    count = strat.readInt16LE()
    axx = []
    str_locs = []
    preloads = []

    for i in range(count):
        kind = strat.readInt8()
        if kind == 0:
            string = read_string(strat)
            if string not in preloads:
                preloads.append(string)
        else:
            location = strat.readInt16LE()
            axx.append({"kind": kind, "location": location})
            str_locs.append(location + 4)

    return axx, str_locs, sorted(preloads)

def read_byte_at(strat, pos):
    if pos < 0 or pos >= strat.getLength():
        return None

    cur_pos = strat.getPos()
    strat.setPos(pos)

    byte = strat.readInt8()

    strat.setPos(cur_pos)

    return byte

def read_string(strat):
    sz = strat.readInt8()
    if sz is None:
        return "<EOF>"
    elif sz > 0:
        return strat.readBytes(sz).decode('latin-1').replace('\x00', '')
    else:
        return ""

if (__name__ == "__main__"):
    if (len(sys.argv) == 3):
        check_diff(sys.argv[1], sys.argv[2])
    else:
        print(f"Usage: {sys.argv[0]} <strat file> <strat file>")
