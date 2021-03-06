# -*- coding: utf-8 -*-

import select
import socket
from random import randint

# Константы, задающие адрес и порт сервера, максимальную длину очереди и ожидаемое кол-во клиентов
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 8008
CLIENTS_QUEUE_LEN = 15
PLAYERS_COUNT = 1

# Переменная, в которой хранятся доходности озера, соответствующие разным уровням загрязнения
lake = [
    [5, -20], [5, -20], [5, -20], [5, -20], [5, -20], [5, -20], [5, -20], [5, -20],
    [19, -8], [19, -8], [19, -8], [19, -8], [19, -8], [19, -8], [19, -8], [19, -8],
    [26, -3], [26, -3], [26, -3], [26, -3], [26, -3], [26, -3], [26, -3], [26, -3],
    [33, 3], [33, 3], [33, 3], [33, 3], [33, 3], [33, 3], [33, 3], [33, 3],
    [41, 7], [41, 7], [41, 7], [41, 7], [41, 7], [41, 7], [41, 7], [41, 7],
    [51, 14], [51, 14], [51, 14], [51, 14], [51, 14], [51, 14], [51, 14], [51, 14],
    [64, 21], [64, 21], [64, 21], [64, 21], [64, 21], [64, 21], [64, 21], [64, 21],
    [80, 28], [80, 28], [80, 28], [80, 28], [80, 28], [80, 28], [80, 28], [80, 28],
    [100, 35], [100, 35], [100, 35], [100, 35], [100, 35], [100, 35], [100, 35], [100, 35],
    [110, 40], [110, 40], [110, 40], [110, 40], [110, 40], [110, 40], [110, 40], [110, 40],
    [121, 63], [121, 63], [121, 63], [121, 63], [121, 63], [121, 63], [121, 63], [121, 63],
    [133, 79], [133, 79], [133, 79], [133, 79], [133, 79], [133, 79], [133, 79], [133, 79],
    [146, 92], [146, 92], [146, 92], [146, 92], [146, 92], [146, 92], [146, 92], [146, 92],
    [161, 111], [161, 111], [161, 111], [161, 111], [161, 111], [161, 111], [161, 111], [161, 111],
    [177, 127], [177, 127], [177, 127], [177, 127], [177, 127], [177, 127], [177, 127], [177, 127]
]

# Помимо этой переменной вам нужно ввести еще несколько:
# 1. Статус игры
status = 0
clients = {}
month = 1
count_klient = 0
pos_lake = 68
strateg = {}
kash = {}
addres = []
game_flag = False

# 4. Переменная сервера



# Функция, отправляющая сообщение всем клиентам на сервере, а также выводящая его в консоль сервера
# 1. Печатаем сообщение на экран
# 2. Обходим все клиентские сокеты и отправляем им сообщение
def broadcast(msg):
    print(msg)
    for conn in clients:
        conn.send(msg.encode())


# Функция, начинающая игру
# 1. Обновить значение переменной, которая хранит информацию о статусе игры
# 2. Разослать уведомления всем игрокам
def start_game():
    global status
    status = 1
    broadcast("Let`s go! Choose your strategy for the first month:")


# Данная функция отвечает за подключение нового клиента. Ее логика следующая:
# 1. При помощи `accept` подключаем нового клиента.
# 2. Если игра уже началась, нужно отправить клиенту сообщение с отказом и отключить его.
# 3. Нужно оповестить других игроков о подключении нового клиента.
# 4. Если набралось необходимое количество игроков, нужно вызвать функцию, начинающую игру.
def connect_new_player():
    global clients, count_klient, conn, inputs, addres
    new_conn, addr = conn.accept()
    print('')
    if status == 1:
        new_conn.send(b"Sorry, the game has been started")
        new_conn.close()
        return
    broadcast("Player {} connected".format(addr))
    count_klient += 1
    clients[new_conn] = addr
    kash[new_conn] = 0
    inputs.append(new_conn)
    addres.append(addr)
    if count_klient == PLAYERS_COUNT:
        start_game()


# Функция, обновляющая балансы игроков
# Пожалуй, самая сложная функция в этой программе. Нужно внимательно изучить правила игры и
# обновить балансы игроков в зависимости от выбранных стратегий и стратегий, выбранных противниками.
def update_balances():
    global kash
    zagr_lake = 0
    count_4 = 0
    count_5 = 0
    print(strateg)
    for i in kash:
        for key, vale in strateg.items():
            if vale == 4:
                count_4 += 1
            if vale == 5:
                count_5 += 1
        print(strateg[i])
        if strateg[i] == '1':
            zagr_lake -= 1
            if count_4 == 0:
                kash[i] += lake[pos_lake][0]
            else:
                kash[i] -= 20
        if strateg[i] == '2':
            kash[i] += lake[pos_lake][1]
            if count_5 != 0:
                kash[i] += 10
        if strateg[i] == '3':
            kash[i] += 8
        if strateg[i] == '4':
            if count_4 == 0:
                kash[i] -= 8
            else:
                kash[i] -= 8 // count_4
        if strateg[i] == '5':
            if count_5 == 0:
                kash[i] -= 8
            else:
                kash[i] -= 8 // count_5
    return zagr_lake


# Функция, обновляющая переменную, указывающую на текущий уровень доходжности озера
# Странно, что для такой простой операции нужна целая функция, да?
# Вот и нет: нам жэе нужно учесть, что это значение не может быть меньше 0 и больше 119
def update_lake(i):
    global pos_lake
    if (pos_lake + i) > -1 and (pos_lake + i) < 120:
        pos_lake += i


# Функция, реализующая паводок
# Вам нужно вспомнить функции из библиотеки `random`
def lake_random_cleaning():
    global pos_lake
    a = randint(1, 12)
    pos_lake += a


# Функция. завершающая игру
# Нужно пройтись по балансам всех клиентов, выбрать максимальный
# и разослать сообщение о том, что игрок одержал победу
def finish_game():
    global game_flag
    maxx = 0
    key_1 = 0
    for key, vaule in kash.items():
        if vaule > maxx:
            maxx = vaule
            key_1 = key
    broadcast("Player {} win".format(clients[key_1][0]))
    game_flag = True

    # Функция, рассылающая всем игрокам актуальную игровую информацию.
    # Информация состоит из:
    # 1. Номер месяца
    # 2. Состояние озера, уровень его прибыльности в следующем месяце
    # 3. Балансы игроков


def send_game_info():
    sp = []
    slov = {}
    for i in kash:
        sp.append(kash[i])
    for i in range(len(addres)):
        slov[addres[i][0]] = sp[i]
    info = f'month number: {month} \n state of the lake: {lake[pos_lake][0], lake[pos_lake][1]} \n player balances: {slov} \n choose a strategy'
    broadcast(info)

    # Функция, реализующая "шаг игры"
    # 1. Пересчитываем балансы игроков.
    # 2. Обновляем переменную, которая хранит состояние озера
    # 3. Проверяем, не закончилась ли игра
    # 4. Проверяем, делится ли шаг на 12. Если так, то запускаем функцию, реализующую паводок.
    # 5. Рассылаем игрокам актуальную информацию по игре.
    # 6. Увеличиваем переменную, хранящую номер месяца.


def game_step():
    global month, strateg
    zagr_lake = update_balances()
    update_lake(zagr_lake)
    strateg = {}
    if month == 40:
        finish_game()
        return
    if month % 12 == 0:
        lake_random_cleaning()
    send_game_info()
    month += 1


# Функция, проверяющая, что все игроки выбрали стратегии в этом месяце
def all_made_decision():
    print(len(strateg.keys()))
    if len(strateg.keys()) == PLAYERS_COUNT:
        return True
    return False


# Функция, откоючающая клиента от игры
# 1. Удаляем клиента из структуры хранения
# 2. Закрываем его сокет
# 3. Информируем об этом других клиентов
def disconnect_client(conn):
    global addres, clients, kash
    broadcast(f'the player {clients[conn]} left the game')
    conn.close()
    kash.pop(conn)
    a = clients.pop(conn)
    b = addres.index(a)
    addres.pop(b)


# Функция, обрабатывающая сообщение, которое прислал нам клиент.
# 1. Принимаем сообщение из сокета. В этой функции используется конструкция try/except,
#    которую мы не проходили. Она выполняет задачу обработки ошибок.
#    Возникновение ошибки означает, что клиента можно отключать и доигрывать без него.
#    Важно: нужно удалить его из игровых структур, чтобы не ждать от него сообщений.
#    Если от клиента пришло пустое сообщение, нужно проверить, что соединение не разорвалось, и, если это так,
#    отключить его.
# 2. Далее следует проставить в структуру, хранящую информацию о клиентах, информацию о сделанном ходе.
#    Затем мы проверяем, все ли клиенты сделали выбор и, в зависимости от этого, делаем "игровой шаг"
def handle_player_msg(conn):
    global strateg
    try:
        msg = conn.recv(1024).decode()
        msg = str(msg)
    except Exception as err:
        print(err)
        disconnect_client(conn)
        return
    if msg is None:
        disconnect_client(conn)
        return
    if msg == "":
        try:
            conn.send("Got it".encode())
        except Exception:
            disconnect_client(conn)
    elif msg not in ['1', '2', '3', '4', '5']:
        return
    else:
        strateg[conn] = msg
    if all_made_decision():
        game_step()


sock = socket.socket()
sock.bind((SERVER_ADDRESS, SERVER_PORT))
sock.listen(5)
inputs = [sock]


# Это основной цикл нашей программы, в нем мы должны ожидать и обрабатывать новые события
# Цикл можно сделать бесконечным, можно ввести переменную-индикатор, отражающую статус игры
while True:
    if game_flag:
        break
    # В данную переменную нужно положить список всех сокетов, на которых могут произойти события
    # Это все сокеты клиентов и сокет сервера
    # Важно: в Windows-системах не удастся передать sys.stdin в select.select(), поэтому мы
    # ограничим количество игроков константой и будем стартовать игру, как только подключится
    # необходимое количество игроков.
    ins, _, _ = select.select(inputs, [], [], 0)
    for conn in ins:
        if conn == sock:
            connect_new_player()
        else:
            handle_player_msg(conn)
