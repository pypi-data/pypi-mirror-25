#!/usr/bin/env python3
"""
Provides a `bind` function to plugins so they can simply bind a function to a queue.
"""

import logging
from json import loads, dumps, decoder
from os import environ
from os.path import join
import urllib
import time

import pika
from minio import Minio
from minio.error import AccessDenied


def bind(function: callable, name: str, version="1.0.0"):
    """binds a function to the input message queue"""

    parameters = pika.ConnectionParameters(
        host=environ["AMQP_HOST"],
        port=int(environ["AMQP_PORT"]),
        credentials=pika.PlainCredentials(environ["AMQP_USER"], environ["AMQP_PASS"]))

    connection = pika.BlockingConnection(parameters)
    input_channel = connection.channel()
    output_channel = connection.channel()

    minio_client = Minio(
        environ["MINIO_HOST"] + ":" + environ["MINIO_PORT"],
        access_key=environ["MINIO_ACCESS"],
        secret_key=environ["MINIO_SECRET"],
        secure=True if environ["MINIO_SCHEME"] == "https" else False)
    minio_client.set_app_info(name, version)

    minio_client.list_buckets()

    monitor_url = environ["MONITOR_URL"]

    logging.info("initialised sld lib")

    def send(chan, method, properties, body: str):
        """unwraps a message and calls the user function"""

        logging.debug("consumed message", extra={
            "chan": chan,
            "method": method,
            "properties": properties})

        raw = body.decode("utf-8")

        try:
            payload = loads(raw)
        except decoder.JSONDecodeError as exp:
            logging.error(exp)
            input_channel.basic_reject(method.delivery_tag, True)
            return

        if not validate_payload(payload, name):
            input_channel.basic_reject(method.delivery_tag, True)
            return

        next_plugin = get_next_plugin(name, payload["nmo"]["job"]["workflow"])
        if next_plugin is None:
            logging.debug("this is the final plugin", extra={
                "job_id": payload["nmo"]["job"]["job_id"],
                "task_id": payload["nmo"]["task"]["task_id"]})

        path = join(
            payload["nmo"]["task"]["task_id"],
            "input",
            "source",
            payload["nmo"]["source"]["name"])

        if not minio_client.bucket_exists(payload["nmo"]["job"]["job_id"]):
            logging.error("job_id does not have a bucket", extra={
                "job_id": payload["nmo"]["job"]["job_id"],
                "task_id": payload["nmo"]["task"]["task_id"]})
            input_channel.basic_reject(method.delivery_tag, True)
            return

        try:
            url = minio_client.presigned_get_object(payload["nmo"]["job"]["job_id"], path)

        except AccessDenied as exp:
            logging.error(exp, extra={
                "job_id": payload["nmo"]["job"]["job_id"],
                "task_id": payload["nmo"]["task"]["task_id"]})
            input_channel.basic_reject(method.delivery_tag, True)
            return

        # calls the user function to mutate the JSON-LD data

        try:
            result = function(payload["nmo"], payload["jsonld"], url)
        except Exception as exp:
            logging.error(exp)
            return

        if result is None:
            input_channel.basic_reject(method.delivery_tag, True)
            logging.error("return value is None")
            return

        if not isinstance(result, dict):
            input_channel.basic_reject(method.delivery_tag, True)
            logging.error("return value must be of type dict, not %s", type(result))
            return

        if "jsonld" in result:
            result = result["jsonld"]
        else:
            result = result

        payload["jsonld"] = result

        logging.debug("finished running user code", extra={
            "job_id": payload["nmo"]["job"]["job_id"],
            "task_id": payload["nmo"]["task"]["task_id"]})

        try:
            urllib.request.Request(
                join(monitor_url, "/v1/task/status/",
                     payload["nmo"]["job"]["job_id"], payload["nmo"]["task"]["task_id"]),
                data=dumps({
                    "t": "",
                    "p": int(time.time())
                }).encode(),
                headers={"Content-Type: application/json"})
        except Exception as exp:
            logging.error(exp)

        input_channel.basic_ack(method.delivery_tag)

        if next_plugin:
            output_channel.queue_declare(
                next_plugin,
                False,
                True,
                False,
                False,
            )
            output_channel.basic_publish(
                "",
                next_plugin,
                dumps(payload)
            )

    logging.debug("consuming from", extra={"queue": name})

    try:
        while True:
            input_channel.queue_declare(name, False, True)
            method_frame, header_frame, body = input_channel.basic_get(name)
            if (method_frame, header_frame, body) == (None, None, None):
                continue  # queue empty

            if body is None:
                logging.error("body received was empty")
                continue  # body empty

            send(input_channel, method_frame, header_frame, body)

    except pika.exceptions.RecursionError as exp:
        input_channel.stop_consuming()
        connection.close()
        raise exp


def validate_payload(payload: dict, name: str) -> bool:
    """ensures payload includes the required metadata and this plugin is in there"""

    if "nmo" not in payload:
        logging.error("no job in nmo")
        return False

    if "job" not in payload["nmo"]:
        logging.error("no job in nmo")
        return False

    if "task" not in payload["nmo"]:
        logging.error("no task in nmo")
        return False

    if not ensure_this_plugin(name, payload["nmo"]["job"]["workflow"]):
        logging.error("declared plugin name does not match workflow", extra={
            "job_id": payload["nmo"]["job"]["job_id"],
            "task_id": payload["nmo"]["task"]["task_id"]})
        return False

    return True


def ensure_this_plugin(this_plugin: str, workflow: list)->bool:
    """ensures the current plugin is present in the workflow"""
    for workpipe in workflow:
        if workpipe["config"]["name"] == this_plugin:
            return True
    return False


def get_next_plugin(this_plugin: str, workflow: list) -> str:
    """returns the next plugin in the sequence"""
    found = False
    for workpipe in workflow:
        if not found:
            if workpipe["config"]["name"] == this_plugin:
                found = True
        else:
            return workpipe["config"]["name"]

    return None
