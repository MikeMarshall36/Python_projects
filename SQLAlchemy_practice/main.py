import sqlite3
from sqlite3 import Error
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Sequence

Base = declarative_base()
engine = create_engine("sqlite:///first.db", echo=False)
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    f_name = Column(String)
    s_name = Column(String)
    nickname = Column(String(50))

    def __repr__(self):
        return f"<User(first name = {self.f_name}, second name = {self.s_name}, nickname = {self.nickname})>"


class File(Base):
    __tablename__ = 'files'
    file_id = Column(Integer, Sequence("file_id_seq"), primary_key=True)
    file_name = Column(String(75))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<File(file id = {self.file_id}, name = {self.file_name}, belongs to user with id = {self.user_id})>"


Base.metadata.create_all(engine)

user_1 = User(f_name="Alex", s_name="Klimov", nickname="VasyaUshankin")
user_2 = User(f_name="Alex", s_name="Kulibin", nickname="OrelGreet")

file_1 = File(file_name="SQL_for_beginners.pdf", user_id="3")
file_2 = File(file_name="logistics.docx", user_id="1")


print(user_1.nickname, user_1.id)
session = Session()
session.add(user_1)
session.add(user_2)
session.add(file_2)
session.add(file_1)

our_user = (session.query(User).filter_by(f_name="Alex").first())

print(user_1 is our_user)

session.add_all([
    User(f_name="Tiler", s_name="Wendy", nickname="TeamWendy"),
    User(f_name="Nikita", s_name="Kolankov", nickname="AgDeSs"),
    User(f_name="Alex", s_name="Nikishin", nickname="RickFlag"),
    User(f_name="Konstantin", s_name="Shalimov", nickname="SimpleGM"),
])

session.commit()

Database = sqlite3.connect('first.db')

cur = Database.cursor()

users = (cur.execute("SELECT * FROM users GROUP BY f_name ").fetchall())
for user in users:
    print(user)

print(cur.execute("SELECT * FROM files GROUP BY user_id").fetchall())
