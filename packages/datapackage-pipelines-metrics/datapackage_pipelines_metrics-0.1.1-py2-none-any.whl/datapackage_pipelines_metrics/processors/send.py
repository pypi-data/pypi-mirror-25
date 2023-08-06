from datapackage_pipelines.wrapper import ingest, spew
from datapackage_pipelines.utilities.resources import PROP_STREAMING
import logging, os
from datapackage_pipelines_metrics.influxdb import send_metric


DEFAULT_ROW_METRICS_BATCH_SIZE=int(os.environ.get("DPP_INFLUXDB_ROWS_BATCH_SIZE", "100"))


parameters, datapackage, resources = ingest()


def filter_resource(metric_tags, descriptor, data, batch_size):
    metric_tags = dict(metric_tags, resource_name=descriptor["name"])
    num_processed_rows = 0
    metrics_batch_count = 0
    for row in data:
        yield row
        num_processed_rows += 1
        metrics_batch_count += 1
        if metrics_batch_count >= batch_size:
            send_metric("processed_row", metric_tags, {"value": metrics_batch_count})
            metrics_batch_count = 0
    if metrics_batch_count > 0:
        send_metric("processed_row", metric_tags, {"value": metrics_batch_count})
    send_metric("processed_resource", metric_tags, {"rows": num_processed_rows})


def filter_resources(parameters, datapackage, resources):
    batch_size = parameters.get("row-batch-size", DEFAULT_ROW_METRICS_BATCH_SIZE)
    for resource_descriptor, resource_data in zip(datapackage["resources"], resources):
        metric_tags = parameters["tags"] if "tags" in parameters else {}
        metric_tags["datapackage_name"] = datapackage["name"]
        yield filter_resource(metric_tags, resource_descriptor, resource_data, batch_size)



spew(datapackage, filter_resources(parameters, datapackage, resources))
