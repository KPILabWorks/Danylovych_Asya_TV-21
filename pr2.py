from datasets import load_dataset
import pandas as pd
import dask.dataframe as dd
import time

# Завантаження датасету
dataset = load_dataset("AmazonScience/massive", "en-US")

# Конвертація Pandas DataFrame
df_train = pd.DataFrame(dataset['train'])

# Конвертація у Dask DataFrame, розбиття на 4 частини
dask_df_train = dd.from_pandas(df_train, npartitions=4)

# Операція для порівняння: підрахунок унікальних значень у стовпці 'intent'

# Порівняння Pandas
start_time = time.time()
unique_counts_pandas = df_train['intent'].value_counts()
end_time = time.time()
print(f"Pandas: Час виконання — {end_time - start_time:.4f} секунд")

# Порівняння Dask
start_time = time.time()
unique_counts_dask = dask_df_train['intent'].value_counts().compute()
end_time = time.time()
print(f"Dask: Час виконання — {end_time - start_time:.4f} секунд")

# Виведення результатів
print("\nРезультати Pandas:")
print(unique_counts_pandas.head())  # Вивід перших 5 унікальних значень

print("\nРезультати Dask:")
print(unique_counts_dask.head())  