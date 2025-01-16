import pandas as pd
import numpy as np
import os
import joblib
import tkinter as tk
from tkinter import filedialog, messagebox
import keras

class App :
    def __init__(self, frame) :
        self.data = None
        self.data_copy = None

        button1 = tk.Button(frame, text="Створити файл для вводу", command=lambda: self.create_excel(), bg="white", fg="black")
        button1.grid(row=0, column=0, padx=20)

        button8 = tk.Button(frame, text="Свторити файл з чинникам, забруднення", command=lambda: self.create_pollution(), bg="white", fg="black")
        button8.grid(row=0, column=2, padx=20)

        button2 = tk.Button(frame, text="Обрати файл з чинниками", command=lambda: self.take_base(), bg="white", fg="black")
        button2.grid(row=1, column=1, padx=20)

        button3 = tk.Button(frame, text="Запустити місячну модель", command=lambda: self.Month_model(), bg="white", fg="black")
        button3.grid(row=2, column=0, padx=20)

        button7 = tk.Button(frame, text="Запустити місячну модель забруднення", command=lambda: self.Pollution_model(), bg="white", fg="black")
        button7.grid(row=2, column=2, padx=20)

        button4 = tk.Button(frame, text="Запустити річну модель", command=lambda: self.Year_model(), bg="white", fg="black")
        button4.grid(row=3, column=0, padx=20)

        button5 = tk.Button(frame, text="Запустити модель пошуку", command=lambda: self.Search_model(), bg="white", fg="black")
        button5.grid(row=4, column=0, padx=20)

        button6 = tk.Button(frame, text="Закрити програму", command=lambda: self.Stop(), bg="white", fg="black")
        button6.grid(row=5, column=0, padx=20)

    def create_excel(event=None):
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
        df.to_excel(output_file, index=False)

        os.startfile(output_file)

    def create_pollution(event=None):
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

        df.to_excel(output_file, index=False)
        os.startfile(output_file)
    
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

    def Year_model(self, event=None):
        messagebox.showinfo('info', 'i`m working for this')
        '''
        way = filedialog.asksaveasfilename(
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
        if sum_of_gaps != 0:
            messagebox.showerror('Error', 'file has gaps(mne len perekluchat yazyk)')
            return
        
        scaler = joblib.load("scaler_RNN.pkl")
        model = keras.models.load_model("trained_model_month.h5", custom_objects={'mse': keras.losses.MeanSquaredError()})
        steps = 12 #Це потрібно для імітації моделювання на рік вперед(шатав я базу даних нову робити буду як євреї)
        predictions = []

        data_scaled = scaler.transform(self.data)
        if "month_cos" in self.data.columns:
            input_sequence = np.expand_dims(data_scaled, axis=0)
            for i in range(steps):
                predicted_data = model.predict(input_sequence)
                predictions.append(predicted_data[0]) 
                new_step = np.expand_dims(predicted_data[0], axis=0)  # Додати вимір
                input_sequence = np.concatenate([input_sequence[:, 1:, :], np.expand_dims(new_step, axis=1)], axis=1)
            predictions_unscaled = scaler.inverse_transform(predictions)
            predictions_df = pd.DataFrame(predictions_unscaled, columns=self.data.columns)
            predictions_df['Місяць(1-12)'] = self.data_copy['Місяць(1-12)'] + 1
            predictions_df = predictions_df.drop(columns='month_sin')
            predictions_df = predictions_df.drop(columns='month_cos')
            month_column = predictions_df.pop('Місяць(1-12)')
            predictions_df.insert(0, 'Місясць(1-12)', month_column)
            predictions_df.to_excel(way, index=False)
        else:
            sequence = 6
            input_data = np.tile(data_scaled, (sequence, 1))
            for i in range(steps):
                predicted = model.predict(np.expand_dims(input_data, axis=0))
                predictions.append(predicted[0])
                predicted_data_3d = np.expand_dims(predicted[0], axis=0)
                input_data = np.vstack([input_data[1:], predicted_data_3d[0]])
            predictions_unscaled = scaler.inverse_transform(predictions)
            predictions_df = pd.DataFrame(predictions_unscaled, columns=self.data.columns)
            predictions_df.to_excel(way, index=False)
            '''

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


    def Stop(element=None):
        root.destroy()

icon_path = "Icos/ico_csv.ico"

root = tk.Tk()
root.geometry("800x500")
root.title("Murti")
root.configure(bg="lightblue")
root.iconbitmap(icon_path)

frame = tk.Frame(root, bg="lightblue")
frame.pack(pady=50)

app = App(frame)

root.mainloop()