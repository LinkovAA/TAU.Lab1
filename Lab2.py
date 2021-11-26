# Импортировали необходимые библиотеки
import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy as numpy
import math
import colorama as color
import sympy as sympy
from sympy import *

# Функция для выбора типа обратной связи
def chFeedback():
    print('Выберите тип обратной связи САУ и тип турбины:')
    # Переменные - типы обратной связи
    rigid = 'Жёсткая'
    flexible = 'Гибкая'
    aperiodicRigid = 'Апериодическая жёсткая'
    aperiodicFlexible = 'Апериодическая гибкая'
    newChoiceFeedback = True
    # Цикл для проверки правильности ввода команды и для присвоения переменной "feedbackType" типа обратной связи
    while newChoiceFeedback:
        print(color.Style.RESET_ALL)
        # Выбор типа обратной связи
        typeOfFeedback = input('Тип обратной связи:\n'
                               'Введите номер команды:\n'
                               '1 - ' + rigid + ';\n'
                               '2 - ' + flexible + ';\n'
                               '3 - ' + aperiodicRigid + ';\n'
                               '4 - ' + aperiodicFlexible + '.\n')
        if typeOfFeedback.isdigit():
            newChoiceFeedback = False
            typeOfFeedback = int(typeOfFeedback)
            if typeOfFeedback == 1:
                feedbackType = 'Жёсткая обратная связь'
            elif typeOfFeedback == 2:
                feedbackType = 'Гибкая обратная связь'
            elif typeOfFeedback == 3:
                feedbackType = 'Апериодическая жёсткая обратная связь'
            elif typeOfFeedback == 4:
                feedbackType = 'Апериодическая гибкая обратная связь'
            else:
                print(color.Fore.RED + '\nНедопустимое значение!')
                newChoiceFeedback = True
        else:
            print(color.Fore.RED + '\nПожалуйста, введите числовое значение!')
            newChoiceFeedback = True
    return feedbackType

# Функция для выбора типа турбины
def chTurbine():
    # Переменные - типы турбины
    hydroTurbine = 'Гидротурбина'
    steamTurbine = 'Паровая турбина'
    newChoiceTurbine = True
    # Цикл для проверки правильности ввода команды и для присвоения переменной "turbine" названия типа турбины
    while newChoiceTurbine:
        print(color.Style.RESET_ALL)
        # Выбор типа турбины
        turbineType = input('Тип турбины:\n'
                            'Введите номер команды:\n'
                            '1 - ' + hydroTurbine + ';\n'
                            '2 - ' + steamTurbine + '.\n')
        if turbineType.isdigit():
            newChoiceTurbine = False
            turbineType = int(turbineType)
            if turbineType == 1:
                turbine = 'Гидротурбина'
            elif turbineType == 2:
                turbine = 'Паровая турбина'
            else:
                print(color.Fore.RED + '\nНедопустимое значение!')
                newChoiceTurbine = True
        else:
            print(color.Fore.RED + '\nПожалуйста, введите числовое значение!')
            newChoiceTurbine = True
    return turbine


feedback = chFeedback()
turbine = chTurbine()
print('\nЭлементы исследуемой системы автоматического управления:\n'
      '1. Усилительно-исполнительный орган;\n'
      '2. ' + turbine + ';\n'
      '3. Генератор;\n'
      '4. ' + feedback + '.\n')

# Функция для ввода коэффициентов передаточной функции исполнительного органа
def chioceOrgan():
    oChoice = True
    while oChoice:
        print(color.Style.RESET_ALL)
        oChoice = False
        print('Введите коэффициенты передаточной функции исполнительного органа:')
        k = input('Пожалуйста, введите коэффициент "Ку": ')
        T = input('Пожалуйста, введите коэффициент "Tу": ')
        # Конструкция try-except для проверки правильности ввода коэффициентов
        try:
            k = float(k)
            T = float(T)
            wfOrgan = matlab.tf([k], [T, 1])
        except ValueError:
            print(color.Fore.RED + '\nПожалуйста, введите числовое значение!\n')
            oChoice = True
    return wfOrgan


# Функция для ввода коэффициентов передаточной функции турбины
def chioceTurbine():
    tChoice = True
    while tChoice:
        print(color.Style.RESET_ALL)
        tChoice = False
        print('Введите коэффициенты передаточной функции турбины:')
        if turbine == 'Гидротурбина':
            T1 = input('Пожалуйста, введите постоянную времени гидротурбины "Тгт": ')
            T2 = input('Пожалуйста, введите постоянную времени генератора "Тг": ')
            try:
                T1 = float(T1)
                T2 = float(T2)
                wfTurbine = matlab.tf([0.01*T1, 1], [0.05*T2, 1])
            except ValueError:
                print(color.Fore.RED + '\nПожалуйста, введите числовое значение!\n')
                tChoice = True
        elif turbine == 'Паровая турбина':
            k = input('Пожалуйста, введите коэффициент усиления "Кпт": ')
            T = input('Пожалуйста, введите постоянную времени "Tпт": ')
            try:
                k = float(k)
                T = float(T)
                wfTurbine = matlab.tf([k], [T, 1])
            except ValueError:
                print(color.Fore.RED + '\nПожалуйста, введите числовое значение!\n')
                tChoice = True
    return wfTurbine


# Функция для ввода коэффициентов передаточной функции генератора
def chioceGenerator():
    gChoice = True
    while gChoice:
        print(color.Style.RESET_ALL)
        gChoice = False
        print('Введите коэффициенты передаточной функции генератора:')
        T = input('Пожалуйста, введите коэффициент "Tг": ')
        try:
            T = float(T)
            wfGenerator = matlab.tf([1], [T, 1])
        except ValueError:
            print(color.Fore.RED + '\nПожалуйста, введите числовое значение!\n')
            gChoice = True
    return wfGenerator


# Функция для ввода коэффициентов обратной связи
def chioceLink():
    lChoice = True
    while lChoice:
        print(color.Style.RESET_ALL)
        lChoice = False
        print('Введите коэффициенты передаточной функции обратной связи:')
        k = input('Пожалуйста, введите коэффициент усиления "Koc": ')
        T = input('Пожалуйста, введите постоянную времени "Toc": ')
        try:
            k = float(k)
            T = float(T)
            if feedback == 'Жёсткая обратная связь':
                wfFeedback = matlab.tf([k], [1])
            elif feedback == 'Гибкая обратная связь':
                wfFeedback = matlab.tf([k, 0], [1])
            elif feedback == 'Апериодическая жёсткая обратная связь':
                wfFeedback = matlab.tf([k], [T, 1])
            elif feedback == 'Апериодическая гибкая обратная связь':
                wfFeedback = matlab.tf([k, 0], [T, 1])
        except ValueError:
            print(color.Fore.RED + '\nПожалуйста, введите числовое значение!\n')
            lChoice = True
    return wfFeedback


# Функция для вывода на экран передаточной функции
def showW():
    print('Передаточная функция САУ:\n %s' % wCloseCAY)


# Функция для построения переходной характеристики
def characteristicH():
    print('Переходная характеристика изображена на графике.\n')
    [y, x] = matlab.step(wCloseCAY)
    pyplot.plot(x, y, 'Blue')
    pyplot.title('Переходная характеристика')
    pyplot.xlabel('t, с')
    pyplot.ylabel("h(t)")
    pyplot.grid()
    pyplot.show()


# Функция для вывода на экран полюсов передаточной функции
def polesW():
    pChoice = True
    while pChoice:
        print(color.Style.RESET_ALL)
        pChoice = False
        print('Полюса передаточной функции:\n %s' % matlab.pole(wCloseCAY))
        a = input('\nВведите "1", если полюса левые, введите "2", если - нет:\n')
        if a.isdigit():
            a = int(a)
            if a == 1:
                print('Полюса левые, следовательно, система устойчива.\n')
            elif a == 2:
                print('Полюс(-а) не является(-ются) левым(-ыми), значит, система неустойчива.\n')
            else:
                print(color.Fore.RED + '\nНекорректное значение!')
                pChoice = True
        else:
            print(color.Fore.RED + '\nНекорректное значение!')
            pChoice = True


# Функция для построения годографа Найквиста
def nyquist():
    pyplot.title('Годограф Найквиста')
    pyplot.ylabel('Im')
    pyplot.xlabel('Re')
    matlab.nyquist(wOpenCAY)
    pyplot.grid(True)
    pyplot.plot()
    pyplot.show()


# Функция для построения ЛАЧХ и ЛФЧХ
def freqCh():
    print('ЛАЧХ и ЛФЧХ изображены на графике.\n')
    matlab.bode(wCloseCAY, dB=False)
    pyplot.plot()
    pyplot.xlabel('Частота (Гц)')
    pyplot.show()


# Функция для определения характеристического уравнения и построения годографа Михайлова
def mikhailovCh():
    print('Передаточная функция САУ:\n %s' % wCloseCAY)
    mChoice = True
    while mChoice:
        print(color.Style.RESET_ALL)
        mChoice = False
        w = sympy.symbols('w')
        print('Пожалуйста, введите коэффициенты знаменателя передаточной функции, начиная от коэффициентов, стоящих\n'
              'при s^4, и заканчивая свободным членом (коэффициентом при s^0).')
        a4 = input('a4: ')
        a3 = input('a3: ')
        a2 = input('a2: ')
        a1 = input('a1: ')
        a0 = input('a0: ')
        try:
            a4 = float(a4)
            a3 = float(a3)
            a2 = float(a2)
            a1 = float(a1)
            a0 = float(a0)
            if a4 == 0:
                dClose = a3 * (1j * w) ** 3 + a2 * (1j * w) ** 2 + a1 * (1j * w) + a0
                dClose = sympy.expand(dClose)
                print('Характеристическое уравнение замкнутой системы: \n%s' % dClose)
                U = re(dClose)
                V = im(dClose)
                x = [U.subs({w: q}) for q in numpy.arange(0, 2, 0.01)]
                y = [V.subs({w: q}) for q in numpy.arange(0, 2, 0.01)]
                pyplot.plot(x, y, 'green')
                pyplot.title('Годограф Михайлова')
                pyplot.ylabel('V(w)')
                pyplot.xlabel('U(w)')
                pyplot.grid(True)
                pyplot.plot()
                pyplot.show()
            else:
                dClose = a4 * (1j * w) ** 4 + a3 * (1j * w) ** 3 + a2 * (1j * w) ** 2 + a1 * (1j * w) + a0
                dClose = sympy.expand(dClose)
                print('Характеристическое уравнение замкнутой системы: \n%s' % dClose)
                U = re(dClose)
                V = im(dClose)
                x = [U.subs({w: q}) for q in numpy.arange(0, 0.2, 0.01)]
                y = [V.subs({w: q}) for q in numpy.arange(0, 0.2, 0.01)]
                pyplot.plot(x, y, 'green')
                pyplot.title('Годограф Михайлова')
                pyplot.ylabel('V(w)')
                pyplot.xlabel('U(w)')
                pyplot.grid(True)
                pyplot.plot()
                pyplot.show()
        except ValueError:
            print(color.Fore.RED + '\nПожалуйста, введите числовое значение!\n')
            mChoice = True


# Функция для замены коэффициента усиления обратной связи
def changeK():
    lChoice = True
    # Цикл для проверки ввода коэффициентов передаточной функции
    while lChoice:
        print(color.Style.RESET_ALL)
        lChoice = False
        print('Введите коэффициенты передаточной функции обратной связи:')
        k = input('Пожалуйста, введите НОВЫЙ коэффициент усиления "Koc": ')
        T = input('Пожалуйста, введите ПРЕЖНЮЮ постоянную времени "Toc": ')
        try:
            k = float(k)
            T = float(T)
            if feedback == 'Жёсткая обратная связь':
                wfFeedback = matlab.tf([k], [1])
            elif feedback == 'Гибкая обратная связь':
                wfFeedback = matlab.tf([k, 0], [1])
            elif feedback == 'Апериодическая жёсткая обратная связь':
                wfFeedback = matlab.tf([k], [T, 1])
            elif feedback == 'Апериодическая гибкая обратная связь':
                wfFeedback = matlab.tf([k, 0], [T, 1])
        except ValueError:
            print(color.Fore.RED + '\nПожалуйста, введите числовое значение!\n')
            lChoice = True
    return wfFeedback

# Функция для выбора действий
def selectCommand1():
    perform = True
    while perform:
        print(color.Style.RESET_ALL)
        commandUser = input('Выберите пункт, который необходимо выполнить:\n'
                            '1 - Показать передаточную функцию исследуемой САУ;\n'
                            '2 - Построить переходную характеристику;\n'
                            '3 - Найти полюса передаточной функции;\n'
                            '4 - Проверить устойчивость по критерию Найквиста;\n'
                            '5 - Построить ЛАЧХ и ЛФЧХ;\n'
                            '6 - Проверить устойчивость по критерию Михайлова;\n'
                            '7 - Найти коэффициент "Кос", при котором система находится на границе устойчивости;\n')
        if commandUser.isdigit():
            commandUser = int(commandUser)
            if commandUser == 1:
                showW()
            elif commandUser == 2:
                characteristicH()
            elif commandUser == 3:
                nyquist()
            elif commandUser == 4:
                polesW()
            elif commandUser == 5:
                freqCh()
            elif commandUser == 6:
                mikhailovCh()
            elif commandUser == 7:
                perform = False
            else:
                print(color.Fore.RED + '\nНедопустимое значение!')
        else:
            print(color.Fore.RED + '\nПожалуйста, введите числовое значение!')


def selectCommand2():
    perform = True
    while perform:
        print(color.Style.RESET_ALL)
        commandUser = input('Выберите пункт, который необходимо выполнить:\n'
                            '1 - Показать передаточную функцию исследуемой САУ;\n'
                            '2 - Построить переходную характеристику;\n'
                            '3 - Найти полюса передаточной функции;\n'
                            '4 - Проверить устойчивость по критерию Найквиста;\n'
                            '5 - Построить ЛАЧХ и ЛФЧХ;\n'
                            '6 - Проверить устойчивость по критерию Михайлова;\n'
                            '7 - Закончить работу;\n')
        if commandUser.isdigit():
            commandUser = int(commandUser)
            if commandUser == 1:
                showW()
            elif commandUser == 2:
                characteristicH()
            elif commandUser == 3:
                nyquist()
            elif commandUser == 4:
                polesW()
            elif commandUser == 5:
                freqCh()
            elif commandUser == 6:
                mikhailovCh()
            elif commandUser == 7:
                perform = False
            else:
                print(color.Fore.RED + '\nНедопустимое значение!')
        else:
            print(color.Fore.RED + '\nПожалуйста, введите числовое значение!')


wOrgan = chioceOrgan()
wTurbine = chioceTurbine()
wGenerator = chioceGenerator()
wFeedback = chioceLink()
wOpenCAY = wOrgan*wTurbine*wGenerator
wCloseCAY = matlab.feedback(wOpenCAY, wFeedback)
choice = selectCommand1()
for Koc in numpy.arange(0, 10, 0.01):

    wFeedback = matlab.tf([Koc], [0, 1])
    wCloseCAY = matlab.feedback(wOpenCAY, wFeedback)
    c = wCloseCAY.den[0][0]
    coef = {}
    size = len(c)
    for j in range(size):
        coef["%s" % j] = c[j]
    matrix = numpy.array([[coef["1"], coef["3"]],
              [coef["0"], coef["2"]]])
    if (numpy.linalg.det(matrix) >= -0.0001) & (numpy.linalg.det(matrix) <= 0.0001):
        print('Предельное значение коэффициента обратной связи:', Koc)
        break
        selectCommand2()

choice = selectCommand2()





