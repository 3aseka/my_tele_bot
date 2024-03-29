from config import Config
import sqlite3

class DataBase:

    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()

    async def add_users(self, user_id, name):
        with self.connect:
            return self.cursor.execute("""INSERT INTO users (user_id, name, role) VALUES (?, ?, ?)""",
                                       [user_id, name, 'admin' if user_id == Config.admin_ids else 'user'])

    # async def update_label(self, label, user_id):
    #     with self.connect:
    #         return self.cursor.execute("""UPDATE users SET label=(?) WHERE user_id=(?)""",
    #                                    [label, user_id])
    #
    # async def get_payment_status(self, user_id):
    #     with self.connect:
    #         return self.cursor.execute("""SELECT bought, label FROM users WHERE user_id=(?)""",
    #                                    [user_id]).fetchall()
    #
    # async def update_payment_status(self, user_id):
    #     with self.connect:
    #         return self.cursor.execute("""UPDATE users SET bought=(?) WHERE user_id=(?)""",
    #                                    [True, user_id])

    async def get_menu(self, category_id):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM menu WHERE category_id=(?)""", [category_id]).fetchall()

    async def get_user_menu(self, product_id):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM menu WHERE product_id=(?)""", [product_id]).fetchall()

    async def get_basket(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM basket WHERE user_id=(?)""", [user_id]).fetchall()

    async def add_to_basket(self, user_id, product_id):
        with self.connect:
            return self.cursor.execute("""INSERT INTO basket (user_id, product_id, count) VALUES (?, ?, ?)""",
                                       [user_id, product_id, 1])

    async def empty_basket(self, user_id):
        with self.connect:
            return self.cursor.execute("""DELETE FROM basket WHERE user_id=(?)""", [user_id])

    async def get_categories(self):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM categories""").fetchall()


    async def get_count_in_basket(self, user_id, product_id):
        with self.connect:
            return self.cursor.execute("""SELECT count FROM basket WHERE user_id=(?) AND product_id=(?)""",
                                       [user_id, product_id]).fetchall()

    async def get_count_in_menu(self, product_id):
        with self.connect:
            return self.cursor.execute("""SELECT count FROM menu WHERE product_id=(?)""",
                                       [product_id]).fetchall()

    async def remove_one_item(self, product_id, user_id):
        with self.connect:
            return self.cursor.execute("""DELETE FROM basket WHERE product_id=(?) AND user_id=(?)""",
                                       [product_id, user_id])

    async def change_count(self, count, product_id, user_id):
        with self.connect:
            return self.cursor.execute("""UPDATE basket SET count=(?) WHERE product_id=(?) AND user_id=(?)""",
                                       [count, product_id, user_id])
