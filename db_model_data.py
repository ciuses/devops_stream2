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

if __name__ == '__main__':
    load_dotenv()
    DSN = os.getenv('data_source_name')
    data_base_name = 'db_num_3'
    create_base(dsn=DSN, b_name=data_base_name)
    DNS_2 = (f"postgresql://{os.getenv('db_user')}:{os.getenv('db_pass')}@"
             f"{os.getenv('db_h')}:{os.getenv('db_po')}/{data_base_name}")


    engine = alch.create_engine(DNS_2)
    Base.metadata.create_all(engine)

