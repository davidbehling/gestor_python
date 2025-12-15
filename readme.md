# 🧮 Gestão Financeira em Python

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-1f77b4?style=flat&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=flat&logo=sqlalchemy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Charts-11557c?style=flat&logo=plotly&logoColor=white)
![Status](https://img.shields.io/badge/status-concluído-green?style=flat)
![License](https://img.shields.io/badge/license-MIT-green?style=flat)

Este projeto é uma aplicação de gestão financeira desenvolvida em Python com interface gráfica usando Tkinter. 

Ele permite organizar receitas, despesas, categorias, usuários e realizar importação/exportação de dados.

O objetivo é servir tanto como ferramenta prática quanto como estudo/portfólio de Python com interface gráfica e banco de dados local.


## 📌 Visão Geral
```
A aplicação oferece funcionalidades como:
- 📊 Dashboard com gráficos e filtros por período e usuário
- 💰 Gestão de Despesas
- 💵 Gestão de Receitas
- 👤 Cadastro e edição de Usuários
- 🏷️ Categorias de transações
- 🏦 Bancos
- 💳 Tipos de Pagamentos
- 📥 Importação de CSV
- 📤 Exportação de dados
```

## 🏗️ Arquitetura da Aplicação

Fluxo simplificado da aplicação:

### Interface Principal
```
Menu lateral com ícones de navegação
Frame principal dinâmico que alterna entre as views
Header com título da seção ativa
```
### Dashboard (Tela Inicial)
```
Filtros (datas, usuário, categorias) 
    ↓
dashboard_service.py (cálculos)
    ↓
Visualizações:
  - Resumo financeiro (renda, despesas, saldo)
  - Gráfico de pizza (despesas por categoria)
  - Gráfico de colunas (comparativo mensal)
  - Barra de progresso (% de gastos)
``` 
### Gestão de Transações (Receitas/Despesas)
```
Formulário de entrada
    ↓
transaction_service.py (validação + parcelamento)
    ↓
transaction_repository.py (CRUD)
    ↓
Banco de dados (SQLite)
    ↓
Atualização da Treeview (listagem)
```
### CRUD Padrão (Usuários, Categorias, Bancos, Pagamentos)
```
View com Treeview
    ↓
Ações: Criar / Editar / Excluir
    ↓
Repository específico
    ↓
Banco de dados
    ↓
Refresh da listagem
```
### Camadas da Arquitetura
```
Views (Tkinter UI)
    ↓
Services (Lógica de negócio)
    ↓
Repositories (Acesso a dados)
    ↓
Models (SQLAlchemy ORM)
    ↓
Database (SQLite)
```
### Fluxo de Dados Típico
```
Usuário interage com View
    ↓
View chama Service (se necessário)
    ↓
Service processa lógica e chama Repository
    ↓
Repository executa query no banco via Models
    ↓
Dados retornam pela cadeia inversa
    ↓
View atualiza interface (Treeview, gráficos, labels)
```


## 🏗️ Estrutura do Projeto

```
gestor_python/
├── app.py                          # Aplicação principal Tkinter com menu lateral e sistema de navegação entre views
├── app_teste.py                    # Script de teste para exportação de dados em CSV com seleção de diretório
├── create_db.py                    # Script para criação das tabelas do banco de dados SQLite
├── dados.db                        # Banco de dados SQLite com dados da aplicação
├── database.py                     # Configuração do SQLAlchemy (engine, session e Base)
├── global_values.py                # Constantes globais (dimensões de janelas e frames)
├── readme.txt                      # Documentação com instruções de instalação e execução
│
├── components/                     # Componentes reutilizáveis da interface
│   ├── bar_and_pie_chart.py       # Componente que alterna entre gráfico de barras e pizza
│   ├── multi_select.py             # Componente básico de seleção múltipla
│   ├── mult_select_obj.py          # Primeira versão de combobox com seleção múltipla
│   ├── mult_select_obj_v2.py       # Segunda versão melhorada de combobox com seleção múltipla
│   ├── mult_select_obj_v3.py       # Terceira versão de combobox com seleção múltipla
│   ├── pie_chart.py                # Componente de gráfico de pizza atualizado dinamicamente
│   └── __pycache__/                # Cache Python dos componentes compilados
│
├── icons/                          # Ícones da aplicação (.png)
│
├── models/                         # Modelos SQLAlchemy (ORM)
│   ├── __init__.py                 # Importações dos modelos User, Category, BankAccount, Payment e Transaction
│   ├── bank_account.py             # Modelo de conta bancária com relacionamentos
│   ├── category.py                 # Modelo de categoria (receitas e despesas)
│   ├── payment.py                  # Modelo de tipo de pagamento (Dinheiro, Débito, Crédito, etc.)
│   ├── transaction.py              # Modelo de transação financeira com parcelamento
│   ├── user.py                     # Modelo de usuário do sistema
│   └── __pycache__/                # Cache Python dos modelos compilados
│
├── public/
│   └── images/                     # Imagens públicas da aplicação
│
├── __pycache__/                    # Cache Python dos arquivos principais
│   ├── app.cpython-38.pyc
│   ├── database.cpython-38.pyc
│   └── global_values.cpython-38.pyc
│
├── repository/                     # Camada de acesso a dados (padrão Repository)
│   ├── __init__.py                 # Inicialização do módulo repository
│   ├── bank_account_repository.py  # CRUD e consultas de contas bancárias
│   ├── category_repository.py      # CRUD e consultas de categorias
│   ├── payment_repository.py       # CRUD e consultas de tipos de pagamento
│   ├── transaction_repository.py   # CRUD complexo de transações com filtros e exportação
│   ├── user_repository.py          # CRUD de usuários
│   └── __pycache__/                # Cache Python dos repositories compilados
│
├── seeders/                        # Scripts de população do banco de dados
│   ├── __init__.py                 # Inicialização do módulo seeders
│   ├── clear_tables.py             # Script para limpar todas as tabelas e resetar IDs
│   ├── seed_categories.py          # Popula categorias de receitas e despesas
│   ├── seed_david.py               # Seed personalizado para usuário David com dados completos
│   ├── seed_payments.py            # Popula tipos de pagamento padrão
│   ├── seed_start.py               # Script principal de seed (usuários, categorias, pagamentos, transações)
│   ├── seed_transactions.py        # Popula transações de exemplo para testes
│   ├── seed_users.py               # Cria usuário padrão David
│   └── __pycache__/                # Cache Python dos seeders compilados
│
├── services/                       # Lógica de negócio e utilitários
│   ├── csv_export_service.py       # Exportação de transações para CSV com modelo e headers
│   ├── csv_importer_service.py     # Importação de transações a partir de arquivo CSV
│   ├── dashboard_service.py        # Cálculos para dashboard (porcentagens, totais)
│   ├── tools.py                    # Funções utilitárias (formatação de datas, moeda, validações)
│   ├── transaction_service.py      # Criação de transações com parcelamento e cálculo de vencimentos
│   └── __pycache__/                # Cache Python dos services compilados
│
└── views/                          # Interface gráfica (views Tkinter)
    ├── colors.py                   # Definição de paleta de cores da aplicação
    ├── header.py                   # Componente de cabeçalho reutilizável com ícone e título
    │
    ├── banks/                      # View de gestão de bancos
    │   ├── banks.py                # Interface para CRUD de contas bancárias com filtro por usuário
    │   └── __pycache__/
    │
    ├── categories/                 # View de gestão de categorias
    │   ├── categories.py           # Interface para CRUD de categorias com filtro por tipo
    │   └── __pycache__/
    │
    ├── dashboard/                  # Views do dashboard principal
    │   ├── columns_chart.py        # Gráfico de colunas (Renda, Despesas, Saldo)
    │   ├── dashboard.py            # Dashboard original com gráficos e resumo financeiro
    │   ├── dashboard_new.py        # Nova versão do dashboard com gráficos interativos
    │   ├── percent_progress.py     # Barra de progresso com porcentagem de gastos
    │   ├── pie_chart.py            # Gráfico de pizza de despesas por categoria
    │   ├── search.py               # Filtros de busca (datas, usuários, categorias)
    │   ├── summary_finances.py     # Resumo financeiro textual (total renda, despesas, saldo)
    │   └── __pycache__/
    │
    ├── expenses/                   # View de gestão de despesas
    │   ├── expenses.py             # Interface completa para CRUD de despesas com filtros avançados
    │   └── __pycache__/
    │
    ├── exports/                    # View de exportação de dados
    │   ├── exports.py              # Interface para exportar transações em CSV
    │   └── __pycache__/
    │
    ├── imports/                    # View de importação de dados
    │   ├── imports.py              # Interface para importar transações de CSV
    │   └── __pycache__/
    │
    ├── incomes/                    # View de gestão de receitas
    │   ├── incomes.py              # Interface para CRUD de receitas com filtros
    │   └── __pycache__/
    │
    ├── payments/                   # View de gestão de tipos de pagamento
    │   ├── payments.py             # Interface para CRUD de pagamentos (Débito, Crédito, etc.)
    │   └── __pycache__/
    │
    ├── users/                      # View de gestão de usuários
    │   ├── users.py                # Interface para CRUD de usuários
    │   └── __pycache__/
    │
    └── __pycache__/                # Cache Python das views principais
```

## ⚙️ Tecnologias Utilizadas

### Core
```
Python 3.8+ - Linguagem de programação principal
```
### Interface Gráfica
```
Tkinter - Biblioteca GUI nativa do Python para construção da interface
ttk - Widgets temáticos do Tkinter (Treeview, Combobox, etc.)
```
### Banco de Dados
```
SQLite - Banco de dados relacional leve e local
SQLAlchemy - ORM (Object-Relational Mapping) para manipulação do banco de dados
```
### Visualização de Dados
```
Matplotlib - Geração de gráficos (pizza, barras, colunas)
matplotlib.backends.backend_tkagg - Integração Matplotlib + Tkinter
```
### Componentes e Utilidades
```
Tkcalendar - Widget DateEntry para seleção de datas
Pillow (PIL) - Processamento e manipulação de imagens/ícones
Unidecode - Normalização e remoção de acentos de strings
```
### Formato de Dados
```
CSV - Importação e exportação de transações financeiras
```

## 🚀 Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter o Python 3.x instalado.

### Instalação de Dependências

Execute no terminal:

```bash
pip install pillow matplotlib tkcalendar sqlalchemy unidecode
```

### Criar e Popular Banco de Dados

```bash
python3 create_db.py
python3 seeders/seed_start.py
python3 seeders/seed_david.py
```

### Iniciar a Aplicação

```bash
python3 app.py
```

## 📦 Package / Pacotes

- pip install pillow

- pip install matplotlib

- pip install tkcalendar

- pip install sqlalchemy

- pip install sqlite3

- pip install unidecode


### 🖥️ Tela Inicial (Dashboard - Gráfico de rosca)

![Tela Inicial](https://github.com/davidbehling/gestor_python/blob/main/public/images/01_DashBoard.png)

### 🖥️ Tela Inicial (Dashboard - Gráfico de barras)

![Tela Inicial](https://github.com/davidbehling/gestor_python/blob/main/public/images/01_DashBoard.png)

### 🖥️ Tela de Despesas

![Tela Inicial](https://github.com/davidbehling/gestor_python/blob/main/public/images/03_Despesas.png)

### 🖥️ Tela de Receiras

![Tela Inicial](https://github.com/davidbehling/gestor_python/blob/main/public/images/04_Receitas.png)

### 🖥️ Tela de Usuários

![Tela Inicial](https://github.com/davidbehling/gestor_python/blob/main/public/images/05_Usuarios.png)


### 🖥️ Tela de Categorias

![Tela Inicial](https://github.com/davidbehling/gestor_python/blob/main/public/images/06_Categorias.png)


### 🖥️ Tela de Bancos

![Tela Inicial](https://github.com/davidbehling/gestor_python/blob/main/public/images/07_Bancos.png)


### 🖥️ Tela de Tipos de Pagamentos

![Tela Inicial](https://github.com/davidbehling/gestor_python/blob/main/public/images/08_Tipos_de_pagamento.png)

### 🖥️ Tela de Tipos de Importação

![Tela Inicial](https://github.com/davidbehling/gestor_python/blob/main/public/images/09_Importacao.png)

### 🖥️ Tela de Tipos de Exṕortação

![Tela Inicial](https://github.com/davidbehling/gestor_python/blob/main/public/images/10_Exportacao.png)
