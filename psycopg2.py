import psycopg2


class ClientsHandler:
    def __init__(self, database, user, password):
        self.database = database
        self.user = user
        self.password = password
        self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)

    def __exit__(self):
        self.conn.close()

    def create_tables(self):
        sql = """
            CREATE TABLE IF NOT EXISTS clients (
                email VARCHAR(50) PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL
                );

            CREATE TABLE IF NOT EXISTS phones (
                email VARCHAR(50) REFERENCES clients(email) ON DELETE CASCADE,
                phone_number VARCHAR(50),
                PRIMARY KEY (email, phone_number)
                );
                """
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql)

    def add_client(self, email, first_name, last_name):
        sql = """
            INSERT INTO clients (email, first_name, last_name)
            VALUES (%s, %s, %s)
            ;
            """
        params = (email, first_name, last_name)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)

    def add_phone(self, email, phone_number):
        sql = """
            INSERT INTO phones (email, phone_number)
            VALUES (%s, %s)
            ;
            """
        params = (email, phone_number)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)

    def delete_client(self, email):
        sql = "DELETE FROM clients WHERE email=%s"
        sql2 = "DELETE FROM phones WHERE email=%s"
        params = (email,)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                cur.execute(sql2, params)

    def delete_phone(self, phone_number):
        sql = """
            DELETE FROM phones
            WHERE phone_number=%s
            ;
            """
        params = (phone_number,)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)

    def update_client(self, email, **kwargs):
        sql = ''
        for key, value in kwargs.items():
            match key:
                case 'first_name':
                    sql = "UPDATE clients SET first_name = %s WHERE email = %s"
                case 'last_name':
                    sql = "UPDATE clients SET last_name = %s WHERE email = %s"
                case 'phone_number':
                    sql = "UPDATE phones SET phone_number = %s WHERE email = %s"
            params = (value, email)
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(sql, params)

    def search_client(self, **kwargs):
        for key, value in kwargs.items():
            sql = ''
            match key:
                case 'email':
                    sql = "SELECT * FROM clients WHERE email = %s"
                case 'first_name':
                    sql = "SELECT * FROM clients WHERE first_name = %s"
                case 'last_name':
                    sql = "SELECT * FROM clients WHERE last_name = %s"
                case 'phone_number':
                    sql = "SELECT email FROM phones WHERE phone_number = %s"
            params = (value,)
            with self.conn:
                with self.conn.cursor() as cur:
                    if key == 'phone_number':
                        cur.execute(sql, params)
                        email = cur.fetchone()
                        sql = "SELECT * FROM clients WHERE email = %s"
                        params = (email,)
                    cur.execute(sql, params)
                    client = cur.fetchone()
                    if client is not None:
                        return client
                    else:
                        return "No client"


if __name__ == '__main__':
    clients_handler = ClientsHandler('clients_db', 'postgres', '1213796')
    clients_handler.create_tables()
    '''
    clients_handler.update_client(email='sarah_connor@gmail.com', first_name='Alena', last_name='Vosmiglazova')
    clients_handler.add_client('john_connor@gmail.com', 'John', 'Connor')
    clients_handler.add_client('future@chatgpt.com', 'Terminator', 'T1000')
    clients_handler.add_client('sarah_connor@gmail.com', 'Sarah', 'Connor')
    clients_handler.add_phone('sarah_connor@gmail.com', '9234134341')
    clients_handler.add_phone('john_connor@gmail.com', '4656456565')
    clients_handler.add_phone('john_connor@gmail.com', '9822222711')
    clients_handler.delete_phone('4656456565')
    clients_handler.update_client(email='sarah_connor@gmail.com', first_name='Alena', last_name='Vosmiglazova')
    clients_handler.delete_client('john_connor@gmail.com')
    clients_handler.add_client('sarah_connor@gmail.com', 'Sarah', 'Connor')
    print(clients_handler.search_client('john_connor@gmail.com))
    print(clients_handler.search_client_by_phone_number('9234134341'))
    '''

