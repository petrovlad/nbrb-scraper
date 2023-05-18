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
            with connect(
                host=self.host,
                user=self.user,
                password=self.password
            ) as connection:
                self.execute_sql_code('truncate table {self.db_name}.currency_stat', None)
        except Error as e:
            print(e)

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

    def add_currency_stat(self, date, currency_name, currency_amount, currency_course):
    
        insert_stat_query = f"""
            insert into {self.db_name}.currency_stat (stat_date, curr_name, curr_amount, curr_course)
            values
                (%s, %s, %s, %s)
        """
        self.execute_sql_code(insert_stat_query, (date, currency_name, currency_amount, currency_course))
