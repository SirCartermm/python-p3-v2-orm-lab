import sqlite3

class Department:
    all_departments = {}

    def __init__(self, name):
        self.id = None
        self.name = name

    def __repr__(self):
        return f"Department({self.name})"

    @classmethod
    def create_table(cls):
        sqlite3.Cursor.execute('''CREATE TABLE IF NOT EXISTS departments
                          (id INTEGER PRIMARY KEY, name TEXT)''')
        sqlite3.connect.commit()

    @classmethod
    def drop_table(cls):
        sqlite3.Cursor.execute("DROP TABLE IF EXISTS departments")
        sqlite3.connect.commit()

    def save(self):
        if self.id:
            sqlite3.Cursor.execute("UPDATE departments SET name=? WHERE id=?", (self.name, self.id))
        else:
            sqlite3.Cursor.execute("INSERT INTO departments (name) VALUES (?)", (self.name,))
            self.id = sqlite3.Cursor.lastrowid
            Department.all_departments[self.id] = self
        sqlite3.connect.commit()

    @classmethod
    def create(cls, name):
        department = Department(name)
        department.save()
        return department

    @classmethod
    def instance_from_db(cls, row):
        department_id = row[0]
        if department_id in Department.all_departments:
            return Department.all_departments[department_id]
        department = Department(row[1])
        Department.all_departments[department_id] = department
        return department

    @classmethod
    def find_by_id(cls, id):
        sqlite3.Cursor.execute("SELECT * FROM departments WHERE id=?", (id,))
        row = sqlite3.Cursor.fetchone()
        if row:
            return cls.instance_from_db(row)
        return None

    def update(self):
        sqlite3.Cursor.execute("UPDATE departments SET name=? WHERE id=?", (self.name, self.id))
        sqlite3.connect.commit()

    def delete(self):
        sqlite3.Cursor.execute("DELETE FROM departments WHERE id=?", (self.id,))
        sqlite3.connect.commit()
        del Department.all_departments[self.id]
        self.id = None