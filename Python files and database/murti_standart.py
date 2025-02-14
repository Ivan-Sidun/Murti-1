import pandas as pd
import numpy as np
import tkinter as tk
import joblib
from tkinter import filedialog, messagebox
from sklearn.preprocessing import MinMaxScaler
import keras



class App :
    def __init__(self, frame):
        self.data = None
        self.way = None

        button1 = tk.Button(frame, text="Обрати базу даних", command=lambda: self.take_base(), bg="white", fg="black")
        button1.grid(row=0, column=0, padx=20)

        button2 = tk.Button(frame, text="Навчити модель", command=lambda: self.train_model(), bg="white", fg="black")
        button2.grid(row=1, column=0, padx=20)

        button4 = tk.Button(frame, text="Збити базу даних", command=lambda: self.Data_zero(), bg="white", fg="black")
        button4.grid(row=2, column=0, padx=20)
    
        button3 = tk.Button(frame, text="Закрити програму", command=lambda: self.Stop(), bg="white", fg="black")
        button3.grid(row=3, column=0, padx=20)
    
    def take_base(self):
        base_way = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Оберіть базу даних"
        )
        if base_way:
            self.data = pd.read_csv(base_way)
            self.way = base_way
            if "Місяць(1-12)" in self.data.columns:
                self.data['month_sin'] = np.sin(2 * np.pi * self.data['Місяць(1-12)'] / 12)
                self.data['month_cos'] = np.cos(2 * np.pi * self.data['Місяць(1-12)'] / 12)
                self.data = self.data.drop(columns=["Місяць(1-12)"])
        else:
            messagebox.showwarning("Помилка", "Файл не обрано")
            return
    
    def model_body(self, data, event=None):
        #Тренувальні данні\\ для RNN треба форматити додаю комент щоб не забути як це робиться... 
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data)

        def create_sequences(data, sequence_length):
            X, y = [], []
            for i in range(len(data) - sequence_length):
                X.append(data[i:i + sequence_length, :])
                y.append(data[i + sequence_length, :])
            return np.array(X), np.array(y)
        
        sequence_length_RNN = 6
        X, y = create_sequences(data_scaled, sequence_length_RNN)
        split = int(0.8 * len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]

        #Сама модель, досить цікавий метод створення rnn - я роблю rnn вперше
        model = keras.models.Sequential([
            keras.layers.LSTM(128, activation="relu", return_sequences=True, input_shape=(sequence_length_RNN, X.shape[2])),
            keras.layers.Dropout(0.2),
            keras.layers.LSTM(64, activation="relu"),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(X.shape[2])
        ])
        model.compile(optimizer="adam", loss="mse")
        #Here i stopped today
        history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=1000, batch_size=32)
        model.save("trained_model_month.h5")
        joblib.dump(scaler, "scaler_RNN.pkl")
        
    def train_model(self):
        if self.data is not None:
            try :
                self.model_body(self.data)
                messagebox.showinfo('Message', f'модель навченно на {self.way}')
            except Exception as e:
                messagebox.showerror('Error',f"Помилка {e}")
        else:
            defolt_filename = 'Data/def_data_base.csv'
            self.data = pd.read_csv(defolt_filename)
            if "Місяць(1-12)" in self.data.columns:
                self.data['month_sin'] = np.sin(2 * np.pi * self.data['Місяць(1-12)'] / 12)
                self.data['month_cos'] = np.cos(2 * np.pi * self.data['Місяць(1-12)'] / 12)
                self.data = self.data.drop(columns=["Місяць(1-12)"])
            data = pd.read_csv(defolt_filename)
            self.model_body(data)
            messagebox.showinfo('Message', f'модель навченно на {defolt_filename}')

    def Data_zero(self, event=None):
        try:
            self.data = None
            messagebox.showinfo('sucess', 'data=None:)')
        except Exception as e:
            messagebox.showerror('error', f'That was an error:{e}')
    
    def Stop(event=None):
        root.destroy()
    

root = tk.Tk()
root.geometry("500x500")
root.title("Murti_standart")
root.configure(bg="lightblue")

frame = tk.Frame(root, bg="lightblue")
frame.pack(pady=50)

app = App(frame)

root.mainloop()