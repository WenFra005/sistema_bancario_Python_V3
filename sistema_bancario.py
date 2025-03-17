"""
Programa que simula um sistema bancário com as seguintes funcionalidades:
- Depósito
- Saque
- Exibir extrato
- Criar usuário
- Criar conta
"""
import textwrap
from datetime import datetime
class Transacao:
    """Classe base para transações bancárias"""
    def __init__(self):
        """Inicializa uma transação com a data e hora atuais"""
        self.data = datetime.now()

    def registrar(self, conta):
        """
        Registra a transação na conta fornecida

        :param conta: A conta onde a transação será registrada
        :type conta: Conta
        """

    def detalhes(self):
        """Retorna os detalhes da transação"""
        return f"Transação em {self.data}"

class Deposito(Transacao):
    """Classe para transações de depósito"""
    def __init__(self, valor):
        """
        Inicializa um depósito com o valor fornecido

        :param valor: O valor do depósito
        :type: float
        """
        super().__init__()
        self.valor = valor

    def registrar(self, conta):
        """
        Registra o depósito na conta fornecida

        :param conta: A conta onde o depósito será registrado
        :type conta: Conta
        """
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)
    def detalhes(self):
        """Retorna os detalhes do depósito"""
        return f"Depósito de R$ {self.valor:.2f} em {self.data}"

class Saque(Transacao):
    """Classe para transações de saque"""
    def __init__(self, valor):
        """
        Inicializa um saque com o valor fornecido

        :param: A conta onde o saque será registrado
        :type valor: float
        """
        super().__init__()
        self.valor = valor

    def registrar(self, conta):
        """
        Registra o saque na conta fornecida, se houver saldo suficiente

        :param conta: A conta onde o saque será registrado
        :type conta: Conta
        :return: True se o saque foi bem-sucedido, False caso contrário
        :rtype: bool
        """
        if conta.saldo >= self.valor:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(self)
            return True
        return False

    def detalhes(self):
        """Retorna os detalhes do saque"""
        return f"Saque de R$ {self.valor:.2f} em {self.data}"

class Historico:
    """Classe para armazenar o histórico de transações de uma conta"""
    def __init__(self):
        """Inicializa um histórico vazio"""
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        """
        Adiciona uma transação ao histórico

        :param transacao: A transação a ser adicionada ao histórico
        :type transacao: Transacao
        """
        self.transacoes.append(transacao)

    def listar_transacoes(self):
        """Lista todas as transações do histórico"""
        return [transacao.detalhes() for transacao in self.transacoes]

class Conta:
    """Classe base para contas bancárias"""
    def __init__(self, numero, cliente, agencia="0001"):
        """Inicializa uma conta com número, cliente e agência fornecidos

        :param numero: O número da conta
        :type numero: int
        :param cliente: O cliente dono da conta
        :type cliente: Cliente
        :param agencia: A agência da conta. Padrão é "0001"
        :type agencia: str, optional
        """
        self.saldo = 0.0
        self.numero = numero
        self.cliente = cliente
        self.agencia = agencia
        self.historico = Historico()

    def sacar(self, valor):
        """Realiza um saque na conta, se houver saldo suficiente

        :param valor: O valor a ser sacado
        :type valor: float
        :return: True se o saque foi bem-sucedido, False caso contrário
        :rtype: bool
        """
        saque = Saque(valor)
        return saque.registrar(self)

    def depositar(self, valor):
        """
        Realiza um depósito na conta

        :param valor: O valor a ser depositado
        :type valor: float
        """
        deposito = Deposito(valor)
        deposito.registrar(self)

class ContaCorrente(Conta):
    """Classe para contas correntes, com limite de saque diário."""
    def __init__(self, cliente, numero, **kwargs):
        """
        Inicializa uma conta-corrente com cliente, número, agência, limite e limite de saques
        diários fornecidos.

        :param cliente: O cliente dono da conta
        :type cliente: Cliente
        :param numero: O número da conta
        :type numero: int
        :param kwargs: Outros parâmetros opcionais (agencia, limite, limite_saques)
        """
        agencia = kwargs.get('agencia', "0001")
        limite = kwargs.get('limite', 1000.0)
        limite_saques = kwargs.get('limite_saques', 3)
        super().__init__(numero, cliente, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_diarios = {"data": datetime.today().date(), "contador": 0}

    def sacar(self, valor):
        """
        Realiza um saque na conta, respeitando o limite diário de saques

        :param valor: O valor a ser sacado
        :type valor: float
        :return: True se o saque foi bem-sucedido, False caso contrário
        :rtype: bool
        """
        if self.saques_diarios["data"] != datetime.today().date():
            self.saques_diarios = {"data": datetime.today().date(), "contador": 0}

        if self.saques_diarios["contador"] >= self.limite_saques:
            print("Limite de saques diários atingido\n")
            return False

        if valor <= self.saldo + self.limite:
            self.saques_diarios["contador"] += 1
            return super().sacar(valor)
        print("Saldo insuficiente\n")
        return False

class Cliente:
    """Classe para clientes do banco"""
    def __init__(self, endereco):
        """
        Inicializa um cliente com o endereço fornecido

        :param endereco: O endereço do cliente
        :type endereco: str
        """
        self.cpf = None
        self.nome = None
        self.nome = None
        self.endereco = endereco
        self.contas = []

    @staticmethod
    def realizar_transacao(conta, transacao):
        """
        Realiza uma transação na conta fornecida

        :param conta: A conta onde a transação será realizada
        :type conta: Conta
        :param transacao: A transação a ser realizada
        :type transacao: Transacao
        """
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """
        Adiciona uma conta ao cliente

        :param conta: A conta a ser adicionada
        :type conta: Conta
        """
        self.contas.append(conta)

class PessoaFisica(Cliente):
    """Classe para clientes do tipo pessoa física"""
    def __init__(self, cpf, nome, data_nascimento, endereco):
        """
        Inicializa um cliente pessoa física com CPF, nome, data de nascimento e endereço
        fornecidos

        :param cpf: O CPF do cliente
        :type cpf: str
        :param nome: O nome do cliente
        :type nome: str
        :param data_nascimento: A data de nascimento do cliente
        :type data_nascimento: str
        :param endereco: O endereço do cliente
        :type endereco: str
        """
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Banco:
    """Classe gerenciar o banco e suas operações"""
    def __init__(self):
        """Inicializa um banco com listas vazias de usuários e contas, e um contador de número de
        contas"""
        self.usuarios = []
        self.contas = []
        self.numero_conta = 0

    def validar_usuario_conta_cpf(self, cpf):
        """
        Valida se um usuário com o CPF fornecido já está cadastrado

        :param cpf: O CPF do usuário
        :type cpf: str
        :return: O usuário encontrado, ou None se não encontrado
        :rtype: Cliente
        """
        return next((usuario for usuario in self.usuarios if usuario.cpf == cpf), None)

    def criar_usuario(self):
        """Cria um novo usuário no banco"""
        cpf = input("Digite o CPF do usuário: ")
        usuario = self.validar_usuario_conta_cpf(cpf)

        if usuario:
            print("Usuário já cadastrado")
            return

        nome = input("Digite o nome do usuário: ")
        data_nascimento = input("Digite a data de nascimento do usuário: ")
        endereco = input(
            "Digite o endereço do usuário (Logradouro, nº - Bairro - Cidade/Sigla do Estado): "
        )

        usuario = PessoaFisica(cpf, nome, data_nascimento, endereco)
        self.usuarios.append(usuario)
        print("Usuário cadastrado com sucesso!\n")

    def criar_conta(self):
        """Cria uma nova conta para um usuário existente"""
        cpf = input("Digite o CPF do usuário: ")
        usuario = self.validar_usuario_conta_cpf(cpf)

        if not usuario:
            print("Usuário não cadastrado")
            return

        self.numero_conta += 1
        conta = ContaCorrente(usuario, self.numero_conta)
        usuario.adicionar_conta(conta)
        self.contas.append(conta)
        print("Conta criada com sucesso!")
        print("Dados da conta".center(25, "="))
        print(f"Agência: {conta.agencia}")
        print(f"Número da conta: {conta.numero}\n")

    @staticmethod
    def exibir_menu():
        """
        Exibe o menu de opções do banco

        :return: A opção escolhida pelo usuário
        :rtype: str
        """
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
        """
        Obtém uma conta pelo número

        :param numero_conta: O número da conta
        :type numero_conta: int
        :return: A conta encontrada, ou None se não encontrada
        :rtype: Conta
        """
        return next((conta for conta in self.contas if conta.numero == numero_conta), None)

    def depositar(self, numero_conta, valor_deposito):
        """
        Realiza um depósito em uma conta

        :param numero_conta: O número da conta
        :type numero_conta: int
        :param valor_deposito: O valor a ser depositado
        :type valor_deposito: float
        """
        conta = self.obter_conta(numero_conta)
        if not conta:
            print("Conta não encontrada\n")
            return

        if valor_deposito <= 0:
            print("Valor inválido\n")
        else:
            conta.depositar(valor_deposito)
            print("Depósito efetuado com sucesso\n")

    def sacar(self, numero_conta, valor_saque):
        """
        Realiza um saque em uma conta

        :param numero_conta: O número da conta
        :type numero_conta: int
        :param valor_saque: O valor a ser sacado
        :type valor_saque: float
        """
        conta = self.obter_conta(numero_conta)
        if not conta:
            print("Conta não encontrada\n")
            return

        if conta.sacar(valor_saque):
            print("Saque efetuado com sucesso\n")
        else:
            print("Saque não efetuado\n")

    def exibir_extrato(self, numero_conta):
        """
        Exibe o extrato de uma conta

        :param numero_conta: O número da conta
        :type numero_conta: int
        """
        conta = self.obter_conta(numero_conta)
        if not conta:
            print("Conta não encontrada\n")
            return

        print("Extrato".center(60, "="))
        print("Dados Pessoais".center(60, "="))
        print(f"Nome: {conta.cliente.nome}")
        print(f"CPF: {conta.cliente.cpf}")
        print(f"Agência: {conta.agencia}")
        print(f"Número da conta: {conta.numero}")
        print("Transações".center(60, "="))

        transacoes_ordernadas = sorted(conta.historico.transacoes, key=lambda t: t.data)
        for transacao in transacoes_ordernadas:
            tipo = "Depósito" if isinstance(transacao, Deposito) else "Saque"
            print(
                f"-> {transacao.data.strftime('%d/%m/%Y %H:%M:%S')} - {tipo} - "
                f"R$ {transacao.valor:.2f}"
            )

        print("Saldo".center(60, "="))
        print(f"R$ {conta.saldo:.2f}")
        print("\n")

    def main(self):
        """Método principal para executar o sistema bancário."""
        while True:
            opcao = self.exibir_menu()
            if opcao == "1":
                numero_conta = int(input("Digite o número da conta: "))
                valor_deposito = float(input("Digite o valor do depósito: "))
                self.depositar(numero_conta, valor_deposito)
            elif opcao == "2":
                numero_conta = int(input("Digite o número da conta: "))
                valor_saque = float(input("Digite o valor do saque: "))
                self.sacar(numero_conta, valor_saque)
            elif opcao == "3":
                numero_conta = int(input("Digite o número da conta: "))
                self.exibir_extrato(numero_conta)
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
