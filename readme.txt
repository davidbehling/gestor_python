```markdown
# 🧮 Gestão Financeira em Python

Este projeto é uma **aplicação de gestão financeira desenvolvida em Python** com interface gráfica usando **Tkinter**. Ele permite organizar receitas, despesas, categorias, usuários e realizar importação/exportação de dados.

O objetivo é servir tanto como ferramenta prática quanto como **estudo/portfólio de Python com interface gráfica e banco de dados local**.


## 📌 Visão Geral

A aplicação oferece funcionalidades como:
- 📊 Dashboard com gráficos e filtros por período e usuário
- 💰 Gestão de **Despesas**
- 💵 Gestão de **Receitas**
- 👤 Cadastro e edição de **Usuários**
- 🏷️ **Categorias** de transações
- 🏦 **Bancos**
- 💳 **Tipos de Pagamentos**
- 📥 **Importação** de CSV
- 📤 **Exportação** de dados


## 🏗️ Estrutura do Projeto

```

gestor_python/
├── components/              # Componentes de interface e lógica separada
├── icons/                   # Ícones e imagens utilizadas (UI)
├── models/                  # Modelos de dados (ORM)
├── public/images/           # Imagens de exemplo exibidas no README
├── repository/              # Repositório de operações com model
├── seeders/                 # Scripts para popular dados iniciais
├── services/                # Serviços de negócio
├── views/                   # Telas e janelas do Tkinter
├── app.py                   # Arquivo principal para iniciar a aplicação
├── create_db.py             # Script para criar a base de dados
├── database.py              # Configuração de conexão com o SQLite
├── global_values.py         # Variáveis globais de configuração
└── dados.db                 # Banco de dados SQLite

````
