import pandas as pd
import numpy as np
from Dishes import Dishes
from Ingredient import Ingredient
from Store import Store
from datetime import datetime

df = pd.read_csv('csv/dishes.csv', encoding='GB18030')
print(df.loc[0])

# 满足用户搜索条件的游戏
comp_k = ['Meat', 'Vegetarian', 'Staple', 'Tool']

component = {k: [] for k in comp_k}
componentVar = {k: [] for k in comp_k}

Dishes_list = []
for idx, _ in df.iterrows():
    for k in comp_k:
        if not pd.isna(_[k]) and _[k] not in component[k]:
            print(_[k])
            component[k].append(_[k])
    Dishes_list.append(Dishes(**_.to_dict()))


df = pd.read_csv('csv/ingredients.csv', encoding='GB18030')
print(df.loc[0])

Ingredient_list = []
for idx, _ in df.iterrows():
    Ingredient_list.append(Ingredient(**_.to_dict()))


df = pd.read_csv('csv/store.csv', encoding='GB18030')
print(df.loc[0])

Store_list = []
for idx, _ in df.iterrows():
    year, month, date = _['ProductionDate'].split('/')
    dtime = datetime(int(year), int(month), int(date))
    timestamp = dtime.timestamp()
    Store_list.append(
        Store(
            Ingredient = _['Ingredient'],
            ProductionDate = int(timestamp)
        )
    )
