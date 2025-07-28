import textwrap
import os
from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n||| Saque realizado com sucesso! |||")
            aperte_para_continuar()
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n||| Depósito realizado com sucesso! |||")
            aperte_para_continuar()
        else:
            print("\n@@@ Operação falhou! O Valor informado é inválido. @@@")

            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [
                transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__
            ]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            aperte_para_continuar()

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido")
            aperte_para_continuar()

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{str(self.numero).zfill(3)}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def tela_inicio():
    tela_inicio = '''*** Sistema Bancário ***

Selecione a opção desejada:

[1] Iniciar Sessão
[2] Usuários
[3] Contas
[0] Sair

=>'''
    return input(textwrap.dedent(tela_inicio))

def tela_usuario():
    tela_usuario = '''*** Sistema Bancário ***

Selecione a opção desejada:

[1] Criar Usuário
[2] Listar Usuários
[9] Voltar
[0] Sair

=>'''
    return input(textwrap.dedent(tela_usuario))

def tela_conta():
    tela_conta = '''*** Sistema Bancário ***

Selecione a opção desejada:

[1] Criar Conta
[2] Listar Contas
[9] Voltar
[0] Sair

=>'''
    return input(textwrap.dedent(tela_conta))

def tela_sessao():
    tela_sessao = '''*** Sistema Bancário ***

Selecione a opção desejada:

[1] Depositar
[2] Sacar
[3] Saldo
[4] Extrato
[9] Voltar
[0] Sair

=>'''
    return input(textwrap.dedent(tela_sessao))

def tela_selecao_clientes(selecao_clientes):
    opcoes_clientes = [f'[{cliente[0]}] {cliente[1]} - Cliente: {cliente[2]} - CPF: {cliente[3]}' for cliente in selecao_clientes]
    
    tela_selecao_clientes = f'''*** Sistema Bancário ***

Selecione o cliente:

{'\n'.join(opcoes_clientes)}

=>'''
    return input(textwrap.dedent(tela_selecao_clientes))

def tela_selecao_contas(selecao_contas):
    opcoes_contas = [f'[{conta[0]}] Conta: {conta[1]} - Saldo: {conta[2]}' for conta in selecao_contas]
    
    tela_selecao_contas = f'''*** Sistema Bancário ***

Selecione a conta:

{'\n'.join(opcoes_contas)}

=>'''
    return input(textwrap.dedent(tela_selecao_contas))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def listar_clientes(clientes):
    lista_clientes = [f'{str(i+1).zfill(3)} - {cliente.nome} - {cliente.cpf} - {[str(conta.numero).zfill(3) for conta in cliente.contas]}' for i, cliente in enumerate(clientes)]

    return lista_clientes if lista_clientes else None

def selecionar_clientes(clientes):
    selecao_clientes = [(str(i+1), str(i+1).zfill(3), cliente.nome, cliente.cpf) for i, cliente in enumerate(clientes)]
    if selecao_clientes:
        opcoes = [list(opcao[0])[0] for opcao in selecao_clientes]
        opcao_cliente = tela_selecao_clientes(selecao_clientes)
        if opcao_cliente in opcoes:
            cpf = list([opcao[3] for opcao in selecao_clientes if opcao[0] == opcao_cliente])[0]
            return cpf

        else:
            print('\n@@@ Opção inválida! @@@')
            aperte_para_continuar()
            return False

    else:
        print("\n@@@ Nenhum Cliente cadastrado. \nCadastre um cliente primeiro")
        aperte_para_continuar()
        return False

def selecionar_conta(cliente):
    selecao_contas = [(str(i+1), str(conta.numero).zfill(3), conta.saldo) for i, conta in enumerate(cliente.contas)]
    if selecao_contas:
        opcoes = [list(opcao[0])[0] for opcao in selecao_contas]
        opcao_conta = tela_selecao_contas(selecao_contas)
        if opcao_conta in opcoes:
            conta = cliente.contas[int(opcao_conta) - 1]
            print(f'Conta: {str(conta.numero).zfill(3)} selecionada!')
            aperte_para_continuar()
            return conta
        else:
            print('\n@@@ Opção inválida! @@@')
            aperte_para_continuar()
            return False
    else:
        print("\n@@@ Nenhuma conta cadastrada. \nCadastre uma conta.")
        aperte_para_continuar()
        return False

def recuperar_conta_cliente(cliente):
    os.system("cls")
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    elif len(cliente.contas) == 1:
        print(f'Conta: {str(cliente.contas[0].numero).zfill(3)} selecionada!')
        aperte_para_continuar()
        return cliente.contas[0]
    
    else:
        conta = selecionar_conta(cliente)
        return conta
    
def depositar(cliente, conta, clientes, contas):
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = input("Informe o valor do depósito: ")
    valor_validado, valor = validar_valor(valor)
    if valor_validado:
        valor = float(valor)
        transacao = Deposito(valor)

        if not conta:
            return

        cliente.realizar_transacao(conta, transacao)

        return clientes, contas, cliente, conta

    else:
        print('\n@@@ Valor informado inválido! @@@')
        aperte_para_continuar()
        return clientes, contas, cliente, conta

def sacar(cliente, conta, clientes, contas):
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = input("Informe o valor do saque: ")
    valor_validado, valor = validar_valor(valor)
    if valor_validado:
        valor = float(valor)
        transacao = Saque(valor)

        if not conta:
            return

        cliente.realizar_transacao(conta, transacao)
        return clientes, contas, cliente, conta
    else:
        print('\n@@@ Valor informado inválido!')
        aperte_para_continuar()
        return clientes, contas, cliente, conta

def exibir_extrato(cliente, conta, clientes, contas):
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")
    aperte_para_continuar()
    return clientes, contas

def criar_cliente(clientes):
    cpf_informado = input("Informe o CPF (somente número): ")
    cpf = valida_cpf(cpf_informado)
    if cpf:
        cliente = filtrar_cliente(cpf, clientes)

        if cliente:
            print("\n@@@ Já existe cliente com esse CPF! @@@")
            aperte_para_continuar()
            return

        nome = input("Informe o nome completo: ")
        if not nome:
            print("\n@@@ Nome Inválido! Digite um nome @@@")
            aperte_para_continuar()
            return
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

        clientes.append(cliente)

        print("\n=== Cliente criado com sucesso! ===")

        return clientes
    
    else:
        print(f'CPF {cpf_informado} inválido')
        aperte_para_continuar()

def criar_conta(numero_conta, clientes, contas):
    cpf = selecionar_clientes(clientes)

    if cpf:
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
            return clientes, contas

        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        cliente.contas.append(conta)

        print("\n=== Conta criada com sucesso! ===")
        aperte_para_continuar()
        return clientes, contas
    
    return clientes, contas

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
    aperte_para_continuar()

def exibir_saldo(conta):
    saldo = conta.saldo
    print(saldo)
    aperte_para_continuar()

def validar_valor(valor: str):
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

def valida_cpf(cpf: str):
    if ('.' or '-') in cpf:
        cpf = cpf.replace('.', '').replace('-', '')

    if cpf.isdigit() and len(cpf) == 11:
        
        return cpf

    else:
        return False

def aperte_para_continuar():
    print('-' * 60)
    input('Aperte ENTER para continuar')

def main():
    clientes = []
    contas = []

    while True:
        os.system("cls")
        opcao = tela_inicio()

        match opcao:
            case '1':
                os.system("cls")
                clientes, contas = menu_sessao(clientes, contas)

            case '2':
                os.system("cls")
                clientes = menu_usuario(clientes)

            case '3':
                os.system("cls")
                clientes, contas = menu_conta(clientes, contas)


            case '0':
                os.system("cls")
                break

            case _:
                os.system("cls")
                print('-' * 60)
                print("Opção inválida")
                input()

def menu_usuario(clientes):
    while True:
        os.system("cls")
        opcao_usuario = tela_usuario()

        match opcao_usuario:
            case '1':
                os.system("cls")
                novo_cliente = criar_cliente(clientes)
                if novo_cliente:
                    aperte_para_continuar()
                    return novo_cliente

            case '2':
                os.system("cls")
                if clientes:
                    [print(cliente) for cliente in listar_clientes(clientes)]
                    aperte_para_continuar()
                    return clientes
                else:
                    print('\n@@@ Nenhum cliente cadastrado! @@@')
                    aperte_para_continuar()
                

            case '9':
                os.system("cls")
                return clientes

            case '0':
                os.system("cls")
                exit()

            case _:
                os.system("cls")
                print('-' * 60)
                print("Opção inválida")
                input()

def menu_conta(clientes, contas):
    while True:
        os.system("cls")
        opcao_conta = tela_conta()

        match opcao_conta:
            case '1':
                os.system("cls")
                numero_conta = len(contas) + 1
                clientes, contas = criar_conta(numero_conta, clientes, contas)
                return clientes, contas

            case '2':
                os.system("cls")
                if contas:
                    listar_contas(contas)
                else: 
                    print("\n@@@ Nenhuma conta cadastrada. \nCadastre uma conta.")
                    aperte_para_continuar()
                return clientes, contas

            case '9':
                os.system("cls")
                return clientes, contas

            case '0':
                os.system("cls")
                exit()

            case _:
                os.system("cls")
                print('-' * 60)
                print("Opção inválida")
                input()

def menu_sessao(clientes, contas):
    cpf = selecionar_clientes(clientes)
    if cpf:
        cliente = filtrar_cliente(cpf, clientes)
        conta = recuperar_conta_cliente(cliente)
        if not conta:
            print("\n@@@ Nenhuma conta cadastrada. \nCadastre uma conta.")
            aperte_para_continuar()
            return clientes, contas

    else:
        return clientes, contas

    while True:
        os.system("cls")

        opcao_sessao = tela_sessao()

        match opcao_sessao:
            case '1':
                clientes, contas, cliente, conta = depositar(cliente, conta, clientes, contas)
                
            case '2':
                clientes, contas, cliente, conta = sacar(cliente, conta, clientes, contas)

            case '3':
                exibir_saldo(conta)
                ...

            case '4':
                clientes, contas = exibir_extrato(cliente, conta, clientes, contas)

            case '9':
                os.system("cls")
                return clientes, contas

            case '0':
                os.system("cls")
                exit()

            case _:
                os.system("cls")
                print('-' * 60)
                print("Opção inválida")
                input()

main()

