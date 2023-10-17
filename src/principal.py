import os
from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_cliente import Controller_Cliente
from controller.controller_comanda import Controller_Comanda
from controller.controller_item_comanda import Controller_Item_Comanda

tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_cliente = Controller_Cliente()
ctrl_comanda = Controller_Comanda()
ctrl_item_comanda = Controller_Item_Comanda()

def reports(opcao_relatorio:int=0):
          
    if opcao_relatorio == 1:
        relatorio.get_relatorio_clientes()
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_comandas()
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_itens_comanda()
    elif opcao_relatorio == 4:
        relatorio.get_relatorio_comanda_cliente()

def inserir(opcao_inserir:int=0):

    if opcao_inserir == 1:
        novo_cliente = ctrl_cliente.inserir_cliente()
    elif opcao_inserir == 2:
        novo_comanda = ctrl_comanda.inserir_comanda()
    elif opcao_inserir == 3:
        novo_item_comanda = ctrl_item_comanda.inserir_item_comanda()

def atualizar(opcao_atualizar:int=0):

    if opcao_atualizar == 1:
        relatorio.get_relatorio_clientes()
        cliente_atualizado = ctrl_cliente.atualizar_cliente()
    elif opcao_atualizar == 2:
        relatorio.get_relatorio_comandas()
        comanda_atualizado = ctrl_comanda.atualizar_status_comanda()
    elif opcao_atualizar == 3:
        relatorio.get_relatorio_itens_comanda()
        item_comanda_atualizado = ctrl_item_comanda.atualizar_item_comanda()

def excluir(opcao_excluir:int=0):

    if opcao_excluir == 1:                
        relatorio.get_relatorio_clientes()
        ctrl_cliente.excluir_cliente()
    elif opcao_excluir == 2:                
        relatorio.get_relatorio_comandas()
        ctrl_comanda.excluir_comanda()
    elif opcao_excluir == 3:
        relatorio.get_relatorio_itens_comanda()
        ctrl_item_comanda.excluir_item_comanda()

def run():
    
    import platform
    print(f"SISTEMA OPERACIONAL: {platform.system()}")
    
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console()
        
        if opcao == 1: # Relatórios
            
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [0-3]: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2: # Inserir Novos Registros
            
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            inserir(opcao_inserir=opcao_inserir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3: # Atualizar Registros

            print(config.MENU_ENTIDADES_ATUALIZAR)
            
            opcao_atualizar = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)
            
            atualizar(opcao_atualizar=opcao_atualizar)

            config.clear_console()

        elif opcao == 4:

            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            excluir(opcao_excluir=opcao_excluir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 5:

            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)
            
run()
#if __name__ == "__main__":
    