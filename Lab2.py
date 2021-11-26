# Импортировали необходимые библиотеки
import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy as numpy
import math
import colorama as color
import sympy as sympy

# Описание функции для выбора типа обратной связи
def chFeedback():
    print('Выберите тип обратной связи САУ и тип турбины:')
    # Переменные - типы обратной связи
    rigid = 'Жёсткая'
    flexible = 'Гибкая'
    aperiodicRigid = 'Апериодическая жёсткая'
    aperiodicFlexible = 'Апериодическая гибкая'
    # Переменная для проверки правильности ввода команды
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
                feedbackType = 'Апериодтческая гибкая обратная связь'
            else:
                print(color.Fore.RED + '\nНедопустимое значение!')
                newChoiceFeedback = True
        else:
            print(color.Fore.RED + '\nПожалуйста, введите числовое значение!')
            newChoiceFeedback = True
    return feedbackType

# Описание функции для выбора типа турбины
def chTurbine():
    # Переменные - типы турбины
    hydroTurbine = 'Гидротурбина'
    steamTurbine = 'Паровая турбина'
    # Переменная для проверки правильности ввода команды
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
    # Цикл для проверки ввода коэффициентов передаточной функции
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
    # Цикл для проверки ввода коэффициентов передаточной функции
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
    # Цикл для проверки ввода коэффициентов передаточной функции
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
    # Цикл для проверки ввода коэффициентов передаточной функции
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


wOrgan = chioceOrgan()
wTurbine = chioceTurbine()
wFeedback = chioceLink()
wGenerator = chioceGenerator()