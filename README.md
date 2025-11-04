# Simulador AHMES

Simulador da máquina hipotética AHMES implementado em Python, baseado no simulador Neander do Prof. Dr. Marcello Batista Ribeiro.

## Estrutura do Projeto

- `compAhmesTXT.py` - Compilador que converte arquivos de memória para formato executável
- `exeprogAhmes.py` - Simulador/executor que executa programas AHMES
- `ahmesexec.py` - Script que automatiza compilação e execução
- `soma_ahmes.TXT` - Exemplo de programa que soma dois números

## Instruções do AHMES

| Código | Instrução | Descrição |
|--------|-----------|-----------|
| 0000 xxxx | NOP | Nenhuma operação |
| 0001 xxxx | STA end | Armazena acumulador no endereço "end" |
| 0010 xxxx | LDA end | Carrega acumulador com conteúdo do endereço "end" |
| 0011 xxxx | ADD end | Soma conteúdo do endereço "end" ao acumulador |
| 0100 xxxx | OR end | Operação lógica OU |
| 0101 xxxx | AND end | Operação lógica E |
| 0110 xxxx | NOT | Inverte todos os bits do acumulador |
| 0111 xxxx | SUB end | Subtrai conteúdo do endereço "end" do acumulador |
| 1000 xxxx | JMP end | Desvio incondicional para "end" |
| 1001 00xx | JN end | Desvio se N=1 (Negative) |
| 1001 01xx | JP end | Desvio se N=0 (Positive) |
| 1001 10xx | JV end | Desvio se V=1 (Overflow) |
| 1001 11xx | JNV end | Desvio se V=0 (No Overflow) |
| 1010 00xx | JZ end | Desvio se Z=1 (Zero) |
| 1010 01xx | JNZ end | Desvio se Z=0 (Not Zero) |
| 1011 00xx | JC end | Desvio se C=1 (Carry) |
| 1011 01xx | JNC end | Desvio se C=0 (No Carry) |
| 1011 10xx | JB end | Desvio se B=1 (Borrow) |
| 1011 11xx | JNB end | Desvio se B=0 (No Borrow) |
| 1110 xx00 | SHR | Desloca acumulador para direita |
| 1110 xx01 | SHL | Desloca acumulador para esquerda |
| 1110 xx10 | ROR | Gira acumulador para direita |
| 1110 xx11 | ROL | Gira acumulador para esquerda |
| 1111 xxxx | HLT | Para a execução |

## Flags do AHMES

- **N** (Negative): Bit mais significativo do resultado
- **Z** (Zero): Resultado é zero
- **V** (Overflow): Overflow em operações aritméticas
- **C** (Carry): Carry de operações aritméticas ou deslocamentos
- **B** (Borrow): Borrow de subtrações

## Como Usar

### Compilação e Execução Manual

1. **Compilar um programa:**
   ```bash
   python compAhmesTXT.py arquivo_entrada.TXT
   ```

2. **Executar o programa:**
   ```bash
   python exeprogAhmes.py
   ```

### Compilação e Execução Automática

```bash
python ahmesexec.py arquivo_entrada.TXT
```

### Formato do Arquivo de Entrada

O arquivo de entrada deve seguir o formato:
```
  0   32 129   LDA 129
  2   48 128   ADD 128
  4   16 131   STA 131
  6  240       HLT
```

Onde:
- Primeira coluna: endereço de memória
- Segunda coluna: código da instrução (opcode)
- Terceira coluna: operando (se a instrução requerer)
- Última coluna: nome da instrução e operando

## Exemplo: Soma de Dois Números

O arquivo `soma_ahmes.TXT` contém um programa que:
1. Carrega o valor do endereço 129 (4) no acumulador
2. Soma com o valor do endereço 128 (126)
3. Armazena o resultado (130) no endereço 131
4. Para a execução

Para executar:
```bash
python ahmesexec.py soma_ahmes.TXT
```

## Arquitetura da Máquina AHMES

- **Memória**: 256 posições (0-255)
- **Acumulador (AC)**: Registrador de 8 bits
- **Contador de Programa (PC)**: Aponta para próxima instrução
- **Flags**: N, Z, V, C, B

## Diferenças em relação ao Neander

O AHMES possui:
- Mais instruções de desvio condicional (JP, JV, JNV, JNZ, JC, JNC, JB, JNB)
- Instrução SUB (subtração)
- Instruções de deslocamento e rotação (SHR, SHL, ROR, ROL)
- Mais flags (V para overflow, C para carry, B para borrow)

## Arquivos de Teste

O projeto inclui vários arquivos de teste para validar diferentes funcionalidades do simulador:

### Arquivos de Teste Disponíveis

1. **`soma_ahmes.TXT`** - Teste básico (5 + 4 = 9)
2. **`sub_ahmes.TXT`** - Testes de subtração (10-3, 10-5, 10-10)
3. **`overflow_ahmes.TXT`** - Testes de overflow e carry em adições
4. **`logicas_ahmes.TXT`** - Testes de operações lógicas (AND, OR, NOT)
5. **`desvios_ahmes.TXT`** - Testes de desvios condicionais (JZ, JNZ, JN, JP)
6. **`shift_ahmes.TXT`** - Testes de deslocamentos (SHL, SHR, ROL, ROR)
7. **`negativo_ahmes.TXT`** - Testes com números negativos e flag N

### Executando os Testes

```bash
# Teste básico
python ahmesexec.py soma_ahmes.TXT

# Testes de subtração
python ahmesexec.py sub_ahmes.TXT

# Testes de overflow (valida flags C e V)
python ahmesexec.py overflow_ahmes.TXT

# Testes de operações lógicas
python ahmesexec.py logicas_ahmes.TXT

# Testes de desvios condicionais
python ahmesexec.py desvios_ahmes.TXT

# Testes de deslocamentos e rotações
python ahmesexec.py shift_ahmes.TXT

# Testes com números negativos (complemento de 2)
python ahmesexec.py negativo_ahmes.TXT
```

### O Que Cada Teste Valida

- **sub_ahmes.TXT**: Subtrações normais e resultado zero
- **overflow_ahmes.TXT**: Flags C (carry) e V (overflow), wraparound em 255
- **logicas_ahmes.TXT**: Operações bit a bit e flag Z
- **desvios_ahmes.TXT**: Desvios baseados em flags Z e N
- **shift_ahmes.TXT**: Deslocamentos, rotações e flag C
- **negativo_ahmes.TXT**: Representação em complemento de 2 e flag N

### Valores Importantes para Testes

- **Overflow**: 200 + 56 = 256 → 0 (C=1), 127 + 1 = 128 (V=1, N=1)
- **Negativos**: 255 = -1, 254 = -2, 128 = -128 (complemento de 2)
- **Operações lógicas**: 170 AND 255 = 170, NOT 170 = 85
- **Deslocamentos**: 1 SHL = 2, 128 SHL = 0 (C=1)
