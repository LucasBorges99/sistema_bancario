# Sistema Bancário Simples (Terminal)

Este projeto é um sistema bancário desenvolvido em Python para o terminal, criado como desafio do Bootcamp Backend Python da DIO.me. O objetivo é permitir que o usuário realize operações bancárias básicas (depósito, saque, consulta de saldo e extrato), respeitando regras definidas.

---

## 📋 Funcionalidades

- 💰 **Depósito**: aceitar apenas valores positivos e registrar cada operação.
- 🏧 **Saque**: até 3 saques diários, com limite máximo de R$500,00 por saque.
- 📄 **Extrato**: lista completa de depósitos e saques, com valor e saldo após cada operação.
- 💳 **Saldo**: consulta rápida do saldo atual.
- 🔍 **Validações de input**: somente números decimais válidos.

---

## 🚀 Tecnologias e Requisitos

- Python 3.7 ou superior
- Sistema operacional: Windows, macOS ou Linux
- Biblioteca padrão do Python (sem dependências externas)

---

## 📂 Estrutura do Projeto
└── app.py     # Arquivo principal

> **Observação**: todo o código está contido em um único arquivo para simplicidade do desafio.

---

## 🛠️ Como Executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/LucasBorges99/sistema_bancario.git
   cd sistema_bancario
2. Execute o script no terminal:
    ```bash
    python app.py
## 🎯 Modo de Uso

Ao executar, um menu será exibido com as opções:
´´´bash
    *** Sistema Bancário ***

    Selecione a opção desejada:
    [1] Depositar
    [2] Sacar
    [3] Saldo
    [4] Extrato
    [0] Sair

    =>
- 1 - Depositar: digite o valor (ex.: 150.50 ou 150,00 (a validação permite o uso de vírgula no input)).

- 2 - Sacar: solicita valor, verifica saques diários e saldo.

- 3 - Saldo: exibe saldo formatado R$ xxx.xx.

- 4 - Extrato: mostra histórico de transações e saldo final.

- 0 - Sair: encerra o sessão.

Use as setas e o ENTER para navegar.

## ⚙️ Detalhamento das Funções

| Função | Descrição |
|--------|-----------|
| `validar_input(valor: str)` | Verifica se a string é um valor decimal válido. Aceita `.` e `,` como separadores.
| `valida_saques_diarios(saques)` | Garante até 3 saques por dia. Retorna `True` se ainda houver saques disponíveis. |
| `valida_limite_maximo_diario(valor, limite)` | Confere se o valor do saque está entre 0 e o limite diário (R$500,00). |
| `valida_saldo(saldo, valor)` | Confere se o saldo é suficiente para o saque. |
| `depositar(valor, saldo, lancamento)` | Realiza depósito: atualiza saldo, numera lançamento e registra mensagem no extrato. |
| `sacar(valor, saldo, lancamento, saques)` | Executa saque: reduz saldo, incrementa contador de saques e registra histórico. |
| `aperte_para_continuar()` | Exibe uma linha separadora e pausa até o ENTER, para fluxo mais amigável. |

> **Observação:** Todas as operações armazenam mensagens em extrato, incluindo o saldo após a transação.

## 📈 Exemplo de Uso
```=> [1] Depositar  
Digite o valor que deseja depositar...  
=> 200,00  
001 - Deposito realizado no valor de: R$200.00  
-> Saldo após transação: R$200.00

=> [2] Sacar  
Digite o valor que deseja sacar...  
=> 50  
002 - Saque realizado no valor de: R$50.00  
-> Saldo após transação: R$150.00  
Saques disponíveis: 2

=> [4] Extrato
------------------------------------------------------------
                       Extrato Bancário                       
------------------------------------------------------------
001 - Deposito realizado no valor de: R$200.00
-> Saldo após transação: R$200.00
------------------------------------------------------------
002 - Saque realizado no valor de: R$50.00
-> Saldo após transação: R$150.00
------------------------------------------------------------
Saldo Atual: R$150.00
```
## 📚 Boas Práticas Aplicadas

- Validações de entrada para evitar erros de tipo.

- Mensagens claras e formatação consistente.

- Uso de match-case (Python 3.10+) para clareza no menu.

- Separação de responsabilidades em funções.

## 🤝 Contribuições

- Contribuições são bem-vindas! Siga estas etapas:

- Fork deste repositório

- Crie uma branch: `git checkout -b feature/nova-funcionalidade`

- Commit suas alterações: `git commit -m "Adiciona nova feature"`

- Push na branch: `git push origin feature/nova-funcionalidade`

- Abra um Pull Request
