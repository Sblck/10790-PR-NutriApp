

class UserManager:
    def __init__(self, repo):
        self.repo = repo


    def validate_dados(self, user):
        '''
        Valida se os dados do utilizador são validos
        Raises erros com descrição de falha
        '''
        if not user.is_valid():
            raise ValueError("Campos Email e password são necessários")
        if not self.is_email_unique(user.email):
            raise ValueError("O Email já se encontra em uso")
        ## outros parametros
    
    def is_email_unique(self, email):
        #querry ao repo users
        #ex: if repo.get_email(email)
        pass


    #outros métodos