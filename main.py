import sqlite3

# Создание базы данных и таблицы заметок
conn = sqlite3.connect('notes.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS notes
             (id INTEGER PRIMARY KEY, title TEXT, content TEXT)''')
conn.commit()


def add_note():
    """Добавляет новую заметку"""
    title = input("Введите заголовок заметки: ")
    content = input("Введите содержание заметки: ")
    c.execute("SELECT * FROM notes WHERE content=? AND title=?", (content, title))
    if c.fetchone() is not None:
        print("Заметка с таким содержанием уже существует.")
    else:
        c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        print("Заметка успешно добавлена!")


def view_notes():
    """Выводит список всех заметок"""
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    if notes:
        print("Список заметок:")
        for note in notes:
            print(f"{note[0]}. {note[1]} - {note[2]} ")
    else:
        print("Заметок пока нет.")


def search_notes():
    """Ищет заметки по ключевому слову"""
    keyword = input("Введите ключевое слово для поиска: ")
    c.execute("SELECT * FROM notes WHERE title LIKE ? OR content LIKE ?", ('%' + keyword + '%', '%' + keyword + '%'))
    notes = c.fetchall()
    if notes:
        print("Результаты поиска:")
        for note in notes:
            print(f"{note[0]}. {note[1]} - {note[2]}")
    else:
        print("По вашему запросу ничего не найдено.")


def delete_note():
    """Удаляет заметку"""
    note_id = input("Введите содержание заметки, которую нужно удалить: ")
    c.execute("DELETE FROM notes WHERE content=?", (note_id,))
    if c.rowcount == 0:
        print("Заметка с таким содержанием не найдена.")
    else:
        conn.commit()
        print("Заметка успешно удалена!")


while True:
    print("\nМенеджер заметок")
    print("1. Добавить заметку")
    print("2. Просмотреть список заметок")
    print("3. Поиск заметок")
    print("4. Удалить заметку")
    print("5. Выйти из приложения")
    choice = input("Выберите действие: ")

    if choice == '1':
        add_note()
    elif choice == '2':
        view_notes()
    elif choice == '3':
        search_notes()
    elif choice == '4':
        delete_note()
    elif choice == '5':
        break
    else:
        print("Некорректный ввод. Попробуйте ещё раз.")
