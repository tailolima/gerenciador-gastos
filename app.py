import os

# --- Configuração Inicial ---
gastos = []
total_gasto = 0.0
arquivo_banco = "gastos.txt"

# 1. Tenta carregar o "caderninho" antigo (se existir)
if os.path.exists(arquivo_banco):
    print("📂 Carregando gastos anteriores...")
    with open(arquivo_banco, "r") as arquivo:
        for linha in arquivo:
            # Quebra a linha "Cafe,5.0" em nome e valor
            dados = linha.strip().split(",")
            nome_salvo = dados[0]
            valor_salvo = float(dados[1])
            
            # Adiciona na memória do programa
            gastos.append({"nome": nome_salvo, "valor": valor_salvo})
            total_gasto += valor_salvo
else:
    print("🆕 Nenhum registro anterior encontrado. Começando do zero!")

# --- Pergunta o Limite ---
limite = float(input("\nQual é o seu limite diário? R$ "))

# --- Loop Principal ---
while True:
    print(f"\n--- SALDO ATUAL: R$ {limite - total_gasto:.2f} ---")
    print("1. Adicionar novo gasto")
    print("2. Ver lista de gastos")
    print("3. Sair")
    
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("O que você comprou? ")
        valor = float(input("Quanto custou? R$ "))

        # Atualiza a memória
        gastos.append({"nome": nome, "valor": valor})
        total_gasto += valor

        # --- A MÁGICA: Escreve no arquivo txt ---
        # 'a' significa append (adicionar no final)
        with open(arquivo_banco, "a") as arquivo:
            arquivo.write(f"{nome},{valor}\n")
        
        print("✅ Gasto salvo com sucesso!")

    elif opcao == "2":
        print("\n--- Seus Gastos ---")
        for g in gastos:
            print(f"- {g['nome']}: R$ {g['valor']:.2f}")
        print(f"Total gasto: R$ {total_gasto:.2f}")
        input("Pressione Enter para voltar...")

    elif opcao == "3":
        print("Saindo... Seus dados estão seguros! 💾")
        break
    else:
        print("Opção inválida!")