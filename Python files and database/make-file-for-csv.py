import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os


icon_path = "Icos/ico_ex.ico"
data = {
    'Місяць(1-12)': [None],
    'Середня температура повітря (°C)': [None],
    'Кількість опадів (мм)': [None],
    'Середня швидкість вітру (м/с)': [None],
    'Відносна вологість повітря (%)': [None],
    'Сонячна радіація (МДж/м²)': [None],
    'Температура ґрунту (°C)': [None],
    'Вологість ґрунту (%)': [None],
    'pH ґрунту': [None],
    'Біомаса рослинності (кг/м²)': [None],
    'Кількість видів рослин': [None],
    'Чисельність травоїдних тварин (особини/км²)': [None],
    'Чисельність хижаків (особини/км²)': [None],
    'Чисельність декомпозиторів (особини/км²)': [None],
    'Смертність тварин (%)': [None],
}


root = tk.Tk()
root.geometry("500x500")
root.title("Створення фалу для моделі")
root.configure(bg="lightblue")
root.iconbitmap(icon_path)


def create(data):
    root.withdraw()
    df = pd.DataFrame(data)
    output_file = filedialog.asksaveasfilename(
    defaultextension=".xslx",
    filetypes=[("Excel files", "*.xlsx")],
    title="Зберегти Excel файл"
    )
    df.to_excel(output_file, index=False)

    os.startfile(output_file)
    root.destroy()
 

button = tk.Button(root, text="Створити", command=lambda: create(data), bg="white", fg="black", width=20, height=2)
button.pack(pady=20)




root.mainloop()
