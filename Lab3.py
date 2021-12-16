# Импортировали необходимые библиотеки
import matplotlib.pyplot as pyplot
import control.matlab as matlab
import control
import numpy as numpy
import math
import sympy as sympy
from scipy import integrate


# Функция для задания параметров регулятора, используемого в САУ
def Regulator(CAYRegulator):
    if CAYRegulator == "ПИД":
        Kp = 1.5
        Ti = 14
        Td = 1.5
        pRegulator = matlab.tf([Kp], [1])
        iRegulator = matlab.tf([1], [Ti, 0])
        dRegulator = matlab.tf([Td, 0], [1])
        PIDRegulator = control.parallel(pRegulator, iRegulator, dRegulator)
        return PIDRegulator
    elif CAYRegulator == 'ПД':
        Kp = 1
        Td = 1
        pRegulator = matlab.tf([Kp], [1])
        dRegulator = matlab.tf([Td, 0], [1])
        PDRegulator = control.parallel(pRegulator, dRegulator)
        return PDRegulator


nameOfRegulator = input("Введите наименование регулятора (ПИД или ПД):\n")
# Передаточные функции звеньев САУ
wFeedback = matlab.tf([1], [1])
wGenerator = matlab.tf([1], [4, 1])
wTurbine = matlab.tf([0.02, 1], [0.2, 1])
wOrgan = matlab.tf([20], [5, 1])

# Определение эквивалентной передаточной функции САУ
wCAY = control.series(Regulator(nameOfRegulator), wGenerator, wTurbine, wOrgan)
wCAYclosed = matlab.feedback(wCAY, wFeedback)
print(wCAYclosed)

# Прямые оценки качества переходного процесса по переходной характеристике
timeLine = numpy.arange(0, 100, 0.01)
[y, x] = matlab.step(wCAYclosed, timeLine)
# Удаление части переходной характеристики (от момента времени t=0 до момента времени достижения первого максимума)
indexFirstMaxValue = numpy.argmax(y)
indexFirstMaxMassive = []
for i in range(indexFirstMaxValue):
    indexFirstMaxMassive.append(i)
y1 = numpy.delete(y, indexFirstMaxMassive)
x1 = numpy.delete(x, indexFirstMaxMassive)
# Значение первого максимума и его момент времени
FirstMaxValue = max(y)
TimeFirstMax = float
for i in range(len(y)):
    if y[i] == FirstMaxValue:
        TimeFirstMax = x[i]
infinityTime = 100
# Нахождение установившегося значения
t = None
for i in range(len(x1)):
    if x1[i] <= infinityTime:
        t = i
InfinityValue = y1[t]
# positiveDeviationOfInfinityValue - положительное отклонение установившейся величины
pDInfinityValue = InfinityValue * 1.05
# negativeDeviationOfInfinityValue - отрицательное отклонение установившейся величины
nDInfinityValue = InfinityValue * 0.95
# Определение длительности переходного процесса
TimePP = float
for i in range(t):
    if (pDInfinityValue - 0.001 < y1[i] < pDInfinityValue + 0.001) or (nDInfinityValue - 0.001 < y1[i] < nDInfinityValue + 0.001):
        TimePP = x1[i]
# Определение степени затухания
# Нахождение первого минимума после первого максимума
indexFirstMinValue = numpy.argmin(y1)
indexFirstMinMassive = []
for i in range(indexFirstMinValue):
    indexFirstMinMassive.append(i)
y2 = numpy.delete(y1, indexFirstMinMassive)
x2 = numpy.delete(x1, indexFirstMinMassive)
# Нахожение второго максимума переходной характеристики
SecondMaxValue = max(y2)
TimeSecondMax = float
for i in range(len(y1)):
    if y[i] == SecondMaxValue:
        TimeSecondMax = x[i]
zatCoef = (FirstMaxValue - SecondMaxValue) / FirstMaxValue
colebCoef = FirstMaxValue / SecondMaxValue
perCoef = ((FirstMaxValue - InfinityValue) / InfinityValue) * 100
# Результаты расчета прямых показателей качества переходного процесса
print("Прямые оценки качества переходного процесса:")
print("а) Время регулирования:", TimePP)
print("б) Перерегулирование:", perCoef)
print("в) Колебательность:", colebCoef)
print("г) Степень затухания:", zatCoef)
print("д) Величина первого максимума:", FirstMaxValue)
print("   Время достижения первого максимума:", TimeFirstMax)
pyplot.plot(x, y, "red")
pyplot.grid(True)
pyplot.title("Переходная характеристика")
pyplot.ylabel("Амплитуда")
pyplot.xlabel("Время, (с)")
pyplot.hlines(1.05 * y[len(timeLine) - 1], 0, 100)
pyplot.hlines(0.95 * y[len(timeLine) - 1], 0, 100)
pyplot.show()

# Определение косвенных показателей качества по распределению корней на комплексной плоскости замкнутой САУ
# Определение значения полюсов передаточной функции замкнутой САУ
Poles = matlab.pole(wCAYclosed)
Poles = numpy.round(Poles, 3)
print('\nПолюса передаточной функции замкнутой САУ:\n', Poles)
# Определение времени регулирования
StartValue = -1000
for i in range(len(Poles)):
 if Poles[i].real >= StartValue:
    StartValue = Poles[i].real
TimePPpoles =math.fabs(3 / StartValue)
# Определение степени колебательности
maxValueRelationRoots = 0
colebCoefPoles = 0
for i in Poles:
    colebCoefPoles = math.fabs(sympy.im(i) / sympy.re(i))
    if colebCoefPoles > maxValueRelationRoots:
        maxValueRelationRoots = colebCoefPoles
colebCoefPoles = maxValueRelationRoots
# Определение перерегулирования
perCoefPoles = math.e**(-math.pi / colebCoefPoles)
# Опеределение степени затухания
zatCoefPoles = 1 - math.e**(-2 * math.pi / colebCoefPoles)
# Карта полюсов и нулей
control.pzmap(wCAYclosed, title='Карта полюсов и нулей замкнутой САУ')
pyplot.show()
# Результаты расчет косвенных показателей качества ппереходного процесса по распределению корней
print('\nОценки качества ПП по распределению корней на комплексной плоскости замкнутой САУ:')
print('а) Время регулирования:', TimePPpoles)
print('б) Перерегулирование:', perCoefPoles)
print('в) Колебательность:', colebCoefPoles)
print('г) Степень затухания:', zatCoefPoles)

# Определение показателей качества ПП по частотным характеристикам
timeLine = numpy.arange(0, 10, 0.01)
mag, phase, omega = matlab.freqresp(wCAYclosed, timeLine)
aMaxValue = max(mag)
aStartValue = mag[0]
indexAMaxValue = numpy.argmax(mag)
# Удаление части логарифмической характеристики до максимального значения
indexAMaxMassive = []
for i in range(0, indexAMaxValue):
    indexAMaxMassive.append(i)
mag1 = numpy.delete(mag, indexAMaxMassive)
omega1 = numpy.delete(omega, indexAMaxMassive)
# Определение частоты среза
indexFrequencySR = 0
for i in range(1, len(mag1)-1):
    if mag1[i-1] >= mag[0] >= mag1[i + 1]:
        indexFrequencySR = i
FrequencySR = omega1[indexFrequencySR]
# Определение времени регулирования
TimePPA = 1 * ((2 * math.pi) / FrequencySR)
pyplot.plot(omega, mag, "red")
pyplot.grid(True)
pyplot.title("АЧХ")
pyplot.ylabel("Амплитуда")
pyplot.xlabel("Угловая частота, (рад/с)")
pyplot.hlines(mag[0], 0, 3, linestyles="--")
pyplot.show()
# Определение показателя колебательности
colebCoefA = aMaxValue / aStartValue
# ЛАЧХ и ЛФЧХ
matlab.bode(wCAYclosed, dB=False)
pyplot.plot()
pyplot.xlabel('Частота (Гц)')
pyplot.show()
# Результаты расчет косвенных показателей по частотным характеристикам
print("\nПоказатели качества ПП по частотным характеристикам")
print("a) Время регулирования:", TimePPA)
print("b) Показатель колебательности:", colebCoefA)

# Интегральный метод
timeLine = numpy.arange(0, 100, 0.1)
[y, x] = matlab.step(wCAYclosed, timeLine)
yValueInt = []
for i in y:
    yValueInt.append(math.fabs(InfinityValue - i))
Q = integrate.trapezoid(yValueInt, x)
print("\nИнтегральный метод Q")
print("Значение интеграла", Q)
print("\nПоказатели качества:")
print("Время регулирования: 11 = ", TimePP)
print("Перерегулирование: 29 = ", perCoef)
print("Показатель колебательности: 1.24 = ", colebCoefA)