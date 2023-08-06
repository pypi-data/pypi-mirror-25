import sqlite_queue
import threading
import time

queue = sqlite_queue.SqliteQueue('test.db')
queue.setDaemon(False)
queue.start()

print(queue.select('stocks').where('price', '>=', 30) \
      .order('price').page(1, 5) \
      .get_sql())

# time.sleep(5)


def cb(lst_row, data):
    print(lst_row)
    print(data)


# print(type("CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)"))
# print(isinstance("CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)", str))

def _t():
    time.sleep(3)
    for i in range(12, 15):
        queue.register_execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',?,35.14)", (i,), callback=cb)


# t = threading.Thread(target=_t)
# t.start()

# queue.register_execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)", callback=cb)
# time.sleep(1)
queue.select('stocks').register(callback=cb)
# time.sleep(2)
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00)]
# queue.register_execute('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases, callback=cb)
queue.register_execute("SELECT * FROM stocks", callback=cb)
queue.select('stocks').where('price', '>=', 30) \
    .order('price').page(1, 5) \
    .register(callback=cb)
time.sleep(2)
