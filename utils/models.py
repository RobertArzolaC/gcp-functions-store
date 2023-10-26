from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Local2(Base):
    __tablename__ = 'local2'
    id = Column(Integer, primary_key=True)
    holding = Column(String)
    codigo_local = Column(String)
    codigo_b2b = Column(String)
