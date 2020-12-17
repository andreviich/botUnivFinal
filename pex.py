from pandas import read_csv, DataFrame, set_option
import settings
from telebot import types
import telebot
import time
set_option('display.max_rows', settings.MAX_ROWS)
bot = telebot.TeleBot(settings.TOKEN)
# print(dir(telebot))
# print('Загружаю группы... ')
groups = read_csv('groups.csv', sep=";")
# print('Загружаю результаты... ')
results = read_csv('results.csv', sep=";")
# print('Загружаю студентов... ')
students = read_csv('students.csv', sep=";")
# print('Загружаю предметы... ')
subjects = read_csv('subjects.csv', sep=";")
# print('Загружаю преподавателей... ')
teachers = read_csv('teachers.csv', sep=";")
# print('Готово! Данные загружены!')
@bot.message_handler(commands=['start'])
def send_welcome(message):

	bot.send_message(
		message.chat.id, 'Привет! Добро пожаловать в бот!'
	)
def tryAgain(message, msg):
	time.sleep(settings.INTERVAL)
	bot.send_message(
		message.chat.id, msg
	)
def OutMessage(message, msg):
	time.sleep(settings.INTERVAL)
	bot.send_message(
		message.chat.id, msg
	)
@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, 'Вывод всех команд...')
	OutMessage(message, """
Для получения студентов по наименованию группы введите команду 'студенты' и название группы в верхнем или нижнем регистре. Например: 'студенты ПИ1-1'
""")
	OutMessage(message, """
Для получения преподавателей по наименованию группы введите команду 'преподаватели' и название группы в верхнем или нижнем регистре. Например: 'преподаватели ПИ1-1'
""")
	OutMessage(message, """
		Для получения списка групп у определенного преподавателя введите команду 'группы' и фамилию преподавателя в именительном падеже. Например: 'группы Милованов'
""")
	OutMessage(message, """
Для получения оценок конкретного студента введите команду 'оценки', фамилию и имя студента в именительном падеже. Например: 'оценки Бирюков Максим'
""")
	OutMessage(message, """
Для получения среднего балла всех студентов у конкретного преподавателя введите команду 'средний балл' и фамилию преподавателя в именительном падеже. Например: 'средний балл Милованов'
""")
	OutMessage(message, """
Для для того, чтобы узнать, ведет ли данный преподаватель у конкретной группы, введите "ведёт" ,  фамилию преподавателя в именительном падеже и название группы. Например: 'ведёт Милованов ПИ1-1'
""")
	OutMessage(message, """
Для для того, чтобы узнать все оценки по конкретному предмету, введите "оценки по предмету" и название предмета. Например: 'оценки по предмету философия'
""")
	OutMessage(message, """
Для для того, чтобы узнать все оценки студентов определенной группы по конкретному предмету, введите "оценки группы", наименование группы и предмет. Например: 'оценки группы пи1-1 Философия'
""")
	OutMessage(message, """
Для для того, чтобы узнать все оценки студентов определенной группы у определенного преподавателя, введите "оценки группы", наименование группы, слово 'преподаватель' и фамилию преподавателя в именительном падеже. Например: 'оценки группы пи1-1 преподаватель Милованов'
""")

	OutMessage(message, """
Для для того, чтобы узнать все оценки студентов у конкретного преподавателя, введите "оценки преподавателя" и фамилию преподавателя в именительном падеже. Например: 'оценки преподавателя Милованов'
""")
	OutMessage(message, """
Возвращает количество оценок 5, 4, 3, 2 у данной группы и преподавателя разбитые по предметам. Для вызова этой команды введите фамилию преподавателя и название группы. Например, 'Милованов пи1-1'
""")
@bot.message_handler(content_types=['text'])
def usualMessage(message):
	comm = message.text
	comm = comm.upper().split()
	allSubjects = subjects['subject_name'].values.tolist()
	allTeachers = teachers['last_name'].values.tolist()
	allGroups = groups['name'].values.tolist()
	print(comm)
	if len(comm) < 2 and 'КОМАНДЫ' not in comm:
		OutMessage(message,'Команда была введена неверно, повторите попытку. Для вывода всех команд введите команду "/help"')
	if 'СТУДЕНТЫ' in comm:
		group = comm[1]
		def getAllStudents(group):
			try:
				id_group = int(groups['id'].where(groups['name'] == group).dropna())
			except:
				tryAgain(message,'Группа не найдена')
				return
			studentsOfThisGroup = students[['last_name', 'first_name']].where(students['group_id'] == id_group).dropna().values.tolist()
			OutMessage(message,f'Студенты группы {group}:')
			msg = ''
			for i in studentsOfThisGroup:
				i = '- ' + ' '.join(i) + '\n'
				msg = msg + i
			OutMessage(message,msg)
		getAllStudents(group)
	if 'ПРЕПОДАВАТЕЛИ' in comm:
		group = comm[1]
		OutMessage(message,f'Преподаватели группы {group}:')
		def getAllTeachers(group):
			try:
				id_group = int(groups['id'].where(groups['name'] == group).dropna())
			except:
				tryAgain(message,'Группа не найдена')
				return
			firstStudentOfThisGroup = students[['id']].where(students['group_id'] == id_group).dropna().iloc[0]
			idFirstStudentOfThisGroup= round(float(firstStudentOfThisGroup.to_string(index=False, header=False)))
			idTeachersOfThisGroup = results['teacher_id'].where(results['student_id'] == idFirstStudentOfThisGroup).dropna().astype('int32').values.tolist()
			TeachersOfThisGroup = teachers[['last_name', 'first_name', 'middle_name']].where(teachers['id'].isin(idTeachersOfThisGroup)).dropna().values.tolist()
			msg = ''
			for i in TeachersOfThisGroup:
				i = '- ' + ' '.join(i) + '\n'
				msg = msg + i
			# TeachersOfThisGroup = TeachersOfThisGroup.to_string(index=False, header=False)
			OutMessage(message,msg)
		getAllTeachers(group)
	if 'ГРУППЫ' in comm and 'ОЦЕНКИ' not in comm:
		teacher = comm[1].lower().capitalize()
		print(teacher)
		OutMessage(message,f'Вывод групп преподавателя {teacher}')
		def grps(teacher):
			try:
				idTeacher = teachers['id'].where(teachers['last_name'] == teacher).dropna().astype('int32').values.tolist()[0]
			except:
				tryAgain(message,'Преподаватель не найден')
				return
			idsStudents = results['student_id'].where(results['teacher_id'] == idTeacher).dropna().astype('int32').values.tolist()
			idsGroup = students['group_id'].where(students['id'].isin(idsStudents)).dropna().astype('int32').values.tolist()

			idsGroup_undublicated = []
			for id in idsGroup:
				if id not in idsGroup_undublicated:
					idsGroup_undublicated.append(id)
			idsGroup_undublicated.sort()
			namesOfGroups = groups['name'].where(groups['id'].isin(idsGroup_undublicated)).dropna().values.tolist()
			msg = ''
			for i in namesOfGroups:
				i = '- ' + i + '\n'
				msg = msg + i
			OutMessage(message,msg)
		grps(teacher)
	if 'ОЦЕНКИ' in comm and len(comm)==3 and not 'ПРЕПОДАВАТЕЛЯ' in comm:
		first_name = comm[2]
		last_name = comm[1]
		first_name = first_name.lower().capitalize()
		last_name = last_name.lower().capitalize()
		def getAllPoints(first_name, last_name):
			try:
				idStudent = students['id'].where((students['last_name'] == last_name) & (students['first_name'] == first_name)).dropna().astype('int32').values.tolist()[0]
			except Exception as e:
				tryAgain(message,'Студент не найден')
				return
			resStudent = results[[ 'subject','att1', 'att2', 'exam', 'total']].where(results['student_id'] == idStudent).dropna().astype('int32')
			resStudent = subjects.merge(resStudent, left_on="id", right_on="subject")[['subject_name', 'total']].values.tolist()
			msg = ''
			msg = msg + f'Оценки студента {last_name} {first_name}:\n------------\n'
			for disc, total in resStudent:
				msg = msg + f'{disc} : {total}\n'
			# print(outputResStudent)
			OutMessage(message, msg)
		getAllPoints(first_name, last_name)
	if 'СРЕДНИЙ' in comm and len(comm) == 3:
		teacher = comm[2].lower().capitalize()
		def average(teacher):
			try:
				idTeacher = teachers['id'].where(teachers['last_name'] == teacher).dropna().astype('int32').values.tolist()[0]
			except Exception as e:
				tryAgain(message,'Преподаватель не найден')
				return
			allPoints = results['total'].where(results['teacher_id'] == idTeacher).dropna().astype('int32').values.tolist()
			average = round(sum(allPoints)/len(allPoints),2)
			OutMessage(message,average)
		average(teacher)
	if 'ВЕДЕТ' in comm and len(comm) ==3 or 'ВЕДЁТ' in comm and len(comm) ==3:
		group = comm[2]
		teacher = comm[1].lower().capitalize()
		def isGroupEducatedByTeacher(group, teacher):
			try:
				idTeacher = teachers['id'].where(teachers['last_name'] == teacher).dropna().astype('int32').values.tolist()[0]
			except:
				tryAgain(message,'Преподаватель не найден')
				return
			try:
				id_group = groups['id'].where(groups['name'] == group).dropna().astype('int32').values.tolist()[0]
			except Exception as e:
				tryAgain(message,'Данная группа не обнаружена в списке')
				return
			try:
				idsStudents = results['student_id'].where(results['teacher_id'] == idTeacher).dropna().astype('int32').values.tolist()[0]
			except:
				tryAgain(message,'У данного преподавателя студенты не найдены')
				return
			idsTeachers = results['teacher_id'].where(results['student_id'] == idsStudents).dropna().astype('int32').values.tolist()
			if idTeacher in idsTeachers:
				OutMessage(message,f'{teacher} ведёт у {group}')
			else:
				OutMessage(message,f'{teacher} не ведёт у {group}')
		isGroupEducatedByTeacher(group, teacher)
	if 'ОЦЕНКИ' in comm and len(comm)==3 and 'ПРЕПОДАВАТЕЛЯ' in comm:
		teacher = comm[2].lower().capitalize()
		def getAllPointsOfTeacher(teacher):
			try:
				idTeacher = teachers['id'].where(teachers['last_name'] == teacher).dropna().astype('int32').values.tolist()[0]
			except:
				tryAgain(message,'Преподаватель не найден')
				return
			allpoints = results[['student_id', 'total']].where(results['teacher_id'] == idTeacher).dropna().astype('int32').values.tolist()
			# print(allpoints)
			massiveToSend = ""
			counter = 0
			for st, point in allpoints:
				# OutMessage(message, f'Номер студака: {st} Балл: {point}')
				if counter > 9:
					OutMessage(message, massiveToSend)
					massiveToSend = ''
					counter = 0
				counter +=1
				massiveToSend += f"Студак: {st}  Балл: {point}\n"
			# OutMessage(message,allpoints)
			
		getAllPointsOfTeacher(teacher)
	if 'ОЦЕНКИ'	in comm and 'ГРУППЫ' in comm and 'ПРЕПОДАВАТЕЛЬ' in comm and len(comm) > 4:
		group = comm[2]
		teacher = comm[4].lower().capitalize()
		print(group, teacher)
		# print('here')
		if group in allGroups:
			if teacher in allTeachers:
				idTeacher = teachers['id'].where(teachers['last_name'] == teacher).dropna().astype('int32').values.tolist()[0]
				# print(idTeacher)
				id_group = groups['id'].where(groups['name'] == group).dropna().astype('int32').values.tolist()[0]
				idsStudents = students['id'].where(students['group_id'] == id_group).dropna().astype('int32').values.tolist()
				print(idsStudents)
				allPoints = results[['student_id','total']].where((results['teacher_id'] == idTeacher)&(results['student_id'].isin(idsStudents))).dropna().astype('int32')
				if len(allPoints.index) > 0 :
					allPoints = allPoints.to_string(index=False, header=['Студак', 'Балл'])
					OutMessage(message, allPoints)
				else:
					tryAgain(message, 'Баллов не найдено')
				print(allPoints.index)
				
			else:
				tryAgain(message, 'Преподаватель не найден')
		else:
			tryAgain(message, "Группа не найдена")
	if 'ОЦЕНКИ'	in comm and 'ГРУППЫ' in comm and len(comm) > 3 and 'ПРЕПОДАВАТЕЛЬ' not in comm:
		group = comm[2]
		subject = comm[3:]
		subject = ' '.join(subject).lower().capitalize()
		if group in allGroups:
			if subject in allSubjects:
				idSubject = subjects['id'].where(subjects['subject_name'] == subject).dropna().astype('int32').values.tolist()[0]
				id_group = groups['id'].where(groups['name'] == group).dropna().astype('int32').values.tolist()[0]
				idsStudents = students['id'].where(students['group_id'] == id_group).dropna().astype('int32').values.tolist()
				allPoints = results[['student_id','total']].where((results['subject'] == idSubject)&(results['student_id'].isin(idsStudents))).dropna().astype('int32').to_string(index=False, header=['Студак', 'Балл'])
				OutMessage(message, allPoints)
			else:
				tryAgain(message, 'Предмет не найден')
		else:
			tryAgain(message, "Группа не найдена")

	
	if 'ОЦЕНКИ' in comm and 'ПО' in comm and 'ПРЕДМЕТУ' in comm:
		subject = comm[3:]
		subject = ' '.join(subject).lower().capitalize()
		print(subject)
		def getAllPointsOfSubject(subject):
			try:
				idSubject = subjects['id'].where(subjects['subject_name'] == subject).dropna().astype('int32').values.tolist()[0]
				print(idSubject)
			except:
				tryAgain(message,'Предмет не найден')
				return
			allpoints = results[['student_id', 'total']].where(results['subject'] == idSubject).dropna().astype('int32').values.tolist()
			massiveToSend = ""
			counter = 0
			for st, point in allpoints:
				# OutMessage(message, f'Номер студака: {st} Балл: {point}')
				if counter > 9:
					OutMessage(message, massiveToSend)
					massiveToSend = ''
					counter = 0
				counter +=1
				massiveToSend += f"Студак: {st}  Балл: {point}\n"
		getAllPointsOfSubject(subject)
	if len(comm)==2:
		teacher = comm[0].lower().capitalize()
		group = comm[1]
		def getAllPointsOfTeacherAndGroup(teacher, group):
			if teacher in allTeachers and group in allGroups:
				idTeacher = teachers['id'].where(teachers['last_name'] == teacher).dropna().astype('int32').values.tolist()[0]
				id_group = groups['id'].where(groups['name'] == group).dropna().astype('int32').values.tolist()[0]
				allPoints = results[['subject','total', 'student_id']].where(results['teacher_id'] == idTeacher).dropna().astype('int32')
				for ind, val in allPoints.iterrows():
					sid = val['subject']
					for subject in allSubjects:
						index  = allSubjects.index(subject)+1
						if sid == index:
							allPoints['subject'] = allPoints['subject'].replace(sid, subject)
				subjects = allPoints['subject'].values.tolist()
				subjects = list(dict.fromkeys(subjects))
				for sub in subjects:
					OutMessage(message,f'Оценки по предмету {sub}:')
					five = 0.86
					four = 0.67
					three = 0.42
					fives = allPoints[['student_id','total']].where((allPoints['subject'] == sub) & (allPoints['total']/100 >= five)).dropna().astype('int32')
					fours = allPoints[['student_id','total']].where((allPoints['subject'] == sub) & (allPoints['total']/100 < five) & (allPoints['total']/100 >= four) ).dropna().astype('int32')
					threes = allPoints[['student_id','total']].where((allPoints['subject'] == sub)  & (allPoints['total']/100 < four) & (allPoints['total']/100 >= three)).dropna().astype('int32')
					twos = allPoints[['student_id','total']].where((allPoints['subject'] == sub) & (allPoints['total']/100 < three)).dropna().astype('int32')
					OutMessage(message,'Оценка "5":')
					if fives.empty:
						OutMessage(message,'Пусто')
					else:
						OutMessage(message,fives.to_string(index=False, header=['ID студента', 'Итог'],justify="left"))
					OutMessage(message,'Оценка "4":')
					if fours.empty:
						OutMessage(message,'Пусто')
					else:
						OutMessage(message,fours.to_string(index=False, header=['ID студента', 'Итог'],justify="left"))
					OutMessage(message,'Оценка "3":')
					if threes.empty:
						OutMessage(message,'Пусто')
					else:
						OutMessage(message,threes.to_string(index=False, header=['ID студента', 'Итог'],justify="left"))
					OutMessage(message,'Оценка "2":')
					if twos.empty:
						OutMessage(message,'Пусто')
					else:
						OutMessage(message,twos.to_string(index=False, header=['ID студента', 'Итог'],justify="left"))

			elif group not in allGroups and teacher in allTeachers:
				tryAgain(message,'Такой группы не существует')
				return
			elif teacher not in allTeachers and group in groups:
				tryAgain(message,'Преподаватель не найден')
				return
			elif 'СТУДЕНТЫ' in comm or 'ПРЕПОДАВАТЕЛИ' in comm or 'ГРУППЫ' in comm:
				pass 
			else:
				tryAgain(message,'Команда была введена неверно, повторите попытку. Для вывода всех команд введите команду "/help"')
				return
		getAllPointsOfTeacherAndGroup(teacher, group)

bot.polling(none_stop=True)