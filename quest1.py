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
plt.show()

# 5
dataset['item_price'] = dataset['item_price'].apply(lambda x: float(x[1:-1]))
print('5. Измените тип переменной item_price c с помощью лямбды функции: \n', dataset.dtypes)

# 6
dataset.groupby('item_name')['item_price'].sum().plot(kind='bar')
plt.xlabel('item_name')
plt.ylabel('Money')
plt.title('Кол-во денег заработанных по каждой позиции')
print('6. Построить гистограмму кол-во денег заработанных по каждой позиции')
plt.show()

# 7
print('7. Средняя сумма заказа?')
print('\t 1 способ: ', dataset['item_price'].sum() / len(dataset.groupby('order_id')))
total_order_sum = dataset['item_price'].sum()
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
total = dataset[dataset['item_name'].str.contains('Steak')].groupby(['item_name'])['quantity', 'item_price'].describe()
print(total)

total = dataset['choice_description'].str.split(expand=True).stack().reset_index(level=1, drop=True).to_frame('roasting').merge(dataset, left_index=True, right_index=True)
total = total[total['roasting'].str.contains('Mild|Medium|Hot')]
total['roasting'] = total.roasting.str.strip(',[]()')
total = total.groupby(['roasting']).agg({"quantity": "sum", "order_id": "count"}).reset_index()
total = total.rename(columns={"order_id": "times_ordered"})
print(total)


# 10
print('10. Добавить новый столбец цен на каждую позицию в заказе в рублях.')
dataset['price_rubles'] = dataset['item_price'].apply(lambda value: str(round(value * 71, 2)) + ' RUB')
print(dataset.head(5))

# 11
print('11. Сгруппировать заказы по входящим позициям в него. Отдельно сгруппировать по стейкам во всех видах прожарках.')
group_order = dataset.groupby('order_id').agg({'item_name': lambda x: ", ".join(x), 'item_price': np.sum, 'quantity': np.sum})
group_order[['quantity', 'item_name']]

dataset[dataset['item_name'].str.contains('Steak')].groupby('order_id').agg({'quantity':np.sum,
                                'item_name': lambda x: ", ".join(x), 
                                'item_price':np.sum})


# 12
print('12. Определить цену по каждой позиции в отдельности.')
contains_and = dataset.item_name.str.contains('and')
dataset.loc[contains_and, ('price_for_one_item')] = round((dataset['item_price'] - 2.15) / dataset['quantity'], 2)
if not np.all(contains_and == False):
    dataset.loc[~contains_and, ('price_for_one_item')] = round(dataset['item_price'] / dataset['quantity'], 2)
dataset.loc[contains_and, ('item_name')] = dataset[contains_and]['item_name'].apply(lambda row: row[10:])

pr_for_1_item = dataset.groupby('item_name').price_for_one_item.agg('unique').reset_index()
pr_for_1_item["mean_price"] = pr_for_1_item["price_for_one_item"].apply(lambda row: round(np.mean(list(row)), 2))
pr_for_1_item[~pr_for_1_item.item_name.str.contains('and')]


