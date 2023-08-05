from zope import interface
from zope import component
from sqlalchemy import orm

from contextlib import contextmanager
from . import ISAScopedTransaction
from ..engine import ISAEngine
from ..ext import ISADeclarativeMeta

@interface.implementer(ISAScopedTransaction)
@component.adapter(ISAEngine, ISADeclarativeMeta)
class ThreadLocalSASessionTransaction(object):
    """Thread safe session transaction context manager implementation
    
    Args:
        engine: ISAEngine provider
        base: ISADeclarativeMeta provider
    """
    def __init__(self, engine, base):
        self._engine = engine
        self._Base = base
        
        self._session_factory = orm.sessionmaker(bind=self.engine)
        self._Session = orm.scoped_session(self._session_factory)
    
    @property
    def Base(self):
        return self._Base
    
    @property
    def engine(self):
        return self._engine
    
    @property
    def session(self):
        return self._Session() #thread-local session
    
    @contextmanager
    def __call__(self):
        try:
            yield self._Session
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self._Session.remove() #http://docs.sqlalchemy.org/en/latest/orm/contextual.html
