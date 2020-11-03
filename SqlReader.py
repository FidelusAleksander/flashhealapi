import pyodbc

class SqlReader:
    def __init__(self, config):
        self._config = config
        self.connstring = 'DRIVER=ODBC Driver 17 for SQL Server;SERVER={};DATABASE={};UID={};PWD={}'.format(
            self._config['sqlserver'],
            self._config['database'],
            self._config['user'],
            self._config['password'])

    def connection(self):
        connection = pyodbc.connect(self.connstring)
        return connection

    def fetch_doctors(self, specialty):
        query = '''WITH  reviews as (
            SELECT 
                doctor_id, 
                ROUND(AVG(CAST(star_rating AS FLOAT)), 1) as avg_review,
                COUNT(star_rating) as review_count
                FROM doctor_reviews GROUP BY doctor_id
            )
            
            SELECT d.*, 
            ISNULL(r.avg_review, 0) as avg_review , 
            ISNULL(r.review_count, 0) as reviews_count
            FROM dbo.doctors as d
            LEFT JOIN
            reviews as r
            ON d.doctor_id = r.doctor_id
        '''

        if specialty != 'all':
            query += f" WHERE specialty = '{specialty}'"

        cursor = None
        conn = None

        result = []

        try:
            conn = self.connection()
            cursor = conn.cursor()
            cursor.execute(query)

            columns = [column[0] for column in cursor.description]

            for row in cursor.fetchall():
                result.append(dict(zip(columns, row)))

        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return result

    def fetch_doctor_details(self, doctor_id):
        query = f"SELECT * FROM dbo.doctor_reviews_by_id({doctor_id})"

        cursor = None
        conn = None

        result = []

        try:
            conn = self.connection()
            cursor = conn.cursor()
            cursor.execute(query)

            columns = [column[0] for column in cursor.description]

            for row in cursor.fetchall():
                result.append(dict(zip(columns, row)))

        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return result


    def insert(self, data):

        cursor = None
        conn = None

        result = []

        try:
            conn = self.connection()
            cursor = conn.cursor()
            for i in data.index:
                query = f"INSERT INTO dbo.doctors VALUES ('{data['first_name'][i]}', '{data['last_name'][i]}', '{data['specialty'][i]}', {data['latitude'][i]}, {data['longtitude'][i]})"

                cursor.execute(query)
                cursor.commit()


        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return result
