# 🛠️ Custom C Columnar Database Engine (with B-Tree & Encryption)

> 🚧 **Status:** *Projeto em Desenvolvimento Ativo / Evolução Arquitetural*  
> Este repositório registra o processo contínuo de engenharia e aprendizado de um motor de banco de dados em C puro. O código reflete o estado atual da implementação e a transição planejada para uma arquitetura cliente-servidor desacoplada.

---

## 📌 Visão Geral do Projeto

A **Custom C Database Engine** é um projeto de sistemas de baixo nível projetado para explorar conceitos de armazenamento analítico e relacional. A solução combina layout orientado a colunas, indexação balanceada via **B-Tree** com complexidade de busca em $\mathcal{O}(\log n)$, paginação manual de memória (Buffer Pool) e segurança at-rest com criptografia simétrica via `libsodium` (AES-256).

---

## 🏗️ Arquitetura Atual & Estrutura de Diretórios

O projeto é mantido de forma modular, permitindo acompanhar o histórico de modificações, ferramentas de estresse e protótipos de integração:

```text
C-Btree-column-db/
├── include/              # Cabeçalhos e definições de estruturas (database.h)
├── src/                  # Código-fonte principal em C
│   ├── Motor.c           # Engine principal (atualmente agrupa rotinas de B-Tree, IO e lógica misturada de Cliente/Servidor)
│   ├── Buffer.c          # Gerenciamento de páginas na memória RAM (Buffer Pool)
│   ├── Teste.c           # Suíte de testes unitários de inserção e consulta
│   └── Teste_Estresse.c  # Benchmarking de carga e verificação de concorrência/memória
├── GUI-temp/             # Protótipo de interface e bindings FFI
│   └── mongoldb.py       # Wrapper em Python conectando à biblioteca .so via ctypes
├── data/                 # Arquivos de dados de teste e persistência local
├── historico_v7.txt      # Diário de bordo e histórico incremental de alterações
└── Makefile              # Automação de compilação da biblioteca (.so) e executáveis
```

---

## 🔄 Diagnóstico e Evolução Planejada (`Motor.c`)

Atualmente, o arquivo `Motor.c` funciona como um núcleo monolítico que concentra tanto as estruturas de dados de baixo nível (B-Tree e paginação) quanto as rotinas operacionais que futuramente pertencerão a camadas distintas. 

### Próximos Passos de Refatoração Arquitetural:
1. **Desacoplamento Cliente-Servidor:**
   - Separar o `Motor.c` em um daemon **Servidor** (`server.c`), responsável pela manipulação direta do disco, concorrência e gerenciamento do Buffer Pool.
   - Criar um módulo **Cliente** (`client.c` / CLI) leve, focado em enviar requisições e receber respostas do processo principal via comunicação IPC ou sockets.
2. **Camada de Interface:**
   - Padronizar o *wrapper* Python em `GUI-temp/mongoldb.py` e expandir a interface de linha de comando (CLI).
3. **Refinamento de Buffer:**
   - Implementar algoritmos formais de substituição de páginas (ex: LRU ou Clock) no `Buffer.c`.

---

## 🚀 Funcionalidades Atuais

- **Armazenamento Colunar:** Leitura e gravação direcionada por colunas para otimização de varreduras analíticas.
- **Indexação por B-Tree:** Algoritmos de busca e divisão de nós balanceados em blocos de memória/disco.
- **Buffer Pool e Paginação (`Buffer.c`):** Abstração de controle de memória RAM para cache de páginas antes da escrita.
- **Criptografia At-Rest:** Integração com primitivas criptográficas da `libsodium`.
- **Interoperabilidade Python:** Geração de biblioteca compartilhada nativa (`libmongoldb.so`) consumida via `ctypes`.
- **Suíte de Estresse (`Teste_Estresse.c`):** Scripts de validação de estabilidade sob carga intensiva.

---

## 🛠️ Como Compilar e Executar

### Pré-requisitos
No Linux (Ubuntu / Lubuntu / Debian), instale o GCC, Make e a biblioteca `libsodium`:

```bash
sudo apt update
sudo apt install build-essential libsodium-dev
```

### 1. Compilação
```bash
# Clonar o repositório
git clone git@github.com:3l3tr0st4t1c/custom-c-database-engine.git
cd custom-c-database-engine

# Compilar a biblioteca compartilhada e os testes
make
```

### 2. Testes de Carga em C
```bash
./bin/teste_estresse
```

### 3. Binding de Teste em Python
```bash
python3 GUI-temp/mongoldb.py
```

---

## 📜 Roadmap de Desenvolvimento

- [x] Implementação da estrutura de dados B-Tree
- [x] Módulo de paginação preliminar (`Buffer.c`)
- [x] Integração da criptografia `libsodium`
- [x] Binding nativo com Python via `ctypes`
- [ ] Refatoração do `Motor.c` para desacoplar as rotinas de Cliente e Servidor
- [ ] Implementação do protocolo de comunicação IPC / Sockets
- [ ] Construção de uma CLI/GUI dedicada