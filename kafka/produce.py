# A simple example demonstrating use of AvroSerializer.
# Heavily inspired by the confluent-kafka-python examples.

import argparse
from dataset import publish
from pagerviews_listener import set_pageviews_event_handler


set_pageviews_event_handler()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AvroSerializer example")
    parser.add_argument('-c', dest="classification", default="avro",
                        help="avro, json or transactional")
    parser.add_argument('-d', dest="dataset", default="pageviews",
                        help="Available datasets under kafka/lib/")
    parser.add_argument('-t', dest="topic", default="pageviews",
                        help="Topic name")
    parser.add_argument('-b', dest="bootstrap_servers", default="localhost:9092",
                        help="Bootstrap broker(s) (host[:port])")
    parser.add_argument('-s', dest="schema_registry", default="http://localhost:8081",
                        help="Schema Registry (http(s)://host[:port]")
    parser.add_argument('-n', dest="num_of_msgs", default=10),

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    publish(dataset=args.dataset, args=args)