import subprocess
import matplotlib.pyplot as plt

file = open("data.txt", "w")
data = subprocess.run(["nfdump", "-o", "fmt:%te|%sa|%da|%byt", "-r", "nfcapd.202002251200"], stdout=subprocess.PIPE, text=True)
file.write(data.stdout)
file.close()
file = open("data.txt", "r")
outputfile = open("output2.txt", "w")

def parsing(file):
	'''Представим нашу таблицу в виде словаря списков.'''
	mydict = {}
	mydict["date_first_seen"] = []
	mydict["src_add"] = []
	mydict["dst_add"] = []
	mydict["bytes"] = []

	line = file.readline() #(просто считываем первую строку, она нам не нужна)
	
	#Столбцы таблицы представим в виде списков - значений для каждого ключа нашего словаря:
	word = ""
	key_number = 1
	for char in file.read():
		if (char == "|") or (char == "\n"):
			if key_number == 1:
				mydict["date_first_seen"].append(word)
			elif key_number == 2:
				word = word.replace(' ', '')
				mydict["src_add"].append(word)
			elif key_number == 3:
				word = word.replace(' ', '')
				mydict["dst_add"].append(word)
			elif key_number == 4:
				word = word.replace(' ', '')
				#если встречается запись "... M", то переводим в байты:
				if word[-1] == "M":
					word = word[:-1]
					word = str(float(word)*1000000)
				mydict["bytes"].append(word)
			word = ""
			
			if key_number < 4:
				key_number += 1
			else:
				key_number = 1
		else:
			word += char
	mydict["date_first_seen"].pop()
	mydict["src_add"].pop()
	mydict["dst_add"].pop()
	mydict["bytes"].pop()
	return mydict

def tariffication(mydict, ip, k):
	'''Тарификация услуг и сохранение нужных данных.'''
	cost = 0
	x = [] #абсцисса для графика
	y = [] #ордината графика
	num = 0 #счетчик
	cur_time = 0 
	for i in mydict["src_add"]:
		if (i == ip) or (mydict["dst_add"][num] == ip):
			cost += float(mydict["bytes"][num]) * k/1000

			if mydict["date_first_seen"][num] != cur_time:
				x.append(mydict["date_first_seen"][num])
				y.append(int(float(mydict["bytes"][num])))
				cur_time = mydict["date_first_seen"][num]
			else:
				y[-1] += int(float(mydict["bytes"][num]))
		num += 1
	
	answer = "Всего потрачено: " + str(round(cost*1000/k, 2)) + " байт = " + str(round(cost, 2)) + " Кбайт.\n"
	return cost - free_cost, x, y, answer

def graph(x, y):
	'''Функция создает график.'''
	plt.plot(x, y, lw=1)
	plt.ylabel('Объем трафика')
	plt.xlabel('Время')
	plt.title('Зависимость объема трафика от времени')
	plt.show()

#Множитель тарифного плана:
k = 1 #руб/Кб
#Количество бесплатных Кбайт:
free_cost = 1000
#IP-адрес абонента:
ip = "192.168.250.59"

mydict = parsing(file)
cost, x, y, answer = tariffication(mydict, ip, k)

answer += "Итоговая стоимость: " + str(round(cost, 2)) + " рублей."
outputfile.write(answer)
graph(x, y)

file.close()
outputfile.close()