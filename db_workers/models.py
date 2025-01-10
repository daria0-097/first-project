import json

from sqlalchemy import Column, String, Integer, create_engine, Date, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, relationship, sessionmaker

import os
from datetime import date


def get_project_root() -> str:
    current_path = os.path.abspath(__file__)
    while not os.path.exists(os.path.join(current_path, 'README.md')):
        current_path = os.path.dirname(current_path)

    return current_path


db_url = f"sqlite:///{get_project_root()}/db_workers/data_base.db"
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


# a = CurrencyInfo(name=..., num_code=..., char_code=...)


class DateStatus(Base):
    __tablename__ = 'date_status'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    status = Column(Integer, nullable=False)        # 1 - успех / 0 - не успех

    def __repr__(self):
        return f'{self.id}) {self.date} | {self.status}'


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


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
# session = Session(engine)
Session_obj = sessionmaker(engine)

# with open('../result_file_without_spaces.json', 'r', encoding='utf-8') as file:
#     all_data = json.load(file)
#
# first_dict = all_data[0]
# for key, value in first_dict['result']['Valute'].items():
#     if key in ['BYN', 'HKD', 'AED', 'USD', 'EUR', 'IDR', 'KZT', 'THB', 'UZS', 'JPY', 'CNY']:
#         session.add(
#             CurrencyInfo(
#                 name=value['Name'],
#                 num_code=value['NumCode'],
#                 char_code=value['CharCode'],
#             )
#         )
# session.commit()


def save_data_from_downtime(all_days: list) -> None:
    with Session_obj() as curr_session:
        for element in all_days[::-1]:
            lst = element['url'].split('/')
            year, month, day = lst[4], lst[5], lst[6]

            curr_date = date(int(year), int(month), int(day))
            if element['status_code'] != 200:
                status_code = 0
            else:
                status_code = 1

            obj = DateStatus(
                date=curr_date,
                status=status_code
            )
            curr_session.add(obj)
            curr_session.commit()

            if status_code:
                BYN = element['result']['Valute']['BYN']['Value'] / element['result']['Valute']['BYN']['Nominal'] if 'BYN' in element['result']['Valute'] else None
                HKD = element['result']['Valute']['HKD']['Value'] / element['result']['Valute']['HKD']['Nominal'] if 'HKD' in element['result']['Valute'] else None
                AED = element['result']['Valute']['AED']['Value'] / element['result']['Valute']['AED']['Nominal'] if 'AED' in element['result']['Valute'] else None
                USD = element['result']['Valute']['USD']['Value'] / element['result']['Valute']['USD']['Nominal'] if 'USD' in element['result']['Valute'] else None
                EUR = element['result']['Valute']['EUR']['Value'] / element['result']['Valute']['EUR']['Nominal'] if 'EUR' in element['result']['Valute'] else None
                IDR = element['result']['Valute']['IDR']['Value'] / element['result']['Valute']['IDR']['Nominal'] if 'IDR' in element['result']['Valute'] else None
                KZT = element['result']['Valute']['KZT']['Value'] / element['result']['Valute']['KZT']['Nominal'] if 'KZT' in element['result']['Valute'] else None
                THB = element['result']['Valute']['THB']['Value'] / element['result']['Valute']['THB']['Nominal'] if 'THB' in element['result']['Valute'] else None
                UZS = element['result']['Valute']['UZS']['Value'] / element['result']['Valute']['UZS']['Nominal'] if 'UZS' in element['result']['Valute'] else None
                JPY = element['result']['Valute']['JPY']['Value'] / element['result']['Valute']['JPY']['Nominal'] if 'JPY' in element['result']['Valute'] else None
                CNY = element['result']['Valute']['CNY']['Value'] / element['result']['Valute']['CNY']['Nominal'] if 'CNY' in element['result']['Valute'] else None

                obj_2 = PriceInfo(
                    date_id=obj.id,
                    BYN=BYN,
                    HKD=HKD,
                    AED=AED,
                    USD=USD,
                    EUR=EUR,
                    IDR=IDR,
                    KZT=KZT,
                    THB=THB,
                    UZS=UZS,
                    JPY=JPY,
                    CNY=CNY,
                )
                curr_session.add(obj_2)

            curr_session.commit()


# print(bool(0))
# print(bool(1))
# print(bool(-1))
# print(bool(1_000))
#
#
# while 1:
#     print(...)

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


















