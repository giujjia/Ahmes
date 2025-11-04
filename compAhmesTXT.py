#Compilador AHMES - Converte arquivos de memória do AHMES para formato executável
import sys
import re

# Mapeamento de códigos de instrução AHMES (em decimal)
# Os valores base são os menores valores em cada faixa
INSTRUCTION_CODES = {
    'NOP': 0,
    'STA': 16,
    'LDA': 32,
    'ADD': 48,
    'OR': 64,
    'AND': 80,
    'NOT': 96,
    'SUB': 112,
    'JMP': 128,
    'JN': 144,
    'JP': 148,
    'JV': 152,
    'JNV': 156,
    'JZ': 160,
    'JNZ': 164,
    'JC': 168,
    'JNC': 172,
    'JB': 176,
    'JNB': 180,
    'SHR': 224,  # 1110 xx00
    'SHL': 225,  # 1110 xx01
    'ROR': 226,  # 1110 xx10
    'ROL': 227,  # 1110 xx11
    'HLT': 240,
}

def parse_line(line):
    """
    Parse uma linha do formato:
      0   32 129   LDA 129
    Retorna: (endereco, opcode, operando, nome_instrucao)
    """
    line = line.strip()
    if not line:
        return None
    
    # Remove espaços extras
    parts = re.split(r'\s+', line)
    
    if len(parts) < 2:
        return None
    
    try:
        endereco = int(parts[0])
    except ValueError:
        return None
    
    # Tenta extrair o opcode (geralmente na segunda ou terceira posição)
    opcode = None
    operando = None
    nome_inst = None
    
    # Procura por números que são opcodes válidos
    for i in range(1, len(parts)):
        try:
            val = int(parts[i])
            # Verifica se é um opcode válido (0-255)
            if 0 <= val <= 255:
                if opcode is None:
                    opcode = val
                elif operando is None and i > 1:  # operando vem depois do opcode
                    operando = val
        except ValueError:
            # Provavelmente é o nome da instrução
            if nome_inst is None:
                nome_inst = parts[i].upper()
    
    # Se não encontrou operando mas há mais números, usa o próximo
    if operando is None and len(parts) > 2:
        for part in parts[2:]:
            try:
                operando = int(part)
                break
            except ValueError:
                continue
    
    return (endereco, opcode, operando, nome_inst)

def main():
    if len(sys.argv) < 2:
        print("Uso: python compAhmesTXT.py <arquivo_entrada>")
        sys.exit(1)
    
    arquivo_entrada = sys.argv[1]
    
    # Inicializa memória
    mem = [0] * 256
    
    # Lê o arquivo de entrada
    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as fp:
            lines = fp.readlines()
    except FileNotFoundError:
        print(f"O arquivo {arquivo_entrada} não pode ser aberto.")
        sys.exit(1)
    
    # Processa cada linha
    for line in lines:
        parsed = parse_line(line)
        if parsed is None:
            continue
        
        endereco, opcode, operando, nome_inst = parsed
        
        if endereco < 0 or endereco >= 256:
            continue
        
        # Se tem opcode, usa ele
        if opcode is not None:
            mem[endereco] = opcode
            # Se a instrução requer operando, coloca na próxima posição
            if operando is not None:
                if endereco + 1 < 256:
                    mem[endereco + 1] = operando
        # Se não tem opcode mas tem nome da instrução, tenta converter
        elif nome_inst and nome_inst in INSTRUCTION_CODES:
            opcode = INSTRUCTION_CODES[nome_inst]
            mem[endereco] = opcode
            # Instruções que requerem operando
            if nome_inst not in ['NOP', 'NOT', 'SHR', 'SHL', 'ROR', 'ROL', 'HLT']:
                if operando is not None and endereco + 1 < 256:
                    mem[endereco + 1] = operando
    
    # Gera arquivo mem.txt
    try:
        with open("mem.txt", "w") as fp:
            for i in range(256):
                fp.write(f"{mem[i]}\n")
    except Exception as e:
        print(f"Erro ao escrever mem.txt: {e}")
        sys.exit(1)
    
    # Gera arquivo ST.h (código assembler)
    try:
        with open("ST.h", "w") as fp:
            programa = True
            
            i = 0
            while i < 256:
                opcode = mem[i]
                
                if opcode == 240:  # HLT
                    fp.write(f"l{i}:  HLT")
                    programa = False
                    break
                
                if not programa:
                    break
                
                # Instruções com operando (2 bytes)
                if 16 <= opcode <= 31:  # STA
                    if i + 1 < 256:
                        fp.write(f"l{i}:  STA({mem[i+1]})\n")
                        i += 1
                elif 32 <= opcode <= 47:  # LDA
                    if i + 1 < 256:
                        fp.write(f"l{i}:  LDA({mem[i+1]})\n")
                        i += 1
                elif 48 <= opcode <= 63:  # ADD
                    if i + 1 < 256:
                        fp.write(f"l{i}:  ADD({mem[i+1]})\n")
                        i += 1
                elif 64 <= opcode <= 79:  # OR
                    if i + 1 < 256:
                        fp.write(f"l{i}:  OR({mem[i+1]})\n")
                        i += 1
                elif 80 <= opcode <= 95:  # AND
                    if i + 1 < 256:
                        fp.write(f"l{i}:  AND({mem[i+1]})\n")
                        i += 1
                elif 112 <= opcode <= 127:  # SUB
                    if i + 1 < 256:
                        fp.write(f"l{i}:  SUB({mem[i+1]})\n")
                        i += 1
                elif 128 <= opcode <= 143:  # JMP
                    if i + 1 < 256:
                        fp.write(f"l{i}:  JMP(l{mem[i+1]})\n")
                        i += 1
                elif 144 <= opcode <= 147:  # JN
                    if i + 1 < 256:
                        fp.write(f"l{i}:  JN(l{mem[i+1]})\n")
                        i += 1
                elif 148 <= opcode <= 151:  # JP
                    if i + 1 < 256:
                        fp.write(f"l{i}:  JP(l{mem[i+1]})\n")
                        i += 1
                elif 152 <= opcode <= 155:  # JV
                    if i + 1 < 256:
                        fp.write(f"l{i}:  JV(l{mem[i+1]})\n")
                        i += 1
                elif 156 <= opcode <= 159:  # JNV
                    if i + 1 < 256:
                        fp.write(f"l{i}:  JNV(l{mem[i+1]})\n")
                        i += 1
                elif 160 <= opcode <= 163:  # JZ
                    if i + 1 < 256:
                        fp.write(f"l{i}:  JZ(l{mem[i+1]})\n")
                        i += 1
                elif 164 <= opcode <= 167:  # JNZ
                    if i + 1 < 256:
                        fp.write(f"l{i}:  JNZ(l{mem[i+1]})\n")
                        i += 1
                elif 168 <= opcode <= 171:  # JC
                    if i + 1 < 256:
                        fp.write(f"l{i}:  JC(l{mem[i+1]})\n")
                        i += 1
                elif 172 <= opcode <= 175:  # JNC
                    if i + 1 < 256:
                        fp.write(f"l{i}:  JNC(l{mem[i+1]})\n")
                        i += 1
                elif 176 <= opcode <= 179:  # JB
                    if i + 1 < 256:
                        fp.write(f"l{i}:  JB(l{mem[i+1]})\n")
                        i += 1
                elif 180 <= opcode <= 183:  # JNB
                    if i + 1 < 256:
                        fp.write(f"l{i}:  JNB(l{mem[i+1]})\n")
                        i += 1
                
                # Instruções sem operando (1 byte)
                elif opcode == 0:  # NOP
                    fp.write(f"l{i}:  NOP\n")
                elif 96 <= opcode <= 111:  # NOT
                    fp.write(f"l{i}:  NOT\n")
                elif opcode in [224, 228, 232, 236]:  # SHR
                    fp.write(f"l{i}:  SHR\n")
                elif opcode in [225, 229, 233, 237]:  # SHL
                    fp.write(f"l{i}:  SHL\n")
                elif opcode in [226, 230, 234, 238]:  # ROR
                    fp.write(f"l{i}:  ROR\n")
                elif opcode in [227, 231, 235, 239]:  # ROL
                    fp.write(f"l{i}:  ROL\n")
                
                i += 1
                
    except Exception as e:
        print(f"Erro ao escrever ST.h: {e}")
        sys.exit(1)
    
    print("O arquivo novo aberto com sucesso.")

if __name__ == "__main__":
    main()
