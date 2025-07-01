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

def valida_cpf(cpf: str):
    if ('.' or '-') in cpf:
        cpf = cpf.replace('.', '').replace('-', '')

    if cpf.isdigit() and len(cpf) == 11:
        
        return cpf

    else:
        print(f'CPF {cpf} inválido')
        aperte_para_continuar()

def seleciona_usuario(usuarios: dict|list, contas: dict|list):
    if usuarios:
        lista_usuarios = {str(idx+1): (list(usuario.keys())[0], usuario[list(usuario.keys())[0]]['nome']) for idx, usuario in enumerate(usuarios)}
        
        print('-' * 60)
        print('Selecione um Usuário para iniciar a sessão:\n')
        [print(f'[{u}] {lista_usuarios[u][1]} - {lista_usuarios[u][0]}') for u in lista_usuarios]
        opcao_usuario = input('\n=>')
        
        if opcao_usuario in lista_usuarios.keys():
            usuario = lista_usuarios[opcao_usuario][1]
            cpf = lista_usuarios[opcao_usuario][0]
            contas_usuario = []
            qtde_contas = 0

            for indice, cont in enumerate(contas):
                num_conta = list(cont.keys())[0]
                cpf_conta = cont.get(num_conta).get('cpf')

                if cpf_conta == cpf:
                    indice_conta = indice
                    conta = list(cont.keys())[0]
                    saldo = cont[num_conta]['saldo']
                    saques = cont[num_conta]['saques']
                    lancamento = cont[num_conta]['lancamento']
                    extrato: list = cont[num_conta]['extrato']
                    qtde_contas = qtde_contas + 1
                    contas_usuario.append((indice_conta, str(qtde_contas), conta, saldo, saques, lancamento, extrato))

            if len(contas_usuario) == 1:
                print('-' * 60)
                print(f'Bem Vindo (a) {usuario}')
                print('-' * 60)
                print(f'Iniciando sessão para Agência: 0001 - Conta: {contas_usuario[0][2]}')
                aperte_para_continuar()
                return usuario, indice_conta, conta, saldo, saques, lancamento, extrato
            
            elif len(contas_usuario) > 1:
                print('-' * 60)
                print(f'Selecione a conta que deseja iniciar a sessão: \n')
                [print(f'[{c[1]}] Agência: 0001 - Conta: {c[2]}') for c in contas_usuario]
                opcao_conta = input('\n=>')

                if opcao_conta.isdigit() and (int(opcao_conta) >= 1 and int(opcao_conta) <= qtde_contas):
                    conta_selecionada = [c for c in contas_usuario if c[1] == opcao_conta]
                    indice_conta, _, conta, saldo, saques, lancamento, extrato = tuple(conta_selecionada[0])
                    print('-' * 60)
                    print(f'Bem Vindo (a) {usuario}')
                    print('-' * 60)
                    print(f'Iniciando sessão para Agência: 0001 - Conta: {conta}')
                    aperte_para_continuar()
                    return usuario, indice_conta, conta, saldo, saques, lancamento, extrato

                else:
                    print(f'Opção {opcao_conta} Inválida!')
                    aperte_para_continuar()
                    return None, None, None, None, None, None, None
        else: 
            print(f'Opção {opcao_usuario} Inválida!')
            aperte_para_continuar()
            return None, None, None, None, None, None, None
    else:
        print('Nenhum usuário cadastrado!\nCadastre um usuário no menu Usuários')
        aperte_para_continuar()
        return None, None, None, None, None, None, None

def msg_extrato(operacao: str, lancamento: int, /, *, valor: float, saldo: float, extrato: list):
    msg_operacao = f'{str(lancamento).zfill(3)} - {operacao} realizado no valor de: R${valor:.2f}'
    msg_saldo = f'-> Saldo após transação: R${saldo:.2f}'

    extrato.append(msg_operacao)
    extrato.append(msg_saldo)
    extrato.append('-' * 60)
    print(f'{msg_operacao}\n{msg_saldo}')

def gerar_extrato(conta: str):
    cabecalho_extrato = [
    '-' * 60,
    ' Extrato Bancário '.center(60, '-'),
    '-' * 60,
    f' Agência: 0001 - Conta: {conta} '.center(60, '-'),
    '-' * 60,
    ]
    return cabecalho_extrato

def depositar(valor: str, saldo: float, lancamento: int, extrato: list):
    valor = float(valor)
    saldo += valor
    lancamento += 1

    msg_extrato('Deposito', lancamento, valor=valor, saldo=saldo, extrato=extrato)

    return saldo, lancamento, extrato
    
def sacar(*, valor: str, saldo: float, lancamento: int, saques: int, extrato: list):
    valor = float(valor)
    saldo -= valor
    lancamento += 1
    saques += 1

    msg_extrato('Saque', lancamento, valor=valor, saldo=saldo, extrato=extrato)

    print(f'Saques disponíveis: {LIMITE_SAQUE - saques}')

    return saldo, lancamento, saques, extrato

def criar_usuario(usuarios: dict|list, contas: dict|list):
    cpfs_cadastrados = [list(u.keys())[0] for u in usuarios if usuarios]
    cpf = input('Digite o CPF do Usuário: \n=>')
    cpf_validado = valida_cpf(cpf)

    if cpf_validado:
        if not cpf_validado in cpfs_cadastrados:
            nome = input('Digite o Nome do Usuário: \n=>')
            data_nascimento = input('Digite a data de nascimento do Usuário: \n=>')
            endereco = input('Digite o Endereco do Usuário: \n=>')

            return cpf_validado, nome, data_nascimento, endereco
        else:
            print(f'{cpf_validado} já existe!')
            aperte_para_continuar()
            return None, None, None, None 
    else:
        return None, None, None, None 

def criar_conta(usuario: str, cpf: str, ultima_conta: int):
    conta = str(ultima_conta+1).zfill(3)
    return conta

def aperte_para_continuar():
    print('-' * 60)
    input('Aperte ENTER para continuar')

def menu_sessao(usuario: str, indice_conta: int, conta: str, saldo: float, saques: int, lancamento: int, extrato: list):
    
    while not tela_sessao == 0:
        os.system("cls")
        opcao = input(tela_sessao)

        saldo = contas[indice_conta][conta]['saldo']
        saques = contas[indice_conta][conta]['saques']
        lancamento = contas[indice_conta][conta]['lancamento']
        extrato = contas[indice_conta][conta]['extrato']


        match opcao:
            case '1':

                valor = input('Digite o valor que deseja depositar...\n=>')
                validacao_input, valor = validar_input(valor)
                if validacao_input:
                    if float(valor) > 0:
                        saldo, lancamento, extrato = depositar(valor, saldo, lancamento, extrato)
                        indice = [idx for idx, c in enumerate(contas) if list(c.keys())[0] == conta]

                        contas[indice[0]][conta]['saldo'] = saldo
                        contas[indice[0]][conta]['lancamento'] = lancamento
                        contas[indice[0]][conta]['extrato'] = extrato

                        aperte_para_continuar()
                    else:
                        print('Valor não pode ser negativo ou igual a 0')
                        aperte_para_continuar()

                else:
                    print('Valor preenchido inválido')
                    aperte_para_continuar()

            case '2':
                if valida_saques_diarios(saques):
                    valor = input('Digite o valor que deseja sacar...\n=>')
                    validacao_input, valor = validar_input(valor)
                    if validacao_input:
                        if float(valor) > 0:

                            if valida_limite_maximo_diario(valor, limite_maximo):
                                if valida_saldo(saldo, valor):
                                    saldo, lancamento, saques, extrato = sacar(valor=valor, saldo=saldo, lancamento=lancamento, saques=saques, extrato=extrato)
                                    
                                    indice = [idx for idx, c in enumerate(contas) if list(c.keys())[0] == conta]

                                    contas[indice[0]][conta]['saldo'] = saldo
                                    contas[indice[0]][conta]['lancamento'] = lancamento
                                    contas[indice[0]][conta]['saques'] = saques
                                    contas[indice[0]][conta]['extrato'] = extrato
                                    
                                    aperte_para_continuar()
                                else:
                                    print(f'Saldo insuficiente para realizar saque!\n=> Saldo disponível: R${saldo:.2f}')
                                    aperte_para_continuar()
                            else:
                                print(f'Valor solicitado para saque é maior do que o limite máximo permitido de R${limite_maximo:.2f}')
                                aperte_para_continuar()
                        else:
                            print('Valor não pode ser negativo ou igual a 0')
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
                cabecalho = gerar_extrato(conta)
                [print(lin) for lin in cabecalho]

                [print(l) for l in extrato]
                print(f' Saldo Atual: R${saldo:.2f} '.center(60, '-'))
                aperte_para_continuar()

            case '9':
                os.system("cls")
                break

            case '0':
                os.system("cls")
                exit()

            case _:
                os.system("cls")
                print('-' * 60)
                print("Opção inválida")
                aperte_para_continuar()

    print('Sessão Encerrada')

def menu_usuarios(usuarios: list|dict, contas: list|dict):

    while not tela_usuario == 0:
        os.system("cls")
        opcao = input(tela_usuario)

        usuarios = usuarios
        contas = contas
        ultima_conta = config['ULTIMA_CONTA']

        match opcao:
            case '1':
                cpf, nome, data_nascimento, endereco = criar_usuario(usuarios, contas)

                if all([cpf, nome, data_nascimento, endereco]):
                    usuarios.append(
                        {cpf: {'nome': nome, 'data_nascimento': data_nascimento, 'endereco': endereco}}
                    )

                    conta = str(ultima_conta+1).zfill(3)
                    
                    contas.append({
                        conta: {
                            'agencia': '0001',
                            'usuario': nome,
                            'cpf': cpf,
                            'saldo': 0, 
                            'saques': 0, 
                            'lancamento': 0, 
                            'extrato': []
                        }
                    })
                    config['ULTIMA_CONTA'] = ultima_conta + 1
                    
                    print(f'Usuário {nome} cadastrado com sucesso!')


                    aperte_para_continuar()
                else:
                    print('Digite corretamente todos os campos.')

            case '2':
                if usuarios:
                    for idx, u in enumerate(usuarios):
                        indice = str(idx + 1).zfill(3)
                        cpf = list(u.keys())[0]
                        nome = list(u.values())[0]['nome']
                        data_nascimento = list(u.values())[0]['data_nascimento']
                        endereco = list(u.values())[0]['endereco']
                        contas_usuario = [list(c.keys())[0] for c in contas if list(c.values())[0]['cpf'] == cpf]

                        print(
                            f'Usuário: {indice}\n',
                            f'Nome: {nome}\n',
                            f'CPF: {cpf}\n',
                            f'Data de nascimento: {data_nascimento}\n',
                            f'Endereço: {endereco}\n',
                            f'Contas: {contas_usuario}\n',
                            '-' * 60,'\n'
                        )

                    aperte_para_continuar()
                else:
                    print('Nenhum Usuário cadastrado!')
                    aperte_para_continuar()

            case '9':
                os.system("cls")
                break

            case '0':
                os.system("cls")
                exit()

            case _:
                os.system("cls")
                print('-' * 60)
                print("Opção inválida")
                aperte_para_continuar()

def menu_contas(usuarios: list|dict, contas: list|dict):

    while not tela_conta == 0:

        os.system("cls")
        opcao = input(tela_conta)

        usuarios = usuarios
        contas = contas
        ultima_conta = config['ULTIMA_CONTA']

        match opcao:
            case '1':
                if usuarios:
                    
                    lista_usuarios = {str(idx+1): (list(u.keys())[0], u[list(u.keys())[0]]['nome']) for idx, u in enumerate(usuarios)}

                    print('-' * 60)
                    print('Selecione um Usuário para iniciar a sessão:\n')
                    [print(f'[{u}] {lista_usuarios[u][1]} - {lista_usuarios[u][0]}') for u in lista_usuarios]
                    opcao_usuario = input('\n=>')

                    if opcao_usuario in lista_usuarios.keys():
                        usuario = lista_usuarios[opcao_usuario][1]
                        cpf = lista_usuarios[opcao_usuario][0]

                        conta = str(ultima_conta+1).zfill(3)
                    
                        contas.append({
                            conta: {
                                'agencia': '0001',
                                'usuario': usuario,
                                'cpf': cpf,
                                'saldo': 0, 
                                'saques': 0, 
                                'lancamento': 0, 
                                'extrato': []
                            }
                        })
                        config['ULTIMA_CONTA'] = ultima_conta + 1
                        print(f'Conta {conta} criada para usuário {usuario}')
                        aperte_para_continuar()
                        
                    else: 
                        print('Opção inválida')
                        aperte_para_continuar()
                
                else: 
                    print('Nenhum Usuário cadastrado. \nCadastre um usuário na seção de usuários')
                    aperte_para_continuar()

            case '2':
                if contas:
                    [print(f'Conta: {list(c.keys())[0]}\nCPF: {list(c.values())[0]['cpf']}\n') for c in contas]
                    aperte_para_continuar()
                else:
                    print('Nenhuma conta cadastrada!')
                    aperte_para_continuar()
            
            case '9':
                os.system("cls")
                break

            case '0':
                os.system("cls")
                exit()

            case _:
                os.system("cls")
                print('-' * 60)
                print("Opção inválida")
                aperte_para_continuar()

def menu_inicio(usuarios: list|dict, contas: list|dict):
    
    while not tela_inicio == 0:

        os.system("cls")
        opcao = input(tela_inicio)

        usuarios = usuarios
        contas = contas

        match opcao:
            case '1':
                usuario, indice_conta, conta, saldo, saques, lancamento, extrato = seleciona_usuario(usuarios, contas)
                if usuario and conta:
                    menu_sessao(usuario, indice_conta, conta, saldo, saques, lancamento, extrato)
                
            case '2':
                menu_usuarios(usuarios, contas)

            case '3':
                menu_contas(usuarios, contas)

            case '0':
                os.system("cls")
                exit()

            case _:
                os.system("cls")
                print('-' * 60)
                print("Opção inválida")
                aperte_para_continuar()

tela_inicio = '''*** Sistema Bancário ***

Selecione a opção desejada:

[1] Iniciar Sessão
[2] Usuários
[3] Contas
[0] Sair

=>'''

tela_usuario = '''*** Sistema Bancário ***

Selecione a opção desejada:

[1] Criar Usuário
[2] Listar Usuários
[9] Voltar
[0] Sair

=>'''

tela_conta = '''*** Sistema Bancário ***

Selecione a opção desejada:

[1] Criar Conta
[2] Listar Contas
[9] Voltar
[0] Sair

=>'''

tela_sessao = '''*** Sistema Bancário ***

Selecione a opção desejada:

[1] Depositar
[2] Sacar
[3] Saldo
[4] Extrato
[9] Voltar
[0] Sair

=>'''

config = {'LIMITE_SAQUES_DIARIOS': 3, 'VALOR_MAXIMO_SAQUE': 500, 'ULTIMA_CONTA': 0}

usuarios = [
    # {'12345678910': {'nome': 'Fulano de Tal', 'data_nascimento': '05/08/1990', 'endereco': 'rua dos bobos, 13 - Centro - São Paulo/SP'}},
    # {'78945612320': {'nome': 'Ciclano da Silva', 'data_nascimento': '25/11/1996', 'endereco': 'Rua de trás, 55 - Longe - São Paulo/SP'}},
]

contas = [
    # {'001': {'agencia': '0001', 'usuario': 'Fulano de Tal', 'cpf': '12345678910', 'saldo': 0, 'saques': 0, 'lancamento': 0, 'extrato': []}},
    # {'002': {'agencia': '0001', 'usuario': 'Ciclano da Silva', 'cpf': '78945612320', 'saldo': 0, 'saques': 0, 'lancamento': 0, 'extrato': []}},
    # {'003': {'agencia': '0001', 'usuario': 'Ciclano da Silva', 'cpf': '78945612320', 'saldo': 0, 'saques': 0, 'lancamento': 0, 'extrato': []}},
]

# lancamento = 0
# saldo = 0
# saques = 0
# extrato = [
#     '-' * 60,
#     ' Extrato Bancário '.center(60, '-'),
#     '-' * 60,
#     f' Agência: 0001 - Conta: 001 '.center(60, '-'),
#     '-' * 60,
# ]

limite_maximo = 500
LIMITE_SAQUE = 3
ultima_conta = 0

if __name__ == '__main__':
    menu_inicio(usuarios, contas)