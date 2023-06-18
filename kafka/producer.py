import argparse
from dataclasses import asdict
from typing import Callable
from uuid import uuid4
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic


def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.
    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    Note:
        In the delivery report callback the Message.key() and Message.value()
        will be the binary format as encoded by any configured Serializers and
        not the same object that was passed to produce().
        If you wish to pass the original object(s) for key and value to delivery
        report callback we recommend a bound callback or lambda where you pass
        the objects along.
    """

    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


def get_producer_config(bootstrap_servers: str, classification: str):
    producer_config = {
        'avro': {
            "bootstrap.servers": bootstrap_servers,
        },
        'json': {
            "bootstrap.servers": bootstrap_servers,
        },
        'transactional': {
            "bootstrap.servers": bootstrap_servers,
            'transactional.id': "trans-id",
            'acks': 'all',
            'enable.idempotence': 'true',
            'max.in.flight.requests.per.connection': '1',
        }
    }
    return producer_config.get(classification, {})


def get_producer(bootstrap_servers: str, classification: str):
    producer_config = get_producer_config(bootstrap_servers=bootstrap_servers, classification=classification)
    return Producer(producer_config)


def create_topic_if_missing(producer_conf: dict, topic: str):
    admin = AdminClient(producer_conf)

    # create topic if not exist
    if admin.list_topics().topics.get(topic) is None:
        admin.create_topics([NewTopic(topic, num_partitions=3)])


def to_dict(pageviews, ctx):
    return asdict(pageviews)


def create_value_serializer(
        classfication: str, schema_registry: str, schema_str: str
):
    schema_registry_conf = {'url': schema_registry}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    value_serializer = JSONSerializer if classfication == "json" else AvroSerializer
    return value_serializer(
        schema_registry_client=schema_registry_client,
        schema_str=schema_str,
        to_dict=to_dict
    )


def produce_topic_data(
        producer: Producer, args: argparse.Namespace,
        schema_str: str, generate_message: Callable
):
    if args.classification == "transactional":
        producer.init_transactions()
        producer.begin_transaction()

    generate_data(
        producer=producer,
        args=args,
        schema_str=schema_str,
        generate_message=generate_message
    )

    if args.classification == "transactional":
        producer.commit_transaction()

    print("\nFlushing records...")
    producer.flush()


def generate_data(
    producer, args: argparse.Namespace, schema_str: str, generate_message: Callable
):
    key_serializer = StringSerializer('utf_8')
    value_serializer = create_value_serializer(
        classfication=args.classification,
        schema_registry=args.schema_registry,
        schema_str=schema_str
    )
    print(f"Producing records to topic {args.topic}. ^C to exit.")
    for i in range(int(args.num_of_msgs)):
        # Serve on_delivery callbacks from previous calls to produce()
        producer.poll(0.0)
        try:
            producer.produce(
                topic=args.topic,
                key=key_serializer(str(uuid4())),
                value=value_serializer(generate_message(i), SerializationContext(args.topic, MessageField.VALUE)),
                on_delivery=delivery_report
            )
        except KeyboardInterrupt:
            break
        except ValueError:
            print("Invalid input, discarding record...")
            continue


def produce_topic_data_to_confluent_kafka(
        args: argparse.Namespace, schema_str: str, generate_message: Callable
):
    producer = get_producer(bootstrap_servers=args.bootstrap_servers, classification=args.classification)

    if args.classification in ["avro", "json", "transactional"]:
        produce_topic_data(
            producer=producer,
            args=args, schema_str=schema_str,
            generate_message=generate_message
        )
    else:
        raise Exception(f"Unsupported classification {args.classification}")
