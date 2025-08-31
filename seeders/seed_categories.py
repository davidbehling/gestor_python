from repository.category_repository import create_category

def seed_categories():
    expenses = [
        "Mercado", 
        "Padaria", 
        "Verdureira", 
        "Empório",
        "Suplemento Alimentar",

        "Farmácia",
        "Saúde",

        "Vestuário",
        "Cosmético",
        "Estética",

        "Lanches",
        "Lazer",
        "Viagem",

        "Veterinário",
        "Pet",

        "Crédito Celular",

        "Diversos",
        "Necessário",
        "Desnecessário", 
        "Indefinido",

        "Jogos Prognósticos",
        "Games",
        "Presentes",

        "Pessoal",
        "Cônjuge",        
        "Filhos",
        "Terceiros",
        "Outros",

        "Trabalho Lanches",
        "Trabalho Presentes",
        "Trabalho Outros",            

        "Combustível Carro",
        "Combustível Moto",
        "Mecânica",

        "Locomoção",
        "Estacionamento",

        "Financiamento",
        "Capitalização",
        "Investimento",
        "Poupança",
        "Doação",
        "Saque",
        
        "Imposto",
        "Tarifa",
        "Multa",
        "Seguro",      

        "Serviços",
        "Serviços Pessoal",
        "Serviços Streams",
        "Serviços automotivos",
        "Serviços Casa",
        "Serviços Lazer",
        
        "Casa",
        "Eletronicos",
        "Eletrodomésticos",
        "Móveis"]
    for expense in expenses:
        create_category(expense, True)

    incomes = ["Pagamento", "Férias", "Décimo", "Bonus", "PPR", "Cripto-moeda", "Indefinido", "Terceiros"]
    for income in incomes:
        create_category(income, False)
