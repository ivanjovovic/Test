import sqlite3

class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            index_number TEXT UNIQUE NOT NULL
        )
        """)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            grade TEXT,
            date TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(course_id) REFERENCES courses(id)
        )
        """)
        self.con.commit()

    def add_student(self, name, index_number):
        self.cur.execute("INSERT INTO students (name, index_number) VALUES (?, ?)", (name, index_number))
        self.con.commit()

    def add_course(self, name):
        self.cur.execute("INSERT INTO courses (name) VALUES (?)", (name,))
        self.con.commit()

    def add_grade(self, student_id, course_id, grade, date):
        self.cur.execute("INSERT INTO grades (student_id, course_id, grade, date) VALUES (?, ?, ?, ?)",
                         (student_id, course_id, grade, date))
        self.con.commit()

    def fetch_students(self):
        self.cur.execute("SELECT * FROM students")
        return self.cur.fetchall()

    def fetch_courses(self):
        self.cur.execute("SELECT * FROM courses")
        return self.cur.fetchall()

    def fetch_grades(self):
        self.cur.execute("""
        SELECT grades.id, students.name, students.index_number, courses.name, grades.grade, grades.date
        FROM grades
        JOIN students ON grades.student_id = students.id
        JOIN courses ON grades.course_id = courses.id
        """)
        return self.cur.fetchall()

    # --- DODATO: Funkcije za brisanje ---
    def delete_student(self, student_id):
        self.cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
        self.con.commit()

    def delete_course(self, course_id):
        self.cur.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        self.con.commit()

    def delete_grade(self, grade_id):
        self.cur.execute("DELETE FROM grades WHERE id = ?", (grade_id,))
        self.con.commit()
    # --- KRAJ ---

    # --- DODATO: Funkcija za izmenu ocene ---
    def update_grade(self, grade_id, new_grade):
        self.cur.execute("UPDATE grades SET grade = ? WHERE id = ?", (new_grade, grade_id))
        self.con.commit()
    # --- KRAJ ---

    # --- DODATO: Funkcije za pretragu ---
    def search_students(self, keyword):
        self.cur.execute("SELECT * FROM students WHERE name LIKE ?", (f"%{keyword}%",))
        return self.cur.fetchall()

    def search_courses(self, keyword):
        self.cur.execute("SELECT * FROM courses WHERE name LIKE ?", (f"%{keyword}%",))
        return self.cur.fetchall()
    # --- KRAJ ---

