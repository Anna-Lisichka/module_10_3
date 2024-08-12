from threading import Thread, Lock
from random import randint
from time import sleep


class Bank(Thread):
    lock1 = Lock()
    lock2 = Lock()
    balance = 0

    def __init__(self):
        super().__init__()

    def deposit(self):
        for i in range(100):
            if self.balance < 500:
                self.lock1.acquire()
                num = randint(5, 500)
                self.balance += num
                print(f'Пополнение: {num}. Баланс: {self.balance}')
                self.lock1.release()
            elif self.balance >= 500 and self.lock1.locked():
                self.lock1.release()
            sleep(0.1)

    def take(self):
        for i in range(100):
            num = randint(5, 500)
            print(f'Запрос на {num}')
            if num <= self.balance:
                self.lock2.acquire()
                self.balance -= num
                print(f'Снятие: {num}. Баланс: {self.balance}')
                self.lock2.release()
                # sleep(0.1)
            else:
                print(f'Запрос отклонён, недостаточно средств')
                self.lock2.locked()
            sleep(0.1)

bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = Thread(target=Bank.deposit, args=(bk,))
th2 = Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
