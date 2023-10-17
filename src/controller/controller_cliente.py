from model.clientes import Cliente
from model.comandas import Comanda
from model.itens_comanda import ItemComanda
from conexion.oracle_queries import OracleQueries


class Controller_Cliente:
    
    def __init__(self):
        pass
    
    def inserir_cliente(self) -> Cliente:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuario o novo CPF
        cpf = input("CPF (Novo): ")

        #Se cpf do cliente não existe na tablea CLIENTES
        if self.verifica_existencia_cliente(oracle, cpf):
            
            # Solicita ao usuario o novo nome
            nome = input("Nome (Novo): ")
            # Solicita ao usuario o novo telefone
            telefone = input("Telefone (Novo): ")
            # Solicita ao usuario o novo email
            email = input("Email (Novo): ")
            
            #SELECT * FROM CLIENTES WHERE CPF_CLIENTE = '20678526722'
            
            # Insere e persiste o novo cliente
            oracle.write(f"insert into clientes values ('{cpf}', '{nome}', '{telefone}', '{email}')")
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = oracle.sqlToDataFrame(f"select * from clientes where cpf_cliente = '{cpf}'")
            # Cria um novo objeto Cliente
            novo_cliente = Cliente(df_cliente.cpf_cliente.values[0], df_cliente.nome_cliente.values[0], df_cliente.telefone_cliente.values[0], df_cliente.email_cliente.values[0])
            # Exibe os atributos do novo cliente
            print(novo_cliente.to_string())
            # Retorna o objeto novo_cliente para utilização posterior, caso necessário
            return novo_cliente
        else:
            print(f"O CPF {cpf} já está cadastrado.")
            return None

    def atualizar_cliente(self) -> Cliente:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do cliente a ser alterado
        cpf = int(input("CPF do cliente que deseja alterar o nome: "))

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(oracle, cpf):
            # Solicita a nova descrição do cliente
            
            # Solicita o novo nome
            novo_nome = input("Nome (Novo): ")
            # Solicita o novo telefone
            novo_telefone = input("Telefone (Novo): ")
            # Solicita o novo email
            novo_email = input("Email (Novo): ")
            
            # Atualiza os dados do cliente existente no banco de dados
            oracle.write(f"""update clientes set nome_cliente = '{novo_nome}', telefone_cliente = '{novo_telefone}', email_cliente = '{novo_email}' 
                         where cpf_cliente = '{cpf}'""")
            
            
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = oracle.sqlToDataFrame(f"select * from clientes where cpf_cliente = '{cpf}'")
            # Cria um novo objeto cliente
            cliente_atualizado = Cliente(df_cliente.cpf_cliente.values[0], df_cliente.nome_cliente.values[0], df_cliente.telefone_cliente.values[0], df_cliente.email_cliente.values[0])
            # Exibe os atributos do novo cliente
            print(cliente_atualizado.to_string())
            # Retorna o objeto cliente_atualizado para utilização posterior, caso necessário
            return cliente_atualizado
        else:
            print(f"O CPF {cpf} não existe.")
            return None

    def excluir_cliente(self):
        
        from controller.controller_comanda import Controller_Comanda
        from controller.controller_item_comanda import Controller_Item_Comanda
        
        self.ctrl_item_comanda = Controller_Item_Comanda()
        self.ctrl_comanda = Controller_Comanda()
        
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o CPF do Cliente a ser alterado
        cpf = int(input("CPF do Cliente que irá excluir: "))        

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(oracle, cpf):            
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = oracle.sqlToDataFrame(f"select * from clientes where cpf_cliente = '{cpf}'")
            
            comanda_cliente = self.ctrl_comanda.valida_comanda_cliente(oracle, cpf)
            
            # Se comanda é vazia pode excluir diretamente o cliente, pois não existe itens sem uma comanda criada
            if comanda_cliente == None:

                # Revome o cliente da tabela
                oracle.write(f"delete from clientes where cpf_cliente = '{cpf}'")            
                # Cria um novo objeto Cliente para informar que foi removido
                cliente_excluido = Cliente(df_cliente.cpf_cliente.values[0], df_cliente.nome_cliente.values[0], df_cliente.telefone_cliente.values[0], df_cliente.email_cliente.values[0])
                # Exibe os atributos do cliente excluído
                print("Cliente Removido com Sucesso!")
                print(cliente_excluido.to_string())
            
            # Se a comanda existe    
            else:
                
                # Valida existencia item comanda associada a comanda e retorna o objeto
                item_comanda = self.ctrl_item_comanda.valida_item_comanda_comanda(oracle, comanda_cliente.get_id_comanda())
                
                #Se não existe item comanda exclui comanda depois o cliente
                if item_comanda == None:
                    
                    # Revome o cliente da tabela
                    oracle.write(f"delete from comandas where cpf_cliente = '{cpf}'") 
                    oracle.write(f"delete from clientes where cpf_cliente = '{cpf}'")           
                    # Cria um novo objeto Cliente para informar que foi removido
                    cliente_excluido = Cliente(df_cliente.cpf_cliente.values[0], df_cliente.nome_cliente.values[0], df_cliente.telefone_cliente.values[0], df_cliente.email_cliente.values[0])
                    # Exibe os atributos do cliente excluído
                    print("Cliente Removido com Sucesso!")
                    print(cliente_excluido.to_string())
                
                # Se existe comanda e item comanda associada a mesma
                else:
                    
                    oracle.write(f"delete from itens_comanda where id_comanda = {comanda_cliente.get_id_comanda()}") 
                    oracle.write(f"delete from comandas where cpf_cliente = '{cpf}'") 
                    oracle.write(f"delete from clientes where cpf_cliente = '{cpf}'")           
                    # Cria um novo objeto Cliente para informar que foi removido
                    cliente_excluido = Cliente(df_cliente.cpf_cliente.values[0], df_cliente.nome_cliente.values[0], df_cliente.telefone_cliente.values[0], df_cliente.email_cliente.values[0])
                    # Exibe os atributos do cliente excluído
                    print("Cliente Removido com Sucesso!")
                    print(cliente_excluido.to_string())
                    
                    
                    
                        
                     
                
            
            
            
            
            #VERIFICAR SE EXISTE COMANDA COM CPF DO CLIENTE
            
        else:
            print(f"O CPF {cpf} não existe.")

    def verifica_existencia_cliente(self, oracle:OracleQueries, cpf:str=None) -> bool:
        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_cliente = oracle.sqlToDataFrame(f"select * from clientes where cpf_cliente = '{cpf}'")
        return df_cliente.empty