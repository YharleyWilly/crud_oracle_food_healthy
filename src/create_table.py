from conexion.oracle_queries import OracleQueries

def crate_tables(query_sql: str):
    list_of_commands = query_sql.split(";")

    oracle = OracleQueries()
    oracle.connect()

    for command in list_of_commands:
        if len(command) > 0:
            print(f"Running command: {command}")
            try:
                oracle.executeDDL(command)
                print("Successfuly executed")
            except Exception as error:
                print(f"Error while running a command: {error}")

def generate_records(query_sql:str):
    list_of_commands = query_sql.split(";")

    oracle = OracleQueries()
    oracle.connect()

    for command in list_of_commands:
        if len(command) > 0:
            print(f"Running command: {command}")
            try:
                oracle.write(command)
                print("Successfuly executed")
            except Exception as error:
                print(f"Error while running a command: {error}")

def run():

    
    query1 = """     
        ALTER TABLE LABDATABASE.COMANDAS DROP CONSTRAINT CLIENTES_COMANDAS_FK;
        ALTER TABLE LABDATABASE.ITENS_COMANDA DROP CONSTRAINT COMANDAS_ITENS_COMANDA_FK;

        
        DROP TABLE LABDATABASE.CLIENTES;
        DROP TABLE LABDATABASE.COMANDAS;
        DROP TABLE LABDATABASE.ITENS_COMANDA;

        DROP SEQUENCE LABDATABASE.COMANDAS_ID_COMANDA_SEQ;
        DROP SEQUENCE LABDATABASE.ITENS_COMANDA_ID_ITEM_COMANDA_SEQ;

        CREATE TABLE LABDATABASE.CLIENTES (
                        CPF_CLIENTE VARCHAR(11) NOT NULL,
                        NOME_CLIENTE VARCHAR(255) NOT NULL,
                        TELEFONE_CLIENTE VARCHAR(11) NOT NULL,
                        EMAIL_CLIENTE VARCHAR(100) NOT NULL,
                        CONSTRAINT CPF PRIMARY KEY (CPF_CLIENTE)
        );

        CREATE TABLE LABDATABASE.COMANDAS (
                        ID_COMANDA INTEGER NOT NULL,
                        DATA_COMANDA DATE NOT NULL,
                        STATUS_COMANDA VARCHAR(50) NOT NULL,
                        CPF_CLIENTE VARCHAR(11) NOT NULL,
                        CONSTRAINT ID_COMANDA PRIMARY KEY (ID_COMANDA)
        );


        CREATE TABLE LABDATABASE.ITENS_COMANDA (
                        ID_ITEM_COMANDA INTEGER NOT NULL,
                        QTD_ITEM NUMERIC NOT NULL,
                        DESCRICAO_PRODUTO VARCHAR(255) NOT NULL,
                        VALOR_UNITARIO_ITEM NUMERIC(9,2) NOT NULL,
                        ID_COMANDA INTEGER NOT NULL,
                        CONSTRAINT ITENS_COMANDA_ID PRIMARY KEY (ID_ITEM_COMANDA)
        );

        CREATE SEQUENCE LABDATABASE.COMANDAS_ID_COMANDA_SEQ;
        CREATE SEQUENCE LABDATABASE.ITENS_COMANDA_ID_ITEM_COMANDA_SEQ;

        ALTER TABLE LABDATABASE.COMANDAS ADD CONSTRAINT CLIENTES_COMANDAS_fk
        FOREIGN KEY (CPF_CLIENTE)
        REFERENCES LABDATABASE.CLIENTES (CPF_CLIENTE)
        NOT DEFERRABLE;

        ALTER TABLE LABDATABASE.ITENS_COMANDA ADD CONSTRAINT COMANDAS_ITENS_COMANDA_fk
        FOREIGN KEY (ID_COMANDA)
        REFERENCES LABDATABASE.COMANDAS (ID_COMANDA)
        NOT DEFERRABLE;

        GRANT ALL ON LABDATABASE.CLIENTES TO LABDATABASE;
        GRANT ALL ON LABDATABASE.COMANDAS TO LABDATABASE;
        GRANT ALL ON LABDATABASE.ITENS_COMANDA TO LABDATABASE;

        ALTER USER LABDATABASE quota unlimited on USERS; 
    """



    crate_tables(query1)
    print("Tables successfully created!")

    

run()