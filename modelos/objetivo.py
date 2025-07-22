class Objetivo:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        # descricao
        #outros futuro

    def __repr__(self):
        return f"<Objetivo id={self.id} nome={self.nome}>"
# objetcA.equals(ObjectB)
    def __eq__(self, other):
        if isinstance(other, Objetivo):
            return self.id == other.id and self.nome == other.nome
        return False 