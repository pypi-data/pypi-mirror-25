from sparc.sa.engine import engine
from sparc.sa.orm.session import ThreadLocalSASessionTransaction
from sqlalchemy.pool import StaticPool

#Our declarative Base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def get_transaction():
    """Return ISAScopedTransaction provider for sqlite memory db with testing 
       schema initialized
    """
    #Memory sqlite engine that isn't thread-safe...but will work with threads
    #See http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#pysqlite-threading-pooling
    sa_engine = engine.SAEngineFromConfigFactory({'dsn': 'sqlite:///:memory:',
                        'kwargs': {'connect_args':{'check_same_thread':False},
                        'poolclass':StaticPool}})
    sa_engine.engine.execute('pragma foreign_keys=ON')
    transaction = ThreadLocalSASessionTransaction(sa_engine, Base)
    transaction.Base.metadata.create_all(bind=sa_engine)
    return transaction

def populate_tables(transaction):
    create_model(transaction, Test1, **{'name': 'test1_1'})
    create_model(transaction, Test1, **{'name': 'test1_2'})
    create_model(transaction, Test1, **{'name': 'test1_3'})
    
    create_model(transaction, Test2, **{'name': 'test2_1'})
    create_model(transaction, Test2, **{'name': 'test2_2'})
    create_model(transaction, Test2, **{'name': 'test2_3'})
    
    create_model(transaction, Test3, **{'test1_id': 1, #test1_1
                                      'test2_id': 1}) #test2_1
    create_model(transaction, Test3, **{'test1_id': 1, #test1_1
                                      'test2_id': 2}) #test2_2
    create_model(transaction, Test3, **{'test1_id': 2, #test1_2
                                      'test2_id': 2}) #test2_2
    
    create_model(transaction, Test4, **{'name': 'test4_1',
                                      'test2_id': 1}) #test2_1
    
    create_model(transaction, Test4, **{'name': 'test4_2',
                                      'test2_id': 3}) #test2_3

def create_model(transaction, class_, **attributes):
    session = transaction.session
    model = class_()
    for k in attributes:
        setattr(model, k, attributes[k])
    session.add(model)
    session.flush()
    return model

#A semi-complex db schema with relationships
import sqlalchemy
from zope import interface
class ITest1(interface.Interface):
    """Marker"""
@interface.implementer(ITest1)
class Test1(Base):
    __tablename__ = 'test1'
    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=False)

class ITest2(interface.Interface):
    """Marker"""
@interface.implementer(ITest2)
class Test2(Base):
    __tablename__ = 'test2'
    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=False)

class ITest3(interface.Interface):
    """Marker"""
@interface.implementer(ITest3)
class Test3(Base):
    __tablename__ = 'test3'
    __table_args__ = \
                    (sqlalchemy.PrimaryKeyConstraint(\
                            'test2_id','test1_id', 
                            name='test3_pk'),
                     )
    test1_id = \
                sqlalchemy.Column(sqlalchemy.String, 
                    sqlalchemy.ForeignKey(\
                                    Test1.__tablename__ + '.id'),
                    nullable=False)
                
    test2_id = sqlalchemy.Column(sqlalchemy.Integer, 
                    sqlalchemy.ForeignKey(Test2.__tablename__ + '.id'),
                    nullable=False)


class ITest4(interface.Interface):
    """Marker"""
@interface.implementer(ITest4)
class Test4(Base):
    __tablename__ = 'test4'
    __table_args__ = \
                    (sqlalchemy.UniqueConstraint(\
                            'name','test2_id', name='test4_name_un'),
                     )
    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    test2_id = sqlalchemy.Column(sqlalchemy.Integer, 
                    sqlalchemy.ForeignKey(Test2.__tablename__ + '.id'),
                    nullable=False)