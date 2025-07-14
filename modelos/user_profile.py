

class userProfile:
    '''
    Class com os dados de perfil de um utilizador
    Nota: Vários dados serão necessários para o cálculos no futuro mas tempráriamente como None para permitir testes rápidos
    '''
    def __init__(self, user_id, nome, data_nascimento=None, altura_cm=None, genero=None, peso_inicial_kg=None, peso_kg=None, data_criacao=None, ultima_atualizacao=None):
        self.user_id = user_id
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.altura_cm = altura_cm
        self.genero = genero
        self.peso_inicial_kg = peso_inicial_kg
        self.peso_kg = peso_kg
        self.data_criacao = data_criacao
        self.ultima_atualizacao = ultima_atualizacao
        