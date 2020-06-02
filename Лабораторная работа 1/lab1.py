# -*- coding: utf-8 -*-

import csv #библиотека для обработки csv-файлов

k_call = 1 #множитель тарифного плана для услуг "Телефония"
k_sms = 1 #множитель тарифного плана для услуг "СМС"

#начальное значение длительности исходящего и входящего вызовов
T_out = 0 
T_in = 0 

N = 0 #начальное значение количества смс

with open ('data.csv') as file:  #открываем файл data.csv и заносим данные в словари
	reader = csv.DictReader(file)

	for row in reader:
#среди абонентов находим нужный и соответствующие ему длительность исходящего и входящего звонка и количество отправленных смс
		if row['msisdn_origin'] == '915642913': 
			T_out = T_out + float(row['call_duration'])
			N = N + int(row['sms_number'])
		if row['msisdn_dest'] == '915642913':
			T_in = T_in + float(row['call_duration'])

#будем считать, что длительности звонков записаны в формате мм:сс (минуты, секунды), переведем его в формат секунд, а затем минут
T_in_float = str(T_in % 1)
if len(T_in_float) == 4:
	T_in_float = (T_in % 1) * 100
elif len(T_in_float) == 3:
	T_in_float = (T_in % 1) *10
T_in_sec = int(T_in / 1) * 60 + T_in_float
T_in = T_in_sec / 60

T_out_float = str(T_out % 1)
if len(T_out_float) == 4:
	T_out_float = (T_out % 1) * 100
elif len(T_out_float) == 3:
	T_out_float = (T_out % 1) *10
T_out_sec = int(T_out / 1) * 60 + T_out_float
T_out = T_out_sec / 60

T = T_in + T_out #общая длительность входящих и исходящих звонков (с учетом того, что коэффициент для входящих и исходящих звонков одинаковый)
#расчет стоимости услуг
X = T * k_call
Y = (N - 5) * k_sms

final_message = 'Результат тарификации услуг "Телефония" для абонента с номером телефона 915642913: ' + str("%.2f" % X) + ' руб.' + '\nРезультат тарификации услуг "СМС" для абонента с номером телефона 915642913: ' + str(Y) + ' руб.' + "\nОбщая стоимость услуг за расчетный период: " + str("%.2f" % (X+Y)) + " руб."

#запись результата тарификации в файл lab1.txt
f = open ('lab1.txt', 'w')
f.write (final_message)
f.close()