from datapackage_pipelines.generators import GeneratorBase

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
            pipeline_steps = pipeline_details.get("pipeline")
            pipeline_steps.append({"run": "metrics.send"})
            pipeline_details["pipeline"] = pipeline_steps
            yield pipeline_id, pipeline_details
