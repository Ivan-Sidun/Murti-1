import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import os


icon_path = "Icos/ico_csv.ico"


root = tk.Tk()
root.geometry("500x500")
root.title("CSV операції")
root.configure(bg="lightblue")
root.iconbitmap(icon_path)

frame = tk.Frame(root, bg="lightblue")
frame.pack(pady=50)


def Old_base():
    new_base = filedialog.askopenfilename(
    filetypes=[("Excel files", "*.xlsx")],
    title="Оберіть файл Excel для претворення"
    )
    old_base = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")],
        title="Оберіть стару базу даних"
    )
    output_file = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Збережіть об'єднаний CSV файл"
    )

    if new_base:
        new_csv = pd.read_excel(new_base)
    else:
        messagebox.showwarning("Помилка", "Файл нової бази не обрано не обрано")
        root.destroy()

    if old_base:
        old_csv = pd.read_csv(old_base)
    else:
        messagebox.showwarning("Помилка", "Файл старої бази не обрано")
        root.destroy()
    
    if new_base and old_base:
        try :
            united_base = pd.concat([old_csv, new_csv], ignore_index=True)
            united_base = united_base.loc[:, ~united_base.columns.str.contains("^Unnamed")]
        except Exception as e:
            messagebox.showerror("Помилка", f"Сталася помилка {e}")
            root.destroy()
    else:
        messagebox.showwarning("Помилка", "Одну з баз не обрано")
        root.destroy()
    
    if output_file:
        united_base.to_csv(output_file, index=False)
        messagebox.showinfo("Успіх", f"Об'єднаний файл збережено як {output_file}")
    else:
        messagebox.showwarning("Помилка", "Файл збереження не обрано")

    
def New_base():
    new_base = filedialog.askopenfilename(
    filetypes=[("Excel files", "*.xlsx")],
    title="Оберіть файл Excel для претворення"
    )
    output_file = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Збережіть CSV файл"
    )
    
    if new_base and output_file:
        try:
            new_csv = pd.read_excel(new_base)
            new_csv = new_csv.loc[:, ~new_csv.columns.str.contains("^Unnamed")]
            new_csv.to_csv(output_file, index=False)
            if "Місяць(1-12)" in new_csv.columns:
                new_csv['month_sin'] = np.sin(2 * np.pi * new_csv['Місяць(1-12)'] / 12)
                new_csv['month_cos'] = np.cos(2 * np.pi * new_csv['Місяць(1-12)'] / 12)
                new_csv = new_csv.drop(columns=["Місяць(1-12)"])
            messagebox.showinfo("Успіх", f"Файл успішно конвертовано як {output_file}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Сталася помилка {e}")
            root.destroy()
    else:
        messagebox.showwarning("Помилка", "Один з ключових файлів не обрано")
        root.destroy()

def Stop():
    root.destroy()

button1 = tk.Button(frame, text="Додати до Створеної бази даних", command=lambda: Old_base(), bg="white", fg="black")
button1.grid(row=0, column=0, padx=20)

button2 = tk.Button(frame, text="Створити нову базу даних", command=lambda: New_base(), bg="white", fg="black")
button2.grid(row=1, column=0, padx=20)

button3 = tk.Button(frame, text="Закрити програму", command=lambda: Stop(), bg="white", fg="black")
button3.grid(row=2, column=0, padx=20)



root.mainloop()