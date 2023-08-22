from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config


engine = create_engine(Config().SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
