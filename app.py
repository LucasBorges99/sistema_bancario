import os

def validar_input(valor: str):
    valor_validado = valor
    if '.' in valor:
        valor_validado = valor.replace('.','')
    elif ',' in valor:
        valor = valor.replace(',', '.')
        valor_validado = valor.replace('.','')
    
    if valor_validado.isdecimal():
        return True, valor
    else:
        return False, '0'

def valida_saques_diarios(saques):
    if not saques >= LIMITE_SAQUE:
        return True
    else:
        return False

def valida_limite_maximo_diario(valor: str, limite_maximo: float):
    if float(valor) > 0 and float(valor) <= limite_maximo:
        return True

def valida_saldo(saldo: float, valor: str):
    valor = float(valor)
    if saldo >= valor:
        return True

def depositar(valor: str, saldo: float, lancamento: int):
    valor = float(valor)
    saldo += valor
    lancamento += 1
    msg_deposito = f'{str(lancamento).zfill(3)} - Deposito realizado no valor de: R${valor:.2f}'
    msg_saldo = f'-> Saldo após transação: R${saldo:.2f}'

    extrato.append(msg_deposito)
    extrato.append(msg_saldo)
    extrato.append('-' * 60)
    print(f'{msg_deposito}\n{msg_saldo}')

    return saldo, lancamento
    
def sacar(valor: str, saldo: float, lancamento: int, saques: int):
    valor = float(valor)
    saldo -= valor
    lancamento += 1
    saques += 1

    msg_saque = f'{str(lancamento).zfill(3)} - Saque realizado no valor de: R${valor:.2f}'
    msg_saldo = f'-> Saldo após transação: R${saldo:.2f}'

    extrato.append(msg_saque)
    extrato.append(msg_saldo)
    extrato.append('-' * 60)
    print(f'{msg_saque}\n{msg_saldo}')
    print(f'Saques disponíveis: {LIMITE_SAQUE - saques}')

    return saldo, lancamento, saques

def aperte_para_continuar():
    print('-' * 60)
    input('Aperte ENTER para continuar')

menu = '''*** Sistema Bancário ***

Selecione a opção desejada:
[1] Depositar
[2] Sacar
[3] Saldo
[4] Extrato
[0] Sair

=>'''

lancamento = 0
saldo = 0
limite_maximo = 500
extrato = [
    '-' * 60,
    ' Extrato Bancário '.center(60, '-'),
    '-' * 60,
]
saques = 0
LIMITE_SAQUE = 3

while not menu == 0:
    os.system("cls")
    opcao = input(menu)

    match opcao:
        case '1':
            valor = input('Digite o valor que deseja depositar...\n=>')
            validacao_input, valor = validar_input(valor)
            if validacao_input:
                saldo, lancamento = depositar(valor, saldo, lancamento)
                aperte_para_continuar()

            else:
                print('Valor preenchido inválido')
                aperte_para_continuar()

        case '2':
            if valida_saques_diarios(saques):
                valor = input('Digite o valor que deseja sacar...\n=>')
                validacao_input, valor = validar_input(valor)
                if validacao_input:
                    if valida_limite_maximo_diario(valor, limite_maximo):
                        if valida_saldo(saldo, valor):
                            saldo, lancamento, saques = sacar(valor, saldo, lancamento, saques)
                            aperte_para_continuar()
                        else:
                            print(f'Saldo insuficiente para realizar saque!\n=> Saldo disponível: R${saldo:.2f}')
                            aperte_para_continuar()
                    else:
                        print(f'Valor solicitado para saque é maior do que o limite máximo permitido de R${limite_maximo:.2f}')
                        aperte_para_continuar()
                else:
                    print('Valor preenchido inválido')
                    aperte_para_continuar()
            else:
                print('Limite de Saques diários expirou. Tente novamente amanhã.')
                aperte_para_continuar()

        case '3':
            print(f"Saldo: R${saldo:.2f}")
            aperte_para_continuar()

        case '4':
            [print(l) for l in extrato]
            print(f'Saldo Atual: R${saldo:.2f}')
            aperte_para_continuar()

        case '0':
            os.system("cls")
            break

        case _:
            os.system("cls")
            print('-' * 60)
            print("Opção inválida")
            aperte_para_continuar()

print('Sessão Encerrada')