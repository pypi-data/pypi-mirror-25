from zope import interface

class ISADeclarativeMeta(interface.Interface):
    """Marker for sqlalchemy.ext.declarative.api.DeclarativeMeta"""
import sqlalchemy.ext.declarative.api
interface.classImplements(sqlalchemy.ext.declarative.api.DeclarativeMeta, ISADeclarativeMeta)