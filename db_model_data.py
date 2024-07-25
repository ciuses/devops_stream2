import os
import time

import sqlalchemy as alch
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from dotenv import load_dotenv


# my_eng = alch.create_engine(os.getenv('data_source_name'), isolation_level='AUTOCOMMIT')
# con = my_eng.connect()
# create_command = alch.sql.text('CREATE DATABASE db_num_2')
# con.execute(create_command)
# con.close()

def create_base(dsn='DSN', b_name='base_name'):
    with alch.create_engine(dsn, isolation_level='AUTOCOMMIT').connect() as con:
        con.execute(alch.sql.text(f'CREATE DATABASE {b_name}'))


Base = declarative_base()

class Telephons(Base):
    __tablename__ = 't_numbers'
    id = alch.Column(alch.Integer, primary_key=True)
    number = alch.Column(alch.VARCHAR(length=20), nullable=False)

    def __str__(self):
        return f'id={self.id}\nnumber={self.number}'


class Emails(Base):
    __tablename__ = 'emails'
    id = alch.Column(alch.Integer, primary_key=True)
    email = alch.Column(alch.String(length=160), nullable=False)

    def __str__(self):
        return f'id={self.id}\nemail={self.email}'

def create_tables(dsn='DSN'):
    engine = alch.create_engine(dsn)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

def fill_the_base(session):
    tel1 = Telephons(id=1, number='+79039533773')
    tel2 = Telephons(id=2, number='+79999999999')
    tel3 = Telephons(id=3, number='+7_000_000_0000')

    email1 = Emails(id=1, email='ciuse@yandex.ru')
    email2 = Emails(id=2, email='ciuse@mail.ru')
    email3 = Emails(id=3, email='zzzzz@zzz.ru')

    my_data = [tel1, tel2, tel3, email1, email2, email3]

    my_sesion = session()
    for dat in my_data:
        my_sesion.add(dat)

    my_sesion.commit()
    my_sesion.close()


if __name__ == '__main__':
    load_dotenv()
    data_base_name = 'db_num_3'
    DSN = os.getenv('data_source_name')
    DNS_2 = (f"postgresql://{os.getenv('db_user')}:{os.getenv('db_pass')}@"
             f"{os.getenv('db_h')}:{os.getenv('db_po')}/{data_base_name}")

    create_base(dsn=DSN, b_name=data_base_name)
    ses = create_tables(dsn=DNS_2)
    fill_the_base(ses)

