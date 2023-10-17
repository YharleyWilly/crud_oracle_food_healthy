class Cliente:
    
    def __init__(self, 
                 CPF:str=None, 
                 nome:str=None,
                 telefone:str=None,
                 email:str=None
                ):
        
        self.set_CPF(CPF)
        self.set_nome(nome)
        self.set_telefone(telefone)
        self.set_email(email)

    def set_CPF(self, CPF:str):
        self.CPF = CPF

    def set_nome(self, nome:str):
        self.nome = nome

    def set_telefone(self, telefone:str):
        self.telefone = telefone
        
    def set_email(self, email:str):
        self.email = email    

    def get_CPF(self) -> str:
        return self.CPF

    def get_nome(self) -> str:
        return self.nome
    
    def get_telefone(self) -> str:
        return self.telefone
    
    def get_email(self) -> str:
        return self.email

    def to_string(self) -> str:
        return f"CPF: {self.get_CPF()} | Nome: {self.get_nome()} | Telefone: {self.get_telefone()} | Email: {self.get_email()}"