import sqlite3

connection = sqlite3.connect('C:\Python\PetGame\PetGame\database.db', check_same_thread=False)
cursor = connection.cursor()


#------------------#USERS DATABASE#------------------#------------------

def table_input(user_id: int, username: str):
    cursor.execute('INSERT INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
    connection.commit()
        
def info(user_id: int):
    cursor.execute('SELECT * FROM users WHERE user_id == ?', (user_id,))
    result = cursor.fetchone()
    return result
    
def request_partner_id(request_partner_id: int, user_id: int,):
    cursor.execute('UPDATE users SET request_partner_id = ? WHERE user_id = ?', (request_partner_id, user_id))
    connection.commit()
        
def partner_update(user_id:int, partner_name: str, partner_id: int):
    cursor.execute('UPDATE users SET partner_id = ? WHERE user_id = ?', (partner_id, user_id))
    cursor.execute('UPDATE users SET partner = ? WHERE user_id = ?', (partner_name, user_id))
    connection.commit()
    
#------------------#PETS DATABASE#------------------#------------------
def info_pet(username: str):
    cursor.execute('SELECT * FROM users WHERE username == ?', (username,))
    result = cursor.fetchone()
    return result