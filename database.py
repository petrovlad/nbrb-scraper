from mysql.connector import connect, Error


class MySQLDB:
    def __init__(self, host, user, password, db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name

    def execute_sql_code(self, sql_code, tuple):
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql_code, tuple)
                    connection.commit()
        except Error as e:
            print(e)

    def clear_stats(self):
        try:
            self.execute_sql_code(f'truncate table {self.db_name}.course_stat', None)
            self.execute_sql_code(f'truncate table {self.db_name}.currency', None)
        except Error as e:
            print(e)

    def get_all(self):
        resp = []
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"""
                    select cs.stat_id,
                           cs.stat_date,
                           cr.full_name,
                           cr.abbreviation,
                           cs.curr_amount, 
                           cs.curr_course
                    from {self.db_name}.course_stat cs
                        join {self.db_name}.currency cr on cs.curr_id = cr.id  
                    """)
                    for (stat_id, stat_date, curr_name, curr_abbrv, curr_amount, curr_course) in cursor:
                        resp.append({
                            'id': stat_id,
                            'date': stat_date,
                            'currency_name': curr_name,
                            'currency_abbreviation': curr_abbrv,
                            'currency_amount': curr_amount,
                            'currency_course': curr_course
                        })
        except Error as e:
            print(e)
        return resp

    def show_table(self, table_name):
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(f'select * from {self.db_name}.{table_name}')
                    for item in cursor:
                        print(item)
        except Error as e:
            print(e)

    def add_course_stat(self,
                        date,
                        currency_name: str,
                        currency_abbreviation: str,
                        currency_amount: float,
                        currency_course: float):
        with connect(
                host=self.host,
                user=self.user,
                password=self.password
        ) as connection:
            with connection.cursor() as cursor:
                existing_curr_query = f"""
                    select id from {self.db_name}.currency where abbreviation = '{currency_abbreviation}' limit 1              
                """
                cursor.execute(existing_curr_query)
                ret = cursor.fetchall()
                existing_curr_id = None if not ret else ret[0][0]

                insert_course_query = f"""
                    insert into {self.db_name}.currency (full_name, abbreviation)
                    values (%s, %s) 
                    on duplicate key update full_name = full_name
                """
                cursor.execute(insert_course_query, (currency_name, currency_abbreviation))

                insert_stat_query = f"""
                    insert into {self.db_name}.course_stat (stat_date, curr_id, curr_amount, curr_course)
                    values
                        (%s, coalesce(%s, last_insert_id()), %s, %s)
                """
                cursor.execute(insert_stat_query, (date, existing_curr_id, currency_amount, currency_course))
                connection.commit()
