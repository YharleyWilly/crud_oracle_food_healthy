from datetime import date
from model.clientes import Cliente

class Comanda:
    
    def __init__(self, id_comanda:int=None, data_comanda:date=None, status_comanda:str= None, 
                 cliente:Cliente=None
                 ):
        
        self.set_id_comanda(id_comanda)
        self.set_data_comanda(data_comanda)
        self.set_status_comanda(status_comanda)
        self.set_cliente(cliente)


    def set_id_comanda(self, id_comanda:int):
        self.id_comanda = id_comanda

    def set_data_comanda(self, data_comanda:date):
        self.data_comanda = data_comanda

    def set_status_comanda(self, status_comanda:str):
        self.status_comanda = status_comanda

    def set_cliente(self, cliente:Cliente):
        self.cliente = cliente

    def get_id_comanda(self) -> int:
        return self.id_comanda

    def get_data_comanda(self) -> date:
        return self.data_comanda

    def get_status_comanda(self) -> str:
        return self.status_comanda
    
    def get_cliente(self) -> Cliente:
        return self.cliente

    def atualizar_status_comanda(self, alterar_status: int):
        """
        Atualiza o status da comanda com base no valor passado como parâmetro.

        Parâmetros:
            alterar_status (int): O valor que indica a ação a ser tomada no status da comanda.
                1: Altera o status para "Em andamento".
                2: Altera o status para "Pronto".
                3: Altera o status para "Cancelado".
        """
        if alterar_status == 1:        
            self.status_comanda = "Em andamento"                  
        elif alterar_status == 2:      
            self.status_comanda = "Pronto"
        elif alterar_status == 3:
            self.status_comanda = "Cancelado"
        else:
            print("Opção inválida")
        return self.status_comanda  # Retorna o novo status

     
    """
    #Metodo para deixar comanda em status "Em andamento"
    def andamento_comanda(self):
        if self.status_comanda == "Aberto":
            self.status_comanda = "Em andamento"
        else:
            print("A comanda já está em andamento ou em outro estado.")
    
    #Metodo para deixar comanda em status "Cancelado"
    def cancelar_comanda(self):   
        self.status_comanda = "Cancelado"
    
    #Metodo para deixar a comanda em status "Pronto"
    def finalizar_comanda(self):
        if self.status_comanda == "Em andamento":
            self.status_comanda = "Pronto"
        else:
            print("A comanda já está finalizada ou em outro estado.")
    """
    
    def to_string(self) -> str:
        return f"Comanda: {self.get_id_comanda()} | Data: {self.get_data_comanda()} | Status: {self.get_status_comanda()} | CPF Cliente: {self.get_cliente().get_CPF()}"