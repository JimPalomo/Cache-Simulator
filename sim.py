#################################################
# ECE 366 Project 4                             #
# Charlie Schafer, Maxwell Thimmig, Jim Palomo  #
#################################################

import os.path as Path      # used to check for invalid file
import copy                 # used to create hard copies of instances

## General Functions ********************************************************************

# twoscomp: 2's Complement [return binary (string)]    (string -> string)
# Input: s = binary (string)
# Return: 2's complement binary (string)
def twoscomp(s):
    for j in reversed(range(len(s))):
        if s[j] == '1':
            break

    t = ""
    for i in range(0, j, 1):        # flip everything
        t += str(1-int(s[i]))

    for i in range(j, len(s), 1):   # until the first 1 from the right
        t += s[i]

    return t                        # return 2's complement binary (string)
    
# twoscomp_dec: 2's Complement [return decimal (int)]     [use for sign extend]
# Input: b = binary (string)
# Return: 2's complement decimal (int)
def twoscomp_dec(b):

    l = len(b)          # length of bit provided

    x = b[:1].zfill(l)  # save the first bit and fill with 0's until original length
    x = x[::-1]         # flip binary

    x = int(x, 2) * -1  # value of binary (unsigned: 10000..0) * -1

    y = int(b[1:], 2)   # value of binary without the first bit

    x += y              # add up differing values

    return x            # return 2's complement decimal (int)

# bin_to_dec: convert binary (string) to decimal (int)  [use for sign extend]
# Input: binary (string)
# Return: Decimal (int)
def bin_to_dec(b):
    if(b[0]=="0"):
        return int(b, base=2)
    else:        
        return twoscomp_dec(b)

# zero_extend: zero extend / unsigned operation (for specific operations)
# Input: binary (string)
# Return: decimal (int)
def zero_extend(b):
    return int(b, base=2)   # given a binary string, get unsigned decimal

# itosbin: convert decimal/integer (int) to binary (string)
# Input: i = decimal/integer (int) | n = amount of bits input (int)
# Return: (signed) binary string
def itosbin(i, n):
    s = ""
    if i >= 0:
        s = bin(i)[2:].zfill(n)
    else:
        s = bin(0-i)[2:].zfill(n)
        s = twoscomp(s)

    return s

# hex_to_bin: convert hex (string) to binary (string)
# Input: line = hex (string)
# Return: unsigned binary (string)
def hex_to_bin(line):
    h = line.replace("\n", "")
    i = int(h, base=16)
    b = bin(i)
    b = b[2:].zfill(32)
    return b

# neg_int_to_hex:
# Input: x = input integer (int)
# Return: x = 2's complemented hexadecimal (string)
def neg_int_to_hex(x):
    x = bin(x & 0xffffffff)[2:]
    x = hex(int(x,2))[2:].zfill(8)
    x = "0x" + x

    return x

# int_to_hex: convert an decimal (int) to hex (string)
# Input: x = input integer (int)
# Return: hex (string)
def int_to_hex(x):
    if (x < 0):
        x = neg_int_to_hex(x)
    else:
        x = "0x" + str(hex(x))[2:].zfill(8)

    return x

# neg_int_to_hex2: convert negative integers to hex with zfill of 8 bits (for DM)
# Input: x = input integer (int)
# Return: x = 2's complemented hexadecimal (string)
def neg_int_to_hex2(x):
    x = bin(x & 0xfff)[2:]
    x = hex(int(x,2))[2:]
    x = "0x" + x

    return x

# neg_int_to_hex2: convert negative integers to hex with zfill of 8 bits (for cache)
# Input: x = input integer (int)
# Return: hex (string)
def int_to_hex2(x):
    if (x < 0):
        x = neg_int_to_hex2(x)
    else:
        x = "0x" + str(hex(x))[2:]

    return x


## Processing Functions *****************************************************************

# processR: process R-type instructions from machine code (string) to hex (string)
# Input: b = 32 bit binary instruction 
# Return: MIPS equivalent instruction in hex (string)
def processR(b): 
    b_op = b[0:6]
    b_rs = b[6:11]
    b_rt = b[11:16]
    b_rd = b[16:21]
    b_sa = b[21:26]
    b_fn = b[26:32]

    asm = ""

    if (b_fn == '100000'):      # ADD
        rs = int((b_rs), base=2)
        rt = int((b_rt), base=2)
        rd = int((b_rd), base=2)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        rd = "$" + str(rd)

        asm = "add " + rd + ", " + rs + ", " + rt 

    elif (b_fn == '100010'):    # SUB
        rs = int((b_rs), base=2)
        rt = int((b_rt), base=2)
        rd = int((b_rd), base=2)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        rd = "$" + str(rd)

        asm = "sub " + rd + ", " + rs + ", " + rt 

    elif (b_fn == '101010'):    # SLT
        rs = int((b_rs), base=2)
        rt = int((b_rt), base=2)
        rd = int((b_rd), base=2)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        rd = "$" + str(rd)

        asm = "slt " + rd + ", " + rs + ", " + rt 

    elif (b_fn == '000000'):    # SLL
        rt = int((b_rt), base=2)
        rd = int((b_rd), base=2)
        sa = int((b_sa), base=2)

        rt = "$" + str(rt)
        rd = "$" + str(rd)
        sa = str(sa)

        asm = "sll " + rd + ", " + rt + ", " + sa

    elif (b_fn == '100110'):    # XOR
        rs = int((b_rs), base=2)
        rt = int((b_rt), base=2)
        rd = int((b_rd), base=2)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        rd = "$" + str(rd)

        asm = "xor " + rd + ", " + rs + ", " + rt 

    elif (b_fn == '000010'):    # SRL
        rt = int((b_rt), base=2)
        rd = int((b_rd), base=2)
        sa = int((b_sa), base=2)

        rt = "$" + str(rt)
        rd = "$" + str(rd)
        sa = str(sa)

        asm = "srl " + rd + ", " + rt + ", " + sa

    elif (b_fn == '000110'):    # SRLV
        rs = int((b_rs), base=2)
        rt = int((b_rt), base=2)
        rd = int((b_rd), base=2)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        rd = "$" + str(rd)

        asm = "srlv " + rd + ", " + rt + ", " + rs
    
    elif (b_fn == '100001'):    # ADDU
        rs = int((b_rs), base=2)
        rt = int((b_rt), base=2)
        rd = int((b_rd), base=2)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        rd = "$" + str(rd)

        asm = "srlv " + rd + ", " + rs + ", " + rt

    elif (b_fn == '010000'):    # MFHI
        rd = int((b_rd), base=2)        
        rd = "$" + str(rd)

        asm = "mfhi " + rd

    elif(b_fn == '010010'):     # MFLO  
        rd = int((b_rd), base=2)        
        rd = "$" + str(rd)

        asm = "mflo " + rd

    else:
        print (f'NO idea about op = {b_fn}')
    return asm
    
# processI: process I-type instructions from machine code (string) to hex (string)
# Input: b = 32 bit binary instruction 
# Return: MIPS equivalent instruction in hex (string)
def processI(b):
    b_op = b[0:6]
    b_rs = b[6:11]
    b_rt = b[11:16]
    b_imm = b[16:]

    asm = ""

    if(b_op == '001000'):       # ADDI
        rs = int(b_rs, base=2)
        rt = int(b_rt, base=2)
        imm = bin_to_dec(b_imm)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        imm = str(imm)

        asm = "addi "+ rt + ", " + rs + ", " + imm

    elif (b_op == '001100'):    # ANDI
        rs = int(b_rs, base=2)
        rt = int(b_rt, base=2)
        imm = zero_extend(b_imm)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        imm = str(imm)

        asm = "andi "+ rt + ", " + rs + ", " + imm

    elif (b_op == '100011'):    # LW
        rs = int(b_rs, base=2)
        rt = int(b_rt, base=2)
        imm = bin_to_dec(b_imm)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        imm = str(imm)

        asm = "lw "+ rt + ", " + imm + "(" + rs + ")"

    elif (b_op == '101011'):    # SW
        rs = int(b_rs, base=2)
        rt = int(b_rt, base=2)
        imm = bin_to_dec(b_imm)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        imm = str(imm)

        asm = "sw "+ rt + ", " + imm + "(" + rs + ")"

    elif (b_op == '101001'):    # SH
        rs = int(b_rs, base=2)
        rt = int(b_rt, base=2)
        imm = bin_to_dec(b_imm)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        imm = str(imm)

        asm = "sh "+ rt + ", " + imm + "(" + rs + ")"

    elif (b_op == '100001'):    # LH
        rs = int(b_rs, base=2)
        rt = int(b_rt, base=2)
        imm = bin_to_dec(b_imm)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        imm = str(imm)

        asm = "lh "+ rt + ", " + imm + "(" + rs + ")"

    elif (b_op == '000100'):    # BEQ
        rs = int(b_rs, base=2)
        rt = int(b_rt, base=2)
        imm = bin_to_dec(b_imm)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        imm = str(imm)

        asm = "beq "+ rs + ", " + rt + ", " + imm

    elif (b_op == '000101'):    # BNE
        rs = int(b_rs, base=2)
        rt = int(b_rt, base=2)
        imm = bin_to_dec(b_imm)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        imm = str(imm)

        asm = "bne "+ rs + ", " + rt + ", " + imm

    elif (b_op == '001101'):    # ORI
        rs = int(b_rs, base=2)
        rt = int(b_rt, base=2)
        imm = zero_extend(b_imm)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        imm = str(imm)

        asm = "ori "+ rt + ", " + rs + ", " + imm    

    elif (b_op == '001110'):    # XORI
        rs = int(b_rs, base=2)
        rt = int(b_rt, base=2)
        imm = zero_extend(b_imm)

        rs = "$" + str(rs)
        rt = "$" + str(rt)
        imm = str(imm)

        asm = "xori "+ rt + ", " + rs + ", " + imm                

    elif (b_op == '001111'):    # LUI
        rt = int(b_rt, base=2)
        imm = bin_to_dec(b_imm)
        
        rt = "$" + str(rt)
        imm = str(imm)

        asm = "lui "+ rt + ", " + imm
    
    elif (b_op == '111111'):    # FW [Special Instruction]
        rs = int(b_rs, base=2)
        rt = int(b_rt, base=2)

        rs = "$" + str(rs)
        rt = "$" + str(rt)

        asm = "fw "+ rt + ", " + rs 

    else:
        print (f'NO idea about op = {b_op}')
    return asm

# processJ: process J-type instructions from machine code (string) to hex (string)
# Input: b = 32 bit binary instruction 
# Return: MIPS equivalent instruction in hex (string)
def processJ(b): 
    b_op = b[0:6]
    b_imm = b[6:]

    asm = ""
    
    imm = bin_to_dec(b_imm)
    imm = str(imm)
    asm = "j " + imm
    
    return asm

# processMUL: process MUL instruction from machine code (string) to hex (string) [treated differently than MULT / NOT R, I, J Type]
# Input: b = 32 bit binary instruction 
# Return: MIPS equivalent instruction in hex (string)
def processMUL(b):
    b_rs = b[6:11]
    b_rt = b[11:16]
    b_rd = b[16:21]
    b_sa = b[21:26]
    b_fn = b[26:32]

    asm = ""      
    
    rs = int((b_rs), base=2)
    rt = int((b_rt), base=2)
    rd = int((b_rd), base=2)
    rs = "$" + str(rs)
    rt = "$" + str(rt)
    rd = "$" + str(rd)

    asm = "mul " + rd + ", " + rs + ", " + rt 

    return asm  

# process: determine whether the process provided by machine code (string) is MUL, R, I, or J type.
# Input: b = 32 bit binary instruction 
# Return: MIPS equivalent instruction in hex (string) after determining instruction type
def process(b):
    b_op = b[0:6]
    b_fn = b[26:32]

    if (b_op == '011100' and b_fn == '000010'):  # MUL (special case due to MARS simulator, non-psuedo)
        return processMUL(b)
    elif (b_op == '000000'):        # R-type
        return processR(b)
    elif (b_op == '000010'):        # J-type
        return processJ(b)
    else:                           # I-type
        return processI(b)

# disassemble: disassembles 32 bit instructions from input .txt file and appends spliced instruction to a list
# Input: input_file = input .txt file (of 32-bit machine code) | asm_instr = output .txt file (hex equivalent of machine code) 
# Return: list (instr) of all instructions from .txt file
def disassemble(input_file, asm_instr):
    instr = []    # create empty list of user inputs

    ''' reasons for list: 
            1. able to append at the end of list to KEEP ORDER
            2. mutable (change elements in list if necessary)
            3. creating a list data structure using string methods (replace, split)
    '''

    line_count = 0

    # convert 32 bit machine code from input and write to output file
    for line in input_file:
        line_count += 1
        bin_str = hex_to_bin(line)
        asmline = process(bin_str) 
        output_file.write(asmline + '\n')

        # splice asmline using string methods and append spliced instruction to list
        asm_instr.append(asmline)                   # save asmline into asm_instr
        asmline = asmline.replace("j", "j,")        # remove j and replace w/ "j,"
        asmline = asmline.replace(", $", ",")       # remove middle $ and replace w/ ","
        asmline = asmline.replace(" $", ",")        # remove first $ and replace w/ ","
        asmline = asmline.replace(")", ",")         # remove ")" and replace w/ ","        
        asmline = asmline.replace(" ", "")          # remove extra spacing
        asmline = asmline.replace("($", ",")        # remove "($" and replace w/ ","
        asmline = asmline.split(",")                # split by "," and generate a list
        instr.append(asmline)                       # append to another list which results in a list-list data structure

    output_file.write("\n") # newline in output file to show finished
    input_file.close()      # close input file since we no longer need it

    return instr          # return list of listed spliced instructions (list-list) to main

## MIPS Specialized Functions ***********************************************************

# and32: perform logic AND on two 32 bit binary (strings)
# Input: x, y = 32-bit binary (strings)
# Return: ANDed binary string
def and32(x, y):
    s = ""
    for i in range(32):
        if (x[i] == '1') and (y[i] == '1'):
            s += '1'
        else:
            s += '0'
    
    return s

# or32: perform logic OR on two 32 bit binary (strings)
# Input: x, y = 32-bit binary (strings)
# Return: ORed binary string
def or32(x, y):
    s = ""
    for i in range(32):
        if (x[i] == '1') or (y[i] == '1'):
            s += '1'
        else:
            s += '0'
    
    return s

# xor32: perform logic XOR on two 32 bit binary (strings)
# Input: x, y = 32-bit binary (strings)
# Return: XORed binary string
def xor32(x, y):
    s = ""
    for i in range(32):
        if x[i] == y[i]:
            s += '0'
        else:
            s += '1'
    
    return s

# lui32: load upper immediate
# x = integer (string) | return = lui of x (int)

# lui32: load upper immediate of 
# Input: x = decimal (string)
# Return: decimal (int)
def lui32(x):
    x = int(x) << 16
    x = itosbin(x, 32)
    x = bin_to_dec(x)
    return x

# j_pc_count: perform PC calculation for j jump instruction
# Input: pc = current value of PC before jump | addr = address from j-type 32 bit instruction
# Return: new value of PC (int)
def j_pc_count(pc, addr):
    # Eqn: pc = (pc & 0xf0000000) | (addr << 2)

    a = itosbin(pc, 32)
    b = '11110000000000000000000000000000'  # 0xf0000000
    c = and32(a,b)
    
    d = itosbin(addr << 2, 32)
    
    z = or32(c, d)

    z = bin_to_dec(z)

    return z

# accessDM: hash function for accessing data memory [O(1) access]
# Input: s = hex or integer/decimal (string)
# Return: data memory location of the data memory array (int)
def accessDM(s):
    if (s[2:] == "0x"):
        s = int(s, base=16)
    else:
        s = int(s)

    s = int((s - 0x2000) / 4)
    
    return s

# findWidth: special instruction used to find the width of a 32-bit binary code
# Input: s = decimal (string)
# Return: width of the specific decimal translated in 32-bit binary 
def findWidth(s):               # take in decimal string 
    b = int(s)                  # convert string decimal to int decimal
    b = itosbin(b, 32)          # convert integer to binary
    return len(b.strip("0"))    # strip surrounding zeros from 1...1 & return length of remaining bits

# mul: multiplication instruction (non R, J, I type) but special non-psuedo instruction
# Input: x, y = decimal values (int)
# Output: decimal pair (int, int) (hi 32bit, lo 32bit)
def mul(x, y):
    product = x * y
    z = itosbin(product, 64)
    mhi, mlo = z[:len(z)//2], z[len(z)//2:]

    return bin_to_dec(mhi), bin_to_dec(mlo)

# srl: bit shift right by n amounts
# Input: b = binary (string) | n = amount of shifts (integer) 
# Output: bit shifted decimal (integer)
def srl(b, n):
    r = 32 - n
    b = b[0:r].zfill(32)

    return bin_to_dec(b)

# sll: bit shift left by n amounts
# Input: b = binary (string) | n = amount of shifts (integer) 
# Output: bit shifted decimal (integer)
def sll(b, n):
    b = b[n:32].ljust(32, '0')

    return bin_to_dec(b)

## Output Functions *********************************************************************
# outputRegisters: output all 32 registers + pc, hi, lo 
# Input: reg = array holding register data | pc, hi, lo = special registers
# Return: outputted registers via console & output file
def outputRegisters(reg, pc, hi, lo, hexValue):
    pReg = "Register"
    pVal = "Value"
    print(f"{pReg:<15}{pVal:^12}")

    # output header output file
    row_item = [pReg, pVal]
    output = '{:<15}{:^12}'.format(row_item[0], row_item[1])
    output_file.write(output + "\n")

    # output 32 registers from reg array 
    for i in range(len(reg)):
        pReg = "$" + str(i)
        if (hexValue == 0):
            pVal = str(reg[i])
        else:
            pVal = int_to_hex(reg[i])
        print(f"{pReg:<15}{pVal:>12}")
        
        # output to txt file
        row_item = [pReg, pVal]
        output = '{:<15}{:>12}'.format(row_item[0], row_item[1])
        output_file.write(output + "\n")        

    # output special registers
    pReg = "pc"
    if (hexValue == 0):
        pVal = str(pc)
    else:
        pVal = int_to_hex(pc)  

    print(f"{pReg:<15}{pVal:>12}")

    row_item = [pReg, pVal] # output to txt file
    output = '{:<15}{:>12}'.format(row_item[0], row_item[1])
    output_file.write(output + "\n")     

    pReg = "hi"
    if (hexValue == 0):
        pVal = str(hi)
    else:
        pVal = int_to_hex(hi)    
    print(f"{pReg:<15}{pVal:>12}")

    row_item = [pReg, pVal] # output to txt file
    output = '{:<15}{:>12}'.format(row_item[0], row_item[1])
    output_file.write(output + "\n") 

    pReg = "lo"
    if (hexValue == 0):
        pVal = str(lo)
    else:
        pVal = int_to_hex(lo) 
    print(f"{pReg:<15}{pVal:>12}")

    row_item = [pReg, pVal] # output to txt file
    output = '{:<15}{:>12}'.format(row_item[0], row_item[1])
    output_file.write(output + "\n" + "\n") 
    print("\n")

# outputDataMem: output data memory array in similar format as MARS
# Input: mem = data memory array | hex_start = starting memory address | hex_end = ending memory address 
#        address = user selected hex or decimal address output |  value = user selected hex or decimal value output
# Output: outputted data memory array in console and output file
def outputDataMem(mem, hex_start, hex_end, address, value):
    addr = v1 = v2 = v3 = v4 = v5 = v6 = v7 = v8 = ""

    # headers
    if (address == 0):      # [decimal address]
        addr = "Address"
        v1 = "Value (+0)"
        v2 = "Value (+4)"
        v3 = "Value (+8)"
        v4 = "Value (+12)"
        v5 = "Value (+16)"
        v6 = "Value (+20)"
        v7 = "Value (+24)"
        v8 = "Value (+28)"

        # output header to output .txt file [decimal]
        row_item = [addr, v1, v2, v3, v4, v5, v6, v7, v8]
        output = '|{:>10}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|'.format(row_item[0], row_item[1], row_item[2], row_item[3], 
            row_item[4], row_item[5], row_item[6], row_item[7], row_item[8])
        output_file.write(output + "\n")

    else:                   # [hexadecimal address]
        addr = "Address"
        v1 = "Value (+0)"
        v2 = "Value (+4)"
        v3 = "Value (+8)"
        v4 = "Value (+c)"
        v5 = "Value (+10)"
        v6 = "Value (+14)"
        v7 = "Value (+18)"
        v8 = "Value (+1c)"

        # output header to output .txt file [hex]
        row_item = [addr, v1, v2, v3, v4, v5, v6, v7, v8]
        output = '|{:^10}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|'.format(row_item[0], row_item[1], row_item[2], row_item[3], 
            row_item[4], row_item[5], row_item[6], row_item[7], row_item[8])
        output_file.write(output + "\n")

    print(f"|{addr:>15}|{v1:>15}|{v2:>15}|{v3:>15}|{v4:>15}|{v5:>15}|{v6:>15}|{v7:>15}|{v8:>15}|")

    j = 0

    if (value == 0):        # data memory [decimal values]
        for i in range(hex_start, hex_end, 4):
            if (j % 8 == 0):
                if (address == 1):
                    addr = "0x" + str(hex(j*4 + 0x2000))[2:].zfill(8)
                else:
                    addr = str(j*4 + 0x2000)

                if j < len(mem):
                    v1 = str(mem[j]) 
                else:
                    v1 = 0
    
                if j+1 < len(mem):
                    v2 = str(mem[j+1]) 
                else:
                    v2 = 0
    
                if j+2 < len(mem):
                    v3 = str(mem[j+2]) 
                else:
                    v3 = 0
    
                if j+3 < len(mem):
                    v4 = str(mem[j+3]) 
                else:
                    v4 = 0
    
                if j+4 < len(mem):
                    v5 = str(mem[j+4]) 
                else:
                    v5 = 0
    
                if j+5 < len(mem):
                    v6 = str(mem[j+5]) 
                else:
                    v6 = 0
    
                if j+6 < len(mem):
                    v7 = str(mem[j+6]) 
                else:
                    v7 = 0
    
                if j+7 < len(mem):
                    v8 = str(mem[j+7]) 
                else:
                    v8 = 0
    
                print(f"|{addr:>15}|{v1:>15}|{v2:>15}|{v3:>15}|{v4:>15}|{v5:>15}|{v6:>15}|{v7:>15}|{v8:>15}|")
                row_item = [addr, v1, v2, v3, v4, v5, v6, v7, v8]
                output = '|{:>10}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|'.format(row_item[0], row_item[1], row_item[2], row_item[3], 
                    row_item[4], row_item[5], row_item[6], row_item[7], row_item[8])
                output_file.write(output + "\n")    

            j += 1

    else:        # data memory [hexadecimal values]
        for i in range(hex_start, hex_end, 4):
            if (j % 8 == 0):
                if (address == 1):
                    addr = "0x" + str(hex(j*4 + 0x2000))[2:].zfill(8)
                else:
                    addr = str(j*4 + 0x2000)

                if j < len(mem):
                    if (mem[j] < 0):
                        v1 = neg_int_to_hex(mem[j])
                    else:
                        v1 = "0x" + str(hex(mem[j]))[2:].zfill(8)
                else:
                    v1 = "0x" + "".zfill(8)
    
                if j+1 < len(mem):
                    if (mem[j+1] < 0):
                        v2 = neg_int_to_hex(mem[j+1])
                    else:
                        v2 = "0x" + str(hex(mem[j+1]))[2:].zfill(8)
                else:
                    v2 = "0x" + "".zfill(8)
    
                if j+2 < len(mem):
                    if (mem[j+2] < 0):
                        v3 = neg_int_to_hex(mem[j+2])
                    else:
                        v3 = "0x" + str(hex(mem[j+2]))[2:].zfill(8)
                else:
                    v3 = "0x" + "".zfill(8)
    
                if j+3 < len(mem):
                    if (mem[j+3] < 0):
                        v4 = neg_int_to_hex(mem[j+3])
                    else:
                        v4 = "0x" + str(hex(mem[j+3]))[2:].zfill(8)                
                else:
                    v4 = "0x" + "".zfill(8)
    
                if j+4 < len(mem):
                    if (mem[j+4] < 0):
                        v5 = neg_int_to_hex(mem[j+4])
                    else:
                        v5 = "0x" + str(hex(mem[j+4]))[2:].zfill(8)
                else:
                    v5 = "0x" + "".zfill(8)
    
                if j+5 < len(mem):
                    if (mem[j+5] < 0):
                        v6 = neg_int_to_hex(mem[j+5])
                    else:
                        v6 = "0x" + str(hex(mem[j+5]))[2:].zfill(8)
                else:
                    v6 = "0x" + "".zfill(8)
    
                if j+6 < len(mem):
                    if (mem[j+6] < 0):
                        v7 = neg_int_to_hex(mem[j+6])
                    else:
                        v7 = "0x" + str(hex(mem[j+6]))[2:].zfill(8)
                else:
                    v7 = "0x" + "".zfill(8)
                    
    
                if j+7 < len(mem):
                    if (mem[j+7] < 0):
                        v8 = neg_int_to_hex(mem[j+7])
                    else:
                        v8 = "0x" + str(hex(mem[j+7]))[2:].zfill(8)
                else:
                    v8 = "0x" + "".zfill(8)
    
                print(f"|{addr:>15}|{v1:>15}|{v2:>15}|{v3:>15}|{v4:>15}|{v5:>15}|{v6:>15}|{v7:>15}|{v8:>15}|")
                row_item = [addr, v1, v2, v3, v4, v5, v6, v7, v8]
                output = '|{:<10}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|'.format(row_item[0], row_item[1], row_item[2], row_item[3], 
                    row_item[4], row_item[5], row_item[6], row_item[7], row_item[8])
                output_file.write(output + "\n")      



            j += 1            
    print("\n")

# outputInstrStats: output instruction statistics (ALU, Jump, branch, memory, other)
# Input: total, alu, jump, branch, memory, other = current values that are held for each count variable
# Return: output instruction statistics on console and output .txt file 
def outputInstrStats(total, alu, jump, branch, memory, other):
    print("Instruction Statistics, Version 1.0")
    output_file.write("\n\nInstruction Statistics, Version 1.0" + "\n")

    print(f"Total:\t{total}\n")
    output_file.write(f"Total:\t{total}\n\n")

    titles = ["ALU:", "Jump:", "Branch:", "Memory:", "Other:"]
    values = [alu, jump, branch, memory, other]
    percentages = [(alu/total)*100, (jump/total)*100, (branch/total)*100, (memory/total)*100, (other/total)*100]
    i = 0
    while i < len(titles):
        print(f"{titles[i]:<8}{values[i]:<8}{percentages[i]:.0f}%")
        output_file.write(f"{titles[i]:<8}{values[i]:<8}{percentages[i]:.0f}%" + "\n")

        i += 1

def outputCache(address, SBCache, DMCache, FACache, SACache):
    # results from cache configuration
    cc = 0  # [hit/miss, tag, idx, ibo, setNum, valid, LRU/before]
    hit = 0

    if (userInput == 0):
        cc = checkSBCache(address, SBCache)
    elif (userInput == 1):
        cc = checkDMCache(mem, DMCache, address)
    elif (userInput == 2):
        cc = checkFACache(FACache, address, mem, 16, cur[0], cur[1])
    else: # 3
        cc = checkSACache(mem, SACache, address)

    # run cache configuration based on userInput 
    if (cc[0] == 1):
        hit = 1
        pAttempt = "hit"

    else:
        hit = 0
        pAttempt = "miss"

    pTag = "Tag"
    pSet = "Set"
    pIbo = "IBO"

    # output cache information:
    print("_" * 90)

    if (userInput == 1 or userInput == 3):  # DM & SA  
        # header
        print(f"                {pTag:^40}  {pSet:^12}  {pIbo:^11} ") if userInput == 1 else print(f"                {pTag:^40}  {pSet:^15}  {pIbo:^15} ")
     
        # mem addr breakdown            
        print(f" ({cacheAccess}) Memory Address: {cc[1]:^26} ({hex(int(cc[1], 2))}) | {cc[2]:^4} ({hex(int(cc[2], 2)):^5}) | {cc[3]:^5} ({hex(int(cc[3], 2)):^5})")
        
        print(f"\tw/ Block # -> {hex(bin_to_dec(str(cc[1] + cc[2])))}") # block # (tag & set)
        
    elif (userInput == 2):      # FA
        print(f"                {pTag:^41}  {pIbo:^12} ")               # header
     
        # mem addr breakdown
        print(f" ({cacheAccess}) Memory Address: {cc[1]:^26} ({str(hex(int(cc[1], 2)))}) | {cc[3]:^3} ({hex(int(cc[3], 2)):^3})")
            
        print(f"\tw/ Block # -> {hex(bin_to_dec(str(cc[1])))}")         # block # (tag & set)

    else:                       # Simple Cache
        print(f"                {pTag:^41}  {pIbo:^12} ")               # header
     
        # mem addr breakdown
        print(f" ({cacheAccess}) Memory Address: {cc[1]:^26} ({hex(int(cc[1], 2))}) | {cc[3]:^5} ({hex(int(cc[3], 2)):^5})")
        
        print(f"\tw/ Block # -> {hex(bin_to_dec(str(cc[1])))}")         # block # (tag & set)
        
    print("-" * 90)

    # cache detailed info:
    print(f"Cache Info: ")
    if (userInput == 0):    # Simple Cache
        # target
        print(f"\t \033[4mTarget:\033[0m")
        print(f"\t set/way  : s0w0")
        print(f"\t tag bits : {cc[1]} ({hex(int(cc[1], 2))})\n")

        # before
        print(f"\t \033[4mIn Cache:\033[0m")
        print(f"\t set/way  : s0w0")
            
        if (cc[6][0] == ""): # if no tag bits
            print(f"\t tag bits : None, empty")            
        else:                # tag bits 
            print(f"\t tag bits : {cc[6][0]} ({hex(int(cc[6][0], 2))})")  
            
        print(f"\t valid bit: {cc[6][2]}")

        # result
        print(f"\n\t \033[4m\033[1mresult  = {pAttempt.upper()}\033[0m")
            
        if (pAttempt == "hit"):
            print(f"\t offset   : {cc[3]} ({hex(int(cc[3], 2))})")
        else:
            print(f"\t block #  : {hex(bin_to_dec(str(cc[1])))}")         # block # (tag & set)
            print(f"\t set/way  : s0w0")
            print(f"\t valid bit: 1")

            if (cc[6][0] == ""):
                print(f"\n\t Miss due to empty block, load in {hex(int(cc[1], 2))}")   
            else:
                print(f"\n\t Miss due to tag mismatch, replace blk # {hex(int(cc[6][0], 2))} by loading in {hex(int(cc[1], 2))}")   
                
    elif (userInput == 1):  # DM
        # target
        print(f"\t \033[4mTarget:\033[0m")
        print(f"\t set/way  : s{int(cc[2], 2)}w0")
        print(f"\t tag bits : {cc[1]} ({hex(int(cc[1], 2))})\n")

        # before

        # s0
        print(f"\t \033[4mIn Cache:\033[0m")
        print(f"\t set/way  : s0w0")
            
        if (cc[6][0][0] == ""): # if no tag bits
            print(f"\t tag bits : None, empty")            
        else:                # tag bits 
            print(f"\t tag bits : {cc[6][0][0]} ({hex(int(cc[6][0][0], 2))})")  
            
        print(f"\t valid bit: {cc[6][0][2]}")

        # s1
        print(f"\n\t set/way  : s1w0")
            
        if (cc[6][1][0] == ""): # if no tag bits
            print(f"\t tag bits : None, empty")            
        else:                # tag bits 
            print(f"\t tag bits : {cc[6][1][0]} ({hex(int(cc[6][1][0], 2))})")  
            
        print(f"\t valid bit: {cc[6][1][2]}")        

        # s2
        print(f"\n\t set/way  : s2w0")
            
        if (cc[6][2][0] == ""): # if no tag bits
            print(f"\t tag bits : None, empty")            
        else:                # tag bits 
            print(f"\t tag bits : {cc[6][2][0]} ({hex(int(cc[6][2][0], 2))})")  
            
        print(f"\t valid bit: {cc[6][2][2]}")       

        # s3
        print(f"\n\t set/way  : s3w0")
            
        if (cc[6][3][0] == ""): # if no tag bits
            print(f"\t tag bits : None, empty")            
        else:                # tag bits 
            print(f"\t tag bits : {cc[6][3][0]} ({hex(int(cc[6][3][0], 2))})")  
            
        print(f"\t valid bit: {cc[6][3][2]}")                          

        # result
        print(f"\n\t \033[4m\033[1mresult  = {pAttempt.upper()}\033[0m")
            
        if (pAttempt == "hit"):
            print(f"\t offset   : {cc[3]} ({hex(int(cc[3], 2))})")

        else:
            print(f"\t block #  : {hex(bin_to_dec(str(cc[1])))}")         # block # (tag & set)
            print(f"\t set/way  : s{int(cc[2], 2)}w0")
            print(f"\t valid bit: 1")
            
            if (cc[6][int(cc[2], 2)][0] == ""):
                print(f"\n\t Miss due to empty block at s{int(cc[2], 2)}w0, load in {hex(int(cc[1], 2))}")                
            else:
                print(f"\n\t Miss due to tag mismatch, replace {hex(int(cc[6][int(cc[2], 2)][0], 2))} at s{int(cc[2], 2)}w0 with {hex(int(cc[1], 2))}")

    elif (userInput == 2):  # FA
        # target
        print(f"\t \033[4mTarget:\033[0m")
        print(f"\t set/way  : s0w{int(cc[4], 2)}")
        print(f"\t tag bits : {cc[1]} ({hex(int(cc[1], 2))})\n")

        # before

        # w0
        print(f"\t \033[4mIn Cache:\033[0m")
        print(f"\t set/way  : s0w0")
            
        if (cc[6][0][0] == 0): # if no tag bits
            print(f"\t tag bits : None, empty")            
        else:                              # tag bits 
            print(f"\t tag bits : {bin(cc[6][0][0])[2:].zfill(28)} ({hex(int(bin(cc[6][0][0])[2:], 2))})")  
            
        print(f"\t valid bit: {cc[6][0][2]}")

        # w1
        print(f"\n\t set/way  : s0w1")
            
        if (cc[6][1][0] == 0): # if no tag bits
            print(f"\t tag bits : None, empty")            
        else:                              # tag bits 
            print(f"\t tag bits : {bin(cc[6][1][0])[2:].zfill(28)} ({hex(int(bin(cc[6][1][0])[2:], 2))})")  
            
        print(f"\t valid bit: {cc[6][1][2]}")      

        # w2
        print(f"\n\t set/way  : s0w2")
        
        if (cc[6][2][0] == 0): # if no tag bits
            print(f"\t tag bits : None, empty")            
        else:                              # tag bits 
            print(f"\t tag bits : {bin(cc[6][2][0])[2:].zfill(28)} ({hex(int(bin(cc[6][2][0])[2:], 2))})")  
            
        print(f"\t valid bit: {cc[6][2][2]}")                               

        # w3
        print(f"\n\t set/way  : s0w3")
        
        if (cc[6][3][0] == 0): # if no tag bits
            print(f"\t tag bits : None, empty")            
        else:                              # tag bits 
            print(f"\t tag bits : {bin(cc[6][3][0])[2:].zfill(28)} ({hex(int(bin(cc[6][3][0])[2:], 2))})")  
        
        print(f"\t valid bit: {cc[6][3][2]}")                  

        # result
        print(f"\n\t \033[4m\033[1mresult  = {pAttempt.upper()}\033[0m")
            
        if (pAttempt == "hit"):
            print(f"\t offset   : {cc[3]} ({hex(int(cc[3], 2))})")
            print(f"\t tag bits : None, empty, valid bit = {cc[6][0][2]}, LRU counter = {cc[6][0][2]}") if (cc[6][0][0] == 0) else print(f"\t s0w0     : tag = {hex(int(bin(cc[6][0][0])[2:].zfill(28), 2))}, valid bit = {cc[6][0][2]}, LRU counter = {cc[6][0][3]}")
            print(f"\t tag bits : None, empty, valid bit = {cc[6][1][2]}, LRU counter = {cc[6][1][2]}") if (cc[6][1][0] == 0) else print(f"\t s0w1     : tag = {hex(int(bin(cc[6][1][0])[2:].zfill(28), 2))}, valid bit = {cc[6][1][2]}, LRU counter = {cc[6][1][3]}")
            print(f"\t tag bits : None, empty, valid bit = {cc[6][2][2]}, LRU counter = {cc[6][2][2]}") if (cc[6][2][0] == 0) else print(f"\t s0w2     : tag = {hex(int(bin(cc[6][2][0])[2:].zfill(28), 2))}, valid bit = {cc[6][2][2]}, LRU counter = {cc[6][2][3]}")
            print(f"\t tag bits : None, empty, valid bit = {cc[6][3][2]}, LRU counter = {cc[6][3][2]}") if (cc[6][3][0] == 0) else print(f"\t s0w3     : tag = {hex(int(bin(cc[6][3][0])[2:].zfill(28), 2))}, valid bit = {cc[6][3][2]}, LRU counter = {cc[6][3][3]}")
                
        else:
            print(f"\t block #  : {hex(bin_to_dec(str(cc[1])))}")         # block # (tag & set)
            print(f"\t tag bits : None, empty, valid bit = {cc[6][0][2]}, LRU counter = {cc[6][0][2]}") if (cc[6][0][0] == 0) else print(f"\t s0w0     : tag = {hex(int(bin(cc[6][0][0])[2:].zfill(28), 2))}, valid bit = {cc[6][0][2]}, LRU counter = {cc[6][0][3]}")
            print(f"\t tag bits : None, empty, valid bit = {cc[6][1][2]}, LRU counter = {cc[6][1][2]}") if (cc[6][1][0] == 0) else print(f"\t s0w1     : tag = {hex(int(bin(cc[6][1][0])[2:].zfill(28), 2))}, valid bit = {cc[6][1][2]}, LRU counter = {cc[6][1][3]}")
            print(f"\t tag bits : None, empty, valid bit = {cc[6][2][2]}, LRU counter = {cc[6][2][2]}") if (cc[6][2][0] == 0) else print(f"\t s0w2     : tag = {hex(int(bin(cc[6][2][0])[2:].zfill(28), 2))}, valid bit = {cc[6][2][2]}, LRU counter = {cc[6][2][3]}")
            print(f"\t tag bits : None, empty, valid bit = {cc[6][3][2]}, LRU counter = {cc[6][3][2]}") if (cc[6][3][0] == 0) else print(f"\t s0w3     : tag = {hex(int(bin(cc[6][3][0])[2:].zfill(28), 2))}, valid bit = {cc[6][3][2]}, LRU counter = {cc[6][3][3]}")

            if (cc[6][0][2] == 0 or cc[6][1][2] == 0 or cc[6][2][2] == 0 or cc[6][3][2] == 0):  # replace by empty way (based on valid bit)
                validBitIndex = 0

                if (cc[6][0][2] == 0):
                    validBitIndex = 0

                elif (cc[6][1][2] == 0):
                    validBitIndex = 1

                elif (cc[6][2][2] == 0):
                    validBitIndex = 2

                else:
                    validBitIndex = 3

                print(f"\n\t Since s0w{validBitIndex} is empty, s{0}w{validBitIndex} will load in blk # {hex(bin_to_dec(str(cc[1])))}")                    

            else: # replace by LRU
                tagLRU      = [hex(int(bin(cc[6][0][0])[2:].zfill(28), 2)), hex(int(bin(cc[6][1][0])[2:].zfill(28), 2)), hex(int(bin(cc[6][2][0])[2:].zfill(28), 2)), hex(int(bin(cc[6][3][0])[2:].zfill(28), 2))]
                countLRU    = [cc[6][0][3], cc[6][1][3], cc[6][2][3], cc[6][3][3]]   
                indexLRU    = countLRU.index(max(countLRU))   

                print(f"\n\t By LRU s0w{indexLRU} containing tag {tagLRU[indexLRU]} will be switched with blk # {hex(bin_to_dec(str(cc[1])))}")
        
    elif (userInput == 3):  # SA
        # target
        print(f"\t \033[4mTarget:\033[0m")
        print(f"\t set/way  : s{cc[4]}w{cc[7]}")
        print(f"\t tag bits : {cc[1]} ({hex(int(cc[1], 2))})\n")

        # before
            
        # w0
        print(f"\t \033[4mIn Cache:\033[0m")
        print(f"\t set/way  : s{cc[4]}w0")
            
        if (cc[6][(cc[4], 0)][0] == ""):        # if no tag bits
            print(f"\t tag bits : None, empty")            
        else:                                   # tag bits 
            print(f"\t tag bits : {cc[6][(cc[4], 0)][0]} ({hex(int(str(cc[6][(cc[4], 0)][0]),2))})")  
            
        print(f"\t valid bit: {cc[6][(cc[4], 0)][2]}")

        # w1
        print(f"\n\t set/way  : s{cc[4]}w1")
            
        if (cc[6][(cc[4], 1)][0] == ""):    # if no tag bits
            print(f"\t tag bits : None, empty")            
        else:                                   # tag bits 
            print(f"\t tag bits : {cc[6][(cc[4], 1)][0]} ({hex(int(str(cc[6][(cc[4], 1)][0]),2))})")  
            
        print(f"\t valid bit: {cc[6][(cc[4], 1)][2]}")        

        # result
        print(f"\n\t \033[4m\033[1mresult  = {pAttempt.upper()}\033[0m")
            
        if (pAttempt == "hit"):
            print(f"\t offset   : {cc[3]} ({hex(int(cc[3], 2))})")
            print(f"\t tag bits : None, empty, valid bit = {cc[6][(cc[4], 0)][2]}, LRU counter = {cc[6][(cc[4], 0)][2]}") if (cc[6][(cc[4], 0)][0] == "") else print(f"\t s{cc[4]}w0     : tag = {hex(int(cc[6][(cc[4], 0)][0], 2))}, valid bit = {cc[6][(cc[4], 0)][2]}, LRU counter = {cc[6][(cc[4], 0)][3]}")
            print(f"\t tag bits : None, empty, valid bit = {cc[6][(cc[4], 1)][2]}, LRU counter = {cc[6][(cc[4], 1)][2]}") if (cc[6][(cc[4], 1)][0] == "") else print(f"\t s{cc[4]}w1     : tag = {hex(int(cc[6][(cc[4], 1)][0], 2))}, valid bit = {cc[6][(cc[4], 1)][2]}, LRU counter = {cc[6][(cc[4], 1)][3]}")
                
        else:
            print(f"\t block #  : {hex(bin_to_dec(str(cc[1])))}")         # block # (tag & set)
            print(f"\t tag bits : None, empty, valid bit = {cc[6][(cc[4], 0)][2]}, LRU counter = {cc[6][(cc[4], 0)][2]}") if (cc[6][(cc[4], 0)][0] == "") else print(f"\t s{cc[4]}w0     : tag = {hex(int(cc[6][(cc[4], 0)][0], 2))}, valid bit = {cc[6][(cc[4], 0)][2]}, LRU counter = {cc[6][(cc[4], 0)][3]}")
            print(f"\t tag bits : None, empty, valid bit = {cc[6][(cc[4], 1)][2]}, LRU counter = {cc[6][(cc[4], 1)][2]}") if (cc[6][(cc[4], 1)][0] == "") else print(f"\t s{cc[4]}w1     : tag = {hex(int(cc[6][(cc[4], 1)][0], 2))}, valid bit = {cc[6][(cc[4], 1)][2]}, LRU counter = {cc[6][(cc[4], 1)][3]}")


            if (cc[6][(cc[4], 0)][0] == ""):
                t0 = "None, empty" 
            else: 
                t0 = hex(int(cc[6][(cc[4], 0)][0], 2))
                    
            if (cc[6][(cc[4], 1)][0] == ""):
                t1 = "None, empty" 
            else:
                t1 = hex(int(cc[6][(cc[4], 1)][0], 2)) 

            if (cc[6][(cc[4], 0)][2] == 0 or cc[6][(cc[4], 1)][2] == 0):    # valid bits = 0
                validBit = 0

                if (cc[6][(cc[4], 0)][2] == 0):
                    validBit = 0
                else:
                    validBit = 1

                print(f"\n\t Since s{cc[4]}w{validBit} is empty, s{cc[4]}w{validBit} will load in blk # {hex(bin_to_dec(str(cc[1])))}")

            else:   # replace by LRU
                tagLRU      = [t0, t1]
                countLRU    = [cc[6][(cc[4], 0)][3], cc[6][(cc[4], 1)][3]]   
                indexLRU    = countLRU.index(max(countLRU))                       
                print(f"\n\t By LRU s{cc[4]}w{indexLRU} containing tag {tagLRU[indexLRU]} will be switched with blk # {hex(bin_to_dec(str(cc[1])))}")
            
    return hit


## Cache Functions **********************************************************************

# get8B: loads data from data memory to cache (used for SA) 
# Input: mem = mem array | cache type | addr = address requested
# Return: data values of size 8B from DM for SA cache
def get8B(mem, cache, addr):
    addr = itosbin(int(addr), 32)[:29] + "000"
    addr = str(bin_to_dec(addr))

    memIndex = accessDM(addr)
    
    word = []
    byte = []

    # get all words for the block size of 16 and store in word array
    for i in range(8//4):
        word.append(itosbin(int(mem[memIndex + i]), 32))
        
    # splice each word into 4 bytes and append to byte array
    for i in range(len(word)):
        byte.append(word[i][:8])
        byte.append(word[i][8:16])
        byte.append(word[i][16:24])
        byte.append(word[i][24:])

    return byte

# get16B: loads data from data memory to cache (used for FA & DM) 
# Input: mem = mem array | cache type | addr = address requested
# Return: data values of size 16B from DM for cache
def get16B(mem, cache, addr):
    addr = itosbin(int(addr), 32)[:28] + "0000"
    addr = str(bin_to_dec(addr))

    memIndex = accessDM(addr)
    
    word = []
    byte = []

    # get all words for the block size of 16 and store in word array (16B = 4words)
    for i in range(16//4):
        word.append(itosbin(int(mem[memIndex + i]), 32))
        
    # splice each word into 4 bytes and append to byte array
    for i in range(len(word)):
        byte.append(word[i][:8])
        byte.append(word[i][8:16])
        byte.append(word[i][16:24])
        byte.append(word[i][24:])

    return byte    

# get64B loads 64B of data to cache (simple cache)
# Input: mem = mem array | cache type | addr = address requested
# Return: data values of size 64B from simple cache
def get64B(mem, cache, addr):
    addr = itosbin(int(addr), 32)[:26] + "000000"
    addr = str(bin_to_dec(addr))

    memIndex = accessDM(addr)
    
    word = []
    byte = []

    # get all words for the block size of 64 and store in word array (16B = 4words)
    for i in range(64//4):
        word.append(itosbin(int(mem[memIndex + i]), 32))
        
    # splice each word into 4 bytes and append to byte array
    for i in range(len(word)):
        byte.append(word[i][:8])
        byte.append(word[i][8:16])
        byte.append(word[i][16:24])
        byte.append(word[i][24:])

    return byte

# checkSBCache: checks to see if a miss or hit occurs and updates cache if a miss occurs
# Input: mem = mem array | cache = simple cache | address = address requested
# Return: miss(0) or hit(1) 
def checkSBCache(address, cache):
    addr = itosbin(int(address), 32)    # convert to int and then to binary  

    blkAddr = addr[:26]                 # set blkAddr to upper 26 bits
    offset = addr[26:]                  # set in-block offset to lower 6 bits (2^6 = 64)
    
    before = copy.deepcopy(SBCache[0])           # get before updated results for return
    
    if(blkAddr == cache.get(0)[0]): 
        return 1, blkAddr, "", offset, "", SBCache[0][2], before

    else:
        data = get64B(mem, cache, address)
        cache.update({0 : [blkAddr, [], 1]})
        return 0, blkAddr, "", offset, "", SBCache[0][2], before

# checkDMCache: checks to see if a miss or hit occurs and updates DMCache if a miss occurs
# Input: mem = mem array | DMCache = cache | address = address requested
# Return: miss(0) or hit(1) 
def checkDMCache(mem, DMCache, address):
    addr = itosbin(int(address), 32)       # convert to integer (string) to binary (string)

    tag = addr[:26]                        # Parse into tag, idx, ibo
    idx = addr[26:28]
    ibo = addr[28:]

    setNum = int(idx, base=2)

    before = copy.deepcopy(DMCache)               # get before updated results for return

    # check if set contains the tag    
    if (tag == DMCache[setNum][0]): # check if requested tag = tag in DMCache        
        return 1, tag, idx, ibo, setNum, DMCache[setNum][2], before
    else:
        data = get16B(mem, DMCache, address) 
        DMCache[setNum] = [tag, data, 1]
        return 0, tag, idx, ibo, setNum, DMCache[setNum][2], before

# checkFACache: check to see if data is in cache for lw/lh
# Input: cache = The entire cache | memAddr = memory address that we would normally be checking | memory = DM
# numBytes = the number of bytes that the operation would read or write | instrnType = instruction that checks cache
# this determines whether or not we read/write cache | rt = Data supply for sw/sh instructions
# Output: updated cache file
def checkFACache(cache, memAddr, memory, numBytes, instrnType, rt): 

    # Get the block number of the memory address that we're after
    # Since that's just the tag, IE the memory address with the 4 least significant digits disregarded
    # We can just shift right by four to wash away those bits, then shift back left 4 to get the address of the start of the block in memory.
    startOfBlockAddrInMemory = (memAddr >> 4) << 4


    # Parse the memory address:
    # Tag is the upper 28 bits
    # IBO is the lower 4 bits
    soughtTag = startOfBlockAddrInMemory
    ibo = memAddr & 0xF

    before = copy.deepcopy(cache)               # get before updated results for return

    # Assume to start that we've got a miss
    hit = 0

    # Flag to for the initial state of the cache being empty
    empty = 1

    # Check if all ways are empty
    for way in range(4):

        # If a single way isn't empty, the cache itself isn't totally empty
        if cache[way][2] != 0:
            empty = 0

    # If even a single block isn't empty, there's a possibility of a hit.
    if not empty:

        # Flag for finding our block or not. Assume not found to start.
        foundBlock = 0

        # Actually check the rest of the ways
        for way in range(4):
            
            # If we have a tag match
            if cache[way][0] == soughtTag:

                # Set the block found flag
                foundBlock = 1

                # We have a hit
                hit = 1
                
                # If we find the block we're looking for, reset its LRU count to 0.
                cache[way][3] = 0
                '''
                # If the instruction is a store instruction
                if 's' in instrnType:

                    # The four bytes that compose the data in rt are broken out so that we can write them individually to the correct ibo in cache.
                    writeBuffer = [rt[0:8], rt[8:16], rt[16:24], rt[24:]]

                    # Write starting from the correct ibo in the block that we want, for as many bytes as the instruction requires.
                    for i in range(numBytes):
                        cache[way][1][ibo + i] = writeBuffer[i]


                # Otherwise its a load instruction
                else:

                    # A list to hold the contents of the read if doing lw or lh
                    readBuffer = [0,0,0,0]

                    # Go to the IBO offset location and start reading sequentially
                    for i in range(numBytes):
                        readBuffer[i] = cache[way][1][ibo + i]

                    # Finally, update rt with the value of the read.
                    rt = readBuffer
                '''
                    
                # If we find the block we're looking for, we shouldn't loop anymore
                #break

            # Otherwise, increment the block's LRU count
            else:
                # If the block wasn't the one we're after, incrment its LRU count by 1
                cache[way][3] += 1

        # If we don't find the block we need, we need to grab it from DM and bring it into cache.
        # This constitutes a cache miss.
        if not foundBlock:

            # Need LRU consideration for this part. We want replace the block with the highest/lowest (depends on how we think of it) LRU Count
            lruCounts = []

            # A flag in case we have ways with validBit == 0
            invalidWaysRemaining = 0

            # Variable for the way that's going to be replaced in cache.
            wayToBeReplaced = 0

            # Check the cache to see if any of the ways still have valid = 0
            for way in range(4):

                # If we find a way that's not yet valid, we wanna replace it first.
                if cache[way][2] == 0:
                    wayToBeReplaced = way
                    invalidWaysRemaining = 1
                    break

            # Gather the LRU counts from each block in cache
            for way in range(4):
                lruCounts.append(cache[way][3])

            # If we have invalid ways remaining, we need to replace those blocks first.
            # Otherwise, we can replace whichever block is the LRU
            if not invalidWaysRemaining:
                # Get the index of the LRU block
                wayToBeReplaced = lruCounts.index(max(lruCounts))

            # Update the block's tag, bring in the new data, set valid = 1, and set LRUCount = 0
            cache[wayToBeReplaced][0] = soughtTag
            cache[wayToBeReplaced][1] = get16B(memory, cache, memAddr)
            cache[wayToBeReplaced][2] = 1
            cache[wayToBeReplaced][3] = 0

    # If all ways are empty, we automatically miss and need to go to memory and get the 16B we need to fill a block
    else:

        # Therefore, just throw the data in way 0.
        cache[0][0] = soughtTag
        cache[0][1] = get16B(memory, cache, memAddr)
        cache[0][2] = 1
        cache[0][3] = 0

    # Return whether or not we hit or missed
    return hit, bin(soughtTag)[2:].zfill(28), "", bin(ibo)[2:].zfill(4), bin(way)[2:], FACache[way][2], before

# checkSACache: checks to see if a miss or hit occurs and updates SACache if a miss occurs
# Input: mem = mem array | SACache = SA cache block | address = address requested
# Return: miss(0) or hit(1) 
def checkSACache(mem, SACache, address):
    addr = itosbin(int(address), 32)       # convert to integer (string) to binary (string)

    tag = addr[:27]                        # parse into tag, idx, ibo
    idx = addr[27:29]
    ibo = addr[29:]

    setNum = int(idx, base=2)

    way = 0

    before = copy.deepcopy(SACache)               # get before updated results for return

    # 1. check if set contains the tag in one of the ways 
    if ((tag == SACache[(setNum, 0)][0]) or (tag == SACache[(setNum, 1)][0])): # check if requested tag = tag in SACache  
        # hit
        data = get8B(mem, SACache, address) 
        SACache[(setNum, way)] = [tag, data, 1, 0]
        
        return 1, tag, idx, ibo, setNum, DMCache[setNum][2], before, way            

    else:   # miss

        # 2. Check valid bits
        if ((SACache[(setNum,0)][2] == 0) or (SACache[(setNum,1)][2] == 0)):    # update based on valid bits if there is at least one 0
            
            # check which way contains a 0 for valid bit
            if (SACache[(setNum,0)][2] == 0):
                way = 0
            else:
                way = 1

            # 3. update LRUs for given set if valid bit is 1
            if (SACache[(setNum, 0)][2] == 1):
                SACache[(setNum, 0)][3] += 1 

            if (SACache[(setNum, 1)][2] == 1):        
                SACache[(setNum, 1)][3] += 1 

            # 4. replace way for valid bit = 0
            data = get8B(mem, SACache, address) 
            SACache[(setNum, way)] = [tag, data, 1, 0]

            return 0, tag, idx, ibo, setNum, DMCache[setNum][2], before, way            
        
        else:   # update based on LRU

            # 3. update LRUs for given set if valid bit is 1
            if (SACache[(setNum, 0)][2] == 1):
                SACache[(setNum, 0)][3] += 1 

            if (SACache[(setNum, 1)][2] == 1):        
                SACache[(setNum, 1)][3] += 1 

            # 4. replace block based on LRU

            # figure out which way contains the greater LRU count
            if (SACache[(setNum, 0)][3] > SACache[(setNum, 1)][3]):
                way = 0
            else:
                way = 1
                        
            data = get8B(mem, SACache, address) 
            SACache[(setNum, way)] = [tag, data, 1, 0]
                    
            return 0, tag, idx, ibo, setNum, DMCache[setNum][2], before, way


## End of Functions *********************************************************************

### Main ================================================================================

print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Project 4 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

## User Input (Input/Output Files) ******************************************************
# input_file = input("Enter input file> ")                # ask for user input file

# file_exists = 0                                         # temp variable to keep track of file exist state 

# # check if input file exists 
# while (file_exists != 1):
#     if Path.isfile(input_file): # file exists
#         print("File sucessfully loaded")
#         input_file = open(input_file, "r")              # open input file in read mode (r)
#         file_exists = 1                                 # file exists so set true
#     else: # file does not exist, so ask for valid file
#         print("File does not exist")
#         file_exists = 0                                 # file does not exists so set false
#         input_file = input("Enter input file> ")

# output_file = input("Enter desired output file> ")      # ask for user output file name
# output_file = open(output_file,"w")                     # create and open output file in write mode (w)

# hardcoded for testing purposes
input_file = open("test_files/mc.txt", "r")
output_file = open("test_files/asm.txt", "w")

## User Input (Data Memory) *************************************************************
choice1 = choice2 = hexAddress = 0
hexValue = 1

# print("\nWhat data representation would you like?")
# while (choice1 == 0 and choice2 == 0):
#     x = input("Hexadecimal Address? (y = yes, n = no)> ")
#     while (choice1 == 0) and (x != 'y' or x != 'n'):
#         if (x == 'y'):
#             hexAddress = 1
#             choice1 = 1
#         elif (x == 'n'):
#             choice1 = 1
#             break
#         else:
#             x = input("Hexadecimal Address? (y = yes, n = no)> ")
#             continue

#     y = input("Hexadecimal Values? (y = yes, n = no)> ")
#     while (choice2 == 0) and (x != 'y' or x != 'n'):
#         if (y == 'y'):
#             hexValue = 1
#             choice2 = 1
#         elif (y == 'n'):
#             choice2 = 1
#             break
#         else:
#             y = input("Hexadecimal Value? (y = yes, n = no)> ")
#             continue

## User Input (Cache Configurations) ****************************************************
# cache configuration options
validConfig = 0
options     = ["A", "B", "C", "D"]

print("Cache Configurations: "
        "\n\tA. (N=1, S=1, b=64) a simplest cache, with only 1 block, size of 64 B."
        "\n\tB. (N=1, S=4, b=16) a DM cache with 4 sets, block size of 16 B."
        "\n\tC. (N=4, S=1, b=16) a 4-way FA cache, cache, block size of 16 B."
        "\n\tD. (N=2, S=4, b=8)  a 2-way 4-set, SA cache, block size of 8 B")

# loop input prompt for cache configuration if non-valid configuration is chosen
while (validConfig == 0):
    config = input("\nWhat cache configuration would you like to perform? (A,B,C,D) > ")
    if ((config == "A") or (config == "B") or (config == "C") or (config == "D")):
        validConfig = 1

# ## Hardcoded for testing purposes
# config = "A"
## ------------------------------

userInput = options.index(config)   # update userInput's selection of cache configuration to appropriate index for cacheConfig function

## User Input (Mode Configurations) *****************************************************
validMode = 0

print("\nDisplay Modes:\n\tDetailed Mode: display step-by-step information and hitrate\n\tFast Mode: display hitrate only\n")

# loop input prompt for mode if non-valid mode is chosen
while (validMode == 0):
    mode = input("Select your mode (A: detailed mode | B: fast mode)>  ")
    if ((mode == "A") or (mode == "B")):
        validMode = 1

if (options.index(mode) == 1): # fast = 0 | detailed = 1
    print("\nYou entered fast mode")
else:
    print("\nYou entered detailed mode (press enter to proceed)")

# ## Hardcoded for testing purposes
# mode = "B"
## ------------------------------
mode = options.index(mode)
cont = 1

print("\n")

## Main components **********************************************************************
asm_instr = []                                          # save default asm instruction

instr = disassemble(input_file, asm_instr)              # disassemble machine code from input file to readable MIPS
                                                        # place results into a list data structure; holds line number [starting at 0 for 1]
                                            
# registers
reg = [0] * 32              # create register from $0 to $31 (w/ pc, lo, hi)
pc = hi = lo = line = 0     # line = current instruction line number

# data memory
mem = [0] * 1024             # (0x3000 - 0x2000) / 4 = 1024 memory cells

# instruction statistics
total = alu = jump = branch = memory = other = 0

## Header *******************************************************************************
# # output header
# pLine = "line"
# pInstr = "Instruction"
# pResult = "Result"
# pPC = "PC"

# print(f"{pLine:<15}{pInstr:<35}{pResult:<25}{pPC:<15}")

# # output header to output .txt file
# row_item = [pLine, pInstr, pResult, pPC]
# output = '{:<8}{:<24}{:<26}{:<8}'.format(row_item[0], row_item[1], row_item[2], row_item[3])

# output_file.write(output + "\n")

## Cache Declarations *******************************************************************
miss = hit = 0
# testHit = totalShots = 0                     # to be removed

# Declaring simple cache of 64B with 1-way and 1-set    
SBCache = {
# | tag | offset |
# | 26  |   6    |    

#   blk    [tag,    data,   valid]
    0   :   ["",    [],     0]
}

# Declaring DM & Mem DS        [Data Structure: Dictionary(setNum)-List(block) style]
DMCache = {
# | tag | set | offset |
# | 26  |  2  |   4    |
 
#   set     [tag,   data,   valid]
    0   :   ["",    [],     0],
    1   :   ["",    [],     0],
    2   :   ["",    [],     0],
    3   :   ["",    [],     0],
}

FACache = [
# | tag | offset |
# | 28  |   4    |
 
#   [tag,  data,   valid,   LRU]
    [0,    [],     0,       0],
    [0,    [],     0,       0],
    [0,    [],     0,       0],
    [0,    [],     0,       0],

]

## Declaring SA                 [Data Structure: Dictionary(set,way)-List(block) style]
SACache = {
# | tag | set | offset |
# | 27  |  2  |   3    |

#   set/way    [tag,   data,   valid,   LRU]
    (0,0)  :   ["",    [],     0,       0],
    (0,1)  :   ["",    [],     0,       0],
    (1,0)  :   ["",    [],     0,       0],
    (1,1)  :   ["",    [],     0,       0],
    (2,0)  :   ["",    [],     0,       0],
    (2,1)  :   ["",    [],     0,       0],
    (3,0)  :   ["",    [],     0,       0],
    (3,1)  :   ["",    [],     0,       0],
}

cacheAccess = 0

## Instruction Loop **********************************************************************
# analyze instructions
while (int(pc/4) < len(instr)):     # int(pc/4) = current instruction
            
    cur = instr[int(pc/4)]          # give access to instr[] list-list
                                    # first list: separated machine code instructions (access to opcode, rs, rt, rd, sa, func, imm)
                                    # second list: holds the first list within itself and replicates "line numbers"

    line += 1                       # update for next instruction in instr list

    # instructions 
    
    # branch instructions 
    if (cur[0] == "j" or cur[0] == "beq" or cur[0] == "bne"):

        if (cur[0] == 'j'):         # J
            pInstr = asm_instr[int(pc/4)]
            pc = j_pc_count(pc, int(cur[1]))
            jump += 1

        elif (cur[0] == "beq"):     # BEQ
            if (reg[int(cur[1])] == reg[int(cur[2])]):
                pInstr = asm_instr[int(pc/4)]                
                pc += 4 + (int(cur[3]) << 2)
            else:
                pInstr = asm_instr[int(pc/4)]
                pc += 4

            branch += 1

        else:                       # BNE
            if (reg[int(cur[1])] != reg[int(cur[2])]):
                pInstr = asm_instr[int(pc/4)]
                pc += 4 + (int(cur[3]) << 2)
            else:
                pInstr = asm_instr[int(pc/4)]
                pc += 4  

            branch += 1

        # update result
        if (cur[0] == "beq" or cur[0] == "bne"):
            pResult = "branch to PC: " + str(pc) 
        else:
            pResult = "jump to PC " + str(pc)
     
    # must be sw/sh/lh/lw
    elif (cur[0] == "sw" or cur[0] == "sh" or cur[0] == "lw" or cur[0] == "lh"):
        # mode A (detailed)
        if (mode == 0 and cont == 1):
            if (input("Press Enter to Continue\n") == ""):
                cont = 1
            else:
                break        
        
        cacheAccess += 1

        # process cache
        address = int(cur[2]) + reg[int(cur[3])]
        if (mode == 0): # detailed mode (mode = 0)
            if (outputCache(address, SBCache, DMCache, FACache, SACache) == 1):
                hit += 1
            else:
                miss += 1
        
            print("\n")

        else:
            if (userInput == 0):
                cc = checkSBCache(address, SBCache)
            elif (userInput == 1):
                cc = checkDMCache(mem, DMCache, address)
            elif (userInput == 2):
                cc = checkFACache(FACache, address, mem, 16, cur[0], cur[1])
            else: # 3
                cc = checkSACache(mem, SACache, address)

            # run cache configuration based on userInput 
            if (cc[0] == 1):
                hit += 1

            else:
                miss += 1
            
        if (cur[0] == "sw"):    # SW
            mem[accessDM(str(int(cur[2]) + reg[int(cur[3])]))] = reg[int(cur[1])]
            pResult = "DM[" + str(int(cur[2]) + reg[int(cur[3])]) + "]" + " = " + str(reg[int(cur[1])])

        elif (cur[0] == "sh"):  # SH
            mem[accessDM(str(int(cur[2]) + reg[int(cur[3])]))] = bin_to_dec(hex_to_bin(int_to_hex(mem[accessDM(str(int(cur[2]) + reg[int(cur[3])]))]))[:16] + 
                hex_to_bin(int_to_hex(reg[int(cur[1])]))[16:])

            pResult = "DM[" + str(int(cur[2]) + reg[int(cur[3])]) + "]" + " = " + str(mem[accessDM(str(int(cur[2]) + reg[int(cur[3])]))])

        elif (cur[0] == "lh"):  # LH
            reg[int(cur[1])] = bin_to_dec(hex_to_bin(int_to_hex(mem[accessDM(str(int(cur[2]) + reg[int(cur[3])]))]))[16:])

            pResult = "$" + cur[1] + " = " + str(reg[int(cur[1])])

        else:                   # LW
            reg[int(cur[1])] = mem[accessDM(str(int(cur[2]) + reg[int(cur[3])]))]

            pResult = "$" + cur[1] + " = " + str(reg[int(cur[1])])

        pc += 4
        pInstr = asm_instr[int(pc/4) - 1]

        memory += 1

    else:   # must not lw/sw or branch instruction
        if (cur[0] == "addi"):      # ADDI
            reg[int(cur[1])] = reg[int(cur[2])] + int(cur[3])      

        elif (cur[0] == "add"):     # ADD
            reg[int(cur[1])] = reg[int(cur[2])] + reg[int(cur[3])]

        elif (cur[0] == "sub"):     # SUB
            reg[int(cur[1])] = reg[int(cur[2])] - reg[int(cur[3])]

        elif (cur[0] == "slt"):     # SLT
            if (reg[int(cur[2])] < reg[int(cur[3])]):  # if x < y 
                reg[int(cur[1])] = 1    # x = 1
            else: # x > y
                reg[int(cur[1])] = 0    # x = 0

        elif (cur[0] == "sll"):     # SLL
            reg[int(cur[1])] = sll(itosbin(reg[int(cur[2])], 32), int(cur[3]))

        elif (cur[0] == "xor"):     # XOR
            reg[int(cur[1])] = reg[int(cur[2])] ^ reg[int(cur[3])]

        elif (cur[0] == "srl"):     # SRL
            reg[int(cur[1])] = srl(itosbin(reg[int(cur[2])], 32), int(cur[3]))

        elif (cur[0] == "srlv"):    # SRLV
            reg[int(cur[1])] = srl(itosbin(reg[int(cur[2])], 32), reg[int(cur[3])])

        elif (cur[0] == "andi"):    # ANDI
            reg[int(cur[1])] = bin_to_dec(and32(itosbin(reg[int(cur[2])], 32), itosbin(int(cur[3]), 32)))
            
        elif (cur[0] == "ori"):     # ORI
            reg[int(cur[1])] = bin_to_dec(or32(itosbin(reg[int(cur[2])], 32), itosbin(int(cur[3]), 32)))

        elif (cur[0] == "xori"):    # XORI
            reg[int(cur[1])] = bin_to_dec(xor32(itosbin(reg[int(cur[2])], 32), itosbin(int(cur[3]), 32)))

        elif (cur[0] == "lui"):     # LUI
            reg[int(cur[1])] = lui32(cur[2])

        elif (cur[0] == "mfhi"):    # MFHI
            reg[int(cur[1])] = hi 

        elif (cur[0] == "mflo"):    # MFLO
            reg[int(cur[1])] = lo
        
        elif (cur[0] == "mul"):     # MUL
            if pInstr.find("$" + cur[3]):
                hi_lo = mul(reg[int(cur[2])], reg[int(cur[3])])    # mul $x, $y
            else:
                hi_lo = mul(reg[int(cur[2])], int(cur[3]))         # mul $x, y

            hi = hi_lo[0]
            lo = hi_lo[1]
            reg[int(cur[1])] = lo

        elif (cur[0] == "fw"):      # FW [Special Instruction]
            reg[int(cur[1])] = findWidth(reg[int(cur[2])])
        
        else:
            print("Instruction not implemented")

        # set $0 as absolute zero
        if (cur[1] == '0'):
            reg[int(cur[1])] = 0    

        # update outputs
        pc += 4

        if (cur[0] == 'slt' or cur[0] == 'mul'):
            other += 1
        else:
            alu += 1

        pResult = "$" + cur[1] + " = " + str(reg[int(cur[1])]) 
        pInstr = asm_instr[int(pc/4) - 1]

    # # update print outputs
    # pLine = line
    # pPC = pc

    # # print outputs
    # print(f"{pLine:<15}{pInstr:<35}{pResult:<25}{pPC:<15}")

    # # output to output .txt file
    # row_item = [pLine, pInstr, pResult, pPC]
    # output = '{:<8}{:<24}{:<26}{:<8}'.format(row_item[0], row_item[1], row_item[2], row_item[3])

    # output_file.write(output + "\n")

    # # To be removed:
    # if ((testHit == 0) and (cur[0] == "sw" or cur[0] == "sh" or cur[0] == "lw" or cur[0] == "lh")):
    #     print("Miss")
    # elif ((testHit == 1) and (cur[0] == "sw" or cur[0] == "sh" or cur[0] == "lw" or cur[0] == "lh")):
    #     print("Hit")


if (mode == 0):
    print("\n")
    output_file.write("\n")

## Final Outputs ************************************************************************
# output registers
# outputRegisters(reg, pc, hi, lo, hexValue)

# output Data Memory
# outputDataMem(mem, 0x2000, 0x3004, hexAddress, hexValue)

# output instruction statistics
total = alu + jump + branch + memory + other
# outputInstrStats(total, alu, jump, branch, memory, other)

output_file.close()

hitrate = (hit / (hit + miss)) * 100

print(f'Hit           : {hit:<10}\nMiss          : {miss:<10}')
print('-' * 20)
print(f'Attempts      : {hit+miss}')
print(f'\n\033[1mHitrate       : {hitrate:.2f}%\033[0m')

print("\nProgram Sucessfully Finished")     # print when program finishes

### End of Main =========================================================================
