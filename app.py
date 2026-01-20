import os

# Lista para guardar os valores
gastos = []

# Limpando a tela (estética)
os.system('cls' if os.name == 'nt' else 'clear')

print("--------------------------------")
print("💰 CONTROLADOR DE ORÇAMENTO v1.0")
print("--------------------------------")

# Passo 1: Definir o limite
limite = float(input("Qual é o seu limite de gastos para hoje? R$ "))

while True:
    # Mostra o menu
    print("\n--- MENU ---")
    print("1. Adicionar novo gasto")
    print("2. Ver resumo e saldo")
    print("3. Sair")
    
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        valor = float(input("Digite o valor do gasto: R$ "))
        gastos.append(valor)
        print("✅ Gasto registrado!")

    elif opcao == "2":
        total_gasto = sum(gastos)
        saldo_restante = limite - total_gasto
        
        print(f"\n--- RESUMO ---")
        print(f"Total gasto até agora: R$ {total_gasto:.2f}")
        print(f"Limite definido:       R$ {limite:.2f}")
        print("------------------------------")
        
        if saldo_restante > 0:
            print(f"🟢 Você ainda pode gastar: R$ {saldo_restante:.2f}")
        elif saldo_restante == 0:
            print("⚠️ Cuidado! Seu orçamento acabou.")
        else:
            print(f"🔴 ALERTA: Você estourou o orçamento em R$ {abs(saldo_restante):.2f}")

    elif opcao == "3":
        print("Encerrando o sistema...")
        break

    else:
        print("Opção inválida!")