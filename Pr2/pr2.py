import pandas as pd
import dask.dataframe as dd
import numpy as np
import time

# Генерація великого датафрейму (1ГБ)
num_rows = 10**7  # 10 мільйонів рядків
num_cols = 10  # 10 колонок

print("Генерація великого набору даних...")
data = {f'col_{i}': np.random.rand(num_rows) for i in range(num_cols)}
df = pd.DataFrame(data)

# Збереження у CSV
csv_filename = "large_dataset.csv"
df.to_csv(csv_filename, index=False)
print(f"Файл {csv_filename} збережено.")

# Час роботи Pandas
start_pandas = time.time()
df_pandas = pd.read_csv(csv_filename)
mean_pandas = df_pandas.mean()
end_pandas = time.time()
pandas_time = end_pandas - start_pandas
print(f"Час обробки Pandas: {pandas_time:.2f} сек")

# Час роботи Dask
start_dask = time.time()
df_dask = dd.read_csv(csv_filename)
mean_dask = df_dask.mean().compute()
end_dask = time.time()
dask_time = end_dask - start_dask
print(f"Час обробки Dask: {dask_time:.2f} сек")

# Висновок
print(f"Dask швидший у {pandas_time / dask_time:.2f} разів")