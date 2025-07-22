from modelos.plano import Plano
from persistencia.basedados.DataBase import DataBase

class PlanoRepository:
    def __init__(self, db : DataBase):
        self.db = db


    def save_new_plano(self, plano : Plano):
        self.db.execute(
            """
            INSERT INTO plano (user_id, nome, estado, data_inicio)
            VALUES (%s, %s, %s, %s)
            """,
            (plano.user_id, plano.nome, plano.estado, plano.data_inicio)
        )
        plano.id = self.db.cursor.lastrowid

        return plano

    def get_by_user_id(self, user_id):
        self.db.execute("SELECT id, user_id, nome, data_inicio, data_fim, estado FROM plano WHERE user_id = %s", (user_id,))
        return [Plano(id=row[0], user_id=row[1], nome=row[2], data_inicio=row[3], data_fim=row[4], estado=row[5]) for row in self.db.fetchall()] 