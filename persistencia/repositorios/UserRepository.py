from typing import Optional
from modelos.user import User
from persistencia.basedados.DataBase import DataBase


class UserRepository:
    def __init__(self, db: DataBase):
        """
        Repositório responsável pelas operações relacionadas ao utilizador.
        Recebe uma instância da classe DataBase para acesso centralizado à base de dados e seus métodos.
        """
        self.db = db


    def save_new_user(self, user: User) -> User:
        """
        Guarda um novo utilizador na base de dados.
        Atualiza o objeto user com o id atribuido.
        """
        query = "INSERT INTO users (email, password) VALUES (%s, %s)"
        params = (user.email, user.password)
        self.db.execute(query, params)
        # obter o id gerado pelo MySQL
        user.id = self.db.cursor.lastrowid
        return user
    
    
    def get_user(self, email : str , password : str) -> Optional[User]:
        """
        Retorna um objeto User com base na combinação email-password.
        Retorna None se email ou password estiverem errados.
        """
        query = "SELECT id, email, password FROM users WHERE email = %s AND password = %s"
        params = (email, password)
        self.db.execute(query, params)
        utilizador = self.db.cursor.fetchone()
        if utilizador:
            return User(
                id=utilizador[0],
                email=utilizador[1],
                password=utilizador[2]
            )
        return None
    

    def email_exists(self, email: str) -> bool:
        '''
        Procura na tabela users por uma linha onde o campo email seja igual ao valor email fornecido.
        Sem retornar dados sensíveis ao retornar (retorna 1)
        Retorna True se existe, False se não existe um email registado.
        '''
        query = "SELECT 1 FROM users WHERE email = %s"
        self.db.execute(query, (email,))
        result = self.db.cursor.fetchone()
        return result is not None 