import pandas as pd
import numpy as np
import tkinter as tk
import joblib
from sklearn.model_selection import train_test_split
from tkinter import filedialog, messagebox
from sklearn.preprocessing import MinMaxScaler
import keras



class App :
    def __init__(self, frame):
        self.data = None

        button1 = tk.Button(frame, text="Обрати базу даних", command=lambda: self.take_base(), bg="white", fg="black")
        button1.grid(row=0, column=0, padx=20)

        button2 = tk.Button(frame, text="Навчити модель", command=lambda: self.train_model(), bg="white", fg="black")
        button2.grid(row=1, column=0, padx=20)

        button3 = tk.Button(frame, text="Закрити програму", command=lambda: self.Stop(), bg="white", fg="black")
        button3.grid(row=2, column=0, padx=20)
    
    def take_base(self):
        base_way = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Оберіть базу даних"
        )
        if base_way:
            self.data = pd.read_csv(base_way)
            if "Місяць(1-12)" in self.data.columns:
                self.data['month_sin'] = np.sin(2 * np.pi * self.data['Місяць(1-12)'] / 12)
                self.data['month_cos'] = np.cos(2 * np.pi * self.data['Місяць(1-12)'] / 12)
                self.data = self.data.drop(columns=["Місяць(1-12)"])
        else:
            messagebox.showwarning("Помилка", "Файл не обрано")
            return
    
    def model_body(self, data, event=None):
        scaler_X = MinMaxScaler()
        scaler_y = MinMaxScaler()
        X = data.iloc[:-1,:]
        y = data.iloc[1:,:]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train_scaled = scaler_X.fit_transform(X_train)
        X_test_scaled = scaler_X.fit_transform(X_test)
        y_train_scaled = scaler_y.fit_transform(y_train)
        y_test_scaled = scaler_y.fit_transform(y_test)

        model = keras.models.Sequential([
            keras.layers.Dense(128, activation='relu', input_dim=X_train_scaled.shape[1]),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(y_train_scaled.shape[1])
        ])

        model.compile(optimizer='adam', loss='mse')

        model.fit(X_train_scaled, y_train_scaled, validation_data=(X_test_scaled, y_test_scaled), epochs=50, batch_size=32)

        model.save('model_pollution.h5')
        joblib.dump(scaler_X, 'scaler_x_pollution.pkl')
        joblib.dump(scaler_y, 'scaler_y_pollution.pkl')

    def train_model(self):
        if self.data is not None:
            try :
                self.model_body(self.data)
                messagebox.showinfo('Hi',f'модель навченно на {self.data}')
            except Exception as e:
                messagebox.showerror('Error',f"Помилка {e}")
        else:
            defolt_filename = 'Data/observations_ingulec.csv'
            data = pd.read_csv(defolt_filename)
            self.model_body(data)
            messagebox.showinfo(f'модель навченно на {defolt_filename}')
    
    def Stop(event=None):
        root.destroy()
    

icon_path = "Icos/ico_csv.ico"

root = tk.Tk()
root.geometry("500x500")
root.title("Murti_pollution")
root.configure(bg="lightblue")
root.iconbitmap(icon_path)

frame = tk.Frame(root, bg="lightblue")
frame.pack(pady=50)

app = App(frame)

root.mainloop()