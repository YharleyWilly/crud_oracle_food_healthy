from model.comandas import Comanda

class ItemComanda:
    
    def __init__(self, 
                 id_item_comanda:int=None,
                 qtd_item:int=None,
                 descricao_produto:str=None,
                 valor_unitario_item:int=None,
                 comanda:Comanda=None,
                 ):
        
        self.set_id_item_comanda(id_item_comanda)
        self.set_qtd_item(qtd_item)
        self.set_descricao_produto(descricao_produto)
        self.set_valor_unitario_item(valor_unitario_item)
        self.set_comanda(comanda)

    def set_id_item_comanda(self, id_item_comanda:int):
        self.id_item_comanda = id_item_comanda

    def set_qtd_item(self, qtd_item:int):
        self.qtd_item = qtd_item
        
    def set_descricao_produto(self, descricao_produto:str):
        self.descricao_produto = descricao_produto

    def set_valor_unitario_item(self, valor_unitario_item:int):
        self.valor_unitario_item = valor_unitario_item
    
    def set_comanda(self, comanda:Comanda):
        self.comanda = comanda

    def get_id_item_comanda(self) -> int:
        return self.id_item_comanda

    def get_qtd_item(self) -> int:
        return self.qtd_item

    def get_descricao_produto(self) -> str:
        return self.descricao_produto

    def get_valor_unitario_item(self) -> int:
        return self.valor_unitario_item
    
    def get_comanda(self) -> Comanda:
        return self.comanda

    def to_string(self):
        return f"Item: {self.get_id_item_comanda()} | Quantidade: {self.get_qtd_item()} | Descricao Produto: {self.get_descricao_produto()} | Valor Unitario: {self.get_valor_unitario_item()} | Comanda: {self.get_comanda().get_id_comanda()}"