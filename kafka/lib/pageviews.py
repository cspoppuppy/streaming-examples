from dataclasses import dataclass


@dataclass
class Pageviews:
    viewtime: int
    userid: str
    pageid: str


def generate_message(msg_index: int):
    return Pageviews(viewtime=msg_index, userid=f"User_{msg_index}", pageid=f"Page_{msg_index}")


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
                "type": "number"
                },
                "userid": {
                "description": "userid",
                "type": "string",
                "exclusiveMinimum": 0
                },
                "pageid": {
                "description": "pageid",
                "type": "string"
                }
            },
            "required": [ "viewtime", "userid", "pageid" ]
        }
    """
