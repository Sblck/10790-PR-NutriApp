from modelos.user import User


class UserRepository:
    def __init__(self, ligacao):
        self.ligacao = ligacao


    def save(self, user: User):
        cursor = self.ligacao.cursor()
        # necessita da tabela
        query = ""
        cursor.execute(query)
        self.ligacao.commit()

        #atualizar class utilizador com o id atribuido
        #utilizador.id = comando
        cursor.close()
        return user
    

    def get_user(self, email, password):
        '''
        Retorna um utilizador objeto User com base na combinação email-password
        Retorna None - email ou password errada
        '''
        cursor = self.ligacao.cursor()
        querry = ""
        cursor.execute(querry)
        utilizador = cursor.fetchone()
        cursor.close()
        if utilizador:
            return User(
                id = utilizador[0],
                email = utilizador[1],
                password = utilizador[2]
                )
        return None

    
