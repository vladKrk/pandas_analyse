#### 1. Вывести: кол-во наблюдений в датасете
#### 2. Вывести названия столбцов
#### 3. Определить самую частую позицию (item) в заказе 
#### 4. Построить гистрограмму частоты заказов по позициям (item )
#### 5. Измените тип переменной item_price c с помощью лямбды функции
#### 6. Построить гистограмму кол-во денег заработанных по каждой позиции (item)
#### 7. Средняя сумма заказа? (минимум 2 способа)
#### 8. Выведите среднее, минимальное и максимальное, медианное значения позиций в заказе
#### 9. Определить статистику заказов стейков, а также статистику заказов прожарки.
#### 10. Добавить новый столбец цен на каждую позицию в заказе в рублях.
#### 11. Сгруппировать заказы по входящим позициям в него. Отдельно сгруппировать по стейкам во всех видах прожарках.
#### 12. Определить цену по каждой позиции в отдельности. 

import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_table('https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv')

print(dataset)

# 1
print('1. Количество наблюдений в дата сете: ', dataset.shape[0])

# 2
print('2. Названия столбцов: ', dataset.columns.tolist())

# 3
print('3. Самая частая позиция в заказе: ', dataset.groupby('item_name')['quantity'].sum().idxmax())

# 4
hist = dataset.groupby('item_name')['quantity'].sum().plot(kind='bar')
hist.set_ylabel('quantity')
plt.title('Частота заказов по позициям')
print('4. Построить гистрограмму частоты заказов по позициям')
# plt.show()

# 5
dataset['item_price'] = dataset['item_price'].apply(lambda x: float(x[1:-1]))
print('5. Измените тип переменной item_price c с помощью лямбды функции: \n', dataset.dtypes)

# 6
item_price = pd.to_numeric(dataset['item_price'])
quantity = pd.to_numeric(dataset['quantity'])

dataset['sum_price'] = quantity * item_price
dataset.groupby('item_name')['sum_price'].sum().plot(kind='bar')
plt.xlabel('item_name')
plt.ylabel('Money')
plt.title('Кол-во денег заработанных по каждой позиции')
print('6. Построить гистограмму кол-во денег заработанных по каждой позиции')
# plt.show()

# 7
print('7. Средняя сумма заказа?')
print('\t 1 способ: ', dataset['sum_price'].sum() / len(dataset.groupby('order_id')))
total_order_sum = dataset['sum_price'].sum()
num_orders = len(set(dataset['order_id']))
average_order_price = total_order_sum / num_orders
print('\t 2 способ: ', average_order_price)

# 8
print("8. Выведите среднее, минимальное и максимальное, медианное значения позиций в заказе")
print('\t Среднее: ', dataset.quantity.sum() / len(dataset.groupby('order_id')))
print('\t Минимальное: ', dataset.groupby('order_id').quantity.sum().min())
print('\t Максимальное: ', dataset.groupby('order_id').quantity.sum().max())
print('\t Медианное: ', dataset.groupby('order_id').quantity.sum().median())

# 9
print('9. Определить статистику заказов стейков, а также статистику заказов прожарки.')

# 10
print('10. Добавить новый столбец цен на каждую позицию в заказе в рублях.')
dataset['price_rubles'] = dataset['item_price'].apply(lambda value: str(round(value * 71, 2)) + ' RUB')
print(dataset.head(5))

# 11
print('11. Сгруппировать заказы по входящим позициям в него. Отдельно сгруппировать по стейкам во всех видах прожарках.')

# 12
print('12. Определить цену по каждой позиции в отдельности.')
