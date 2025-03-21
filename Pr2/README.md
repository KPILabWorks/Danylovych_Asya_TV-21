# Практична №2, Варіант 8
 
 ## Завдання
 Використання Dask для роботи з великими DataFrame. Прочитайте великий набір даних у Dask і порівняйте швидкість обробки з Pandas.
 
 ## Опис
 У цьому проекті генерується великий набір даних (розмір 1 ГБ), що складається з 10 мільйонів рядків і 10 колонок. Дані генеруються випадковим чином і зберігаються у CSV файл.
 Потім цей файл зчитується і обробляється за допомогою двох бібліотек:
 - **Pandas**: популярна бібліотека для роботи з даними в Python.
 - **Dask**: бібліотека для обробки великих даних, що дозволяє здійснювати паралельне виконання задач, що дає можливість працювати з даними, що не вміщуються в пам'ять.
 
 ## Результати
 - Генерація великого набору даних...
 - Файл `large_dataset.csv` збережено.
 - Час обробки Pandas: 12.90 сек
 - Час обробки Dask: 4.40 сек
 - Dask швидший у 2.93 разів
 
 ## Висновки
 Dask значно швидший за Pandas при обробці великих наборів даних завдяки своїй здатності до паралельної обробки, що дозволяє зменшити час обробки в порівнянні з традиційним однопотоковим виконанням в Pandas.
