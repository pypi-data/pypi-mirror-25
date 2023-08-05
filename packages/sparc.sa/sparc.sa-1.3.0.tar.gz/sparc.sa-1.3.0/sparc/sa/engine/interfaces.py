from zope import interface

class ISAEngine(interface.Interface):
    """Marker for sqlalchemy.engine.Engine"""
import sqlalchemy.engine
interface.classImplements(sqlalchemy.engine.Engine, ISAEngine)