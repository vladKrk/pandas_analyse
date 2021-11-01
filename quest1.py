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
hist = dataset.groupby('item_name')['quantity'].sum().hist()
hist.set_xlabel('quantity')
hist.set_ylabel('item_name')
plt.show()
