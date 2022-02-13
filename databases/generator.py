import sqlite3
from random import *
from sqlite3.dbapi2 import Error


def create_table(con: sqlite3.Connection):
    cur = con.cursor()
    cur.executescript('''
        CREATE TABLE clients(
	        id INTEGER PRIMARY KEY AUTOINCREMENT,
	        name TEXT NOT NULL,
	        email TEXT NOT NULL,
	        tel TEXT NOT NULL,
	        address TEXT NOT NULL,
	        birth_date DATETIME NOT NULL,
            login TEXT UNIQUE NOT NULL, 
            registration_date DATE NOT NULL, 
            parol integer NOT NULL,
            parol_text TEXT NOT NULL
        );
        CREATE TABLE orders(
	        id INTEGER PRIMARY KEY AUTOINCREMENT,
	        type INTEGER NOT NULL,
	        address TEXT NOT NULL,
	        dilivery_date DATE NOT NULL,
	        client_id INTEGER NOT NULL,
	        FOREIGN KEY (client_id) REFERENCES clients(id)
        );
        CREATE TABLE products(
	        id INTEGER PRIMARY KEY AUTOINCREMENT,
	        name TEXT NOT NULL,
	        short_description TEXT NOT NULL,
	        description TEXT NOT NULL,
	        price INTEGER NOT NULL,
	        main_image TEXT NOT NULL,
	        amount INTEGER NOT NULL
        );
        CREATE TABLE order_good(
	        id INTEGER PRIMARY KEY AUTOINCREMENT,
	        order_id INTEGER NOT NULL,
	        good_id INTEGER NOT NULL,
	        amount INTEGER NOT NULL,
	        FOREIGN KEY (order_id) REFERENCES orders(id),
	        FOREIGN KEY (good_id) REFERENCES products(id)
        );
    
    ''')

    cur.close()


def add_clients(con: sqlite3.Connection, n: int):
    cur = con.cursor()
    cur.execute("SELECT login FROM clients")
    used_logins = set([a[0] for a in cur.fetchall()])
    used_logins.add('')
    names = ['George', 'Paul', 'Oleg', 'Mike', 'Lisa', 'Lera', 'Nat', 'Egor', 'Ira', 'Dan', 'Buddy',
             'Tereza', 'Madlen', 'Dasha', 'Vlada', 'Den', 'Mary', 'Ksenya', 'Anasteisa', 'Tima', 'Alex']
    emails = ['ya.ru', 'yandex.ru', 'gmail.com', 'mail.com']
    towns = ['Moscow', 'Lubertsy', 'StPetersburg', 'Nizhniy-Novgorod', 'Kazan']
    streets = ['Lenin', 'Kirova', 'Zheleznodorozhnaya',
               'Oktyabr', 'Komsomol', 'Mytnaya', 'Arbat', 'Poluboyarova']
    cods = ['903', '925', '495', '756', '457', '982', '874']

    clients = []
    for i in range(n):
        name = choice(names)
        address = choice(towns)+', '+choice(streets)+' street, ' + \
            str(randint(1, 20))+', '+str(randint(1, 100))
        email = name+str(randint(0, 9999))+'@'+choice(emails)
        tel = '8'+'('+choice(cods)+')'+str(randint(0, 9))+str(randint(0, 9))+str(randint(0, 9)) + \
            '-'+str(randint(0, 9))+str(randint(0, 9))+'-' + \
            str(randint(0, 9))+str(randint(0, 9))
        login = ''
        while login in used_logins:
            login = name[:randint(3, len(name))] + \
                str(randint(99999999, 9999999999))
        used_logins.add(login)
        parol = ''.join([choice('0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
                         for i in range(randint(4, 16))])
        birth_date = str(randint(1965, 2006))+'-' + \
            f'{randint(1,12):0>2}'+'-'+f'{randint(1,31):0>2}'
        registration_date = str(randint(2019, 2021))+'-' + \
            f'{randint(1,12):0>2}'+'-'+f'{randint(1,31):0>2}'
        clients.append((name, email, tel, address, birth_date,
                        registration_date, login, hash(parol), parol))

    cur.executemany(
        """INSERT INTO clients (name,email,tel,address,birth_date,registration_date,login,parol,parol_text) 
                        VALUES (?,       ?,  ?,      ?,         DATE(?),                DATE(?),     ?,    ?,?) 
        """, clients)

    cur.close()


def add_orders(con: sqlite3.Connection, n: int):
    cur = con.cursor()
    cur.execute("SELECT id FROM clients")
    client_ids = [a[0] for a in cur.fetchall()]
    client_type = {a: False for a in client_ids}
    cur.execute("SELECT client_id FROM orders")
    for i, in cur.fetchall():
        client_type[i] = True
    res = []
    for _ in range(n):
        client_id = choice(client_ids)
        typ = 1 if client_type[client_id] else randint(0, 1)
        if typ == 0:
            client_type[client_id] = True

        dilivery_date = str(2021)+'-' + \
            f'{randint(9,12):0>2}'+'-'+f'{randint(1,31):0>2}'
        res.append((typ, dilivery_date, client_id, client_id))
    cur.executemany("""INSERT INTO orders (type,dilivery_date,client_id,address) VALUES 
                                        (?,DATE(?),?,(SELECT address FROM clients WHERE id = ?))
    """, res)

    cur.close()


def add_products(con: sqlite3.Connection):
    cur = con.cursor()
    cur.executescript("""
        INSERT INTO products (name,short_description, description, price, main_image, amount) VALUES 
        ("Цепь Арго","Мягкие руки убаюкают Вас","Мягкие руки убаюкают Вас. Проводится мягким жгутом и профессиональными руками. Ваш мозг отдыхает от лишнего кислорода и избыточной крови.",453,"./images/strangulation.png",666),
        ("Шарф",	"Стандартный способ зависнуть с друзьями",	"Стандартный способ зависнуть с друзьями. Верёвка из волос Ваших кошмаров оплетёт нежную кожу шеи и сломает слабое звено хорды.",	820,	"./images/hanging.png",	42),
        ("Кухонный нож",	"Хороший массаж от наших профессионалов",	"Хороший массаж от наших профессионалов. Нет ничего лучше холодного ножа, проникающего сквозь кожу в мясо. Рекомендуется для людей, которым надо выпустить себя наружу.",	265,	"./images/chop.png",	137)
    """)
    con.commit()
    cur.close()


def add_connections(con: sqlite3.Connection):
    cur = con.cursor()
    cur.execute("SELECT id FROM products")
    good_ids = [a[0] for a in cur.fetchall()]
    cur.execute('select id from orders')
    for i, in cur.fetchall():
        dif = set([choice(good_ids) for _ in range(len(good_ids))])
        amount = [randint(1, 5) for _ in range(len(dif))]
        for pr, am in zip(dif, amount):
            cur.execute("insert into order_good (order_id,good_id,amount) values (:order, :good, :amount)", {
                        "order": i, "good": pr, "amount": am})

    cur.close()


if __name__ == '__main__':
    try:
        con = sqlite3.connect('./databases/for_aub.db')
        create_table(con)
        print('Table created')
        add_clients(con, 1000000)
        print('Clients added')
        add_products(con)
        print('Products added')
        add_orders(con, 3000000)
        print('Oreders added')
        add_connections(con)
        print('Connections added')
    except Error as e:
        print('Error:', e)
    else:
        print('Everything is Ok')
        con.commit()
        con.close()
