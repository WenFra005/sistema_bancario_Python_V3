# Sistema Bancário Simples em Python

## Descrição  
Este projeto apresenta um sistema bancário simples desenvolvido inteiramente em Python, no qual os usuários podem realizar as seguintes operações:  
- Criar usuários  
- Criar contas bancárias  
- Depositar valores  
- Sacar valores (com limite diário)  
- Visualizar o extrato de transações  

Os diferentes componentes do projeto são representados como classes dentro de um sistema baseado em programação orientada a objetos (POO). O sistema é composto pelas seguintes classes:

## Estrutura do Projeto

### 1. **Transação**  
Classe base que define todas as transações bancárias. Contém:  
- Atributo `data`, que registra a data e hora da transação.  
- Método `detalhes()`, que retorna as informações sobre a transação.  

### 2. **Depósito (herda de Transação)**  
Classe filha de Transação que representa um depósito. Contém:  
- Atributo `valor`, que armazena o montante depositado.  
- Método `registrar(conta)`, que adiciona o valor ao saldo da conta.  

### 3. **Saque (herda de Transação)**  
Classe filha de Transação que representa um saque. Contém:  
- Atributo `valor`, que armazena o montante retirado.  
- Método `registrar(conta)`, que verifica se há saldo suficiente antes de efetuar o saque.  

### 4. **Histórico**  
Classe responsável por gerenciar o histórico de transações de uma conta. Contém:  
- Lista `transacoes`, onde todas as operações são armazenadas.  
- Método `adicionar_transacao()`, que adiciona novas transações ao histórico.  

### 5. **Conta**  
Classe base para representar contas bancárias. Contém:  
- **Atributos:** `saldo`, `numero`, `cliente`, `agencia` e `historico`.  
- **Métodos:** `sacar(valor)` e `depositar(valor)`.  

### 6. **Conta Corrente (herda de Conta)**  
Classe que representa uma conta corrente, com limites para saque e restrições quanto à quantidade de saques diários. Contém:  
- **Atributos:** `limite`, `limite_saques` e `saques_diarios`.  
- **Método:** `sacar(valor)`, que verifica se o usuário atingiu o limite diário antes de permitir a operação.  

### 7. **Cliente**  
Classe que representa um cliente do banco. Contém:  
- **Atributos:** `cpf`, `nome`, `endereco` e `contas`.  
- **Método:** `adicionar_conta()`, que permite associar contas ao cliente.  

### 8. **Pessoa Física (herda de Cliente)**  
Extensão da classe Cliente para representar uma pessoa física. Contém:  
- **Atributo:** `data_nascimento`.  

### 9. **Banco**  
Classe responsável por gerenciar o funcionamento do banco. Contém:  
- **Listas:** `usuarios` e `contas`.  
- **Métodos** para validar usuários, criar contas, realizar transações e exibir extratos.  
- **Método:** `main()`, que executa o loop principal do programa.  

## Como Executar o Programa  
1. Verifique se você tem o Python instalado (versão 3.x recomendada).  
2. Salve o código em um arquivo Python, como `banco.py`.  
3. Execute o arquivo pelo terminal ou prompt de comando:  

   ```sh  
   python banco.py  
   ```
   
## Funcionalidades do Menu
Ao iniciar o programa, o usuário verá um menu com as seguintes opções:

1. **Depositar** – Solicita o número da conta e o valor do depósito. 
2. **Sacar** – Solicita o número da conta e o valor do saque (respeitando limites e saldo disponível). 
3. **Exibir extrato** – Exibe o histórico de transações e o saldo atual. 
4. **Criar usuário** – Cadastra um novo cliente, solicitando CPF, nome, data de nascimento e endereço. 
5. **Criar conta** – Associa uma nova conta a um usuário já cadastrado. 
6. **Sair** – Encerra a execução do programa.