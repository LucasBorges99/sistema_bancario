# Sistema Bancário em Python (POO)
Este projeto implementa um sistema bancário completo utilizando Programação Orientada a Objetos (POO) em Python. O sistema oferece funcionalidades para gerenciar clientes, contas correntes e transações financeiras através de uma interface de terminal intuitiva.
## Funcionalidades Principais
### Gestão de Clientes
- **Criação de usuários**: Cadastro de pessoas físicas com nome, CPF, data de nascimento e endereço
- **Listagem de clientes**: Visualização de todos os clientes cadastrados no sistema
- **Validação de CPF**: Verificação de formato e duplicidade
### Gestão de Contas
- **Criação de contas**: Vinculação de contas correntes a clientes existentes
- **Listagem de contas**: Visualização de todas as contas cadastradas com detalhes
- **Seleção de contas**: Interface para escolher entre múltiplas contas de um cliente
### Operações Bancárias
- **Depósitos**: Adição de fundos à conta corrente
- **Saques**: Retirada de fundos com limites configuráveis
- **Consulta de saldo**: Visualização do saldo atual
- **Extrato bancário**: Histórico completo de transações com data/hora
## Estrutura do Projeto
### Classes Principais
| Classe           | Descrição                                                                 |
|------------------|---------------------------------------------------------------------------|
| `Cliente`        | Classe base para clientes do banco                                        |
| `PessoaFisica`   | Implementação específica para clientes pessoa física (herda de `Cliente`) |
| `Conta`          | Classe base para contas bancárias                                         |
| `ContaCorrente`  | Implementação de conta corrente com limites específicos (herda de `Conta`)|
| `Historico`      | Registro de todas as transações realizadas em uma conta                   |
| `Transacao`      | Classe abstrata base para transações                                      |
| `Saque`          | Implementação específica de transação de saque (herda de `Transacao`)     |
| `Deposito`       | Implementação específica de transação de depósito (herda de `Transacao`)  |
### Funções de Interface
| Função                      | Descrição                                       |
|-----------------------------|-------------------------------------------------|
| `tela_inicio()`             | Exibe o menu principal do sistema               |
| `tela_usuario()`            | Menu de gerenciamento de usuários               |
| `tela_conta()`              | Menu de gerenciamento de contas                 |
| `tela_sessao()`             | Menu de operações bancárias                     |
| `tela_selecao_clientes()`   | Interface para seleção de clientes              |
| `tela_selecao_contas()`     | Interface para seleção de contas                |
### Funções Operacionais
| Função                      | Descrição                                       |
|-----------------------------|-------------------------------------------------|
| `filtrar_cliente()`         | Localiza cliente por CPF                        |
| `listar_clientes()`         | Retorna lista formatada de clientes             |
| `selecionar_clientes()`     | Processa seleção de cliente na interface        |
| `selecionar_conta()`        | Processa seleção de conta na interface          |
| `recuperar_conta_cliente()` | Obtém conta associada a um cliente              |
| `depositar()`               | Executa operação de depósito                    |
| `sacar()`                   | Executa operação de saque                       |
| `exibir_extrato()`          | Mostra histórico de transações e saldo          |
| `criar_cliente()`           | Cadastra novo cliente no sistema                |
| `criar_conta()`             | Cria nova conta corrente                        |
| `listar_contas()`           | Exibe todas as contas cadastradas               |
| `exibir_saldo()`            | Mostra saldo atual da conta                     |
| `validar_valor()`           | Valida valores monetários informados            |
| `valida_cpf()`              | Valida formato e duplicidade de CPF             |
## Pré-requisitos
- Python 3.x instalado
- Nenhuma dependência externa necessária
## Como Executar
1. Salve o código em um arquivo com extensão `.py` (ex: `sistema_bancario.py`)
2. Execute o comando no terminal:
   ```bash
   python app.py
   ```
## Fluxo de Uso
### 1. Menu Principal
```
*** Sistema Bancário ***
Selecione a opção desejada:
[1] Iniciar Sessão
[2] Usuários
[3] Contas
[0] Sair
=>
```
### 2. Menu de Usuários
```
*** Sistema Bancário ***
Selecione a opção desejada:
[1] Criar Usuário
[2] Listar Usuários
[9] Voltar
[0] Sair
=>
```
### 3. Menu de Contas
```
*** Sistema Bancário ***
Selecione a opção desejada:
[1] Criar Conta
[2] Listar Contas
[9] Voltar
[0] Sair
=>
```
### 4. Menu de Operações Bancárias
```
*** Sistema Bancário ***
Selecione a opção desejada:
[1] Depositar
[2] Sacar
[3] Saldo
[4] Extrato
[9] Voltar
[0] Sair
=>
```
## Regras de Negócio
- **Limites de Saque**:
  - Máximo de 3 saques por dia
  - Limite de R$ 500,00 por saque
- **Formato de CPF**:
  - Aceita 11 dígitos (com ou sem pontuação)
  - Verifica duplicidade
- **Formato de Valores**:
  - Aceita valores com ponto ou vírgula como separador decimal
- **Histórico de Transações**:
  - Registra data e hora exata de cada operação
  - Mantém registro permanente durante a sessão
## Exemplos de Operações
### Criação de Cliente
```
Informe o CPF (somente número): 12345678901
Informe o nome completo: João Silva
Informe a data de nascimento (dd-mm-aaaa): 15-05-1990
Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): Rua ABC, 123 - Centro - São Paulo/SP
=== Cliente criado com sucesso! ===
```
### Operação de Depósito
```
*** Sistema Bancário ***
Selecione a opção desejada:
[1] Depositar
[2] Sacar
[3] Saldo
[4] Extrato
[9] Voltar
[0] Sair
=>1
Informe o valor do depósito: 350.50
||| Depósito realizado com sucesso! |||
------------------------------------------------------------
Aperte ENTER para continuar
```
### Extrato Bancário
```
================ EXTRATO ================
Deposito:
	R$ 350.50
Saque:
	R$ 100.00
Saldo:
	R$ 250.50
==========================================
```
## Melhorias Futuras
1. Implementar persistência de dados em arquivo
2. Adicionar sistema de autenticação com senha
3. Implementar operações de transferência entre contas
4. Adicionar diferentes tipos de conta (poupança, investimento)
5. Implementar sistema de tarifas e taxas
6. Desenvolver interface web ou gráfica
## Observações
- O sistema utiliza `os.system("cls")` para limpar o terminal, o que é compatível com Windows
- Para sistemas Linux/macOS, substitua por `os.system("clear")` se necessário
- Todos os dados são armazenados em memória durante a execução do programa
Este projeto demonstra os princípios de Programação Orientada a Objetos aplicados a um sistema bancário real, com separação clara de responsabilidades entre classes e implementação de regras de negócio específicas.