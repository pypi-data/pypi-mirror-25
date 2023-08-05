from zope import interface

class ISAInstrumentedAttribute(interface.Interface):
    """SQLAlchemy ORM model attribute"""
from sqlalchemy.orm import attributes
interface.classImplements(attributes.InstrumentedAttribute, ISAInstrumentedAttribute)
