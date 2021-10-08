# Импортировали необходимые библиотеки
import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy as numpy
import math
import colorama as color

# Задали функцию выбора требуемого звена
def choice():
    inertialessUnitName = 'Безынерциальное звено'
    aperiodicUnitName = 'Апериодическое звено'
    integratingUnitName = 'Интегрирующее звено'
    idealDiffereniatingUnitName = 'Идеально дифференцирующее звено'
    reallyDifferentiatingUnitName = 'Реально дифференцирующее звено'

    needNewChoice = True
    # Цикл для проверки правильности ввода
    while needNewChoice:
        print(color.Style.RESET_ALL)
        # Выбор пользователем требуемого звена
        userInput = input('Введите номер команды: \n'
                          '1 - ' + inertialessUnitName + ';\n'
                          '2 - ' + aperiodicUnitName + ';\n'
                          '3 - ' + integratingUnitName + ';\n'
                          '4 - ' + idealDiffereniatingUnitName + ';\n'
                          '5 - ' + reallyDifferentiatingUnitName + '.\n')
        # Условие для присвоения значения переменной "name"в соответствии с вводом
        if userInput.isdigit():
            needNewChoice = False
            userInput = int(userInput)
            if userInput == 1:
                name = 'Безынерциальное звено'
            elif userInput == 2:
                name = 'Апериодическое звено'
            elif userInput == 3:
                name = 'Интегрирующее звено'
            elif userInput == 4:
                name = 'Идеально дифференцирующее звено'
            elif userInput == 5:
                name = 'Реально дифференцирующее звено'
            else:
                # Сигнализация об ошибке ввода, при введении числа большего, чем 5
                print(color.Fore.RED + '\nНедопустимое значение!\n')
                needNewChoice = True
        # Сигнализация о некорректном вводе (введено не числовое значение)
        else:
            print( color.Fore.RED + '\nПожалуйста, введите числовое значение!\n')
            needNewChoice = True
    return name

# Функция для определения передаточной функции в соответсвии с значением переменной "name"
def getUnit(name):
    needNewChoice = True
    # Цикл для проверки ввода коэффициентов передаточной функции
    while needNewChoice:
        print(color.Style.RESET_ALL)
        needNewChoice = False
        k = input('Пожалуйста, введите коэффициент "k": ')
        T = input('Пожалуйста, введите коэффициент "T": ')
        # Конструкция try-except для проверки правильности ввода коэффициентов
        try:
            k = float(k)
            T = float(T)
            # Условие для присвоения переменной "unit" передаточной функции
            if name == 'Безынерциальное звено':
                unit = matlab.tf([k], [1])
            elif name == 'Апериодическое звено':
                unit = matlab.tf([k], [T, 1])
            elif name == 'Интегрирующее звено':
                unit = matlab.tf([k], [1, 0])
            elif name == 'Идеально дифференцирующее звено':
                unit = matlab.tf([k, 0], [1/1000000000, 1])
            elif name == 'Реально дифференцирующее звено':
                unit = matlab.tf([k, 0], [T, 1])
        except ValueError:
            print(color.Fore.RED + '\nПожалуйста, введите числовое значение!\n')
            needNewChoice = True
    return unit

# Функция для построения графиков переходной и импульсной характеристики
def graph(num, title, y, x):
    pyplot.subplot(2, 1, num)
    pyplot.grid(True)
    if title == 'Переходная харакетристика':
        pyplot.plot(x, y, 'purple')
    elif title == 'Импульсная харакетристика':
        pyplot.plot(x, y, 'green')
    pyplot.ylabel('Амплитуда')
    pyplot.xlabel('Время (с)')
    pyplot.title(title)


unitName = choice()
unit = getUnit(unitName)

timeLine = []
for i in range(0,10000):
    timeLine.append(i/1000)

# Графики переходной и импульсной характеристик
[y, x] = matlab.step(unit, timeLine)
graph(1, 'Переходная харакетристика', y, x)
[y, x] = matlab.impulse(unit, timeLine)
graph(2, 'Импульсная харакетристика', y, x)
pyplot.show()

# Код для построения АЧХ и ФЧХ
matlab.bode(unit, dB=False)
pyplot.plot()
pyplot.xlabel('Частота (Гц)')
pyplot.show()