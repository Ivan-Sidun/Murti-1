import pandas as pd
import numpy as np
import tkinter as tk
import joblib
from tkinter import filedialog, messagebox
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import keras


class App :
    def __init__(self, frame, event=None):
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
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data)

        for target_index in range(data.shape[1]):
            X = np.delete(data_scaled, target_index, axis=1)
            Y = data_scaled[:, target_index]
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

            model = keras.models.Sequential([
                keras.layers.Dense(64, activation='relu', input_dim=X.shape[1]),
                keras.layers.Dropout(0.2),
                keras.layers.Dense(32, activation='relu'),
                keras.layers.Dropout(0.2),
                keras.layers.Dense(1, activation='linear')
            ])

            model.compile(optimizer='adam', loss='mse', metrics=['mae'])

            history = model.fit(X_train, Y_train, epochs=100, batch_size=16, verbose=1, validation_data=(X_test, Y_test))

            model.save(f"model_for_{data.columns[target_index]}.h5")
            
        joblib.dump(scaler, 'search_scaler.pkl')
    
    def train_model(self, event=None):
        if self.data is not None:
            self.model_body(self.data)
        else:
            data = pd.read_csv('Data/def_data_base.csv')
            self.model_body(data)
            messagebox.showinfo('Some', f'model was studied on {data}')

    def Stop(event=None):
        root.destroy()

icon_path = "Icos/ico_csv.ico"

root = tk.Tk()
root.geometry("500x500")
root.title("Навчання моделі")
root.configure(bg="lightblue")
root.iconbitmap(icon_path)

frame = tk.Frame(root, bg="lightblue")
frame.pack(pady=50)

app = App(frame)

root.mainloop()