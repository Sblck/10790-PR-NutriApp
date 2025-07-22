

class userProfile:
    '''
    Class com os dados de perfil de um utilizador
    '''
    def __init__(
        self,
        user_id, 
        nome, 
        data_nascimento, 
        altura_cm, 
        genero, 
        peso_inicial_kg, 
        peso_kg, 
        data_criacao, 
        ultima_atualizacao,
        id=None, 
    ):
        self.id = id
        self.user_id = user_id
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.altura_cm = altura_cm
        self.genero = genero
        self.peso_inicial_kg = peso_inicial_kg
        self.peso_kg = peso_kg
        self.data_criacao = data_criacao
        self.ultima_atualizacao = ultima_atualizacao

    def is_valid(self) -> bool:
        '''
        Valida se os campos obrigatórios existem
        '''
        return all([
            self.user_id is not None,
            self.nome is not None,
            self.data_nascimento is not None,
            self.altura_cm is not None,
            self.genero is not None,
            self.peso_inicial_kg is not None,
            self.peso_kg is not None,
            self.data_criacao is not None,
            self.ultima_atualizacao is not None
        ])
        