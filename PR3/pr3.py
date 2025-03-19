import pandas as pd
import numpy as np

# Створення тестового DataFrame
np.random.seed(42) # фіксація початкового стану генератора випадкових чисел
data = {
    'date': pd.date_range(start='2025-01-01', periods=365, freq='D'),  # Дати на 1 рік
    'group': np.random.choice(['A', 'B', 'C', 'D'], size=365),  # Випадково присвоєння однієї з груп A, B, C або D кожному дню
    'consumption': np.abs(np.random.randn(365) * 100)  # Випадкові значення споживання енергії
}
df = pd.DataFrame(data)

# Встановлюємо 'date' як індекс
df.set_index('date', inplace=True)

# Агрегація за днями
daily = df.groupby('group').resample('D').sum().drop(columns=['group'])

# Агрегація за місяцями
monthly = df.groupby('group').resample('ME').sum().drop(columns=['group'])

# Агрегація за роками
yearly = df.groupby('group').resample('YE').sum().drop(columns=['group'])

# Вивід результатів
print("=== Денна агрегація ===\n", daily.head(), "\n")
print("=== Місячна агрегація ===\n", monthly.head(), "\n")
print("=== Річна агрегація ===\n", yearly.head(), "\n")
