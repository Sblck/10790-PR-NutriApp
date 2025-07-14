

class User:
    '''
    Class user -> utilizador
    Descreve um utilizador único registado no sistema por meio de um email e password.

    '''
    def _init__(self, email, password, id=None):
        self.id = id
        self.email = email
        self.password = password