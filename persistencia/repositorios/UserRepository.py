from modelos.user import User
from persistencia.basedados.DataBase import DataBase


class UserRepository:
    def __init__(self, db: DataBase):
        """
        Repositório responsável pelas operações relacionadas ao utilizador.
        Recebe uma instância da classe DataBase para acesso centralizado à base de dados e seus métodos.
        """
        self.db = db

    def save(self, user: User):
        """
        Guarda um novo utilizador na base de dados.
        Atualiza o objeto user com o id atribuido.
        """
        query = "INSERT INTO users (email, password) VALUES (%s, %s)"
        params = (user.email, user.password)
        self.db.execute(query, params)
        # TODO : Recuperar o id gerado pelo MySQL
        #user.id =
        return user
    
    def get_user(self, email, password):
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