from dataclasses import dataclass


@dataclass
class Pageviews:
    viewtime: int
    userid: str
    pageid: str
    test1: int


def generate_message(msg_index: int):
    return Pageviews(viewtime=msg_index, userid=f"User_{msg_index}", pageid=f"Page_{msg_index}", test1=msg_index)


def avro_schema():
    return """
        {
            "namespace": "confluent.io.examples.serialization.avro",
            "name": "pageviews",
            "type": "record",
            "fields": [
                {
                "name": "viewtime",
                "type": "long"
                },
                {
                "name": "userid",
                "type": "string"
                },
                {
                "name": "pageid",
                "type": "string"
                },
                {
                "name": "test1",
                "type": "long",
                "default": 0
                }
            ]
        }
    """


def json_schema():
    return """
        {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "pageviews",
            "description": "test",
            "type": "object",
            "properties": {
                "viewtime": {
                "description": "viewtime",
                "type": "string"
                },
                "userid": {
                "description": "userid",
                "type": "string",
                "exclusiveMinimum": 0
                },
                "pageid": {
                "description": "pageid",
                "type": "string"
                },
                "test1": {
                "description": "test1",
                "type": "number",
                "default": 0
                }
            },
            "required": [ "viewtime", "userid", "pageid" ]
        }
    """
