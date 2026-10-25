# 🛠️ Custom C Columnar Database Engine (with B-Tree & Encryption)

> 🚧 **Status:** *Projeto em Desenvolvimento Ativo / Registro de Evolução Técnica*  
> Este repositório reflete a construção progressiva e iterativa de um motor de banco de dados orientada a colunas feito em C puro, documentando o aprendizado em estruturas de dados avançadas, gerenciamento manual de memória e segurança cibernética.

---

## 📌 Visão Geral do Projeto

A **Custom C Database Engine** é um projeto de sistemas de baixo nível focado na construção de um motor de armazenamento relacional/analítico de alto desempenho. A arquitetura combina armazenamento orientado a colunas para consultas analíticas rápidas, indexação via **B-Tree** para busca eficiente em tempo $\mathcal{O}(\log n)$, gerencimento de memória paginada (Buffer Pool) e camada de segurança *at-rest* via criptografia simétrica (`libsodium` / AES-256).

---

## 🏗️ Arquitetura e Módulos do Sistema

O projeto é organizado de forma modular para demonstrar a separação clara entre o motor nativo, a gestão de buffers, a suíte de testes de estresse e as camadas de abstração superior:

```text
C-Btree-column-db/
├── include/              # Cabecalhos C e definicoes de estruturas de dados (database.h)
├── src/                  # Implementacao nativa da engine em C
│   ├── Motor.c           # Lógica principal da B-Tree e layout de páginas em disco
│   ├── Buffer.c          # Gerenciamento de páginas na memória (Buffer Pool & Eviction)
│   ├── Teste.c           # Testes funcionais das rotinas de inserção/busca
│   └── Teste_Estresse.c  # Suíte de benchmark e testes de estresse sob carga
├── GUI-temp/             # Protótipo de interface e bindings FFI
│   └── mongoldb.py       # Wrapper Python conectando à biblioteca .so via ctypes
├── data/                 # Conjuntos de dados de teste e formatos de persistência
├── historico_v7.txt      # Diário de bordo e registro de alterações de versões anteriores
└── Makefile              # Automação de compilação da biblioteca compartilhada
