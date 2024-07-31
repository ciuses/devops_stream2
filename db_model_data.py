import os
import sqlalchemy as alch
from sqlalchemy import String, Select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from dotenv import load_dotenv

load_dotenv()
DSN = os.getenv('data_source_name')
data_base_name = 'db_num_3'
DNS_2 = (f"postgresql://{os.getenv('db_user')}:{os.getenv('db_pass')}@"
         f"{os.getenv('db_h')}:{os.getenv('db_po')}/{data_base_name}")


def create_base(dsn: str = DSN, b_name='base_name') -> None:
    with alch.create_engine(dsn, isolation_level='AUTOCOMMIT').connect() as con:
        con.execute(alch.sql.text(f'CREATE DATABASE {b_name}'))


class Base(DeclarativeBase):
    pass


class Telephons(Base):
    __tablename__ = 't_numbers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self) -> str:
        return f'id={self.id}\nnumber={self.number}'


class Emails(Base):  # todo переписать email на address
    __tablename__ = 'emails'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(160), nullable=False)

    def __repr__(self) -> str:
        return f'id={self.id}\nemail={self.email}'


def create_tables(dsn: str = DNS_2) -> object:
    engine = alch.create_engine(dsn)
    Base.metadata.drop_all(engine)  # можно не дропать базки
    Base.metadata.create_all(engine)
    return Session(engine)


def fill_the_base(session) -> None:
    tel1 = Telephons(number='+79039533663')
    tel2 = Telephons(number='+79999999999')
    tel3 = Telephons(number='+70000000000')

    email1 = Emails(email='ddfbfdb@yandex.ru')
    email2 = Emails(email='dbfdbdfb@mail.ru')
    email3 = Emails(email='zzzzz@zzyyyyyyz.ru')

    my_data = [tel1, tel2, tel3, email1, email2, email3]

    # for dat in my_data:
    #     my_session.add(dat)

    session.add_all(my_data)
    session.commit()
    session.close()


def add_the_data(dsn: str = DNS_2) -> None:
    my_se = Session(alch.create_engine(dsn))
    any_tel = Telephons(number='+72112221111')
    my_se.add(any_tel)
    any_emeil = Emails(email='adadaa@gkgkkgkygkg.com')
    my_se.add(any_emeil)

    my_se.commit()
    my_se.close()


def add_telephons(dsn: str = DNS_2, my_num: str = '+79999999999') -> None:
    my_se = Session(alch.create_engine(dsn))
    any_tel = Telephons(number=my_num)
    my_se.add(any_tel)
    my_se.commit()
    my_se.close()

def add_emails(dsn: str = DNS_2, my_ema: str = 'zzz@zzz.com') -> None:
    my_se = Session(alch.create_engine(dsn))
    any_emeil = Emails(email=my_ema)
    my_se.add(any_emeil)
    my_se.commit()
    my_se.close()

def select_from_tables(dsn: str = DNS_2, many_data: tuple = None) -> list:
    list_of_rows = []
    with Session(alch.create_engine(dsn)) as sess:
        for rows in sess.execute(Select(*many_data)):
            list_of_rows.append(rows)

    return list_of_rows


if __name__ == '__main__':
    '''создать базку'''
    # create_base(dsn=DSN, b_name=data_base_name)
    '''создать таблички'''
    # ses = create_tables(dsn=DNS_2)
    '''налить данных'''
    # fill_the_base(ses)
    #
    # add_the_data(dsn=DNS_2)

    q_list_tel = Telephons.id, Telephons.number
    q_list_em = Emails.id, Emails.email

    tels = select_from_tables(dsn=DNS_2, many_data=q_list_tel)
    mails = select_from_tables(dsn=DNS_2, many_data=q_list_em)
    for r in tels:
        print(r)
    print(mails)
