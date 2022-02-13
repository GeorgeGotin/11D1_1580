import sqlite3
import random


def change_parol(con: sqlite3.Connection, login, old_parol, new_parol):
    cur = con.cursor()
    cur.execute("select parol from clients where login = :login",
                {"login": login})
    base = cur.fetchone()[0]
    if base == hash(old_parol):
        cur.execute("update clients set parol = :new_parol where login = :login", {
                    "new_parol": hash(new_parol), "login": login})
        cur.commit()
        cur.close()
        return 'Successfuly'
    else:
        return 'Wrong parol'


def sum_of_order(con: sqlite3.Connection, order_id):
    cur = con.cursor()
    cur.execute("SELECT order_good.amount as am, products.price as pr FROM order_good,products WHERE order_good.order_id = :order AND order_good.good_id = products.id", {
                "order": order_id})
    res = sum([i[0]*i[1] for i in cur.fetchall()])
    cur.close()
    return res


def product_for_period(con: sqlite3.Connection, start='1900-01-01', end='9999-12-31'):
    cur = con.cursor()
    cur.execute("SELECT id,price FROM products")
    products = {}
    for i, price in cur.fetchall():
        cur.execute(
            "SELECT sum(amount) FROM order_good LEFT JOIN orders ON order_good.order_id = orders.id WHERE good_id = :good AND orders.dilivery_date BETWEEN DATE(:start) AND DATE(:end)", {"good": i, "start": start, "end": end})
        amount = cur.fetchone()[0]
        products[i] = {"amount": amount, "sum": price*amount}
    cur.close()
    return products


def choice_of_client(con: sqlite3.Connection, client_id):
    cur = con.cursor()
    cur.execute("SELECT id FROM products")
    amounts = {}
    for i, in cur.fetchall():
        cur.execute(
            "SELECT sum(amount) FROM order_good LEFT JOIN orders ON order_good.order_id = orders.id WHERE good_id = :good AND orders.client_id = :id", {"good": i, "id": client_id})
        amounts[i] = cur.fetchone()[0]
    cur.close()
    return amounts


def email_product_period(con: sqlite3.Connection, product_id, start='1900-01-01', end='9999-12-31'):
    cur = con.cursor()
    cur.execute("SELECT order_id FROM order_good LEFT JOIN orders ON order_good.order_id = orders.id WHERE good_id = :good AND orders.dilivery_date BETWEEN DATE(:start) AND DATE(:end)", {
                "good": product_id, "start": start, "end": end})
    emails = {}
    for i, in cur.fetchall():
        cur.execute(
            "SELECT name,email FROM clients LEFT JOIN orders ON orders.client_id = clients.id WHERE orders.id = :id", {"id": i})
        res = cur.fetchone()
        emails[res[0]] = res[1]
    cur.close()
    return emails


def sum_of_order(con: sqlite3.Connection, i):
    cur = con.cursor()
    cur.execute(
        "SELECT sum(products.price*order_good.amount) FROM order_good LEFT JOIN products ON order_good.good_id = products.id WHERE order_good.order_id = :id", {"id": i})
    res = cur.fetchone()[0]
    cur.close()
    return res


def add_product_to_order(con: sqlite3.Connection, order_id: int, product_id: int, amount: int):
    cur = con.cursor()
    cur.execute("SELECT amount FROM order_good WHERE order_id = :order AND good_id = :good", {
                "order": order_id, "good": product_id})
    res = cur.fetchall()
    if len(res) == 0:
        cur.execute("INSERT INTO order_good (order_id,good_id,amount) VALUES (:order,:good,:amount)", {
                    "order": order_id, "good": product_id, "amount": amount})
    else:
        cur.execute("UPDATE order_good SET amount = :new_amount WHERE order_id = :order AND good_id = :good", {
                    "new_amount": amount+res[0][0], "order": order_id, "good": product_id})
    con.commit()
    cur.close()


if __name__ == '__main__':

    '''con = sqlite3.connect('./databases/shop_data.db')
    print(add_product_to_order(con, 1, 2, 1))

    con.close()'''
    def foo(a):
        return a**2
    assert foo(5) == 25, "25"
    assert foo(6) in [36, 15, 0], "36"
    assert foo(12) == 113, "12 в квадрате должно быть равно 144"
