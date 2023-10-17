import json
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:/oracle/instantclient_21_11")
from pandas import DataFrame

class OracleQueries:

    def __init__(self, can_write:bool=False):
        self.can_write = can_write
        self.host = 'localhost'
        self.port = 1521
        self.service_name = 'bd_food_healthy'
        self.sid = 'XE'
        self.cur = None
        self.user = 'system'
        self.passwd = 'system2023'

        #with open("conexion\\passphrase\\authentication.oracle", "r") as f:
        #    self.user, self.passwd = f.read().split(',')            

    def __del__(self):
        if self.cur:
            self.close()

    def connectionString(self, in_container:bool=False):
        '''
        Esse método cria uma string de conexão utilizando os parâmetros necessários
        Parameters:
        - host: endereço da localização do servidor
        - port: porta a qual o Oracle está escutando
        - service_name: nome do serviço criado para o banco de dados Oracle
        - sid: id do serviço
        return: string de conexão
        '''
        if not in_container:
            string_connection = cx_Oracle.makedsn(host=self.host,
                                                port=self.port,
                                                sid=self.sid
                                                )
        elif in_container:
            string_connection = cx_Oracle.makedsn(host=self.host,
                                                port=self.port,
                                                service_name=self.service_name
                                                )
        return string_connection

    def connect(self):
        '''
        Esse método realiza a conexão com o banco de dados Oracle
        Parameters:
        - user: nome do usuário criado para utilização do banco de dados
        - password: senha do usuário criado para utilização do banco de dados
        - dsn: string de conexão para acessar o banco de dados oracle
        - enconding: codificação de caracteres para não haver erros com caracteres em português
        return: um cursor que permite utilizar as funções da biblioteca cx_Oracle
        '''

        self.conn = cx_Oracle.connect(user=self.user,
                                      password=self.passwd,
                                      dsn=self.connectionString()
                                     )
        self.cur = self.conn.cursor()
        return self.cur

    def sqlToDataFrame(self, query:str) -> DataFrame:
        '''
        Esse método irá executar uma query
        Parameters:
        - query: consulta utilizada para recuperação dos dados
        return: um DataFrame da biblioteca Pandas
        '''
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return DataFrame(rows, columns=[col[0].lower() for col in self.cur.description])

    def sqlToMatrix(self, query:str) -> tuple:
        '''
        Esse método irá executar uma query
        Parameters:
        - query: consulta utilizada para recuperação dos dados
        return: uma matriz (lista de listas), uma lista com os nomes das colunas(atributos) da(s) tabela(s)
        '''
        self.cur.execute(query)
        rows = self.cur.fetchall()
        matrix = [list(row) for row in rows]
        columns = [col[0].lower() for col in self.cur.description]
        return matrix, columns

    def sqlToJson(self, query:str):
        '''
        Esse método irá executar uma query
        Parameters:
        - query: consulta utilizada para recuperação dos dados
        return: um objeto json
        '''
        self.cur.execute(query)
        columns = [col[0].lower() for col in self.cur.description]
        self.cur.rowfactory = lambda *args: dict(zip(columns, args))
        rows = self.cur.fetchall()
        return json.dumps(rows, default=str)

    def write(self, query:str):
        if not self.can_write:
            raise Exception("Cant write using this connection")

        self.cur.execute(query)
        self.conn.commit()

    def close(self):
        if self.cur:
            self.cur.close()

    def executeDDL(self, query:str):
        '''
        Esse método irá executar o comando DDL enviado no atributo query
        Parameters:
        - query: consulta utilizada para comandos DDL
        '''
        self.cur.execute(query)
        
