from zope import interface

class ISAMapper(interface.Interface):
    """SQLAlchemy ORM mapper"""
from sqlalchemy.orm.mapper import Mapper
interface.classImplements(Mapper, ISAMapper)
