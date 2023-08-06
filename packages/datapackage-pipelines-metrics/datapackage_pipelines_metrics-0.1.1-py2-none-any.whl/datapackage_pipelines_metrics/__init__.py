from datapackage_pipelines.generators import GeneratorBase


def append_metrics(pipeline_details):
    pipeline_steps = pipeline_details.get("pipeline")
    pipeline_steps.append({"run": "metrics.send"})
    pipeline_details["pipeline"] = pipeline_steps
    return pipeline_details


class Generator(GeneratorBase):

    @classmethod
    def get_schema(cls):
        return {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object"
        }

    @classmethod
    def generate_pipeline(cls, source):
        for pipeline_id, pipeline_details in source.items():
            yield pipeline_id, append_metrics(pipeline_details)
