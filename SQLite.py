import sqlite3
from sqlite3 import Error

DataBase = sqlite3.connect('Student.db')

cur = DataBase.cursor()

create_student = """
CREATE TABLE IF NOT EXISTS student (
student_id integer PRIMARY KEY,
surname text NOT NULL,
name text NOT NULL,
stipend integer,
kurs integer,
city text not null,
birthday data,
univ_id integer not null,
foreign key (univ_id) references university (univ_id) );
"""

create_lecturer = """
create table if not exists lecturer (
lecturer_id int primary_key,
surname text not null,
name text not null,
city text not null,
univ_id integer,
foreign key (univ_id) references university (univ_id)
); """

create_subject = """
CREATE TABLE IF NOT EXISTS subject (
subj_id integer PRIMARY KEY,
SUBJ_NAME text NOT NULL,
HOUR integer NOT NULL,
SEMESTER integer NOT NULL
); """

create_university = """
CREATE TABLE IF NOT EXISTS university (
univ_id integer PRIMARY KEY,
UNIV_NAME text NOT NULL,
RATING integer NOT NULL,
CITY text NOT NULL
); """

create_exam_marks = """
CREATE TABLE IF NOT EXISTS exam_marks (
exam_id integer PRIMARY KEY,
student_id integer NOT NULL,
subj_id integer,
mark integer,
exam_date date,
foreign key (student_id) references student (student_id),
foreign key (subj_id) references subject (subj_id)
); """

create_subj_lect = """
CREATE TABLE IF NOT EXISTS subj_lect (
lecturer_id int,
subj_id int,
primary key (lecturer_id, subj_id),
foreign key (subj_id) references subject (subj_id),
foreign key (lecturer_id) references lecturer (lecturer_id)
);"""

tables = [create_student, create_lecturer, create_subject, create_university, create_exam_marks, create_subj_lect]

for i in range(len(tables)):
    DataBase.execute(tables[i])

table_names = ['student', 'lecturer', 'subject', 'university', 'exam_marks', 'subj_lect']


def insert_data(table_name, data):
    if table_name == 'student':
        insert = f'''
        INSERT INTO {table_name} (student_id, surname, name, stipend, kurs, city, birthday, univ_id)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?);
            '''
        DataBase.execute(insert, data)

    elif table_name == 'exam_marks':
        insert = f'''
        INSERT INTO {table_name} (exam_id, student_id, subj_id, mark, exam_date)
            VALUES(?, ?, ?, ?, ?)
            '''
        DataBase.execute(insert, data)

    elif table_name == 'lecturer':
        insert = f'''
        INSERT INTO {table_name} (lecturer_id, surname, name, city, univ_id)
        VALUES(?, ?, ?, ?, ?);
        '''
        DataBase.execute(insert, data)

    elif table_name == 'subject':
        insert = f'''
        INSERT INTO {table_name} (subj_id, SUBJ_NAME, HOUR, SEMESTER)
        VALUES(?, ?, ?, ?);
        '''
        DataBase.execute(insert, data)

    elif table_name == 'university':
        insert = f'''
        INSERT INTO {table_name} (univ_id, UNIV_NAME, RATING, CITY)
        VALUES(?, ?, ?, ?);
        '''
        DataBase.execute(insert, data)

    elif table_name == 'subj_lect':
        insert = f'''
        INSERT INTO {table_name} (lecturer_id, subj_id)
        VALUES(?, ?);
        '''
        DataBase.execute(insert, data)

def data_input(table_name, data_set):
    for i in range(len(data_set)):
        insert_data(table_name, data_set[i])

students = [(1, "Иванов", "Иван", 150, 1, "Орел", "3/12/1988", 10),
            (3, "Петров", "Петр", 200, 3, "Курск", "11/12/1986", 10),
            (6, "Сидоров", "Вадим", 150, 1, "Москва", "7/06/1985", 22),
            (10, "Кузнецов", "Борис", 0, 2, "Брянск", "8/12/1987", 10),
            (12, "Иванов", "Иван", 250, 1, "Орел", "3/12/1988", 10),
            (265, "Павлов", "Андрей", 0, 3, "Воронеж", "5/11/1985", 10),
            (32,"Котов", "Павел", 150, 5, "Белгород", "NULL", 14),
            (654, "Лукин", "Артем", 200, 3, "Воронеж", "11/12/1987", 10),
            (276, "Петров", "Антон", 200, 4, "NULL", "5/08/1987", 22),
            (55, "Белкин", "Вадим", 250, 5, "Воронеж", "20/01/1986", 10)]

speakers = [(24, 'Колесников', 'Борис', 'Воронеж', 10),
            (46, 'Никонов', 'Иван', 'Воронеж', 10),
            (74, 'Лагутин', 'Павел', 'Москва', 22),
            (108, 'Струков', 'Николай', 'Москва', 22),
            (276, 'Николаев', 'Виктор', 'Воронеж', 10),
            (328, 'Сорокин', 'Андрей', 'Орел', 10)]

subjects = [(10, 'Информатика', 56, 1),
            (22, 'Физика', 34, 1),
            (43, 'Математика', 56, 2),
            (56, 'История', 34, 4),
            (94, 'Английский', 56, 3),
            (73, 'Физкультура', 34, 5)]

universities =[(22, 'МГУ', 610, 'Москва'),
               (10, 'ВГУ', 296, 'Воронеж'),
               (11, 'НГУ', 345, 'Новосибирск'),
               (32, 'РГУ', 421, 'Ростов'),
               (14, 'БГУ', 326, 'Белгород'),
               (15, 'ТГУ', 373, 'Томск'),
               (18, 'ВГМА', 327, 'Воронеж')]

exam_marks = [(145, 12, 10, 5, '12/01/2006'),
              (34, 32, 10, 4, '23/01/2006'),
              (75, 55, 10, 5, '05/01/2006'),
              (238, 12, 22, 3, '17/06/2005'),
              (639, 55, 22, 'NULL', '22/06/2005'),
              (43, 6, 22, 4, '18/01/2006')]

subject_speakers = [(24, 24),
                    (46, 46),
                    (74, 74),
                    (108, 108),
                    (276, 276),
                    (328, 328)]

data_sets = [students, speakers, subjects, universities, exam_marks, subject_speakers]

for i in range(len(table_names)):
    data_input(table_names[i], data_sets[i])


for value in DataBase.execute("SELECT * FROM student WHERE BIRTHDAY < 2002"):
    print(value)

print(cur.execute("SELECT SEMESTER, SUM(HOUR) FROM SUBJECT GROUP BY SEMESTER").fetchall())

print(cur.execute("SELECT count(name), exam_date FROM student, exam_marks").fetchall()) #22
print(cur.execute("SELECT exam_date, sum(exam_id) FROM exam_marks GROUP BY exam_date").fetchall())#23
print(cur.execute("SELECT name||' '||surname, subj_id FROM lecturer, subj_lect").fetchall())#24
print(cur.execute("SELECT DISTINCT student.student_id, name||' '||surname, mark FROM student, exam_marks WHERE mark == 5 ORDER BY student.student_id").fetchall())#25
#ver 2 ("SELECT STUDENT_ID FROM exam_marks GROUP BY STUDENT_ID HAVING MIN(MARK) = 5")