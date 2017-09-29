from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Enum
import enum

dbbase  = declarative_base()

class Market(dbbase):
    __tablename__ = 'Market'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    marketopen = Column(DateTime, nullable=False)
    auctionclose = Column(DateTime)
    def __repr__(self):
        return self.name

class User(dbbase):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    marketid=Column(Integer,ForeignKey('Market.id'), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    passwordhash = Column(String(100), nullable=False)
    passwordsalt = Column(String(100), nullable=False)
    def __repr__(self):
        return self.name

class Team(dbbase):
    __tablename__ = 'Team'

    id = Column(Integer, primary_key=True)
    marketid=Column(Integer,ForeignKey('Market.id'), nullable=False)
    name = Column(String(100), nullable=False)
    numberofshares=Column(Integer,nullable=False) 
    auctionprice=Column(Numeric(8, 2))
    auctionuserid=Column(Integer,ForeignKey('User.id'))
    lasttradedprice=Column(Numeric(8, 2))
    bestbidprice=Column(Numeric(8, 2))
    bestofferprice=Column(Numeric(8, 2))
    
    def __repr__(self):
        return self.name

class DealType(enum.Enum):
    bid='B'
    offer='O'

class DealStatus(enum.Enum):
    open=1
    accepted=2
    cancelled=3

class Deal(dbbase):
    __tablename__ = 'Deal'

    id = Column(Integer, primary_key=True)
    teamid=Column(Integer,ForeignKey('Team.id'), nullable=False)
    type=Column(Enum(DealType), nullable=False)
    status=Column(Enum(DealStatus), nullable=False)
    price=Column(Numeric(8, 2), nullable=False)
    createuserid=Column(Integer,ForeignKey('User.id'), nullable=False)
    createdate=Column(DateTime, nullable=False)
    acceptuserid=Column(Integer,ForeignKey('User.id'))
    acceptdate=Column(DateTime)
    
    def __repr__(self):
        return self.name


# #  create tables
# from sqlalchemy import create_engine
# dbengine = create_engine('mysql+mysqlconnector://admin:ronaldo7@teamtrader.csywb8hubjmd.eu-west-2.rds.amazonaws.com/teamtrader', echo=True)
# dbbase.metadata.drop_all(dbengine)
# dbbase.metadata.create_all(dbengine)
