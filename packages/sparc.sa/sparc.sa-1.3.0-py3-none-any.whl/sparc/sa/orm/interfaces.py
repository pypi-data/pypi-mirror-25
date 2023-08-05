from zope import interface

class ISASession(interface.Interface):
    """Marker for sqlalchemy.orm.session.Session"""
import sqlalchemy.orm.session
interface.classImplements(sqlalchemy.orm.session.Session, ISASession)

class ISAScopedSession(interface.Interface):
    """Marker for sqlalchemy.orm.scoping.scoped_session"""
import sqlalchemy.orm.scoping
interface.classImplements(sqlalchemy.orm.scoping.scoped_session, ISAScopedSession)

class ISAScopedTransaction(interface.Interface):
    """SQLAlchemy context manager for sessions"""
    Base = interface.Attribute("ISADeclarativeMeta provider")
    engine = interface.Attribute("ISAEngine provider")
    session = interface.Attribute("ISASession provider")
    
    def __call__():
        """Return a Python context manager whose __enter__() returns a 
        ISAScopedSession provider and whose __exit__() will commit/abort the
        current session transaction"""
    