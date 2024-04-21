ARRAY_TYPE = {'type': 'array'}
STRING_TYPE = {'type': 'string'}
INTEGER_TYPE = {'type': 'integer'}
NUMBER_TYPE = {'type': 'number'}
NULL_TYPE = {'type': 'null'}
BOOL_TYPE = {'type': 'boolean'}
OBJECT_TYPE = {
    'type': 'object',
    'additionalProperties': False,  # only permit props defined in this schema
    'properties': {},
    'required': ()
}


def one_of(*types):
    return {
        'oneOf': list(types)
    }


def list_of(item_type):
    return {
        **ARRAY_TYPE,
        **{'items': item_type}
    }


def object_type_factory(**properties):
    return {
        **OBJECT_TYPE,
        **{
            'properties': properties,
            'required': list(properties.keys())
        }
    }
