#!/usr/bin/env python3
import sqlite3

class Debug:
    @classmethod
    def print_departments(cls):
        sqlite3.Cursor.execute("SELECT * FROM departments")
        rows = sqlite3.Cursor.fetchall()
        for row in rows:
            print(f"Department {row[0]}: {row[1]}")

    @classmethod
    def print_employees(cls):
        sqlite3.Cursor.execute("SELECT * FROM employees")
        rows = sqlite3.Cursor.fetchall()
        for row in rows:
            print(f"Employee {row[0]}: {row[1]} {row[2]} (Department {row[3]})")

    @classmethod
    def print_reviews(cls):
        from lib.review import Review
        sqlite3.Cursor.execute("SELECT * FROM reviews")
        rows = sqlite3.Cursor.fetchall()
        for row in rows:
            review = Review.instance_from_db(row)
            print(f"Review {review.id}: {review.comments} (Rating: {review.rating})")

    @classmethod
    def drop_all_tables(cls):
        sqlite3.Cursor.execute("DROP TABLE IF EXISTS departments")
        sqlite3.Cursor.execute("DROP TABLE IF EXISTS employees")
        sqlite3.Cursor.execute("DROP TABLE IF EXISTS reviews")
        sqlite3.connect.commit()
