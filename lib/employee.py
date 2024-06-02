# lib/employee.py
import sqlite3

class Employee:
    all_employees = {}

    def __init__(self, first_name, last_name, department_id):
        self.id = None
        self.first_name = first_name
        self.last_name = last_name
        self.department_id = department_id
        self.department = None

    def __repr__(self):
        return f"Employee({self.first_name} {self.last_name})"

    @classmethod
    def create_table(cls):
        sqlite3.Cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                          (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, department_id INTEGER)''')
        sqlite3.connect.commit()

    @classmethod
    def drop_table(cls):
        sqlite3.Cursor.execute("DROP TABLE IF EXISTS employees")
        sqlite3.connect.commit()

    def save(self):
        if self.id:
            sqlite3.Cursor.execute("UPDATE employees SET first_name=?, last_name=?, department_id=? WHERE id=?", 
                           (self.first_name, self.last_name, self.department_id, self.id))
        else:
            sqlite3.Cursor.execute("INSERT INTO employees (first_name, last_name, department_id) VALUES (?, ?, ?)", 
                           (self.first_name, self.last_name, self.department_id))
            self.id = sqlite3.Cursor.lastrowid
            Employee.all_employees[self.id] = self
        sqlite3.connect.commit()

    @classmethod
    def create(cls, first_name, last_name, department):
        employee = Employee(first_name, last_name, department.id)
        employee.department = department
        employee.save()
        return employee

    @classmethod
    def instance_from_db(cls, row):
        employee_id = row[0]
        if employee_id in Employee.all_employees:
            return Employee.all_employees[employee_id]
        employee = Employee(row[1], row[2], row[3])
        Employee.all_employees[employee_id] = employee
        return employee

    @classmethod
    def find_by_id(cls, id):
        sqlite3.Cursor.execute("SELECT * FROM employees WHERE id=?", (id,))
        row = sqlite3.Cursor.fetchone()
        if row:
            return cls.instance_from_db(row)
        return None

    def update(self):
        sqlite3.Cursor.execute("UPDATE employees SET first_name=?, last_name=?, department_id=? WHERE id=?", 
                       (self.first_name, self.last_name, self.department_id, self.id))
        sqlite3.connect.commit()

    def delete(self):
        sqlite3.Cursor.execute("DELETE FROM employees WHERE id=?", (self.id,))
        sqlite3.connect.commit()
        del Employee.all_employees[self.id]
        self.id = None

    @property
    def reviews(self):
        from lib.review import Review
        sqlite3.Cursor.execute("SELECT * FROM reviews WHERE employee_id=?", (self.id,))
        rows = sqlite3.Cursor.fetchall()
        return [Review.instance_from_db(row) for row in rows]