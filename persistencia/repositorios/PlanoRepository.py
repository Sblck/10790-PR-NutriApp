from modelos.plano import Plano
from persistencia.basedados.DataBase import DataBase

class PlanoRepository:
    def __init__(self, db : DataBase):
        self.db = db


    def save_new_plano(self, plano):
        self.db.execute(
            """
            INSERT INTO plano (user_id, nome, estado)
            VALUES (%s, %s, %s)
            """,
            (plano.user_id, plano.nome, plano.estado)
        )
        plano.id = self.db.cursor.lastrowid
        # querry as datas  atribuidas pela base de dados e atualizar o objeto em memoria
        self.db.execute(
            "SELECT data_inicio, data_fim FROM plano WHERE id = %s",
            (plano.id,)
        )
        result = self.db.cursor.fetchone()
        if result:
            plano.data_inicio = result[0]
            plano.data_fim = result[1]

        return plano

    def get_by_user_id(self, user_id):
        self.db.execute("SELECT id, user_id, nome, data_inicio, data_fim, estado FROM plano WHERE user_id = %s", (user_id,))
        return [Plano(id=row[0], user_id=row[1], nome=row[2], data_inicio=row[3], data_fim=row[4], estado=row[5]) for row in self.db.fetchall()] 