import argparse
from dataset import subscribe
from lib.pageviews1 import avro_schema, json_schema, generate_message
from producer import produce_topic_data_to_confluent_kafka


def get_schema_str(classification):
    return json_schema() if classification == "json" else avro_schema()


def handle_pageviews_dataset(args: argparse.Namespace):
    schema_str = get_schema_str(classification=args.classification)
    produce_topic_data_to_confluent_kafka(
        args=args, schema_str=schema_str, generate_message=generate_message
    )


def set_pageviews_event_handler():
    subscribe(dataset="pageviews1", fn=handle_pageviews_dataset)
