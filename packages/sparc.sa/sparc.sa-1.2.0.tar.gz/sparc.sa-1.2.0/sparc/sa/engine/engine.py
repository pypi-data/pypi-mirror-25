from zope import interface
from zope.component.factory import Factory

import sqlalchemy
from . import ISAEngine

@interface.implementer(ISAEngine)
class SAEngineFromConfig(object):
    def __new__(cls, SQLAlchemyEngine):
        """Return a ISAEngine provider
        
        Kwargs:
            see SQLAlchemyEngine def in configure.yaml
        """
        return sqlalchemy.create_engine(SQLAlchemyEngine.get('dsn', ''), **SQLAlchemyEngine.get('kwargs', {}))
SAEngineFromConfigFactory = Factory(SAEngineFromConfig)