from zope import interface

class ISAMapper(interface.Interface):
    """SQLAlchemy ORM mapper"""
from sqlalchemy.orm import mapper
interface.classImplements(mapper.Mapper, ISAMapper)
