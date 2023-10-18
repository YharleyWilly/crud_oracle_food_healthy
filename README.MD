Exemplo de Sistema em Python fazendo CRUD no Oracle

Esse sistema de exemplo é composto por um conjunto de tabelas que representam pedidos de uma lanchonete, contendo tabelas como: clientes, comandas e itens de comanda.

O sistema exige que as tabelas existam, então basta executar o script a seguir para criação das tabelas:

src/create_table.py

Ou no sql developer:
sql/create_table_sistema_lanches_saudaveis.sql

Após criado as tabelas no sql developer, basta executar o script Python a seguir:
~$ python principal.py

Para que possa testar as conexões com o banco de dados Oracle e o módulo Conexion desenvolvido para esse projeto, basta executar o script Python a seguir:
~$ python test.py

Organização

diagrams: Nesse diretório está o diagrama relacional (lógico) do sistema.
O sistema possui três entidades: CLIENTES, COMANDAS, ITENS_COMANDA.

sql: Nesse diretório estão os scripts para criação das tabelas e inserção de dados fictícios para testes do sistema

Certifique-se de que o usuário do banco possui todos os privilégios antes de executar os scripts de criação, caso ocorra erro, execute o comando a seguir com o superusuário via SQL Developer: GRANT ALL PRIVILEGES TO SYSTEM;

create_table_sistema_lanches_saudaveis.sql: script responsável pela criação das tabelas, relacionamentos e criação de permissão no esquema LabDatabase.

BancoLanchonete_Consultas~11.sql: script usado para teste de inserção.

src: Nesse diretório estão os scripts do sistema

conexion: Nesse repositório encontra-se o módulo de conexão com o banco de dados Oracle. Esse módulo possui

algumas funcionalidades úteis para execução de instruções DML e DDL, sendo possível obter JSON, Matriz e Pandas DataFrame.

Exemplo de utilização para consultas simples:

def listar_clientes(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select * 
                from clientes c
                order by c.nome_cliente
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

Exemplo de utilização para alteração de registros

from conexion.oracle_queries import OracleQueries



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



Outros exemplos: test.py

Caso esteja utilizando na máquina virtual antiga, você precisará alterar o método connect de:

self.conn = cx_Oracle.connect(user=self.user,
                        password=self.passwd,
                        dsn=self.connectionString()
                        )
Para:

self.conn = cx_Oracle.connect(user=self.user,
                        password=self.passwd,
                        dsn=self.connectionString(in_container=True)
                        )

controller: Nesse diretório encontram-sem as classes controladoras, responsáveis por realizar inserção, alteração e exclusão dos registros das tabelas.

model: Nesse diretório encontram-ser as classes das entidades descritas no diagrama relacional
reports Nesse diretório encontra-se a classe responsável por gerar todos os relatórios do sistema

sql: Nesse diretório encontram-se os scripts utilizados para geração dos relatórios a partir da classe relatorios. No nosso exemplo não utilizamos esse módulo, as consultas são passadas como atributos e método na classe Relatorio, path: "src/reports/relatorios.py" 
Exemplo:
#Relatorio clientes
        self.query_relatorio_clientes = '''    
            select c.cpf_cliente
            , c.nome_cliente
            , c.telefone_cliente
            , c.email_cliente
            from clientes c
            order by c.cpf_cliente 
        '''

utils: Nesse diretório encontram-se scripts de configuração e automatização da tela de informações iniciais

create_table_sistema_lanches_saudaveis.sql: Script responsável por criar as tabelas e registros fictícios. Esse script deve ser executado no sql developer antes do script principal.py para gerar as tabelas.

principal.py: Script responsável por ser a interface entre o usuário e os módulos de acesso ao Banco de Dados. Deve ser executado após a criação das tabelas.

Bibliotecas Utilizadas

requirements.txt: pip install -r requirements.txt
pip install cx_Oracle
pip install pandas
Ferramentas de dados do Visual Studio para C++

Em caso de problemas com a execução dos software dando a seguinte mensagem ORA-28001: the password has expired, execute as linhas de comando a seguir no Oracle:

ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;
ALTER USER SYSTEM IDENTIFIED BY "SYSTEM2023";
ALTER USER SYSTEM IDENTIFIED BY  "SYSTEM2023";
Instalando Oracle InstantClient
Baixe a versão do InstantClient de acordo com a versão do Banco de Dados

Caso esteja utilizando uma distribuição Linux baseado em Debian, será necessário executar o comando a seguir para converter o arquivo .rpm para .deb.

sudo alien --scripts oracle-instantclient18.5-basic-18.5.0.0.0-3.x86_64.rpm
Descompacte o arquivo e será gerado um diretório em um diretório de fácil acesso.

Mova os diretórios lib e share para dentro do diretório do InstantClient

sudo mv lib /usr/local/oracle/instantclient_18_5/
sudo mv share instantclient_18_5/
Edite o arquivo .bash_profile incluindo as linhas a seguir ao final do arquivo:

export ORACLE_HOME=/usr/local/oracle/instantclient_18_5/lib/oracle/18.5/client64
export LD_LIBRARY_PATH=$ORACLE_HOME/lib
export PATH=$PATH:$ORACLE_HOME/bin
export PATH
