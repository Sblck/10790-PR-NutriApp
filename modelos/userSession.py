# Class que contém toda a informação do utilizador corrente

# Quando instanciado em run-time dar querry a base de dados para popular campos

class UserSession:
    def __init__(self, user, profile=None, plano=None, objetivo=None, metas=None) -> None:
        self.user = user
        self.profile = profile
        self.plano = plano
        self.objetivo = objetivo
        self.metas = metas or []  # lista de metas ? semanais ? ou target calorico

# outros metodos, getters nd setters etc

    #TODO : 
    def __repr__(self):
        return (f"<UserSession user={self.user.email} profile={self.profile} "
                f"plano={self.plano} objetivo={self.objetivo}>")