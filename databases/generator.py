from random import *


'''
names = ['George', 'Paul', 'Oleg', 'Mike', 'Lisa', 'Lera', 'Nat', 'Egor', 'Ira', 'Dan', 'Buddy',
         'Tereza', 'Madlen', 'Dasha', 'Vlada', 'Den', 'Mary', 'Ksenya', 'Anasteisa', 'Tima', 'Alex']
emails = ['ya.ru', 'yandex.ru', 'gmail.com', 'mail.com']
towns = ['Moscow', 'Lubertsy', 'StPetersburg', 'Nizhniy-Novgorod', 'Kazan']
streets = ['Lenin', 'Kirova', 'Zheleznodorozhnaya',
           'Oktyabr', 'Komsomol', 'Mytnaya', 'Arbat', 'Poluboyarova']
cods = ['903', '925', '495', '756', '457', '982', '874']
with open('help.txt', 'w') as text:
    text.write(
        f'INSERT INTO clients (name,email,tel,address,birth_date,registration_date,login,parol) VALUES ')
    for i in range(1000):
        name = choice(names)
        address = choice(towns)+', '+choice(streets)+' street, ' + \
            str(randint(1, 20))+', '+str(randint(1, 100))
        email = name+str(randint(0, 9999))+'@'+choice(emails)
        tel = '8'+'('+choice(cods)+')'+str(randint(0, 9))+str(randint(0, 9))+str(randint(0, 9)) + \
            '-'+str(randint(0, 9))+str(randint(0, 9))+'-' + \
            str(randint(0, 9))+str(randint(0, 9))
        login = name.lower()[:3]
        parol = ''.join([choice('0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
                         for i in range(randint(4, 16))])
        birth_date = str(randint(1965, 2006))+'-' + \
            f'{randint(1,12):0>2}'+'-'+f'{randint(1,31):0>2}'
        registration_date = str(2021)+'-' + \
            f'{randint(1,12):0>2}'+'-'+f'{randint(1,31):0>2}'

        text.write(
            f'("{name}","{email}","{tel}","{address}","{birth_date}","{registration_date}","{login}","{parol}"), \n')
'''
'''
types = [False]*1011
with open('help.txt', 'w') as text:
    text.write(
        f'INSERT INTO orders (type,dilivery_date,client_id,address) VALUES ')
    for i in range(1000):
        client_id = randint(1, 1011)
        typ = 1 if types[client_id-1] else randint(0, 1)
        if typ == 0:
            types[client_id-1] = True

        birth_date = str(randint(1965, 2006))+'-' + \
            f'{randint(1,12):0>2}'+'-'+f'{randint(1,31):0>2}'
        dilivery_date = str(2021)+'-' + \
            f'{randint(11,12):0>2}'+'-'+f'{randint(1,31):0>2}'

        text.write(
            f'({typ},date("{dilivery_date}"),{client_id},(SELECT address FROM clients WHERE id = {client_id})), \n')
'''

with open('help.txt', 'w') as text:
    text.write(
        f'INSERT INTO orders (type,dilivery_date,client_id,address) VALUES ')
    for i in range(1000):
        client_id = randint(1, 1011)
        typ = 1 if types[client_id-1] else randint(0, 1)
        if typ == 0:
            types[client_id-1] = True

        birth_date = str(randint(1965, 2006))+'-' + \
            f'{randint(1,12):0>2}'+'-'+f'{randint(1,31):0>2}'
        dilivery_date = str(2021)+'-' + \
            f'{randint(11,12):0>2}'+'-'+f'{randint(1,31):0>2}'

        text.write(
            f'({typ},date("{dilivery_date}"),{client_id},(SELECT address FROM clients WHERE id = {client_id})), \n')