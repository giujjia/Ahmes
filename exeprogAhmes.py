# Simulador AHMES

import sys
import math

Nbit = 8  # número de bits que a máquina opera
MAX = int(pow(2, Nbit))  # Número máximo permitido para endereçamento

def update_flags(ac, result, carry=0, borrow=0):
    """Atualiza as flags N, Z, V, C, B baseado no resultado"""
    # N (Negative): bit mais significativo (bit 7)
    N = 1 if (result & 0x80) != 0 else 0
    
    # Z (Zero): resultado é zero
    Z = 1 if (result & 0xFF) == 0 else 0
    
    # V (Overflow): verifica overflow em operações aritméticas
    # Para adição: ambos operandos positivos e resultado negativo, ou ambos negativos e resultado positivo
    # Para subtração: similar mas invertido
    # Simplificação: verifica se o sinal mudou de forma inesperada
    V = 0  # Será calculado nas operações específicas
    
    # C (Carry): carry da operação
    C = carry
    
    # B (Borrow): borrow da subtração
    B = borrow
    
    return N, Z, V, C, B

def main():
    pc = 0
    ac = 0
    mem = [0] * 256
    
    # Flags do AHMES
    N = 0  # Negative
    Z = 0  # Zero
    V = 0  # Overflow
    C = 0  # Carry
    B = 0  # Borrow
    
    # Carrega memória do arquivo mem.txt
    try:
        with open("mem.txt", "r") as fp:
            lines = fp.readlines()
            for i, line in enumerate(lines[:256]):
                line = line.strip()
                if line:
                    mem[i] = int(line)
    except FileNotFoundError:
        print("O arquivo mem.txt não pode ser aberto.")
        sys.exit(1)
    
    print("\n Memória antes do processamento:")
    for i in range(256):
        print(f"{i}:{mem[i]}", end=" ")
        if (i + 1) % 8 == 0:
            print()
    
    print("\n")
    
    # Executa o programa
    halted = False
    labels = {}  # Mapeia endereços para labels (para uso com goto)
    
    # Cria labels para cada endereço (para compatibilidade com o código gerado)
    for i in range(256):
        labels[f"l{i}"] = i
    
    while not halted and pc < 256:
        opcode = mem[pc] & 0xFF
        
        # NOP (0000 xxxx = 0)
        if opcode == 0:
            pc += 1
        
        # STA end (0001 xxxx = 16-31)
        elif 16 <= opcode <= 31:
            end = mem[pc + 1] & 0xFF
            mem[end] = ac & 0xFF
            pc += 2
        
        # LDA end (0010 xxxx = 32-47)
        elif 32 <= opcode <= 47:
            end = mem[pc + 1] & 0xFF
            ac = mem[end] & 0xFF
            N, Z, V, C, B = update_flags(ac, ac)
            pc += 2
        
        # ADD end (0011 xxxx = 48-63)
        elif 48 <= opcode <= 63:
            end = mem[pc + 1] & 0xFF
            old_ac = ac
            value = mem[end] & 0xFF
            result = ac + value
            carry = (result >> 8) & 1
            ac = result & 0xFF
            
            # Calcula overflow: se ambos são positivos (<128) e resultado >= 128, ou ambos negativos (>=128) e resultado < 128
            overflow = 0
            if ((old_ac < 128) and (value < 128) and (ac >= 128)) or \
               ((old_ac >= 128) and (value >= 128) and (ac < 128)):
                overflow = 1
            
            N, Z, V, C, B = update_flags(ac, ac, carry, 0)
            V = overflow
            pc += 2
        
        # OR end (0100 xxxx = 64-79)
        elif 64 <= opcode <= 79:
            end = mem[pc + 1] & 0xFF
            ac = (ac | mem[end]) & 0xFF
            N, Z, V, C, B = update_flags(ac, ac)
            pc += 2
        
        # AND end (0101 xxxx = 80-95)
        elif 80 <= opcode <= 95:
            end = mem[pc + 1] & 0xFF
            ac = (ac & mem[end]) & 0xFF
            N, Z, V, C, B = update_flags(ac, ac)
            pc += 2
        
        # NOT (0110 xxxx = 96-111)
        elif 96 <= opcode <= 111:
            ac = ((~ac) & 0xFF)
            N, Z, V, C, B = update_flags(ac, ac)
            pc += 1
        
        # SUB end (0111 xxxx = 112-127)
        elif 112 <= opcode <= 127:
            end = mem[pc + 1] & 0xFF
            old_ac = ac
            value = mem[end] & 0xFF
            result = ac - value
            borrow = 1 if result < 0 else 0
            ac = result & 0xFF
            
            # Calcula overflow na subtração
            overflow = 0
            if ((old_ac < 128) and (value >= 128) and (ac >= 128)) or \
               ((old_ac >= 128) and (value < 128) and (ac < 128)):
                overflow = 1
            
            N, Z, V, C, B = update_flags(ac, ac, 0, borrow)
            V = overflow
            pc += 2
        
        # JMP end (1000 xxxx = 128-143)
        elif 128 <= opcode <= 143:
            end = mem[pc + 1] & 0xFF
            pc = end
        
        # JN end (1001 00xx = 144-147)
        elif 144 <= opcode <= 147:
            end = mem[pc + 1] & 0xFF
            if N == 1:
                pc = end
            else:
                pc += 2
        
        # JP end (1001 01xx = 148-151)
        elif 148 <= opcode <= 151:
            end = mem[pc + 1] & 0xFF
            if N == 0:
                pc = end
            else:
                pc += 2
        
        # JV end (1001 10xx = 152-155)
        elif 152 <= opcode <= 155:
            end = mem[pc + 1] & 0xFF
            if V == 1:
                pc = end
            else:
                pc += 2
        
        # JNV end (1001 11xx = 156-159)
        elif 156 <= opcode <= 159:
            end = mem[pc + 1] & 0xFF
            if V == 0:
                pc = end
            else:
                pc += 2
        
        # JZ end (1010 00xx = 160-163)
        elif 160 <= opcode <= 163:
            end = mem[pc + 1] & 0xFF
            if Z == 1:
                pc = end
            else:
                pc += 2
        
        # JNZ end (1010 01xx = 164-167)
        elif 164 <= opcode <= 167:
            end = mem[pc + 1] & 0xFF
            if Z == 0:
                pc = end
            else:
                pc += 2
        
        # JC end (1011 00xx = 168-171)
        elif 168 <= opcode <= 171:
            end = mem[pc + 1] & 0xFF
            if C == 1:
                pc = end
            else:
                pc += 2
        
        # JNC end (1011 01xx = 172-175)
        elif 172 <= opcode <= 175:
            end = mem[pc + 1] & 0xFF
            if C == 0:
                pc = end
            else:
                pc += 2
        
        # JB end (1011 10xx = 176-179)
        elif 176 <= opcode <= 179:
            end = mem[pc + 1] & 0xFF
            if B == 1:
                pc = end
            else:
                pc += 2
        
        # JNB end (1011 11xx = 180-183)
        elif 180 <= opcode <= 183:
            end = mem[pc + 1] & 0xFF
            if B == 0:
                pc = end
            else:
                pc += 2
        
        # SHR (1110 xx00 = 224, 228, 232, 236)
        elif opcode in [224, 228, 232, 236]:
            old_carry = C
            C = ac & 1  # bit menos significativo vai para carry
            ac = (ac >> 1) & 0xFF  # desloca para direita, bit 7 recebe 0
            N, Z, V, _, B = update_flags(ac, ac)
            pc += 1
        
        # SHL (1110 xx01 = 225, 229, 233, 237)
        elif opcode in [225, 229, 233, 237]:
            old_carry = C
            C = (ac >> 7) & 1  # bit mais significativo vai para carry
            ac = ((ac << 1) & 0xFE) & 0xFF  # desloca para esquerda, bit 0 recebe 0
            N, Z, V, _, B = update_flags(ac, ac)
            pc += 1
        
        # ROR (1110 xx10 = 226, 230, 234, 238)
        elif opcode in [226, 230, 234, 238]:
            old_carry = C
            new_carry = ac & 1  # bit menos significativo vai para carry
            ac = ((ac >> 1) | (old_carry << 7)) & 0xFF  # desloca para direita, bit 7 recebe o carry antigo
            C = new_carry
            N, Z, V, _, B = update_flags(ac, ac)
            pc += 1
        
        # ROL (1110 xx11 = 227, 231, 235, 239)
        elif opcode in [227, 231, 235, 239]:
            old_carry = C
            new_carry = (ac >> 7) & 1  # bit mais significativo vai para carry
            ac = (((ac << 1) | old_carry) & 0xFF)  # desloca para esquerda, bit 0 recebe o carry antigo
            C = new_carry
            N, Z, V, _, B = update_flags(ac, ac)
            pc += 1
        
        # HLT (1111 xxxx = 240-255)
        elif 240 <= opcode <= 255:
            halted = True
            pc += 1
        
        else:
            print(f"Instrução desconhecida: {opcode} no endereço {pc}")
            pc += 1
    
    print("\n Memória após o processamento:")
    for i in range(32):
        for offset in [0, 32, 64, 96, 128, 160, 192, 224]:
            addr = i + offset
            print(f"{addr}:{mem[addr]}", end=" ")
        print()
    
    print("\n")
    print(f"pc = {pc}")
    print(f"ac = {ac}")
    print(f"Número de bits = {Nbit}")
    print(f"Flags: N={N}, Z={Z}, V={V}, C={C}, B={B}")
    
    if ac >= 128:
        print("Negativo\n")
    else:
        print("Positivo\n")
    
    if ac == 0:
        print("Zero")
    else:
        print("Diferente de Zero")

if __name__ == "__main__":
    main()
