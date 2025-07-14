

from modelos.user import User


class UserService:
    def __init__(self, repo, gestor):
        self.repo = repo
        self.gestor = gestor
    

    def registar_user(self, **dados):
        #verificar se já se existe 
        #if self.repo 

        user = User(**dados)
        #if user dados valido

        #chamar o repositor para users
        self.repo.save(user)
