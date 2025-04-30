from faker import Faker
import pandas as pd
import uuid

# Ініціалізація Faker
fake = Faker()

# Кількість записів
num_records = 10

# Список для збереження синтетичних записів
synthetic_data = []

# Генерація записів
for i in range(num_records):
    data = {
        'id': str(uuid.uuid4()),
        'name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'country': fake.country(),
        'address': fake.address().replace('\n', ', '),
        'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d')
    }
    synthetic_data.append(data)  # Додаємо до списку

# Створення DataFrame
df = pd.DataFrame(synthetic_data)

# Збереження у CSV-файл
df.to_csv('synthetic_data.csv', index=False)

print(f"Створено {num_records} записів у файлі 'synthetic_data.csv'")
