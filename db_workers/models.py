from sqlalchemy import Column, String, Integer, create_engine, Date, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, relationship

import os

db_url = f"sqlite:///{os.getcwd() + ('/' if os.name == 'posix' else r'\\') + 'data_base.db'}"
engine = create_engine(db_url)


class Base(DeclarativeBase):
    pass


class CurrencyInfo(Base):
    __tablename__ = 'currency_info'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    num_code = Column(String, nullable=False)
    char_code = Column(String, nullable=False)
    # пока что мы думаем как поступить с номиналом


class DateStatus(Base):
    __tablename__ = 'date_status'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    status = Column(Integer, nullable=False)


class PriceInfo(Base):
    __tablename__ = 'price_info'

    id = Column(Integer, primary_key=True)
    date_id = Column(Integer, ForeignKey('date_status.id'))
    BYN = Column(Float, nullable=True, default=None)
    HKD = Column(Float, nullable=True, default=None)
    AED = Column(Float, nullable=True, default=None)
    USD = Column(Float, nullable=True, default=None)
    EUR = Column(Float, nullable=True, default=None)
    IDR = Column(Float, nullable=True, default=None)
    KZT = Column(Float, nullable=True, default=None)
    THB = Column(Float, nullable=True, default=None)
    UZS = Column(Float, nullable=True, default=None)
    JPY = Column(Float, nullable=True, default=None)
    CNY = Column(Float, nullable=True, default=None)


Base.metadata.create_all(engine)
session = Session(engine)




#
#
# class Book(Base):
#     __tablename__ = 'Books_2'
#
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     author = Column(String)
#
#     def __repr__(self):
#         return f'"Книга от {self.author} с названием {self.title}"'
#
#
# Base.metadata.create_all(engine)
# session = Session(engine)


# a = Book(title='Капитанская дочка', author='Пушкин А.С.')
# b = Book(title='Анна Каренина', author='Толстой Л.Н.')
#
# session.add(b)
# session.commit()

# result_query = session.query(Book)
# for i in result_query:
#     print(i.id, i.title, i.author)

# SELECT * FROM Books_2 WHERE author = ''

