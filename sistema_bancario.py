import textwrap
from datetime import date

class Transacao:
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.saldo >= self.valor:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(self)
            return True
        return False

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.numero_conta = 0

    def validar_usuario_conta_cpf(self, cpf):
        return next((usuario for usuario in self.usuarios if usuario["cpf"] == cpf), None)

    def criar_usuario(self):
        cpf = input("Digite o CPF do usuário: ")
        usuario = self.validar_usuario_conta_cpf(cpf)

        if usuario:
            print("Usuário já cadastrado")
            return

        nome = input("Digite o nome do usuário: ")
        data_nascimento = input("Digite a data de nascimento do usuário: ")
        email = input("Digite o email do usuário: ")
        endereco = input(
            "Digite o endereço do usuário (Logradouro, nº - Bairro - Cidade/Sigla do Estado): "
        )

        self.usuarios.append({
            "cpf": cpf,
            "nome": nome,
            "data_nascimento": data_nascimento,
            "email": email,
            "endereco": endereco
        })
        print("Usuário cadastrado com sucesso")

    def criar_conta(self):
        cpf = input("Digite o CPF do usuário: ")
        usuario = self.validar_usuario_conta_cpf(cpf)

        if not usuario:
            print("Usuário não cadastrado")
            return

        self.numero_conta += 1
        conta = {
            "agencia": "0001",
            "numero_conta": self.numero_conta,
            "usuario": usuario,
            "saldo": 0,
            "extrato": {"depositos": [], "saques": []},
            "saques_diarios": {"data": date.today(), "contador": 0}
        }

        self.contas.append(conta)
        print("Conta criada com sucesso!")
        print("Dados da conta".center(25, "="))
        print(f"Agência: {conta['agencia']}")
        print(f"Número da conta: {conta['numero_conta']}\n")

    @staticmethod
    def exibir_menu():
        menu = """
        1. Depositar
        2. Sacar
        3. Exibir extrato
        4. Criar usuário
        5. Criar conta
        6. Sair

        Escolha uma opção: """
        return input(textwrap.dedent(menu))

    def obter_conta(self, numero_conta):
        return next((conta for conta in self.contas if conta["numero_conta"] == numero_conta), None)

    def depositar(self, numero_conta, valor_deposito):
        conta = self.obter_conta(numero_conta)
        if not conta:
            print("Conta não encontrada\n")
            return

        if valor_deposito <= 0:
            print("Valor inválido\n")
        else:
            conta["saldo"] += valor_deposito
            conta["extrato"]["depositos"].append(valor_deposito)
            print("Depósito efetuado com sucesso\n")

    def sacar(self, *, numero_conta, valor_saque):
        conta = self.obter_conta(numero_conta)
        if not conta:
            print("Conta não encontrada\n")
            return

        if conta["saques_diarios"]["data"] != date.today():
            conta["saques_diarios"] = {"data": date.today(), "contador": 0}

        if conta["saques_diarios"]["contador"] >= 3:
            print("Limite de saques diários atingido\n")
            return

        if valor_saque <= conta["saldo"]:
            conta["saldo"] -= valor_saque
            conta["extrato"]["saques"].append(valor_saque)
            conta["saques_diarios"]["contador"] += 1
            print("Saque efetuado com sucesso\n")
        elif valor_saque > conta["saldo"]:
            print("Saldo insuficiente\n")
        elif valor_saque == 0:
            print("Valor inválido\n")
        else:
            print("Inválido\n")

    def exibir_extrato(self, numero_conta):
        conta = self.obter_conta(numero_conta)
        if not conta:
            print("Conta não encontrada\n")
            return

        print("Extrato".center(25, "="))
        print("Dados Pessoais".center(25, "="))
        print(f"Nome: {conta['usuario']['nome']}")
        print(f"CPF: {conta['usuario']['cpf']}")
        print(f"Agência: {conta['agencia']}")
        print(f"Número da conta: {conta['numero_conta']}")
        print("Depósitos".center(25, "="))
        for i, valor in enumerate(conta["extrato"]["depositos"]):
            print(f"{i + 1}. R$ {valor:.2f}")
        print("Saques".center(25, "="))
        for i, valor in enumerate(conta["extrato"]["saques"]):
            print(f"{i + 1}. R$ {valor:.2f}")
        print("Saldo".center(25, "="))
        print(f"R$ {conta["saldo"]:.2f}")
        print("\n")

    def main(self):
        while True:
            opcao = self.exibir_menu()
            if opcao == "1":
                numero_conta = int(input("Digite o número da conta: "))
                valor_deposito = float(input("Digite o valor do depósito: "))
                self.depositar(numero_conta, valor_deposito)
            elif opcao == "2":
                numero_conta = int(input("Digite o número da conta: "))
                valor_saque = float(input("Digite o valor do saque: "))
                self.sacar(numero_conta=numero_conta, valor_saque=valor_saque)
            elif opcao == "3":
                numero_conta = int(input("Digite o número da conta: "))
                self.exibir_extrato(numero_conta=numero_conta)
            elif opcao == "4":
                self.criar_usuario()
            elif opcao == "5":
                self.criar_conta()
            elif opcao == "6":
                break
            else:
                print("Opção inválida")


if __name__ == "__main__":
    banco = Banco()
    banco.main()