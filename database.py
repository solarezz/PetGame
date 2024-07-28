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

def info_username(username: str):
    cursor.execute('SELECT * FROM users WHERE username == ?', (username, ))
    result = cursor.fetchone()
    return result
    
def request_partner_id(request_partner_id: int, user_id: int,):
    cursor.execute('UPDATE users SET request_partner_id = ? WHERE user_id = ?', (request_partner_id, user_id))
    connection.commit()
        
def partner_update(user_id: int, partner_name: str, partner_id: int):
    cursor.execute('UPDATE users SET partner_id = ? WHERE user_id = ?', (partner_id, user_id))
    cursor.execute('UPDATE users SET partner = ? WHERE user_id = ?', (partner_name, user_id))
    connection.commit()
    
#------------------#PETS DATABASE#------------------#------------------
def info_pet(owner: str):
    cursor.execute('SELECT * FROM pets WHERE owner1 == ?', (owner,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute('SELECT * FROM pets WHERE owner2 == ?', (owner,))
        result = cursor.fetchone()
    return result

def delete_pet(owner: str):
    cursor.execute("DELETE FROM pets WHERE owner1 = ?", (owner,))
    deleted_rows = cursor.rowcount  # Получаем количество удаленных строк

    # Если ничего не удалено, попробуем удалить записи со вторым владельцем
    if deleted_rows == 0:
        cursor.execute("DELETE FROM pets WHERE owner2 = ?", (owner,))

    # Сохраняем изменения и закрываем соединение
    connection.commit()

def pet_update(owner1: str, owner2: str, pet: str):
    cursor.execute('INSERT INTO pets (owner1, owner2, pet) VALUES (?, ?, ?)', (owner1, owner2, pet))
    connection.commit()
    
def update_petname(owner: str, petname: str):
    cursor.execute('UPDATE pets SET pet_name = ? WHERE owner1 = ?', (petname, owner))
    connection.commit()
    if cursor.rowcount == 0:
        cursor.execute('UPDATE pets SET pet_name = ? WHERE owner2 = ?', (petname, owner))
        connection.commit()

def update_locate(owner: str):
    cursor.execute('UPDATE pets SET locate = ? WHERE owner1 = ?', (owner, owner))
    connection.commit()
    if cursor.rowcount == 0:
        cursor.execute('UPDATE pets SET locate = ? WHERE owner2 = ?', (owner, owner))
        connection.commit()

def update_timelocate(owner: str, locate_time: int):
    cursor.execute('UPDATE pets SET locate_time = ? WHERE owner1 = ?', (locate_time, owner))
    connection.commit()
    if cursor.rowcount == 0:
        cursor.execute('UPDATE pets SET locate_time = ? WHERE owner2 = ?', (locate_time, owner))
        connection.commit()