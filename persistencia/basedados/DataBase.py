import configparser
import mysql.connector

class DataBase:
    """
    Classe responsável por gerir a ligação a base de dados e fornecer métodos utilitários
    para executar comandos SQL, obter resultados e criar as tabelas principais do sistema.
    Lê as configurações do ficheiro config.ini.
    """
    def __init__(self, config_path='config.ini'):
        """
        Inicializa a ligação a base de dados usando as configurações fornecidas no ficheiro config.ini.
        Lança uma exceção se nao for possível estabelecer a ligação.
        """
        config = configparser.ConfigParser()
        config.read(config_path)
        db = config['database']
        try:
            self.connection = mysql.connector.connect(
                host=db['host'],
                user=db['user'],
                password=db['password'],
                database=db['dbname']
            )
            self.cursor = self.connection.cursor()
            print("Ligação estabelecida com sucesso!")
        except mysql.connector.Error as erro:
            print(f"Erro ao estabelecer ligação à BD: {erro}")
            raise  # TODO : TRATAR DEPOIS

    def execute(self, query, params=None):
        """
        Executa um comando SQL (INSERT, UPDATE, DELETE, etc.) na base de dados.
        :param query: Comando SQL a ser executado.
        :param params: Parametros opcionais para o comando SQL.
        """
        self.cursor.execute(query, params or ())
        self.connection.commit()

    def fetchall(self):
        """
        Retorna todos os resultados da ultima consulta (querry) executada.
        :return: Lista de tuplos com os resultados.
        """
        return self.cursor.fetchall()

    def close(self):
        """
        Fecha o cursor e a ligação com a base de dados.
        NOTA : Deve ser chamado ao terminar as operações com a base de dados.
        """
        self.cursor.close()
        self.connection.close()