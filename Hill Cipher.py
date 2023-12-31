#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np  # Mengimpor modul numpy dan memberinya alias "np" untuk operasi matriks
import string  # Mengimpor modul string untuk akses alfabet dan karakter
import random  # Mengimpor modul random untuk menghasilkan karakter acak
from sympy import Matrix  # Mengimpor kelas Matrix dari modul sympy untuk operasi matriks

def input_key_matrix(dimension): # memebuat function untuk  meminta input key matrix dari user dengan parameter dimensi
    key = [] # Inisialisasi list/array kosong untuk matriks kunci
    print("Masukkan nilai-nilai untuk matrix kunci:") # Menampilkan pesan kepada pengguna
    for i in range(dimension): # Membuat for Loop pertama untuk mengisi baris matriks sesuai dimensi
        row = [] # Inisialisasi list kosong untuk setiap baris matriks
        for j in range(dimension): # Membuat for Loop kedua untuk mengisi kolom matriks sesuai dimensi
            while True: #Membuat while loop untuk memastikan input yang valid
                try: # menggunakan exception handling untuk menangani kesalahan
                    value = int(input(f"Masukan nilai untuk baris {i + 1}, kolom {j + 1}: ")) # Meminta user untuk memasukkan nilai matriks berdasarkan baris dan kolom
                    break   # Keluar dari loop jika input berhasil dikonversi menjadi integer
                except ValueError:  # Menangani kesalahan jika input tidak dapat dikonversi ke integer
                    print("Input invalid. Masukkan nilai dalam integer.") # Menampilkan pesan kesalahan jika input tidak valid
            row.append(value) # Menambahkan nilai ke dalam baris saat ini
        key.append(row) # Menambahkan baris ke dalam matriks kunci
    return key  # Mengembalikan nilai matriks kunci yang telah dibuat


def encrypt(plaintext, key): # Mmebuat fucntion untuk mengenkripsi dengan parameter plantext dan key
    dimension = len(key)  # Menentukan dimensi matriks kunci yang diambil dar panjang kunci yang disimpan di variabel dimension
    alphabet = string.ascii_uppercase  # Menyimpan alfabet dalam huruf besar ke variabel alphabet 
    encrypted_message = ""  # Inisialisasi pesan terenkripsi sebagai string kosong
    plaintext = plaintext.upper()  # Mengubah teks plainteks menjadi huruf besar

    
    plaintext = ''.join(char for char in plaintext if char in alphabet) # MengHapus karakter non-abjad dari plaintext dengan method join yang didalamnya ada argumen loop for yang mengiterasu setiap karakter pada plaintext jika karakter ada dalam alphabet maka aakn dipertahankan kemudian akan digabungakn kembali dengan method join.

    # Isi plainteks dengan karakter acak jika diperlukan
    padding_length = (dimension - (len(plaintext) % dimension)) % dimension  # Menghitung panjang padding yang diperlukan dengan rumus dari dimensi dikurangi dengan modulus dari panajang palintex dan dimensi kemudian hasilnya dimodulus lagi dengan dimensi
    plaintext += ''.join(random.choice(alphabet) for _ in range(padding_length))  # menggabungkan/ menambahkan karakter acak sebagai padding ke teks plainteks jika panjang teks plainteks tidak habis dibagi dengan dimensi matriks kunci
    
    for index in range(0, len(plaintext), dimension):  # Loop pertama untuk mengelompokkan plaintext ke dalam blok seukuran dimensi matriks kunci 
        values = [] # Menginisisalisasi list values.

        for j in range(dimension):  # Loop kedua untuk mengisi nilai-nilai blok plaintext ke dalam vektor
            if index + j < len(plaintext): # jika nilai index ditambah j kurang dari panajng plaintext maak:
                values.append([alphabet.index(plaintext[index + j])])  # Mengambil indeks karakter alfabet dari plaintext

        vector = np.matrix(values)  # Membuat matriks vektor dari nilai-nilai blok plaintext
        result = key * vector % 26  # Mengenkripsi blok plaintext dengan matriks kunci

        for j in range(dimension): # Membuat loop untuk 
            encrypted_message += alphabet[result.item(j)]  # Menambahkan karakter terenkripsi ke pesan terenkripsi

    return encrypted_message  # Mengembalikan pesan terenkripsi



def generate_inverse_matrix(key_matrix): # Membaut function  utnuk mendpat invers matrix yang memiliki parameter key_matrix
    key = Matrix(key_matrix) # mengkonversi matriks kunci menjadi objek matriks dengan bantuan modul sympy
    key_inv = key.inv_mod(26) # Menggunakan metod inv_mod() pada objek matriks key untuk menghitung invers dari matriks kunci. 
    return key_inv # mengembalikan nilai matriks invers kunci 

 # Mmebuat fucntion untuk mengdekripsi dengan parameter ecrypted text dan key
def decrypt(encrypted_message, key_matrix):
    dimension = len(key_matrix)  # Menentukan dimensi matriks kunci yang diambil dar panjang kunci yang disimpan di variabel dimension
    alphabet = string.ascii_uppercase   # Menyimpan alfabet dalam huruf besar ke variabel alphabet 
    key_inv = generate_inverse_matrix(key_matrix)  # Menghitung matriks invers kunci menggunakan fungsi generate_inverse_matrix

    if key_inv is None:  # Memeriksa apakah matriks invers kunci dapat dihitung
        return "Matriks kunci dekripsi tidak dapat diinvers."

    key_inv = key_inv.tolist()  # Mengkonversi matriks invers kunci ke dalam bentuk daftar (list)
    decrypted_message = ""  # Inisialisasi pesan yang akan didekripsi sebagai string kosong

    for index, char in enumerate(encrypted_message):  # Loop melalui setiap karakter dalam pesan terenkripsi
        values = [] # Menginisisalisasi list values.
        if index % dimension == 0:  # Jika sudah mencapai batas dimensi matriks kunci, lakukan dekripsi
            for j in range(dimension):  # Loop untuk mengisi nilai-nilai blok terenkripsi ke dalam vektor
                values.append([alphabet.index(encrypted_message[index + j])])  # Mengambil indeks karakter alfabet dari pesan terenkripsi

            vector = np.matrix(values)  # Membuat matriks vektor dari nilai-nilai blok terenkripsi
            result = key_inv * vector % 26  # Mendekripsi blok terenkripsi dengan matriks invers kunci

            for j in range(dimension):  # Loop untuk menggabungkan karakter-karakter terdekripsi ke pesan terdekripsi
                decrypted_message += alphabet[result.item(j)].lower()  # Mengubah huruf besar menjadi huruf kecil

    return decrypted_message  # Mengembalikan pesan yang telah didekripsi


if __name__ == "__main__": # membuat konstruktor yang menjalankan blok kode di dalamnya  jika skrip ini dijalankan sebagai program utama
    dimension = int(input("Masukkan dimensi matriks kunci untuk enkripsi : "))  # Meminta pengguna memasukkan dimensi matriks kunci enkripsi
    key_matrix = input_key_matrix(dimension)  # Meminta pengguna memasukkan nilai-nilai matriks kunci enkripsi

    print("Matriks kunci enkripsi:")  # Mencetak pesan untuk menampilkan matriks kunci enkripsi
    print(np.matrix(key_matrix))  # Mencetak matriks kunci enkripsi sebagai representasi matriks

    plaintext = input("Masukan plaintext: ").upper()  # Meminta pengguna memasukkan teks plainteks
    encrypted_message = encrypt(plaintext, np.matrix(key_matrix))  # Mengenkripsi teks plainteks menggunakan matriks kunci enkripsi
    print("Teks Terenkripsi:", encrypted_message)  # Mencetak pesan terenkripsi

    decrypt_option = input("Apakah mau mendekripsi teks? (Y/N): ").upper()  # Meminta pengguna apakah ingin melakukan dekripsi

    if decrypt_option == "Y":  # Jika pengguna ingin melakukan dekripsi
        key_matrix = input_key_matrix(dimension)  # Meminta pengguna memasukkan nilai-nilai matriks kunci dekripsi
        decrypted_message = decrypt(encrypted_message, key_matrix)  # Mendekripsi pesan terenkripsi menggunakan matriks kunci dekripsi
        print("Teks terdekripsi:", decrypted_message)  # Mencetak pesan yang telah didekripsi

