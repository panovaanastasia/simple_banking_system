import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('DROP TABLE card')
cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()
class CreditCards:

    def __init__(self):
        self.exit = 0
        self.exit2 = 0
        self.id = 1

    def work(self):
        while self.exit == 0:
            print('1. Create an account')
            print('2. Log into account')
            print('0. Exit')
            choice = input()
            print()
            if choice == '1':
                self.create()
                print()
            if choice == '2':
                self.login()
                print()
            if choice == '0':
                self.exit = 1
        print('Bye!')

    def create(self):
        rand = str(random.randint(0, 999999999))
        number = '400000' + (9 - len(rand)) * '0' + rand
        s = 0
        for i in range(15):
            a = int(number[i])
            if i % 2 == 0:
                a *= 2
            if a > 9:
                a -= 9
            s += a
        s = (10 - s % 10) % 10
        number += str(s)
        new_rand = str(random.randint(0, 9999))
        password = (4 - len(new_rand)) * '0' + new_rand
        print('Your card has been created')
        print('Your card number:')
        print(number)
        print('Your card PIN:')
        print(password)
        cur.execute('INSERT INTO card (id, number, pin) VALUES ('+ str(self.id) + ", '" + number + "', '" + password + "')")
        conn.commit()
        self.id += 1

    def login(self):
        self.exit2 = 0
        print('Enter your card number:')
        number = input()
        print('Enter your PIN:')
        password = input()
        print()
        cur.execute("SELECT balance FROM card WHERE number = '" + number + "' AND pin = '" + password + "'")
        balance = cur.fetchone()
        if balance is None:
            print('Wrong card number or PIN!')
        else:
            print('You have successfully logged in!')
            while self.exit2 == 0:
                cur.execute("SELECT balance FROM card WHERE number = '" + number + "' AND pin = '" + password + "'")
                balance = cur.fetchone()
                print()
                print('1. Balance')
                print('2. Add income')
                print('3. Do transfer')
                print('4. Close account')
                print('5. Log out')
                print('0. Exit')
                choice = input()
                print()
                if choice == '1':
                    print(f"Balance: {balance}")
                elif choice == '2':
                    print('Enter income:')
                    added = int(input())
                    cur.execute('UPDATE card SET balance = balance + ' + str(added) + " WHERE number = '" + number + "'")
                    conn.commit()
                    print('Income was added!')
                elif choice == '3':
                    self.transfer(number, balance[0])
                elif choice == '4':
                    cur.execute("DELETE FROM card WHERE number = '" + number + "'")
                    conn.commit()
                    print('The account has been closed!')
                    self.exit2 = 1
                elif choice == '5':
                    print('You have successfully logged out!')
                    self.exit2 = 1
                elif choice == '0':
                    self.exit = 1
                    self.exit2 = 1
    def transfer(self, n, b):
        print('Transfer')
        print('Enter card number:')
        n2 = input()
        if n2 == n:
            print("You can't transfer money to the same account!")
        else:
            s = 0
            for i in range(15):
                a = int(n2[i])
                if i % 2 == 0:
                    a *= 2
                if a > 9:
                    a -= 9
                s += a
            if (s + int(n2[15])) % 10 != 0:
                print('Probably you made mistake in the card number. Please try again!')
            else:
                cur.execute("SELECT balance FROM card WHERE number = '" + n2 + "'")
                b2 = cur.fetchone()
                if b2 is None:
                    print('Such a card does not exist.')
                else:
                    print('Enter how much money you want to transfer:')
                    money = int(input())
                    if b < money:
                        print('Not enough money!')
                    else:
                        cur.execute('UPDATE card SET balance = balance - ' + str(money) + " WHERE number = '" + n + "'")
                        conn.commit()
                        cur.execute('UPDATE card SET balance = balance + ' + str(money) + " WHERE number = '" + n2 + "'")
                        conn.commit()
                        print('Success!')

my_cards = CreditCards()
my_cards.work()
