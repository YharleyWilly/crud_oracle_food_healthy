from model.itens_comanda import ItemComanda
from model.comandas import Comanda
from controller.controller_comanda import Controller_Comanda
from conexion.oracle_queries import OracleQueries
from utils import config

class Controller_Item_Comanda:
    def __init__(self):
 
        self.ctrl_comanda = Controller_Comanda()
        
        
    def inserir_item_comanda(self) -> ItemComanda:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        
        # Lista as comandas existentes para inserir no item de comanda
        self.listar_comandas(oracle, need_connect=True)
        
        #Espaçamento
        print("\n")   
        
        id_comanda = int(input("Digite o número da Comanda onde serão inserido os itens: "))
  
        comanda = self.valida_comanda(oracle, id_comanda)
        if comanda == None:
            return None

        #Exibe o cardapio
        print(config.MENU_CARDAPIO)
 
        opcao_produto = str(input(f"Informe a opção do produto da comanda {comanda.get_id_comanda()} | Cliente {comanda.cliente.get_nome()}:  "))

        print("\n")
        
        #A descrição e valor do produto serão definidos de acordo com a opção escolhida pelo usuário.
        match opcao_produto.upper():
            
            case '1':
                
                descricao_produto = "Sanduíche Natural"
                valor_unitario_item = 9.90
                print(f"Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
                
            case '2':
                
                descricao_produto = "Salada de Frutas"
                valor_unitario_item = 6.50
                print(f"Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
                
                
            case '3':
                
                descricao_produto = "Smoothie de Frutas"
                valor_unitario_item = 7.90
                print(f"Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
                
            case '4':
                
                descricao_produto = "Wrap de Vegetais"
                valor_unitario_item = 8.50
                print(f"Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
                
                
            case '5':    
                
                descricao_produto = "Iogurte com Granola"
                valor_unitario_item = 5.50
                print(f"Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
                
            case 'A':
                
                descricao_produto = "Água Mineral"
                valor_unitario_item = 3.00
                print(f"Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
            
            case 'B':
                
                descricao_produto = "Suco Natural"
                valor_unitario_item = 5.00
                print(f"Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
                
            case 'C':
                
                descricao_produto = "Chá Verde"
                valor_unitario_item = 4.00
                print(f"Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
               
            case _:
                print("Opção inválida.")
        
        # Solicita a quantidade de itens da comanda selecionada
        quantidade = int(input(f"Informe a quantidade de itens da comanda {comanda.get_id_comanda()} | Cliente {comanda.cliente.get_nome()}: "))
        
        # Solicita o valor unitário do produto selecionado
        #valor_unitario_item = float(input(f"Informe o valor unitario do produto {descricao_produto} | Cliente {comanda.cliente.get_nome()}:  "))

        #Espaçamento
        print("\n")   
        
        # Recupera o cursor para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(id_item_comanda=output_value, qtd_item=quantidade, descricao_produto=descricao_produto,valor_unitario_item=valor_unitario_item, id_comanda=int(comanda.get_id_comanda()))
        # Executa o bloco PL/SQL anônimo para inserção do novo item de comanda e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            :id_item_comanda := itens_comanda_id_item_comanda_SEQ.NEXTVAL;
            insert into itens_comanda values(:id_item_comanda, :qtd_item, :descricao_produto, :valor_unitario_item, :id_comanda);
        end;
        """, data)
        # Recupera o código do novo item de comanda
        id_item_comanda = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados do novo item de comanda criado transformando em um DataFrame
        df_item_comanda = oracle.sqlToDataFrame(f"select * from itens_comanda where id_item_comanda = {id_item_comanda}")
        # Cria um novo objeto Item de Comanda
        novo_item_comanda = ItemComanda(df_item_comanda.id_item_comanda.values[0], df_item_comanda.qtd_item.values[0], df_item_comanda.descricao_produto.values[0], df_item_comanda.valor_unitario_item.values[0], comanda)
        # Exibe os atributos do novo Item de Comanda
        print(novo_item_comanda.to_string())
        # Retorna o objeto novo_item_comanda para utilização posterior, caso necessário
        return novo_item_comanda

    def atualizar_item_comanda(self) -> ItemComanda:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do item de comanda a ser alterado
        codigo_item_comanda = int(input("Código do Item de Comanda que irá alterar: "))        

        #Espaçamento
        print("\n")   
        
        # Verifica se o item de comanda existe na base de dados
        if not self.verifica_existencia_item_comanda(oracle, codigo_item_comanda):

            # Lista as comanda existentes para atualizar os itens de comanda
            #self.listar_comandas(oracle, need_connect=True)
            
            #Espaçamento
            print("\n")   
            
            # Valida existencia item comanda e retorna o objeto
            itemComanda = self.valida_item_comanda(oracle, codigo_item_comanda)
            
            #id_comanda = str(input("Digite o número da comanda que irá receber os itens de comanda {}: "))
            comanda = self.valida_comanda(oracle, itemComanda.get_comanda().get_id_comanda())
            if comanda == None:
                return None

                #Exibe o cardapio
            print(config.MENU_CARDAPIO)
            
            opcao_produto = str(input(f"Informe a NOVA opção do produto Item de comanda {codigo_item_comanda} | Cliente {comanda.cliente.get_nome()}:  "))

            print("\n")
            
            #A descrição e valor do produto serão definidos de acordo com a opção escolhida pelo usuário.
            match opcao_produto.upper():
                
                case '1':
                    
                    descricao_produto = "Sanduíche Natural"
                    valor_unitario_item = 9.90
                    print(f"Item comanda: {codigo_item_comanda} | Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
                    
                case '2':
                    
                    descricao_produto = "Salada de Frutas"
                    valor_unitario_item = 6.50
                    print(f"Item comanda: {codigo_item_comanda} | Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
                    
                    
                case '3':
                    
                    descricao_produto = "Smoothie de Frutas"
                    valor_unitario_item = 7.90
                    print(f"Item comanda: {codigo_item_comanda} | Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
                    
                case '4':
                    
                    descricao_produto = "Wrap de Vegetais"
                    valor_unitario_item = 8.50
                    print(f"Item comanda: {codigo_item_comanda} | Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
                    
                    
                case '5':    
                    
                    descricao_produto = "Iogurte com Granola"
                    valor_unitario_item = 5.50
                    print(f"Item comanda: {codigo_item_comanda} | Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
                    
                case 'A':
                    
                    descricao_produto = "Água Mineral"
                    valor_unitario_item = 3.00
                    print(f"Item comanda: {codigo_item_comanda} | Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
                
                case 'B':
                    
                    descricao_produto = "Suco Natural"
                    valor_unitario_item = 5.00
                    print(f"Item comanda: {codigo_item_comanda} | Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
                    
                case 'C':
                    
                    descricao_produto = "Chá Verde"
                    valor_unitario_item = 4.00
                    print(f"Item comanda: {codigo_item_comanda} | Cliente: {comanda.cliente.get_nome()} | Descrição produto: {descricao_produto} | Valor unitario: {valor_unitario_item}")
                
                case _:
                    print("Opção inválida.")

            # Solicita a quantidade de itens da comanda para o item de comanda selecionado
            quantidade = int(input(f"Informe a nova quantidade de itens do produto: "))
            
            # Atualiza o item de comanda existente
            oracle.write(f"update itens_comanda set qtd_item = {quantidade}, descricao_produto = '{descricao_produto}', valor_unitario_item = {valor_unitario_item}, id_comanda = {comanda.get_id_comanda()} where id_item_comanda = {codigo_item_comanda}")
            # Recupera os dados do novo item de comanda criado transformando em um DataFrame
            df_item_comanda = oracle.sqlToDataFrame(f"select * from itens_comanda where id_item_comanda = {codigo_item_comanda}")
            # Cria um novo objeto Item de Comanda
            item_comanda_atualizado = ItemComanda(df_item_comanda.id_item_comanda.values[0], df_item_comanda.qtd_item.values[0], df_item_comanda.descricao_produto.values[0], df_item_comanda.valor_unitario_item.values[0], comanda)
            # Exibe os atributos do item de comanda
            print(item_comanda_atualizado.to_string())
            # Retorna o objeto comanda_atualizado para utilização posterior, caso necessário
            return item_comanda_atualizado
        else:
            print(f"O código {codigo_item_comanda} não existe.")
            return None

    def excluir_item_comanda(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do item de comanda a ser alterado
        codigo_item_comanda = int(input("Código do Item de Comanda que irá excluir: "))        

        # Verifica se o item de comanda existe na base de dados
        if not self.verifica_existencia_item_comanda(oracle, codigo_item_comanda):            
            # Recupera os dados do novo item de comanda criado transformando em um DataFrame
            df_item_comanda = oracle.sqlToDataFrame(f"select * from itens_comanda where id_item_comanda = {codigo_item_comanda}")
            comanda = self.valida_comanda(oracle, df_item_comanda.id_comanda.values[0])
                    
            opcao_excluir = input(f"Tem certeza que deseja excluir o item de comanda {codigo_item_comanda} [S ou N]: ")
            
            if opcao_excluir.lower() == "s":
                # Revome o produto da tabela
                oracle.write(f"delete from itens_comanda where id_item_comanda = {codigo_item_comanda}")                
                # Cria um novo objeto Item de Comanda para informar que foi removido
                item_comanda_excluido = ItemComanda(df_item_comanda.id_item_comanda.values[0], df_item_comanda.qtd_item.values[0], df_item_comanda.descricao_produto.values[0], df_item_comanda.valor_unitario_item.values[0], comanda)
                # Exibe os atributos do produto excluído
                print("Item da Comanda Removido com Sucesso!")
                print(item_comanda_excluido.to_string())
        else:
            print(f"O código {codigo_item_comanda} não existe.")

    def verifica_existencia_item_comanda(self, oracle:OracleQueries, codigo:int=None) -> bool:
        # Recupera os dados do novo comanda criado transformando em um DataFrame
        df_comanda = oracle.sqlToDataFrame(f"select * from itens_comanda where id_item_comanda = {codigo}")
        return df_comanda.empty
    
    # Verifica existencia de item comanda associado a comanda especifica
    def verifica_existencia_item_comanda_comanda(self, oracle:OracleQueries, id_comanda:int=None) -> bool:
        # Recupera os dados do novo comanda criado transformando em um DataFrame
        df_comanda = oracle.sqlToDataFrame(f"select * from itens_comanda where id_comanda = {id_comanda}")
        return df_comanda.empty
    
    def listar_comandas(self, oracle: OracleQueries, need_connect: bool = False):
        query = """
            SELECT c.ID_COMANDA,
                c.DATA_COMANDA,
                c.STATUS_COMANDA,
                cl.NOME_CLIENTE AS CLIENTE,
                ic.ID_ITEM_COMANDA AS ITEM_COMANDA,
                ic.DESCRICAO_PRODUTO AS PRODUTO,
                ic.QTD_ITEM AS QUANTIDADE,
                ic.VALOR_UNITARIO_ITEM AS VALOR_UNITARIO,
                (ic.QTD_ITEM * ic.VALOR_UNITARIO_ITEM) AS VALOR_TOTAL
            FROM COMANDAS c
            INNER JOIN CLIENTES cl ON c.CPF_CLIENTE = cl.CPF_CLIENTE
            LEFT JOIN ITENS_COMANDA ic ON c.ID_COMANDA = ic.ID_COMANDA
            ORDER BY cl.NOME_CLIENTE, c.ID_COMANDA, ic.ID_ITEM_COMANDA
        """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    
    def listar_itens_comanda(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select prd.id_item_comanda
                    , prd.qtd_item
                    , prd.descricao_produto
                    , prd.valor_unitario_item
                from itens_comanda prd
                order by prd.descricao_produto 
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))
        
    def valida_comanda(self, oracle:OracleQueries, id_comanda:int=None) -> Comanda:
        if self.ctrl_comanda.verifica_existencia_comanda(oracle, id_comanda):
            print(f"\n\nA comanda {id_comanda} informado não existe na base.\n\n")
            return None
        else:
            oracle.connect()
            # Recupera os dados da nova comanda criada transformando em um DataFrame
            df_comanda = oracle.sqlToDataFrame(f"select * from comandas where id_comanda = {id_comanda}")
            
            # Cria um novo objeto cliente
            cliente = self.ctrl_comanda.valida_cliente(oracle, df_comanda.cpf_cliente.values[0])
                  
            comanda = Comanda(df_comanda.id_comanda.values[0], df_comanda.data_comanda.values[0], df_comanda.status_comanda.values[0], cliente)
            return comanda
        
    def valida_item_comanda(self, oracle:OracleQueries, id_item_comanda:int=None) -> ItemComanda:
        if self.verifica_existencia_item_comanda(oracle, id_item_comanda):
            print(f"\n\nO Item de comanda {id_item_comanda} informado não existe na base.\n\n")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo item de comanda criado transformando em um DataFrame
            df_item_comanda = oracle.sqlToDataFrame(f"select * from itens_comanda where id_item_comanda = {id_item_comanda}")
            
            # Cria um novo objeto comanda
            comanda = self.ctrl_comanda.valida_comanda(oracle, df_item_comanda.id_item_comanda.values[0])
                  
            itensComanda = ItemComanda(df_item_comanda.id_item_comanda.values[0], df_item_comanda.qtd_item.values[0], df_item_comanda.descricao_produto.values[0], df_item_comanda.valor_unitario_item.values[0], comanda)    
            return itensComanda
       
        
    # Valida item comanda associada ao id da comanda específica    
    def valida_item_comanda_comanda(self, oracle:OracleQueries, id_comanda:int=None) -> ItemComanda:
        if self.verifica_existencia_item_comanda_comanda(oracle, id_comanda):
            print(f"\n\nNão existem itens na comanda de id {id_comanda}.\n\n")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo item de comanda criado transformando em um DataFrame
            df_item_comanda = oracle.sqlToDataFrame(f"select * from itens_comanda where id_comanda = {id_comanda}")
            
            # Cria um novo objeto comanda
            comanda = self.ctrl_comanda.valida_comanda(oracle, df_item_comanda.id_comanda.values[0])
                  
            item_comanda = ItemComanda(df_item_comanda.id_item_comanda.values[0], df_item_comanda.qtd_item.values[0], df_item_comanda.descricao_produto.values[0], df_item_comanda.valor_unitario_item.values[0], comanda)    
            return item_comanda   
        
        