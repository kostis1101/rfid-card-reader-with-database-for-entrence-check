import pickle
import os
import os.path

os.chdir('C:\\Users\\ΙΤ\\Desktop\\Kostis-Computer\\pythonProjects\\munDataBase')

file_name = 'main_db.pickle'
students = {0: True, 1: False, 2: False, 3: True}

def create_db(_file_name, _students):
	print('creating database...')
	if not os.path.isfile(_file_name):
		with open(_file_name, 'wb') as f:
			pickle.dump(_students, f)
	else:
		print('database already exists!')

def load_db(_file_name):
	print('loading database...')
	if os.path.isfile(_file_name):
		with open(_file_name, 'rb') as f:
			print('database successfully loaded!')
			return pickle.load(f)
	else:
		print('No file found with the name {}'.format(_file_name))

def check(student_number, _students, _file_name):
	try:
		if not _students[student_number]:
			_students[student_number] = True
			update_db(_file_name, _students)
			return False
		else:
			return True
	except KeyError as ke:
		print('not valid number')
		return -1

def open_from_file(_file, _encoding='utf-8'):
	if os.path.isfile(_file):
		with open(_file, 'r', encoding=_encoding) as f:
			_students = {}
			for line in f:
				if line.strip().isdigit():
					_students[int(line)] = False
			return _students

def update_db(_file_name, _students):
	with open(_file_name, 'wb') as f:
		pickle.dump(_students, f)

def reset_db(_file_name):
	_students = load_db(_file_name)
	for num in _students:
		_students[num] = False
	update_db(_file_name, _students)
	print('resetting database...')