import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

# =========================================
# F. Custom Exception
# =========================================
class ValidationError(Exception):
    pass


# =========================================
# E. Abstract Base Class + Special Method
# =========================================
class Person(ABC):
    def __init__(self, name, age):
        self.name = name          # public
        self.__age = age          # private

    def get_age(self):
        return self.__age

    def set_age(self, age):
        if age <= 0:
            raise ValidationError("Umur harus lebih dari 0")
        self.__age = age

    @abstractmethod
    def get_role(self):
        pass

    def __str__(self):
        return f"{self.name} - {self.get_role()}"


# =========================================
# D. Inheritance & Polymorphism
# =========================================
class Student(Person):
    def __init__(self, name, age, nim):
        super().__init__(name, age)
        self._nim = nim           # protected

    def get_role(self):
        return "Mahasiswa S1"


class GraduateStudent(Student):
    def __init__(self, name, age, nim, thesis):
        super().__init__(name, age, nim)
        self.thesis = thesis

    def get_role(self):
        return "Mahasiswa Pascasarjana"


# =========================================
# C & G. Aggregation + Collections of Object
# =========================================
class DataManager:
    def __init__(self):
        self.students = []        # list of objects

    def add_student(self, student):
        self.students.append(student)

    def get_all_students(self):
        return self.students


# =========================================
# H. GUI Tkinter Berbasis Class (Association)
# =========================================
class StudentApp:
    def __init__(self, root):
        self.manager = DataManager()

        self.root = root
        self.root.title("Aplikasi Manajemen Mahasiswa")

        # === Form Input ===
        tk.Label(root, text="Nama").grid(row=0, column=0)
        tk.Label(root, text="Umur").grid(row=1, column=0)
        tk.Label(root, text="NIM").grid(row=2, column=0)

        self.name_entry = tk.Entry(root)
        self.age_entry = tk.Entry(root)
        self.nim_entry = tk.Entry(root)

        self.name_entry.grid(row=0, column=1)
        self.age_entry.grid(row=1, column=1)
        self.nim_entry.grid(row=2, column=1)

        # === Button ===
        tk.Button(root, text="Tambah Mahasiswa", command=self.add_student)\
            .grid(row=3, column=0, columnspan=2)

        # === Area Output ===
        self.output = tk.Text(root, width=45, height=10)
        self.output.grid(row=4, column=0, columnspan=2)

    # =====================================
    # F. Exception Handling (try-except)
    # =====================================
    def add_student(self):
        try:
            name = self.name_entry.get()
            age = int(self.age_entry.get())
            nim = self.nim_entry.get()

            if not name or not nim:
                raise ValidationError("Data tidak boleh kosong")

            student = Student(name, age, nim)
            self.manager.add_student(student)

        except ValidationError as ve:
            messagebox.showerror("Error", str(ve))

        except ValueError:
            messagebox.showerror("Error", "Umur harus berupa angka")

        else:
            self.output.insert(tk.END, str(student) + "\n")

        finally:
            self.name_entry.delete(0, tk.END)
            self.age_entry.delete(0, tk.END)
            self.nim_entry.delete(0, tk.END)


# =========================================
# Main Program
# =========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
    