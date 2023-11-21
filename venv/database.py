from pydantic import BaseModel
import sqlite3
from fastapi import FastAPI

app = FastAPI()

def connect_to_database():
    return sqlite3.connect('Samurais.db')

def create_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Samurais(
        id INTEGER PRIMARY KEY,
        first_name TEXT NULL,
        katana TEXT NULL,
        age INTEGER NULL,
        clan TEXT NULL )
    ''')

    connection.commit()
    connection.close()


def insert_samurai(first_name, katana, age, clan):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Samurais (first_name, katana, age, clan) VALUES(?,?,?,?)',
                   (first_name, katana, age, clan))
    connection.commit()
    connection.close()


def select_all_samurais():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Samurais')
    samurais = cursor.fetchall()
    for samurai in samurais:
        print(samurai)

    connection.close()


def select_samurai_by_katana_or_clan(name):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Samurais WHERE katana LIKE ? OR clan LIKE ?', (name, name))
    samurais = cursor.fetchall()
    for samurai in samurais:
        print(samurai)

    connection.close()


def delete_samurai_by_katana_or_clan(name):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('DELETE FROM Samurais WHERE katana = ? OR clan = ?', (name, name))

    connection.commit()
    connection.close()


def update_clan_by_name(name, new_clan):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('UPDATE Samurais SET clan = ? WHERE first_name = ? OR katana = ?', (new_clan, name, name))

    connection.commit()
    connection.close()


def main():
    create_table()

    while True:
        print("\nВыберите действие:\n"
              "1. Добавить нового самурая\n"
              "2. Посмотреть всех самураев\n"
              "3. Поиск самурая по катане или клану\n"
              "4. Обновить клан самурая\n"
              "5. Удалить самурая\n"
              "0. Выйти")

        choice = input()

        if choice == "1":
            first_name = input("Введите имя: ")
            katana = input("Введите название катаны: ")
            age = input("Введите возраст: ")
            clan = input("Введите клан: ")
            insert_samurai(first_name, katana, age, clan)

        elif choice == "2":
            select_all_samurais()

        elif choice == "3":
            name = input("Введите название катаны или клан самурая: ")
            select_samurai_by_katana_or_clan(name)

        elif choice == "4":
            name = input("Введите название катаны или клан самурая: ")
            new_clan = input("Введите новый клан: ")
            update_clan_by_name(name, new_clan)

        elif choice == "5":
            name = input("Введите название катаны или клан самурая: ")
            delete_samurai_by_katana_or_clan(name)

        else:
            break;


class SamuraiCreate(BaseModel):
    first_name: str
    katana: str
    age: int
    clan: str=None

@app.post('/samurais/', response_model=SamuraiCreate)
async def create_samurai(samurai: SamuraiCreate):
    insert_samurai(samurai.first_name, samurai.katana, samurai.age, samurai.clan)
    return samurai

@app.get('/samurais/')
async def read_samurais():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Samurais')
    samurais = cursor.fetchall()

    return {'samurais': samurais}

@app.get('/samurais/{name}')
async def read_samurai(name):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(f'SELECT * FROM Samurais WHERE first_name = "{name}"')
    results = cursor.fetchall()
    connection.close()

    if not results:
        raise HTTPException(status_code=404, detail="Samurai not found")

    return {'samurai': results[0]}

if __name__ == '__main__':
    main()