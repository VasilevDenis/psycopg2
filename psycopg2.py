import psycopg2


class ClientsHandler:
    def __init__(self, database, user, password):
        self.database = database
        self.user = user
        self.password = password

    def create_tables(self):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            cur = conn.cursor()
            cur.execute("""
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
                """)
            conn.commit()
            cur.close()

    def add_client(self, email, first_name, last_name):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO clients (email, first_name, last_name)
            VALUES (%s, %s, %s)
            ;
            """, (email, first_name, last_name))
            conn.commit()
            cur.close()

    def add_phone(self, email, phone_number):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO phones (email, phone_number)
            VALUES (%s, %s)
            ;
            """, (email, phone_number))
            conn.commit()
            cur.close()

    def delete_client(self, email):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            cur = conn.cursor()
            try:
                conn.autocommit = False
                delete_client_query = "DELETE FROM clients WHERE email=%s"
                cur.execute(delete_client_query, (email,))
                delete_phones_query = "DELETE FROM phones WHERE email=%s"
                cur.execute(delete_phones_query, (email,))
                conn.commit()
            except psycopg2.Error as e:
                print(str(e))
                conn.rollback()
            finally:
                cur.close()

    def delete_phone(self, phone_number):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            cur = conn.cursor()
            cur.execute("""
            DELETE FROM phones
            WHERE phone_number=%s
            ;
            """, (phone_number,))
            conn.commit()
            cur.close()

    def update_client(self, email, first_name, last_name):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            cur = conn.cursor()
            try:
                cur.execute("""
                UPDATE clients SET (first_name, last_name) = (%s, %s)
                WHERE email = %s
                ;""", (first_name, last_name, email))
                conn.commit()
            except psycopg2.Error as e:
                print(f"Error updating client: {e}")
            finally:
                cur.close()

    def search_client_by_email(self, email):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM clients WHERE email = %s", (email,))
            client = cur.fetchone()
            if client is not None:
                print(client)
            else:
                print(f"No client")
            cur.close()

    def search_client_by_first_name(self, first_name):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM clients WHERE first_name = %s", (first_name,))
            client = cur.fetchall()
            if client is not None:
                print(client)
            else:
                print(f"No client")
            cur.close()

    def search_client_by_last_name(self, last_name):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM clients WHERE last_name = %s", (last_name,))
            client = cur.fetchall()
            if client is not None:
                print(client)
            else:
                print(f"No client")
            cur.close()

    def search_client_by_phone_number(self, phone_number):
        with psycopg2.connect(database=self.database, user=self.user, password=self.password) as conn:
            cur = conn.cursor()
            cur.execute("SELECT email FROM phones WHERE phone_number = %s", (phone_number,))
            email = cur.fetchone()
            if email is not None:
                cur.execute("SELECT * FROM clients WHERE email = %s", (email,))
                client = cur.fetchone()
                print(client)
            else:
                print(f"No client")
            cur.close()


clients_handler = ClientsHandler('clients_db', 'postgres', '1213796')
clients_handler.create_tables()
"""
clients_handler.add_client('john_connor@gmail.com', 'John', 'Connor')
clients_handler.add_client('future@chatgpt.com', 'Terminator', 'T1000')
clients_handler.add_client('sarah_connor@gmail.com', 'Sarah', 'Connor')
clients_handler.add_phone('sarah_connor@gmail.com', '9234134341')
clients_handler.add_phone('john_connor@gmail.com', '4656456565')
clients_handler.add_phone('john_connor@gmail.com', '9822222711')
clients_handler.delete_phone('4656456565')
clients_handler.update_client('sarah_connor@gmail.com', 'Elena', 'Semiglazova')
clients_handler.delete_client('john_connor@gmail.com')
clients_handler.add_client('sarah_connor@gmail.com', 'Sarah', 'Connor')
clients_handler.search_client_by_email('john_connor@gmail.com')
clients_handler.search_client_by_first_name('Terminator')
clients_handler.search_client_by_last_name('Connor')
clients_handler.search_client_by_phone_number('9234134341')
"""
