import os
from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):
        # Consultas de contagem de registros - inicio
        self.qry_total_clientes = config.QUERY_COUNT.format(tabela="clientes")
        self.qry_total_comandas = config.QUERY_COUNT.format(tabela="comandas")
        self.qry_total_itens_comanda = config.QUERY_COUNT.format(tabela="itens_comanda")
        # Consultas de contagem de registros - fim

        # Nome(s) do(s) criador(es)
        self.created_by = "Yharley Willy | Tiago Morais | Kezia Barbosa | Jefferson Bulloto | Rodrigo Campos"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2023/2"

    def get_total_clientes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_clientes)["total_clientes"].values[0]

    def get_total_comandas(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_comandas)["total_comandas"].values[0]

    def get_total_itens_comanda(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_itens_comanda)["total_itens_comanda"].values[0]

    def get_updated_screen(self):
        return f"""
        ╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
        │                                           FOOD HEALTHY                                               │
        ├──────────────────────────────────────────────────────────────────────────────────────────────────────│
        │                                                                                                      
        │       TOTAL DE REGISTROS:                                                                              
        │                                                                                                      
        │       1 - CLIENTES:         {str(self.get_total_clientes()).rjust(3)}                                
        │       2 - COMANDAS:          {str(self.get_total_comandas()).rjust(3)}                               
        │       3 - ITENS DE COMANDAS: {str(self.get_total_itens_comanda()).rjust(3)}                                                                                            
        │                                                                                                     
        │       CRIADO POR: {self.created_by}                                                                  
        │                                                                                                      
        │       PROFESSOR:  {self.professor}                                                                 
        │                                                                                                      
        │       DISCIPLINA: {self.disciplina}                                                                  
        │                   {self.semestre}                                                                    
        │                                                                                                      
        │━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│
        """
        
        