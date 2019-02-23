from sqlalchemy import Column, String, Integer, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import mapper, sessionmaker, clear_mappers


Base = declarative_base()
engine = create_engine(r'sqlite:///C:\Users\BadWolf\Desktop\news\db.sqlite3')
session = scoped_session(sessionmaker(bind=engine))


class News(Base):
    __tablename__ = "polls_newsmodel"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

Base.metadata.create_all(bind=engine)

def save(news_list):
    s = session()
    for new in news_list:
        news = News(title=new[0],
                    author=new[1],
                    url=new[2],
                    comments=new[3],
                    points=new[4])

        s.add(news)
        s.commit()
        print(news.id, news.title)
