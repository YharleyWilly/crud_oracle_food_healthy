import os
from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):
    
        #Relatorio clientes
        self.query_relatorio_clientes = '''    
            select c.cpf_cliente
            , c.nome_cliente
            , c.telefone_cliente
            , c.email_cliente
            from clientes c
            order by c.cpf_cliente 
        '''
        #Relatorio comandas de todos os clientes
        self.query_relatorio_comandas = '''
            SELECT co.ID_COMANDA,
            i.ID_ITEM_COMANDA as item_comanda,
            c.CPF_CLIENTE,
            c.NOME_CLIENTE as cliente,
            co.DATA_COMANDA,
            co.STATUS_COMANDA,
            i.DESCRICAO_PRODUTO as produto,
            i.QTD_ITEM as quantidade,
            i.VALOR_UNITARIO_ITEM as valor_unitario,
            (i.QTD_ITEM * i.VALOR_UNITARIO_ITEM) as valor_total
            FROM SYSTEM.CLIENTES c
            INNER JOIN SYSTEM.COMANDAS co ON c.CPF_CLIENTE = co.CPF_CLIENTE
            LEFT JOIN SYSTEM.ITENS_COMANDA i ON co.ID_COMANDA = i.ID_COMANDA
            ORDER BY c.NOME_CLIENTE, i.ID_ITEM_COMANDA
        '''
        #Relatorio itens comanda de todos os clientes
        self.query_relatorio_itens_comanda = ''' 
            select i.id_comanda
            , i.id_item_comanda
            , i.descricao_produto
            , i.qtd_item
            , i.valor_unitario_item
            , (i.qtd_item * i.valor_unitario_item) as valor_total
            from itens_comanda i
            order by i.id_comanda
        '''       
    #Relatorio comanda cliente específico 
    def query_relatorio_comanda_cliente(cpf_cliente:str):
        return f'''
            SELECT c.CPF_CLIENTE,
            c.NOME_CLIENTE as cliente,
            co.ID_COMANDA,
            i.ID_ITEM_COMANDA as item_comanda,
            co.DATA_COMANDA,
            co.STATUS_COMANDA,
            i.DESCRICAO_PRODUTO as produto,
            i.QTD_ITEM as quantidade,
            i.VALOR_UNITARIO_ITEM as valor_unitario,
            (i.QTD_ITEM * i.VALOR_UNITARIO_ITEM) as valor_total
            FROM SYSTEM.CLIENTES c 
            INNER JOIN SYSTEM.COMANDAS co ON c.CPF_CLIENTE = co.CPF_CLIENTE
            LEFT JOIN SYSTEM.ITENS_COMANDA i ON co.ID_COMANDA = i.ID_COMANDA
            WHERE c.CPF_CLIENTE = '{cpf_cliente}'
            ORDER BY c.NOME_CLIENTE, i.ID_ITEM_COMANDA
        '''

    def get_relatorio_clientes(self):
        # Cria uma nova conexão com o banco que permite alteração
  
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_clientes))
        input("\nPressione Enter para Sair do Relatório de Clientes\n")

    def get_relatorio_comandas(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_comandas))
        input("\nPressione Enter para Sair do Relatório de Comandas\n")

    def get_relatorio_itens_comanda(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_itens_comanda))
        input("\nPressione Enter para Sair do Relatório de Itens de Comandas\n")
        
    def get_relatorio_comanda_cliente(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        
        # Solicita ao usuario o cpf para fazer a consulta
        cpf_cliente = str(input("Informe o CPF do cliente: "))

        relatorio_comanda_cliente = Relatorio.query_relatorio_comanda_cliente(cpf_cliente)
        # Exibe na tela o resultado do retorno da consulta com base no cpf informado
        print(oracle.sqlToDataFrame(relatorio_comanda_cliente))
        input("\nPressione Enter para Sair do Relatório de Comanda do cliente\n")
    
