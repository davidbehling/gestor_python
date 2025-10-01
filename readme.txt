Estudo focado em Python com tkinter.

Esse projeto tem como base uma aplicação de gestão financeira.

A aplicação as seguinte funcionalidades:

- Dashboard.  
- Receitas
- Usuários
- Categorias
- Bancos
- Tipos de pagamaneto
- Importação
- Exportação


import pdb; pdb.set_trace()

sudo apt-get install python3-tk

pip install pillow

pip install matplotlib

pip install tkcalendar

pip install sqlalchemy

pip install sqlite3

pip install unidecode




python3 create_db.py

python3 seeders/seed_start.py

python3 seeders/seed_david.py




* Dashboard.

= Busca:
- Período de datas;
- Usuário;
- Categoria: Casa, Combustível...

= Gráficos:
- Rosca;
- Barras.

![01_DashBoard](public/images/01_DashBoard.png)

![02_DashBoard](https://github.com/davidbehling/gestor_python/raw/main/public/images/02_DashBoard.png)


* Despesas.

= Ações:
- Adicionar;
- Editar;
- Apagar;
- Pagar: quando crédito ou crediário.

= Filtro:
- Período de datas;
- Usuários;
- Categoria: Casa, Combustível...
- Pagamentos: Débito, Dinheiro...
- Status: Todos, Pago ou Pendente.

![Despesas](https://github.com/davidbehling/gestor_python/blob/main/public/images/03_Despesas.png)


* Receiras.

= Ações:
- Adicionar;
- Editar;
- Apagar.

= Filtro:
- Período de datas
- Usuários
- Categoria: Casa, Combustível...
- Pagamentos: Débito, Dinheiro...

![Despesas](https://github.com/davidbehling/gestor_python/blob/main/public/images/04_Receitas.png)


* Usuários.

= Ações:
- Adicionar;
- Editar;
- Apagar.

![Despesas](https://github.com/davidbehling/gestor_python/blob/main/public/images/05_Usuarios.png)


* Categorias.

= Ações:
- Adicionar;
- Editar;
- Apagar.

= Filtro:
- Todos, Despesa ou Receita.

![Despesas](https://github.com/davidbehling/gestor_python/blob/main/public/images/06_Categorias.png)


* Bancos.

= Ações:
- Adicionar;
- Editar;
- Apagar.

![Despesas](https://github.com/davidbehling/gestor_python/blob/main/public/images/07_Bancos.png)


* Tipo de Pagamentos.

= Ações:
- Adicionar;
- Editar;
- Apagar.

= Filtro:
- Usuário.

![Despesas](https://github.com/davidbehling/gestor_python/blob/main/public/images/08_Tipos_de_pagamento.png)


* Importação.

Importação csv por usuário de acordo com o modelo.

![Despesas](https://github.com/davidbehling/gestor_python/blob/main/public/images/09_Importacao.png)


* Exportação.

Exportação csv por usuário.

![Despesas](https://github.com/davidbehling/gestor_python/blob/main/public/images/10_Exportacao.png)
