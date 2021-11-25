# Импортировали необходимые библиотеки
import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy as numpy
import math
import colorama as color
import sympy as sympy

# Описание функции для выбора типа обратной связи
def chFeedback():
    print('\nВыберите тип обратной связи САУ и тип турбины:')
    # Переменные - типы обратной связи
    rigid = 'Жёсткая'
    flexible = 'Гибкая'
    aperiodicRigid = 'Апериодическая жёсткая'
    aperiodicFlexible = 'Апериодическая гибкая'
    # Переменная для проверки правильности ввода команды
    newChoiceFeedback = True
    # Цикл для проверки правильности ввода команды и для присвоения переменной feedback названия типа обратной связи
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


def chTurbine():
    # Переменные - типы турбины
    hydroTurbine = 'Гидротурбина'
    steamTurbine = 'Паровая турбина'
    # Переменная для проверки правильности ввода команды
    newChoiceTurbine = True
    # Цикл для проверки правильности ввода команды и для присвоения переменной turbine названия типа турбины
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


print('Элементы исследуемой системы автоматического управления:\n'
      '1. Усилительно-исполнительный орган;\n'
      '2. ' + turbine + ';\n'
      '3. Генератор;\n'
      '4. ' + feedback + '.\n')


