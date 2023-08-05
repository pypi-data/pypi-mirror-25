from zope.component.factory import Factory
from zope import interface
from . import interfaces as qry_ifaces

import logging
logger = logging.getLogger(__name__)

@interface.implementer(qry_ifaces.IORMRelatedModelsAdder)
class ORMRelatedModelsAdder(object):
    def __init__(self, models=None):
        self._models = {}
        if models:
            self.add_sequence(models)
    def add_sequence(self, sequence):
        for i, model in enumerate(sequence):
            if model not in self._models:
                self._models[model] = set()
            #add left-side
            if i:
                self._models[model].add(sequence[i-1])
            #add right-side
            if i < len(sequence)-1:
                self._models[model].add(sequence[i+1])
            
    def flattened(self, seed):
        q = [seed]
        flattened = []
        while q:
            model = q.pop(0)
            if model not in flattened:
                flattened.append(model)
            for r in [r for r in self._models[model] if r not in flattened]:
                q.append(r)
        return tuple(flattened)
ORMRelatedModelsAdderFactory = Factory(ORMRelatedModelsAdder)


@interface.implementer(qry_ifaces.ISAInstrumentedAttribute)
class SAInstrumentedAttributeFromDottedString(object):
    def __new__(self, Base, dotted_name):
        class_name, property_name = dotted_name.split('.')
        base_classes = Base._decl_class_registry
        if class_name not in base_classes:
            raise TypeError('unable to find {} type in SQLAlchemy base classes {}'.format(class_name, base_classes.keys()))
        class_ = base_classes[class_name]
        property_ = getattr(class_, property_name)
        interface.alsoProvides(property_, qry_ifaces.ISAInstrumentedAttribute)
        return getattr(class_, property_name)
SAInstrumentedAttributeFromDottedStringFactory = Factory(SAInstrumentedAttributeFromDottedString)
    

@interface.implementer(qry_ifaces.ISAQuery)
class SAOuterJoinQuery(object):
    def __new__(cls, session, models, select=None):
        """Return ISAQuery provider based on related models
        
        args:
            session: sparc.sa.orm.ISASession provider
            models: sequence of ISAModel providers ordered left->right in terms
                    of required SQL query dependency structure.
            select: sequence of models to return data for.  default is all 
                    entries in models
        """
        models = [m for m in models]
        if not select:
            select = models
        
        q = session.query(*select) # base query
        for m in models[1:]:
            q = q.outerjoin(m)
        logger.debug("ISAQuery provider inited with sequenced joins {}".format(models))
        return q
SAOuterJoinQueryFactory = Factory(SAOuterJoinQuery)

