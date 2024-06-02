import sqlite3

class Review:
    all_reviews = {}

    def __init__(self, year, summary, employee):
        self.id = None
        self.year = year
        self.summary = summary
        self.employee = employee

    def __repr__(self):
        return f"Review({self.year}, {self.summary}, {self.employee})"

    @classmethod
    def create_table(cls):
        sqlite3.Cursor.execute('''CREATE TABLE IF NOT EXISTS reviews
                          (id INTEGER PRIMARY KEY, year INTEGER, summary TEXT, employee_id INTEGER)''')
        sqlite3.connect.commit()

    @classmethod
    def drop_table(cls):
        sqlite3.Cursor.execute("DROP TABLE IF EXISTS reviews")
        sqlite3.connect.commit()

    def save(self):
        if self.id:
            sqlite3.Cursor.execute("UPDATE reviews SET year=?, summary=?, employee_id=? WHERE id=?", 
                           (self.year, self.summary, self.employee.id, self.id))
        else:
            sqlite3.Cursor.execute("INSERT INTO reviews (year, summary, employee_id) VALUES (?, ?, ?)", 
                           (self.year, self.summary, self.employee.id))
            self.id = sqlite3.Cursor.lastrowid
            Review.all_reviews[self.id] = self
        sqlite3.connect.commit()

    @classmethod
    def create(cls, year, summary, employee):
        review = Review(year, summary, employee)
        review.save()
        return review

    @classmethod
    def instance_from_db(cls, row):
        review_id = row[0]
        if review_id in Review.all_reviews:
            return Review.all_reviews[review_id]
        review = Review(row[1], row[2], Employee.get_by_id(row[3]))
        Review.all_reviews[review_id] = review
        return review

    @classmethod
    def find_by_id(cls, id):
        sqlite3.Cursor.execute("SELECT * FROM reviews WHERE id=?", (id,))
        row = sqlite3.Cursor.fetchone()
        if row:
            return cls.instance_from_db(row)
        return None

    def update(self):
        sqlite3.Cursor.execute("UPDATE reviews SET year=?, summary=?, employee_id=? WHERE id=?", 
                       (self.year, self.summary, self.employee.id, self.id))
        sqlite3.connect.commit().commit()

    def delete(self):
        sqlite3.Cursor.execute("DELETE FROM reviews WHERE id=?", (self.id,))
        sqlite3.connect.commit().commit()
        del Review.all_reviews[self.id]
        self.id = None

    @classmethod
    def get_all(cls):
        sqlite3.Cursor.execute("SELECT * FROM reviews")
        rows = sqlite3.Cursor.fetchall()
        return [cls.instance_from_db(row) for row in rows]