import psycopg2
import csv

from variables import CUSTOMERS, EMPLOYEES, ORDERS


def load_from_csv(filepath):
    try:
        with open(filepath, encoding='utf-8') as file:
            csv_file = csv.DictReader(file)
            return list(csv_file)
    except FileNotFoundError as e:
        print(e)
        return []


# подставить имя и пароль такие же как и в docker-compose.yaml
connect = psycopg2.connect(database='north', user='...', password='...')
try:
    with connect as conn:
        with conn.cursor() as cur:

            customers = load_from_csv(CUSTOMERS)
            employees = load_from_csv(EMPLOYEES)
            orders = load_from_csv(ORDERS)

            if customers == [] or employees == [] or orders == []:
                raise FileNotFoundError('Файл csv не найден')

            for item in customers:
                cur.execute('INSERT INTO customers VALUES (%s, %s, %s)',
                            (item['customer_id'], item['company_name'], item['contact_name']))

            for item in employees:
                cur.execute('INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)',
                            (item['employee_id'], item['first_name'],
                             item['last_name'], item['title'], item['birth_date'], item['notes']))

            for item in orders:
                cur.execute('INSERT INTO orders VALUES (%s, %s, %s, %s, %s)',
                            (item['order_id'], item['customer_id'], item['employee_id'], item['order_date'],
                             item['ship_city']))

finally:
    conn.close()
