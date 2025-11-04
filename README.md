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

```bash
# Teste de adição
python ahmesexec.py soma_ahmes.TXT

# Teste de subtração
python ahmesexec.py sub_ahmes.TXT
```


