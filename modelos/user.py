

class User:
    '''
    Class user -> utilizador
    Descreve um utilizador único registado no sistema por meio de um email e password.

    '''
    def _init__(self, email, password, id=None):
        self.id = id
        self.email = email
        self.password = password


    def is_valid(self):
        '''
        Valida se os campos obrigatórios existem
        '''
        return self.email is not None and self.password is not None