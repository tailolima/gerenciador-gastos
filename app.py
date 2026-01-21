#!/usr/bin/env python3
import sqlite3
import sys
from dataclasses import dataclass
from typing import List, Optional
import matplotlib.pyplot as plt

# --- Configurações e Constantes ---
DB_NAME = "finance.db"

# --- Camada de Modelo (Model) ---
@dataclass
class Expense:
    """Representa um registro de despesa no domínio da aplicação."""
    name: str
    amount: float
    id: Optional[int] = None

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("O valor da despesa não pode ser negativo.")

# --- Camada de Acesso a Dados (DAO - Data Access Object) ---
class ExpenseRepository:
    """Gerencia todas as interações com o banco de dados SQLite."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _initialize_db(self) -> None:
        """Garante que a estrutura da tabela exista."""
        query = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL
        )
        """
        with self._get_connection() as conn:
            conn.execute(query)

    def add(self, expense: Expense) -> None:
        query = "INSERT INTO expenses (name, amount) VALUES (?, ?)"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (expense.name, expense.amount))
            expense.id = cursor.lastrowid

    def get_all(self) -> List[Expense]:
        query = "SELECT id, name, amount FROM expenses"
        expenses = []
        with self._get_connection() as conn:
            cursor = conn.execute(query)
            for row in cursor.fetchall():
                # Converte a tupla crua do banco para nosso Objeto Expense
                expenses.append(Expense(id=row[0], name=row[1], amount=row[2]))
        return expenses

    def delete(self, expense_id: int) -> bool:
        query = "DELETE FROM expenses WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.execute(query, (expense_id,))
            return cursor.rowcount > 0

# --- Camada de Serviços (Services/Business Logic) ---
class ChartService:
    """Responsável apenas pela visualização de dados."""
    
    @staticmethod
    def show_pie_chart(expenses: List[Expense]) -> None:
        if not expenses:
            print("⚠️  Não há dados suficientes para gerar analytics.")
            return

        labels = [e.name for e in expenses]
        values = [e.amount for e in expenses]

        plt.figure(figsize=(10, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.title('Distribuição Orçamentária')
        plt.axis('equal')
        
        print("📊 Dashboard gerado. Verifique a janela popup.")
        plt.show()

# --- Camada de Apresentação (CLI/Controller) ---
class ExpenseApp:
    """Controlador principal da interface de linha de comando."""

    def __init__(self):
        self.repository = ExpenseRepository(DB_NAME)
        self.budget_limit = 0.0

    def run(self):
        print("🚀 Inicializando Sistema Financeiro v3.0 (Enterprise Ed.)")
        self._configure_budget()
        
        while True:
            self._show_dashboard_summary()
            self._print_menu()
            
            choice = input(">> Opção: ").strip()
            
            if choice == "1":
                self._handle_add_expense()
            elif choice == "2":
                self._handle_list_expenses()
            elif choice == "3":
                print("\nEncerrando sessão. Até logo.")
                sys.exit(0)
            elif choice == "4":
                self._handle_remove_expense()
            elif choice == "5":
                self._handle_chart()
            else:
                print("❌ Opção desconhecida.")

    def _configure_budget(self):
        while True:
            try:
                # Ajuste: se o usuário der Enter sem nada, assume 100
                raw_input = input("\nDefina seu budget diário (R$) [Padrao: 100]: ").replace(',', '.')
                if not raw_input:
                    self.budget_limit = 100.0
                else:
                    self.budget_limit = float(raw_input)
                break
            except ValueError:
                print("❌ Valor inválido. Use formato numérico (ex: 150.00)")

    def _show_dashboard_summary(self):
        # CORREÇÃO APLICADA AQUI:
        expenses = self.repository.get_all()
        
        total_spent = sum(e.amount for e in expenses)
        balance = self.budget_limit - total_spent
        
        status_icon = "🟢" if balance >= 0 else "🔴 ALERT"
        print(f"\n{'='*40}")
        print(f"💰 BUDGET: R$ {self.budget_limit:.2f} | GASTO: R$ {total_spent:.2f}")
        print(f"📉 SALDO:  R$ {balance:.2f} {status_icon}")
        print(f"{'='*40}")

    def _print_menu(self):
        menu = [
            "1. Registrar Despesa",
            "2. Relatório Detalhado",
            "3. Sair",
            "4. Remover Registro",
            "5. Analytics (Gráfico)"
        ]
        print("\n" + "\n".join(menu))

    def _handle_add_expense(self):
        name = input("Descrição: ")
        try:
            amount_str = input("Valor (R$): ").replace(',', '.')
            amount = float(amount_str)
            expense = Expense(name=name, amount=amount)
            self.repository.add(expense)
            print("✅ Registro persistido com sucesso.")
        except ValueError:
            print("❌ Erro de input: Certifique-se de digitar um número válido.")

    def _handle_list_expenses(self):
        expenses = self.repository.get_all()
        if not expenses:
            print("\n📭 Nenhum registro encontrado.")
            return
            
        print("\n--- Relatório de Despesas ---")
        print(f"{'ID':<5} {'DESCRIÇÃO':<20} {'VALOR'}")
        print("-" * 35)
        for e in expenses:
            print(f"#{e.id:<4} {e.name:<20} R$ {e.amount:.2f}")

    def _handle_remove_expense(self):
        try:
            self._handle_list_expenses()
            input_val = input("\nID para remoção: ")
            if not input_val: return # Se der enter vazio, cancela
            
            id_to_remove = int(input_val)
            
            if self.repository.delete(id_to_remove):
                print(f"✅ Registro #{id_to_remove} removido.")
            else:
                print(f"⚠️ ID #{id_to_remove} não localizado.")
        except ValueError:
            print("❌ ID deve ser um número inteiro.")

    def _handle_chart(self):
        expenses = self.repository.get_all()
        ChartService.show_pie_chart(expenses)

# --- Entry Point ---
if __name__ == "__main__":
    try:
        app = ExpenseApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nInterrupção forçada. Saindo...")
        sys.exit(0)