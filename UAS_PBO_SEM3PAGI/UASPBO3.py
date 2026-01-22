import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

# ==================================================
# F. CUSTOM EXCEPTION
# ==================================================
class DataTidakValidError(Exception):
    pass


# ==================================================
# F. ABSTRACTION (ABC)
# ==================================================
class Data(ABC):
    @abstractmethod
    def tampilkan(self):
        pass


# ==================================================
# A & B. CLASS MAHASISWA (ENCAPSULATION)
# ==================================================
class Mahasiswa(Data):
    def __init__(self, nim, nama, jurusan):
        self.__nim = nim          # PRIVATE
        self.nama = nama         # PUBLIC
        self._jurusan = jurusan  # PROTECTED

    # Getter
    def get_nim(self):
        return self.__nim

    # Setter
    def set_jurusan(self, jurusan):
        self._jurusan = jurusan

    def tampilkan(self):
        return f"{self.__nim} | {self.nama} | {self._jurusan}"

    # F. SPECIAL METHOD
    def __str__(self):
        return self.tampilkan()


# ==================================================
# D. INHERITANCE & POLYMORPHISM
# ==================================================
class User:
    def __init__(self, nama):
        self.nama = nama

    def akses_menu(self):
        return "Akses umum"


class Admin(User):
    def akses_menu(self):
        return "Admin: tambah & hapus data"


class MahasiswaUser(User):
    def akses_menu(self):
        return "Mahasiswa: lihat data"


# ==================================================
# C & G. MANAGER (AGGREGATION + COLLECTION)
# ==================================================
class MahasiswaManager:
    def __init__(self):
        self.data_mahasiswa = []  # list of objects

    def tambah(self, mahasiswa):
        self.data_mahasiswa.append(mahasiswa)

    def hapus(self, nim):
        self.data_mahasiswa = [
            m for m in self.data_mahasiswa if m.get_nim() != nim
        ]

    def semua_data(self):
        return self.data_mahasiswa


# ==================================================
# H. GUI BERBASIS CLASS (COMPOSITION)
# ==================================================
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Aplikasi Manajemen Mahasiswa")

        # Composition
        self.manager = MahasiswaManager()

        # ===== FORM INPUT =====
        tk.Label(self.root, text="NIM").grid(row=0, column=0)
        tk.Label(self.root, text="Nama").grid(row=1, column=0)
        tk.Label(self.root, text="Jurusan").grid(row=2, column=0)

        self.entry_nim = tk.Entry(self.root)
        self.entry_nama = tk.Entry(self.root)
        self.entry_jurusan = tk.Entry(self.root)

        self.entry_nim.grid(row=0, column=1)
        self.entry_nama.grid(row=1, column=1)
        self.entry_jurusan.grid(row=2, column=1)

        # ===== BUTTON AKSI =====
        tk.Button(self.root, text="Tambah", command=self.tambah_data).grid(row=3, column=0)
        tk.Button(self.root, text="Hapus", command=self.hapus_data).grid(row=3, column=1)

        # ===== AREA OUTPUT =====
        self.text_output = tk.Text(self.root, height=10, width=45)
        self.text_output.grid(row=4, column=0, columnspan=2)

        self.root.mainloop()

    # ==================================================
    # F. EXCEPTION HANDLING (try-except-else-finally)
    # ==================================================
    def tambah_data(self):
        try:
            nim = self.entry_nim.get()
            nama = self.entry_nama.get()
            jurusan = self.entry_jurusan.get()

            if nim == "" or nama == "" or jurusan == "":
                raise DataTidakValidError("Semua field harus diisi")

            mhs = Mahasiswa(nim, nama, jurusan)
            self.manager.tambah(mhs)

        except DataTidakValidError as e:
            messagebox.showerror("Error", str(e))

        else:
            messagebox.showinfo("Sukses", "Data berhasil ditambahkan")
            self.tampilkan_data()

        finally:
            print("Proses tambah selesai")

    def hapus_data(self):
        nim = self.entry_nim.get()
        self.manager.hapus(nim)
        self.tampilkan_data()
        messagebox.showinfo("Info", "Data berhasil dihapus")

    def tampilkan_data(self):
        self.text_output.delete("1.0", tk.END)
        for mhs in self.manager.semua_data():
            self.text_output.insert(tk.END, str(mhs) + "\n")


# ==================================================
# MAIN PROGRAM
# ==================================================
if __name__ == "__main__":
    # Polymorphism test (boleh discreenshot)
    users = [Admin("Admin"), MahasiswaUser("Mahasiswa")]
    for u in users:
        print(u.akses_menu())

    App()
    