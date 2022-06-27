import os
import copy
import time
from time import sleep
from pandas import read_csv
from tkinter import Label, Frame, Button, Checkbutton, Tk, IntVar, HORIZONTAL, Scale, filedialog
import tkinter.font as tkFont
from tkinter import ttk, scrolledtext
from ActionData import ActionData
from Dishes import Dishes
from Ingredient import Ingredient
from Store import Store

import pandas as pd
import numpy as np

from Init import *


action_data = ActionData()

today = int(datetime.now().timestamp())


# WHEN CHANGED方法
def switch_property(direction):
    if direction == 'prev':
        message = action_data.goto_prev_property()
    else:
        message = action_data.goto_next_property()
    result_message['text'] = message


# 守护程序
def filter(mode):
    # 从各个组件中得到界面中用户选择的查询条件 
    req = {}
    for k in comp_k:
        req[k] = []
        for _component, _var in zip(component[k], componentVar[k]):
            if _var.get():
                req[k].append(_component)

    action_data.properties = []
    for _dishes in Dishes_list:
        if mode == "fuzzy":
            if (_dishes.Meat in req['Meat']) or \
               (_dishes.Vegetarian in req['Vegetarian']) or \
               (_dishes.Staple in req['Staple']) or \
               (_dishes.Tool in req['Tool']):
                action_data.properties.append(_dishes)
        elif mode == "exact":
            if req['Tool'] == []:
                req['Tool'] = component['Tool']
            if (pd.isna(_dishes.Meat)       or _dishes.Meat in req['Meat']) and \
               (pd.isna(_dishes.Vegetarian) or _dishes.Vegetarian in req['Vegetarian']) and \
               (pd.isna(_dishes.Staple)     or _dishes.Staple in req['Staple']) and \
               (pd.isna(_dishes.Tool)       or _dishes.Tool in req['Tool']):
                action_data.properties.append(_dishes)

    # 终端符合用户要求的选取结果
    print('【RESULT】', len(action_data.properties))
    # 在窗口中显示符合用户要求的首条记录
    # 检测结果条数是否 > 0
    if len(action_data.properties):
        action_data.selection = 0
        result_message['text'] = action_data.change_display()
    else:
        result_message['text'] = '数据库中没有符合要求的食谱'

def fuzzy_filter():
    return filter(mode = 'fuzzy')

def exact_filter():
    return filter(mode = 'exact')

# WHEN CHANGE方法
def find_out_date():
    warning_text = ""
    for _store in Store_list:
        for _ingredient in Ingredient_list:
            if _store.Ingredient == _ingredient.Ingredient:
                if _store.ProductionDate + (_ingredient.BestBefore - 3) * 24 * 60 * 60 <= today:
                    warning_text = warning_text + f"{_store.Ingredient} 三天内即将过期\n"

    warning_message['text'] = warning_text


import os
def add_ingredient():
    file_list = os.listdir("new_ingredient")
    # MOCK
    add_info = ""
    for _file in file_list:
        if _file.split('.')[0] == 'pork':
            ingredient_name = '猪肉'
        elif _file.split('.')[0] == 'rice':
            ingredient_name = '米饭'
        elif _file.split('.')[0] == 'toufu':
            ingredient_name = '豆腐'
        else:
            continue
        _ = Store(
                Ingredient = ingredient_name,
                ProductionDate = today
            )
        Store_list.append(_)
        add_info = add_info + f"新增食材 {ingredient_name}; "
        for _ingredient in Ingredient_list:
            if ingredient_name == _ingredient.Ingredient:
                add_info = add_info + f"存储方式 {_ingredient.Storage}; 保存时间 {_ingredient.BestBefore}天; "
                if not pd.isna(_ingredient.Remark):
                    add_info = add_info + f"备注 {_ingredient.Remark}"
                break
        add_info = add_info + "\n"
    add_message['text'] = add_info
    find_out_date()


if __name__ == '__main__':

    window = Tk()
    window.title("Food-Smart Expert System")
    window.geometry('1024x768')
    window.resizable(width=False, height=False)

    row_idx = 0
    message = Label(window, text='[Food-Smart]', font=('Microsoft YaHei', 18))
    message.grid(row=row_idx, columnspan=5)
    
    row_idx = 1
    result_window = Frame(window, width=1024, height=150)
    result_window.propagate(0)
    result_message = Label(result_window, text='请选择食谱筛选条件')
    result_message.pack()
    result_window.grid(row=row_idx, columnspan=5)

    # 第二行设置按钮，有多条推荐信息时用按钮进行切换
    row_idx = 2
    prev_btn = Button(window, text='上一条', command=lambda:switch_property('prev'))
    next_btn = Button(window, text='下一条', command=lambda:switch_property('next'))
    prev_btn.grid(row=row_idx, column=3, sticky='e', ipadx=20, pady=30)
    next_btn.grid(row=row_idx, column=4, ipadx=20)

    # 食材选择
    row_idx = 3
    for col_idx, _component in enumerate(component.keys()):
        _frame = Frame(window)
        _frame.grid(row=row_idx, column=col_idx, sticky='nw', ipadx=30, ipady=10, pady=10)
        _note_label = Label(_frame, text=_component, font=('tMicrosoft YaHei',12,'bold'))
        _note_label.pack()
        for _idx, _item in enumerate(component[_component]):
            componentVar[_component].append(IntVar(value=0))
            check = Checkbutton(_frame, text=_item, variable=componentVar[_component][_idx], onvalue=1, offvalue=0)
            check.pack(side='top', fill='both', padx=30)

    # 筛选
    row_idx = 4
    submit_btn_1 = Button(window, text='模糊筛选', font=('Microsoft YaHei', 15), command=fuzzy_filter)
    submit_btn_1.grid(row=row_idx, column=1, ipadx=70, ipady=10, pady=10)
    submit_btn_2 = Button(window, text='精确筛选', font=('Microsoft YaHei', 15), command=exact_filter)
    submit_btn_2.grid(row=row_idx, column=2, ipadx=70, ipady=10, pady=10)

    row_idx = 5
    warning_window = Frame(window, width=1024, height=100)
    warning_window.propagate(0)
    warning_message = Label(warning_window, text='')
    warning_message.pack()
    warning_window.grid(row=row_idx, columnspan=5)

    row_idx = 6
    add_window = Frame(window, width=1024, height=100)
    add_window.propagate(0)
    add_message = Label(add_window, text='')
    add_message.pack()
    add_window.grid(row=row_idx, columnspan=5)

    # 新增食材
    row_idx = 7
    submit_btn_0 = Button(window, text='新增食材', font=('Microsoft YaHei', 15), command=add_ingredient)
    submit_btn_0.grid(row=row_idx, column=1, ipadx=70, ipady=10, pady=10)

    find_out_date()
    window.mainloop()
