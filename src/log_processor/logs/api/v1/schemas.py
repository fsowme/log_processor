from log_processor.tools.tests.schemas import INTEGER_TYPE, NULL_TYPE, STRING_TYPE, list_of, object_type_factory, one_of

NGINX_LOG_SCHEMA = object_type_factory(
    id=INTEGER_TYPE,
    time=STRING_TYPE,
    remote_ip=STRING_TYPE,
    method=STRING_TYPE,
    uri=STRING_TYPE,
    response_status_code=INTEGER_TYPE,
    response_size=INTEGER_TYPE
)

NGINX_LOG_SCHEMA_LIST = object_type_factory(
    count=INTEGER_TYPE,
    next=one_of(STRING_TYPE, NULL_TYPE),
    previous=one_of(STRING_TYPE, NULL_TYPE),
    results=list_of(NGINX_LOG_SCHEMA)
)
