from pydoc import cli
from model.comandas import Comanda
from model.clientes import Cliente
from controller.controller_cliente import Controller_Cliente
from conexion.oracle_queries import OracleQueries
from datetime import date
from utils import config

class Controller_Comanda:

    data = date.today()
    data_hoje = '{}/{}/{}'.format(data.day, data.month, data.year)
    
        
    def __init__(self):
        
        self.ctrl_cliente = Controller_Cliente()
        
    def inserir_comanda(self) -> Comanda:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        
        # Lista os clientes existentes para inserir na comanda
        self.listar_clientes(oracle, need_connect=True)
        cpf = str(input("Digite o número do CPF do Cliente: "))
        cliente = self.valida_cliente(oracle, cpf)
        if cliente == None:
            return None

        # Recupera o cursos para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(id_comanda=output_value, data_comanda=self.data_hoje, status_comanda="Aberto",cpf_cliente=cliente.get_CPF())
        
        # Executa o bloco PL/SQL anônimo para inserção da nova comanda e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            :id_comanda := comandas_id_comanda_SEQ.NEXTVAL;
            insert into comandas values(:id_comanda, :data_comanda, :status_comanda, :cpf_cliente);
        end;
        """, data)
        
        # Recupera o código da nova comanda
        id_comanda = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados da nova comanda criado transformando em um DataFrame
        df_comanda = oracle.sqlToDataFrame(f"select * from comandas where id_comanda = {id_comanda}")
        # Cria um novo objeto Comanda
        nova_comanda = Comanda(df_comanda.id_comanda.values[0], df_comanda.data_comanda.values[0], df_comanda.status_comanda.values[0], cliente)
        # Exibe os atributos da nova comanda
        print(nova_comanda.to_string())
        # Retorna o objeto nova_comanda para utilização posterior, caso necessário
        return nova_comanda

    def atualizar_status_comanda(self) -> Comanda:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da comanda a ser alterada
        id_comanda = int(input("Código da Comanda que irá alterar: "))        

        # Verifica se a comanda existe na base de dados
        if not self.verifica_existencia_comanda(oracle, id_comanda):

            comanda = self.valida_comanda(oracle, id_comanda)
            if comanda ==  None:
                return None        
            
            cliente = self.valida_cliente(oracle, comanda.get_cliente().get_CPF())
            if cliente == None:
                return None

            # Exibe o satus atual da comanda
            print(f"\nStatus da comanda [{id_comanda}]: {comanda.get_status_comanda()}\n")
            
            print("----------ESCOLHA O OPÇÃO DO STATUS DA COMANDA----------\n")
            # Menu das opções de status da comanda "Aberto", "Em Andamento", "Finalizado", "Pronto"
            status_comanda = int(input(config.STATUS_COMANDA))
            
            # Chama o método de atualizar status da comanda 
            novo_status = comanda.atualizar_status_comanda(status_comanda)
            
            print(f"Novo status: {novo_status}")
            print(f"Cliente: {comanda.get_cliente().get_CPF()}")
            
            # Atualiza o status da comanda 
            oracle.write(f"update comandas set status_comanda = '{novo_status}' where id_comanda = {id_comanda}")
            # Recupera os dados da nova comanda criado transformando em um DataFrame
            df_comanda = oracle.sqlToDataFrame(f"select * from comandas where id_comanda = {id_comanda}")
            # Cria um novo objeto comanda
            comanda_atualizado = Comanda(df_comanda.id_comanda.values[0], df_comanda.data_comanda.values[0], df_comanda.status_comanda.values[0], cliente)
            # Exibe os atributos da nova comanda
            print(comanda_atualizado.to_string())
            # Retorna o objeto comanda_atualizado para utilização posterior, caso necessário
            return comanda_atualizado
        else:
            print(f"O código {id_comanda} não existe.")
            return None

    def excluir_comanda(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do comanda a ser alterado
        id_comanda = int(input("Código do Comanda que irá excluir: "))        

        # Verifica se o comanda existe na base de dados
        if not self.verifica_existencia_comanda(oracle, id_comanda):            
            # Recupera os dados da nova comanda criada transformando em um DataFrame
            df_comanda = oracle.sqlToDataFrame(f"select * from comandas where id_comanda = {id_comanda}")
            cliente = self.valida_cliente(oracle, df_comanda.cpf_cliente.values[0])
            
            from controller.controller_item_comanda import Controller_Item_Comanda
            self.ctrl_item_comanda = Controller_Item_Comanda()
            
            # Valida existencia item comanda associada a comanda e retorna o objeto
            #item_comanda = self.ctrl_item_comanda.valida_item_comanda_comanda(oracle, id_comanda)
                
            #Se não existe item comanda exclui comanda depois o cliente
            if self.ctrl_item_comanda.valida_item_comanda_comanda(oracle, id_comanda) == None:
                
                # Revome a comanda da tabela
                oracle.write(f"delete from comandas where id_comanda = {id_comanda}") 
                # Cria um novo objeto Comanda para informar que foi removido
                comanda_excluido = Comanda(df_comanda.id_comanda.values[0], df_comanda.data_comanda.values[0], df_comanda.status_comanda.values[0], cliente)
                # Exibe os atributos da comanda excluída
                print("Comanda Removida com Sucesso!")
                print(comanda_excluido.to_string())
                
            # Se existe itens na comanda    
            else:  
                
                opcao_excluir = input(f"A comanda possui itens. Tem certeza que deseja excluir a comanda {id_comanda} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    
                    print("\nAtenção, a comanda possui itens!\n")
                    opcao_excluir = input(f"\nTem certeza que deseja excluir o comanda {id_comanda} [S ou N]: \n")
                    
                    if opcao_excluir.lower() == "s":
                    
                        # Revome a comanda da tabela
                        oracle.write(f"delete from itens_comanda where id_comanda = {id_comanda}")
                        print("Itens da comanda removidos com sucesso!")
                        oracle.write(f"delete from comandas where id_comanda = {id_comanda}")
                        
                        # Cria um novo objeto Comanda para informar que foi removido
                        comanda_excluido = Comanda(df_comanda.id_comanda.values[0], df_comanda.data_comanda.values[0], df_comanda.status_comanda.values[0], cliente)
                        # Exibe os atributos da comanda excluída
                        print("Comanda Removida com Sucesso!")
                        print(comanda_excluido.to_string())           
        else:
            print(f"O código {id_comanda} não existe.")
    
    def verifica_existencia_comanda(self, oracle:OracleQueries, id_comanda:int=None) -> bool:
        # Recupera os dados da nova comanda criada, transformando em um DataFrame
        df_comanda = oracle.sqlToDataFrame(f"select * from comandas where id_comanda = {id_comanda}")
        return df_comanda.empty
    
    def verifica_existencia_comanda_cliente(self, oracle:OracleQueries, cpf_cliente:str=None) -> bool:
        # Recupera os dados da nova comanda criada, transformando em um DataFrame
        df_comanda = oracle.sqlToDataFrame(f"select * from comandas where cpf_cliente = '{cpf_cliente}'")
        return df_comanda.empty
    

   
    def listar_clientes(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select * 
                from clientes c
                order by c.nome_cliente
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))
    
    
    def valida_cliente(self, oracle:OracleQueries, cpf:str=None) -> Cliente:
        if self.ctrl_cliente.verifica_existencia_cliente(oracle, cpf):
            print(f"\n\nO CPF {cpf} informado não existe na base.\n\n")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = oracle.sqlToDataFrame(f"select * from clientes where cpf_cliente = '{cpf}'")
            # Cria um novo objeto cliente
            cliente = Cliente(df_cliente.cpf_cliente.values[0], df_cliente.nome_cliente.values[0], df_cliente.telefone_cliente.values[0], df_cliente.email_cliente.values[0])
            return cliente
        
    def valida_comanda(self, oracle:OracleQueries, id_comanda:int=None) -> Comanda:
        if self.verifica_existencia_comanda(oracle, id_comanda):
            print(f"\n\nO codigo da comanda {id_comanda} informado não existe na base.\n\n")
            return None
        else:
            oracle.connect()
            # Recupera os dados da nova comanda criada transformando em um DataFrame
            df_comanda = oracle.sqlToDataFrame(f"select * from comandas where id_comanda = {id_comanda}")
            
            # Cria um novo objeto cliente
            cliente = self.valida_cliente(oracle, df_comanda.cpf_cliente.values[0])
            
            # Cria um novo objeto comanda
            comanda = Comanda(df_comanda.id_comanda.values[0], df_comanda.data_comanda.values[0], df_comanda.status_comanda.values[0], cliente)
            return comanda
        
    # Retorna comanda associada ao cpf do cliente    
    def valida_comanda_cliente(self, oracle:OracleQueries, cpf_cliente:str=None) -> Comanda:
        if self.verifica_existencia_comanda_cliente(oracle, cpf_cliente):
            print(f"\n\nNão existe comanda associada ao cpf {cpf_cliente} na base.\n\n")
            return None
        else:
            oracle.connect()
            # Recupera os dados da nova comanda criada transformando em um DataFrame
            df_comanda = oracle.sqlToDataFrame(f"select * from comandas where cpf_cliente = '{cpf_cliente}'")
            
            # Cria um novo objeto cliente
            cliente = self.valida_cliente(oracle, df_comanda.cpf_cliente.values[0])
            
            # Cria um novo objeto comanda
            comanda = Comanda(df_comanda.id_comanda.values[0], df_comanda.data_comanda.values[0], df_comanda.status_comanda.values[0], cliente)
            return comanda
        
        
    