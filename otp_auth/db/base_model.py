""" Module with a declarative base for SQLAlchemy ORM """

from sqlalchemy.ext.declarative import declarative_base, declared_attr


class CustomBase:
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):  # pylint: disable=no-self-argument
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)
