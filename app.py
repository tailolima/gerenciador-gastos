import sqlite3
import os

# --- FUNÇÕES DE BANCO DE DADOS (O "Motor" do app) ---

def inicializar_banco():
    """Cria a tabela e o arquivo .db se não existirem"""
    conexao = sqlite3.connect('gastos.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor REAL NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

def adicionar_gasto(nome, valor_str):
    """Trata o valor (troca vírgula por ponto) e salva no banco"""
    try:
        # Tratamento: troca vírgula por ponto para o Python entender
        valor_limpo = float(valor_str.replace(',', '.'))
        
        conexao = sqlite3.connect('gastos.db')
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO gastos (nome, valor) VALUES (?, ?)", (nome, valor_limpo))
        conexao.commit()
        conexao.close()
        print("✅ Gasto salvo com segurança no Banco de Dados!")
        return True
    except ValueError:
        print("❌ Erro: Valor inválido! Digite apenas números (ex: 10,50).")
        return False

def buscar_gastos():
    """Retorna a lista completa e o total gasto"""
    conexao = sqlite3.connect('gastos.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, valor FROM gastos")
    dados = cursor.fetchall()
    conexao.close()
    
    # Calcula o total somando a coluna de valores
    total = sum([item[1] for item in dados])
    return dados, total

# --- INÍCIO DO PROGRAMA ---

inicializar_banco()

print("📂 Sistema de Gastos com SQLite Iniciado...")

# Pega o total atual do banco para começar o dia certo
_, total_gasto_inicial = buscar_gastos()

# --- Pergunta o Limite ---
try:
    limite_input = input("\nQual é o seu limite diário? R$ ").replace(',', '.')
    limite = float(limite_input)
except ValueError:
    print("Valor inválido. Definindo limite padrão de R$ 100.00")
    limite = 100.0

# --- Loop Principal ---
while True:
    # Recalcula o total atualizado direto do banco
    lista_atual, total_atual = buscar_gastos()
    saldo = limite - total_atual

    print(f"\n--- SALDO RESTANTE: R$ {saldo:.2f} ---")
    if saldo < 0:
        print("⚠️  ATENÇÃO: VOCÊ ESTOUROU O ORÇAMENTO! ⚠️")
    
    print("1. Adicionar novo gasto")
    print("2. Ver lista de gastos")
    print("3. Sair")
    
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("O que você comprou? ")
        # Agora lemos como TEXTO (input puro) para tratar a vírgula depois
        valor_texto = input("Quanto custou? R$ ")
        
        adicionar_gasto(nome, valor_texto)

    elif opcao == "2":
        print("\n--- 📝 Histórico de Gastos (Do Banco de Dados) ---")
        if not lista_atual:
            print("Nenhum gasto registrado ainda.")
        else:
            for item in lista_atual:
                # item[0] é o nome, item[1] é o valor
                print(f"- {item[0]}: R$ {item[1]:.2f}")
        
        print(f"----------------------")
        print(f"TOTAL GASTO: R$ {total_atual:.2f}")
        input("Pressione Enter para voltar...")

    elif opcao == "3":
        print("Saindo... Seus dados estão salvos no arquivo 'gastos.db'! 💾")
        break
    else:
        print("Opção inválida!")