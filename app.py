import sqlite3
import os

# --- FUNÇÕES DE BANCO DE DADOS ---

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
    """Trata o valor e salva no banco"""
    try:
        # Troca vírgula por ponto para o Python entender
        valor_limpo = float(valor_str.replace(',', '.'))
        
        conexao = sqlite3.connect('gastos.db')
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO gastos (nome, valor) VALUES (?, ?)", (nome, valor_limpo))
        conexao.commit()
        conexao.close()
        print("✅ Gasto salvo com sucesso!")
        return True
    except ValueError:
        print("❌ Erro: Valor inválido! Digite apenas números (ex: 10,50).")
        return False

def buscar_gastos():
    """Retorna a lista completa (ID, Nome, Valor) e o total gasto"""
    conexao = sqlite3.connect('gastos.db')
    cursor = conexao.cursor()
    # ATENÇÃO: Agora pegamos também o 'id'
    cursor.execute("SELECT id, nome, valor FROM gastos")
    dados = cursor.fetchall()
    conexao.close()
    
    # Soma o total (o valor é o item[2] agora)
    total = sum([item[2] for item in dados])
    return dados, total

def remover_gasto(id_gasto):
    """Remove um gasto baseado no ID"""
    conexao = sqlite3.connect('gastos.db')
    cursor = conexao.cursor()
    
    # Tenta apagar a linha onde o id é igual ao informado
    cursor.execute("DELETE FROM gastos WHERE id = ?", (id_gasto,))
    
    # Verifica se alguma linha foi afetada (se deletou de verdade)
    linhas_afetadas = cursor.rowcount
    
    conexao.commit()
    conexao.close()

    if linhas_afetadas > 0:
        print(f"✅ Gasto #{id_gasto} removido com sucesso!")
    else:
        print(f"❌ Erro: Não encontrei nenhum gasto com o ID {id_gasto}.")

# --- INÍCIO DO PROGRAMA ---

inicializar_banco()

print("📂 Sistema de Gastos (v2.0) Iniciado...")

# Busca inicial para calcular o saldo
_, total_gasto_inicial = buscar_gastos()

# Pergunta o Limite
try:
    limite_input = input("\nQual é o seu limite diário? R$ ").replace(',', '.')
    limite = float(limite_input)
except ValueError:
    print("Valor inválido. Definindo limite padrão de R$ 100.00")
    limite = 100.0

# --- Loop Principal ---
while True:
    # Atualiza os dados a cada volta do menu
    lista_atual, total_atual = buscar_gastos()
    saldo = limite - total_atual

    print(f"\n--- SALDO RESTANTE: R$ {saldo:.2f} ---")
    if saldo < 0:
        print("⚠️  VOCÊ ESTOUROU O ORÇAMENTO! ⚠️")
    
    print("1. Adicionar gasto")
    print("2. Ver lista (com IDs)")
    print("3. Sair")
    print("4. Remover um gasto") # Nova opção!
    
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("O que você comprou? ")
        valor_texto = input("Quanto custou? R$ ")
        adicionar_gasto(nome, valor_texto)

    elif opcao == "2":
        print("\n--- 📝 Seus Gastos ---")
        if not lista_atual:
            print("Nenhum gasto registrado.")
        else:
            for item in lista_atual:
                # item[0]=ID, item[1]=Nome, item[2]=Valor
                print(f"ID: {item[0]} | {item[1]} - R$ {item[2]:.2f}")
        
        print(f"----------------------")
        print(f"TOTAL GASTO: R$ {total_atual:.2f}")
        input("Pressione Enter para voltar...")

    elif opcao == "3":
        print("Saindo... Até a próxima! 👋")
        break

    elif opcao == "4":
        # Nova funcionalidade de deletar
        try:
            print("\n(Dica: Use a opção 2 para ver os IDs)")
            id_para_apagar = int(input("Digite o número do ID que deseja apagar: "))
            remover_gasto(id_para_apagar)
        except ValueError:
            print("❌ Erro: Digite apenas o número do ID.")

    else:
        print("Opção inválida!")