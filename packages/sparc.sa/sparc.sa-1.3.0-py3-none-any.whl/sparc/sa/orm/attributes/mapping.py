from zope import interface
from zope import component
from zope.interface.common.mapping import IIterableMapping
from .. import ISASession
from . import ISAInstrumentedAttribute

@interface.implementer(IIterableMapping)
@component.adapter(ISAInstrumentedAttribute, ISASession)
class ModelMappingForUniqueInstrumentedAttribute(object):
    """Read Mapping of sparc.sa.ext.ISADeclarativeMeta providers with 
       sparc.sa.attributes.ISAInstrumentedAttribute scalers as keys
    
    This effectively creates a map of a column value vs the matched row.
    """
    
    def __init__(self, attribute, session):
        self.attribute = attribute
        self.session = session
        
        self.attribute_model_type = attribute.class_
        self.attribute_name = attribute.property.key
        self.query = self.session.query(self.attribute_model_type)
    
    #IItemMapping
    def __getitem__(self, key):
        """Get a value for a key

        A KeyError is raised if there is no value for the key.
        """
        model = self.query.filter(self.attribute == key).one_or_none()
        if not model:
            raise KeyError(key)
        return model
    
    #IReadMapping
    def get(self, key, default=None):
        """Get a value for a key

        The default is returned if there is no value for the key.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        """Tell if a key exists in the mapping."""
        return True if self.query.filter(self.attribute == key).one_or_none() else False
    
    
    #IEnumerableMapping  
    def keys(self):
        """Return the keys of the mapping object.
        """
        return [key for key in self]

    def __iter__(self):
        """Return an iterator for the keys of the mapping object.
        """
        for model in self.query:
            yield getattr(model, self.attribute_name)

    def values(self):
        """Return the values of the mapping object.
        """
        return list(self.itervalues())

    def items(self):
        """Return the items of the mapping object.
        """
        return list(self.iteritems())

    def __len__(self):
        """Return the number of items.
        """
        return self.query.count()

    #IIterableMapping
    def iterkeys(self):
        "iterate over keys; equivalent to __iter__"
        return iter(self)

    def itervalues(self):
        "iterate over values"
        for model in self.query:
            yield model

    def iteritems(self):
        "iterate over items"
        for model in self.query:
            yield (getattr(model, self.attribute_name), model)
