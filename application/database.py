import sqlite3 as sql
import os

class Database :

    def __init__(self) -> None:
        self.__db_path = os.path.join(os.path.dirname('bot_maksim'), 'db_bot.db')
        self.connect = sql.connect(self.__db_path)
        self.db_cursor = self.connect.cursor()

    
    def create_new_group(self, tg_id) :
        try:
            self.db_cursor.execute(f'INSERT INTO groups(chat_id) VALUES ({tg_id})')
            self.connect.commit()
        except Exception:
            self.connect.rollback()
        finally: 
            self.connect.close()
            
        
    def read_groups(self):
        try:
            tg_ids = self.db_cursor.execute('SELECT chat_id FROM groups')
            return tg_ids.fetchall()
        
        except Exception as e:
            print(e)
        finally: 
            self.connect.close()

            
        """функция для обработки кика бота из канала и удалении записи о канале(чате)"""
    def delete_group(self, chat_id):
        try: 
            self.db_cursor.execute(f'DELETE FROM groups WHERE chat_id = {chat_id}')
            self.connect.commit()
        except Exception as e:
            print(e)
        finally: 
            self.connect.close()
    
    def get_admins(self): 
        try: 
            admins_ids = self.db_cursor.execute('SELECT tg_id FROM admins')
            return admins_ids.fetchall()
        except Exception as e: 
            print(e)

    def get_current_admin(self, chat_id): 
        try:
            admins_ids = self.db_cursor.execute(f'SELECT tg_id FROM admins WHERE tg_id = {chat_id}')
            return admins_ids.fetchone()
        except Exception as e:
            print(e)


