import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy as numpy
import math
import colorama as color

def choice():
    inertialessUnitName = 'Безынерциальное звено'
    aperiodicUnitName = 'Апериодическое звено'
    integratingUnitName = 'Интегрирующее звено'
    idealDiffereniatingUnitName = 'Идеально дифференцирующее звено'
    reallyDifferentiatingUnitName = 'Реально дифференцирующее звено'

    needNewChoice = True

    while needNewChoice:
        print(color.Style.RESET_ALL)
        userInput = input('Введите номер команды: \n'
                          '1 - ' + inertialessUnitName + ';\n'
                          '2 - ' + aperiodicUnitName + ';\n'
                          '3 - ' + integratingUnitName + ';\n'
                          '4 - ' + idealDiffereniatingUnitName + ';\n'
                          '5 - ' + reallyDifferentiatingUnitName + '.\n')

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
                print(color.Fore.RED + '\nНедопустимое значение!\n')
                needNewChoice = True
        else:
            print( color.Fore.RED + '\nПожалуйста, введите числовое значение!\n')
            needNewChoice = True
    return name

def getUnit(name):
    needNewChoice = True
    while needNewChoice:
        print(color.Style.RESET_ALL)
        needNewChoice = False
        k = input('Пожалуйста, введите коэффициент "k": ')
        T = input('Пожалуйста, введите коэффициент "T": ')
        if k.isdigit() and T.isdigit():
            k = int(k)
            T = int(T)
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
        else:
            print(color.Fore.RED + '\nПожалуйста, введите числовое значение!\n')
            needNewChoice = True
    return unit

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
    timeLine.append(i/500)

[y, x] = matlab.step(unit, timeLine)
graph(1, 'Переходная харакетристика', y, x)
[y, x] = matlab.impulse(unit, timeLine)
graph(2, 'Импульсная харакетристика', y, x)
pyplot.show()
matlab.bode(unit, dB=False)
pyplot.plot()
pyplot.xlabel('Частота (Гц)')
pyplot.show()