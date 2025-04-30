import customtkinter as ctk  # Uvozimo customtkinter biblioteku za lepse GUI komponente
from tkinter import ttk, messagebox  # Uvozimo ttk za napredne widgete (combo box, treeview) i messagebox za poruke
from db import Database  # Uvozimo nasu klasu za rad sa bazom podataka
from datetime import datetime  # Uvozimo datetime kako bismo mogli raditi sa vremenom i datumima

class StudentGradeApp(ctk.CTk):  # Definisemo klasu nase aplikacije koja nasledjuje CTk prozor
    def __init__(self):  # Konstruktor klase
        super().__init__()  # Pozivamo konstruktor nadklase

        self.db = Database("StudentRelational.db")  # Pravljenje konekcije ka SQLite bazi podataka

        self.title("Sistem za ocjene")  # Postavljanje naslova prozora
        self.geometry("1400x900")  # Definisanje dimenzija glavnog prozora
        self.configure(fg_color="#2c3e50")  # Postavljanje boje pozadine

        self.name = ctk.StringVar()  # Promenljiva za ime studenta
        self.index_number = ctk.StringVar()  # Promenljiva za indeks studenta
        self.course_name = ctk.StringVar()  # Promenljiva za naziv kursa
        self.grade = ctk.StringVar()  # Promenljiva za ocenu

        self.search_student_var = ctk.StringVar()  # Promenljiva za pretragu studenta
        self.search_course_var = ctk.StringVar()  # Promenljiva za pretragu kursa

        self.selected_grade_id = None  # Cuva ID selektovane ocene za izmenu/brisanje

        self.create_widgets()  # Pravimo sve GUI komponente
        self.refresh_data()  # Ucitavamo podatke iz baze

    def create_widgets(self):  # Funkcija za kreiranje svih elemenata interfejsa
        tabview = ctk.CTkTabview(self)  # Kreiramo tabove (kartice)
        tabview.pack(expand=True, fill="both", padx=20, pady=20)  # Postavljamo ih da zauzmu ceo prostor

        tab_students = tabview.add("Students")  # Dodajemo tab za studente
        tab_courses = tabview.add("Courses")  # Dodajemo tab za kurseve
        tab_grades = tabview.add("Grades")  # Dodajemo tab za ocene

        tab_students.columnconfigure((0, 3), weight=1)  # Prazne kolone za centriranje
        tab_students.columnconfigure((1, 2), weight=0)  # Kolone sa sadrzajem

        ctk.CTkLabel(tab_students, text="Name:").grid(row=0, column=1, sticky="e", padx=10, pady=5)  # Labela za ime
        ctk.CTkEntry(tab_students, textvariable=self.name).grid(row=0, column=2, sticky="w", padx=10, pady=5)  # Polje za unos imena

        ctk.CTkLabel(tab_students, text="Index Number:").grid(row=1, column=1, sticky="e", padx=10, pady=5)  # Labela za indeks
        ctk.CTkEntry(tab_students, textvariable=self.index_number).grid(row=1, column=2, sticky="w", padx=10, pady=5)  # Polje za unos indeksa

        ctk.CTkButton(tab_students, text="Add Student", command=self.add_student).grid(row=2, column=1, columnspan=2, pady=10)  # Dugme za dodavanje studenta

        tab_courses.columnconfigure((0, 3), weight=1)  # Prazne kolone za centriranje
        tab_courses.columnconfigure((1, 2), weight=0)  # Kolone sa sadrzajem

        ctk.CTkLabel(tab_courses, text="Course Name:").grid(row=0, column=1, sticky="e", padx=10, pady=5)  # Labela za kurs
        ctk.CTkEntry(tab_courses, textvariable=self.course_name).grid(row=0, column=2, sticky="w", padx=10, pady=5)  # Polje za unos kursa

        ctk.CTkButton(tab_courses, text="Add Course", command=self.add_course).grid(row=1, column=1, columnspan=2, pady=10)  # Dugme za dodavanje kursa

        tab_grades.columnconfigure((0, 1), weight=1)  # Dve kolone za ocene

        self.combo_students = ttk.Combobox(tab_grades, state="readonly")  # Padajuca lista za izbor studenta
        self.combo_students.grid(row=0, column=0, padx=10, pady=5, sticky="ew")  # Pozicioniranje padajuce liste

        self.combo_courses = ttk.Combobox(tab_grades, state="readonly")  # Padajuca lista za izbor kursa
        self.combo_courses.grid(row=0, column=1, padx=10, pady=5, sticky="ew")  # Pozicioniranje padajuce liste

        ctk.CTkLabel(tab_grades, text="Grade:").grid(row=1, column=0, sticky="e", padx=10, pady=5)  # Labela za ocenu
        ctk.CTkEntry(tab_grades, textvariable=self.grade).grid(row=1, column=1, sticky="ew", padx=10, pady=5)  # Polje za unos ocene

        ctk.CTkButton(tab_grades, text="Add Grade", command=self.add_grade).grid(row=2, column=0, columnspan=2, pady=10)  # Dugme za dodavanje ocene

        ctk.CTkEntry(tab_grades, textvariable=self.search_student_var, placeholder_text="Search Student...").grid(row=3, column=0, padx=10, pady=5, sticky="ew")  # Pretraga studenata
        ctk.CTkEntry(tab_grades, textvariable=self.search_course_var, placeholder_text="Search Course...").grid(row=3, column=1, padx=10, pady=5, sticky="ew")  # Pretraga kurseva

        ctk.CTkButton(tab_grades, text="Filter Grades", command=self.filter_grades).grid(row=4, column=0, columnspan=2, pady=5)  # Dugme za filtriranje

        ctk.CTkButton(tab_grades, text="Update Grade", command=self.update_grade).grid(row=5, column=0, pady=5)  # Dugme za izmenu ocene
        ctk.CTkButton(tab_grades, text="Delete Grade", command=self.delete_grade).grid(row=5, column=1, pady=5)  # Dugme za brisanje ocene

        self.tv = ttk.Treeview(tab_grades, columns=(1, 2, 3, 4, 5, 6), show="headings", height=10)  # Tabela za prikaz ocena
        self.tv.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)  # Pozicioniranje tabele

        tab_grades.rowconfigure(6, weight=1)  # Tabela se rasteze sa prozorom

        self.tv.heading(1, text="ID")  # Kolona ID
        self.tv.heading(2, text="Student Name")  # Kolona za ime
        self.tv.heading(3, text="Index")  # Kolona za indeks
        self.tv.heading(4, text="Course")  # Kolona za kurs
        self.tv.heading(5, text="Grade")  # Kolona za ocenu
        self.tv.heading(6, text="Date")  # Kolona za datum

        self.tv.bind("<Double-1>", self.select_grade)  # Dvoklik za selekciju ocene

    def refresh_data(self):  # Ucitavanje i prikaz svih podataka iz baze
        self.combo_students["values"] = [f"{s[0]} - {s[1]} ({s[2]})" for s in self.db.fetch_students()]  # Studenti u padajucu listu
        self.combo_courses["values"] = [f"{c[0]} - {c[1]}" for c in self.db.fetch_courses()]  # Kursevi u padajucu listu

        for i in self.tv.get_children():  # Brisemo stare redove
            self.tv.delete(i)

        for row in self.db.fetch_grades():  # Dodajemo sve ocene u tabelu
            self.tv.insert("", "end", values=row)

    def add_student(self):  # Dodavanje novog studenta
        if self.name.get() and self.index_number.get():  # Ako su popunjena polja
            try:
                self.db.add_student(self.name.get(), self.index_number.get())  # Dodajemo studenta u bazu
                self.refresh_data()  # Osvezimo prikaz
                messagebox.showinfo("Success", "Student added.")  # Poruka o uspehu
                self.name.set("")  # Brisemo ime iz forme
                self.index_number.set("")  # Brisemo indeks iz forme
            except Exception as e:
                messagebox.showerror("Error", str(e))  # Prikazujemo gresku

    def add_course(self):  # Dodavanje novog kursa
        if self.course_name.get():  # Ako je popunjeno polje
            try:
                self.db.add_course(self.course_name.get())  # Dodajemo kurs u bazu
                self.refresh_data()  # Osvezavamo prikaz
                messagebox.showinfo("Success", "Course added.")  # Poruka o uspehu
                self.course_name.set("")  # Brisemo unos
            except Exception as e:
                messagebox.showerror("Error", str(e))  # Greska

    def add_grade(self):  # Dodavanje nove ocene
        try:
            student_info = self.combo_students.get().split(" - ")[0]  # Uzimamo ID studenta
            course_info = self.combo_courses.get().split(" - ")[0]  # Uzimamo ID kursa
            student_id = int(student_info)  # Pretvaramo u broj
            course_id = int(course_info)  # Pretvaramo u broj
            grade_value = self.grade.get()  # Ocena
            date = datetime.now().strftime("%Y-%m-%d")  # Datum danasnji
            if grade_value:
                self.db.add_grade(student_id, course_id, grade_value, date)  # Ubacujemo ocenu
                self.refresh_data()  # Osvezavamo prikaz
                messagebox.showinfo("Success", "Grade added.")  # Poruka
                self.grade.set("")  # Cistimo formu
        except Exception as e:
            messagebox.showerror("Error", str(e))  # Prikaz greske

    def select_grade(self, event):  # Selektujemo red u tabeli
        selected = self.tv.focus()
        values = self.tv.item(selected, "values")
        if values:
            self.selected_grade_id = int(values[0])  # Cuvamo ID ocene
            self.grade.set(values[4])  # Postavljamo ocenu u formu

            student_name = values[1]  # Ime
            index = values[2]  # Indeks
            course_name = values[3]  # Kurs

            for student in self.combo_students["values"]:
                if f"{student_name} ({index})" in student:
                    self.combo_students.set(student)
                    break

            for course in self.combo_courses["values"]:
                if course_name in course:
                    self.combo_courses.set(course)
                    break

    def update_grade(self):  # Azuriramo ocenu
        if self.selected_grade_id is not None and self.grade.get():
            try:
                new_grade = self.grade.get()  # Nova ocena
                self.db.update_grade(self.selected_grade_id, new_grade)  # Upis u bazu
                self.refresh_data()  # Osvezavamo prikaz
                messagebox.showinfo("Success", "Grade updated.")  # Poruka
                self.grade.set("")  # Cistimo formu
                self.selected_grade_id = None  # Resetujemo ID
            except Exception as e:
                messagebox.showerror("Error", str(e))  # Greska
        else:
            messagebox.showwarning("Select Grade", "Please double-click a grade in the table to update it.")  # Upozorenje

    def delete_grade(self):  # Brisemo ocenu
        selected = self.tv.focus()
        values = self.tv.item(selected, "values")
        if values:
            try:
                self.db.delete_grade(values[0])  # Brisemo iz baze
                self.refresh_data()  # Osvezavamo prikaz
                messagebox.showinfo("Success", "Grade deleted.")  # Poruka
            except Exception as e:
                messagebox.showerror("Error", str(e))  # Greska

    def search_students(self):  # Pretraga studenata
        keyword = self.search_student_var.get()
        students = self.db.search_students(keyword)
        if not students:
            messagebox.showinfo("Not found", "No matching students.")  # Nema rezultata
        self.combo_students["values"] = [f"{s[0]} - {s[1]} ({s[2]})" for s in students]  # Prikaz u listi

    def search_courses(self):  # Pretraga kurseva
        keyword = self.search_course_var.get()
        courses = self.db.search_courses(keyword)
        if not courses:
            messagebox.showinfo("Not found", "No matching courses.")  # Nema rezultata
        self.combo_courses["values"] = [f"{c[0]} - {c[1]}" for c in courses]  # Prikaz u listi

    def filter_grades(self):  # Filtriranje ocena u tabeli
        student_kw = self.search_student_var.get().lower()
        course_kw = self.search_course_var.get().lower()

        for i in self.tv.get_children():
            self.tv.delete(i)

        for row in self.db.fetch_grades():
            student_name = row[1].lower()
            course_name = row[3].lower()
            if (student_kw in student_name) and (course_kw in course_name):
                self.tv.insert("", "end", values=row)

if __name__ == "__main__":  # Pokretanje aplikacije
    ctk.set_appearance_mode("dark")  # Tamni mod
    ctk.set_default_color_theme("blue")  # Tema
    app = StudentGradeApp()  # Kreiramo instancu aplikacije
    app.mainloop()  # Pokrecemo GUI
