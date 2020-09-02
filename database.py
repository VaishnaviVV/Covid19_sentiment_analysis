from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
engine = create_engine('sqlite:///twitter.db', echo = True)
meta = MetaData()

discussion = Table(
   'discussion', meta,
   Column('id', String(64),index=True),
   Column('tweet', String(2000),index=True)
)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()


meta.create_all(engine)
# meta.drop_all(engine)
session.commit()
