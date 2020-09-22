""" Module with session and engine declarations """

import config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
