from modelos.objetivo import Objetivo

class ObjetivoRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        self.db.execute("SELECT id, nome FROM objetivo")
        return [Objetivo(id=row[0], nome=row[1]) for row in self.db.fetchall()]

    def get_by_nome(self, nome):
        self.db.execute("SELECT id, nome FROM objetivo WHERE nome = %s", (nome,))
        row = self.db.cursor.fetchone()
        return Objetivo(id=row[0], nome=row[1]) if row else None

    def get_by_id(self, id):
        self.db.execute("SELECT id, nome FROM objetivo WHERE id = %s", (id,))
        row = self.db.cursor.fetchone()
        return Objetivo(id=row[0], nome=row[1]) if row else None 