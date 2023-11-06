from sqlalchemy import Column, Integer, String, DateTime
from dbsetting import Engine
from dbsetting import Base

class MusicInfo(Base): 
    __tablename__ = 'music_info'
    __table_args__ = {
        'comment': '楽曲情報のマスターテーブル'
    }

    id = Column('id', Integer, primary_key=True, nullable=False)
    artist_name = Column('artist_name', String(50), nullable=False)
    music_name = Column('music_name', String(100), nullable=False)
    length = Column('length', Integer, nullable=False)
    release = Column('release', Integer, nullable=False)
    url = Column('url', String(512))

class MusicFeature(Base):
    __tablename__ = "music_feature"
    __table_args__ = {
        'comment': '楽曲特徴のマスターテーブル'
    }

    id = Column('id', Integer, primary_key=True, nullable=False)
    rock = Column('rock', Integer)
    pop = Column('pop', Integer)
    painful = Column('painful', Integer)
    magnificent = Column('magnificent', Integer)
    sad = Column('sad', Integer)
    kyomu = Column('kyomu', Integer)

if __name__ == '__main__':
    Base.metadata.create_all(bind=Engine)