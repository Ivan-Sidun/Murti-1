import pandas as pd
import numpy as np
import os
import joblib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import keras

class App :
    def __init__(self, frame) :
        self.data = None
        self.data_copy = None
        self.index_create = None
        self.index_model = None

        self.create = ["На 15 чинників", "На 21 чинник"]
        self.model = ["Murti_standart", "Murti_pollution", "Murti_search"]

        self.create_list = ttk.Combobox(frame, values=self.create, state="readonly")
        self.create_list.grid(row=0, column=1, padx=20)

        self.model_list = ttk.Combobox(frame, values=self.model, state="readonly")
        self.model_list.grid(row=2, column=1, padx=20)


        button1 = tk.Button(frame, text="Створити файл для вводу", command=lambda: self.create_excel(), bg="white", fg="black")
        button1.grid(row=0, column=0, padx=20)


        button2 = tk.Button(frame, text="Обрати файл з чинниками", command=lambda: self.take_base(), bg="white", fg="black")
        button2.grid(row=1, column=0, padx=20)

        button3 = tk.Button(frame, text="Запустити модель", command=lambda: self.Predict(), bg="white", fg="black")
        button3.grid(row=2, column=0, padx=20)


        button6 = tk.Button(frame, text="Закрити програму", command=lambda: self.Stop(), bg="white", fg="black")
        button6.grid(row=5, column=0, padx=20)

    def select_create(self, combo, list, event=None):
        selected_text = combo.get()
        self.index_create = list.index(selected_text)

    def select_model(self, combo, list, event=None):
        selected_text = combo.get()
        self.index_model = list.index(selected_text)

    def create_excel(self, event=None):
        self.select_create(self.create_list, self.create)
        if self.index_create is not None:
            match self.index_create:
                case 0:
                    data = {
                        'Місяць(1-12)': [None],
                        'Температура повітря (°C)': [None],
                        'Кількість опадів (мм)': [None],
                        'Швидкість вітру (м/с)': [None],
                        'Відносна вологість (%)': [None],
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

                    df = pd.DataFrame(data)
                    output_file = filedialog.asksaveasfilename(
                    defaultextension=".xslx",
                    filetypes=[("Excel files", "*.xlsx")],
                    title="Зберегти Excel файл"
                    )
                    if df is None:
                        return
                    df.to_excel(output_file, index=False)

                    os.startfile(output_file)
                
                case 1:
                    data = {
                        'Місяць(1-12)': [None],
                        'Середня температура повітря (°C)' : [None],
                        'Відносна вологість повітря (%)' : [None],
                        'Швидкість вітру (м/с)' : [None],
                        'Кількість опадів (мм)' : [None],
                        'Сонячна радіація (МДж/м²)' : [None],
                        'Тривалість сонячного дня (годин)' : [None],
                        'Температура ґрунту (°C)' : [None],
                        'Вологість ґрунту (%)' : [None],
                        'pH ґрунту' : [None],
                        'Вміст органічної речовини в ґрунті (%)' : [None],
                        'Вміст важких металів у ґрунті (мг/кг)' : [None],
                        'Вміст викидів пилу у повітрі (мг/м³)' : [None],
                        'Концентрація діоксиду азоту (NO₂, мг/м³)' : [None],
                        'Концентрація діоксиду сірки (SO₂, мг/м³)' : [None],
                        'Присутність фосфатів у водоймах (мг/л)' : [None],
                        'Біомаса рослинності (кг/м²)' : [None],
                        'Чисельність травоїдних тварин (особини/км²)' : [None],
                        'Чисельність хижаків (особини/км²)' : [None],
                        'Чисельність декомпозиторів (особини/км²)' : [None],
                        'Різноманіття видів рослин (кількість видів)' : [None]
                    }

                    df = pd.DataFrame(data)
                    output_file = filedialog.asksaveasfilename(
                        defaultextension=".xslx",
                        filetypes=[("Excel files", "*.xlsx")],
                        title="Зберегти Excel файл"
                    )
                    if df is None:
                        return

                    df.to_excel(output_file, index=False)
                    os.startfile(output_file)
        else:
            messagebox.showwarning("Помилка", "Тип моделі не обрано")

    def take_base(self, event=None):
        data = filedialog.askopenfilename(
        defaultextension=".xslx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Обрати файл з чинниками"    
        )

        if data is None:
            return
        
        self.data = pd.read_excel(data)
        self.data_copy = self.data.copy()
        if "Місяць(1-12)" in self.data.columns:
            self.data['month_sin'] = np.sin(2 * np.pi * self.data['Місяць(1-12)'] / 12)
            self.data['month_cos'] = np.cos(2 * np.pi * self.data['Місяць(1-12)'] / 12)
            self.data = self.data.drop(columns=["Місяць(1-12)"])

    def Month_model(self, event=None):
        way = filedialog.asksaveasfilename(
            defaultextension=".xslx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Зберегти Excel файл з результатом"
        )

        if way is None:
            return
        
        if self.data is None:
            messagebox.showwarning('Error',"не обрано файйл із чинниками")
            return
        
        sum_of_gaps = self.data.isna().sum().sum()
        if sum_of_gaps != 0:
            messagebox.showerror('Error', 'file has gaps(mne len perekluchat yazyk)')
            return
        
        scaler = joblib.load("scaler_RNN.pkl")
        model = keras.models.load_model("trained_model_month.h5", custom_objects={'mse': keras.losses.MeanSquaredError()})

        scaled_data = scaler.transform(self.data)
        input_sequence = np.expand_dims(scaled_data, axis=0)
        predicted_data = model.predict(input_sequence)
        data_output = scaler.inverse_transform(predicted_data)
        df = pd.DataFrame(data_output, columns=self.data.columns)
        
        if 'month_cos' in self.data.columns:
            if self.data_copy['Місяць(1-12)'].sum() == 12:
                df['Місяць(1-12)'] = 1
            else:
                df['Місяць(1-12)'] = self.data_copy['Місяць(1-12)'] + 1
            df = df.drop(columns='month_sin')
            df = df.drop(columns='month_cos')
            month_column = df.pop('Місяць(1-12)')
            df.insert(0, 'Місяць(1-12)', month_column)

        def round_df(value):
            if isinstance(value, float):
                return round(value, 2)
            return value
        df.apply(lambda col: col.apply(round_df()) if col.dtype == 'float64' else col)
        output = df.to_excel(way, index=False)
        os.startfile(way)

    def Pollution_model(self, event=None):
        way = filedialog.asksaveasfilename(
            defaultextension=".xslx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Зберегти Excel файл з результатом"
        )

        if way is None:
            return
        
        if self.data is None:
            messagebox.showwarning('Error',"не обрано файйл із чинниками")
            return
        
        sum_of_gaps = self.data.isna().sum().sum()
        if sum_of_gaps != 0:
            messagebox.showerror('Error', 'file has gaps(mne len perekluchat yazyk)')
            return
        
        scaler_x = joblib.load('scaler_x_pollution.pkl')
        scaler_y = joblib.load('scaler_y_pollution.pkl')
        model = keras.models.load_model('model_pollution.h5', custom_objects={'mse': keras.losses.MeanSquaredError()})

        scaled_input = scaler_x.transform(self.data)
        predicted_data = model.predict(scaled_input)
        data_output = scaler_y.inverse_transform(predicted_data)
        df = pd.DataFrame(data_output, columns=self.data.columns)
        
        if 'month_cos' in self.data.columns:
            df['Місяць(1-12)'] = self.data_copy['Місяць(1-12)'] + 1
            df = df.drop(columns='month_sin')
            df = df.drop(columns='month_cos')
            month_column = df.pop('Місяць(1-12)')
            df.insert(0, 'Місяць(1-12)', month_column)

        output = df.to_excel(way, index=False)
        os.startfile(way)

    def Search_model(self, event=None):
        way = filedialog.asksaveasfile(
            defaultextension=".xslx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Зберегти Excel файл з результатом"
        )
         
        if way is None:
            return
        
        if self.data is None:
            messagebox.showwarning("не обрано файл із чинниками")
            return
        
        sum_of_gaps = self.data.isna().sum().sum()
        if sum_of_gaps > 1:
            messagebox.showinfo('Try again', 'sorry but this feature is under develompent, try to use file with only one gape :(//:3)')
            return
        else:
            scaler = joblib.load('search_scaler.pkl')
            missing_column = self.data.columns[self.data.isna().sum().idxmax()]
            model = keras.models.load_model(f'model_for_{missing_column}.h5', custom_objects={'mse': keras.losses.MeanSquaredError()})

            data_row = self.data.drop(columns=[missing_column])
            scaled_data = scaler.transform(data_row)

            predict = model.predict(scaled_data)
            predict_unsc = scaler.inverse_transform(predict)
            self.data[missing_column] = predict_unsc
            self.data['Місяць(1-12)'] = self.data_copy['Місяць(1-12)'] + 1
            self.data = self.data.drop(columns='month_sin')
            self.data = self.data.drop(columns='month_cos')
            month_column = self.data.pop('Місяць(1-12)')
            self.data.insert(0, 'Місяць(1-12)', month_column)
            self.data.to_excel(way, index=False)
            os.startfile(way)

    def Predict(self):
        self.select_model(self.model_list, self.model)
        if self.index_model is not None:
            match self.index_model:
                case 0:
                    self.Month_model()
                case 1:
                    self.Pollution_model()
                case 2:
                    self.Search_model()

    def Stop(element=None):
        root.destroy()


root = tk.Tk()
root.geometry("800x500")
root.title("Murti")
root.configure(bg="lightblue")

frame = tk.Frame(root, bg="lightblue")
frame.pack(pady=50)

app = App(frame)

root.mainloop()