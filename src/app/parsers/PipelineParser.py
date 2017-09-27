from src.app.models.Pipeline import Pipeline
from src.app.models.Job import Job


class PipelineParser:


    def extract_pipeline_name(self, full_pipeline_name):
        splitted_build_locator = full_pipeline_name.split('/')
        pipeline_name = splitted_build_locator[0]
        return pipeline_name

    def get_scheduled_pipelines_from_job_xml(self, jobs_xml):
        scheduled_pipelines = []

        for job_xml in jobs_xml:
            full_pipeline_name = job_xml.find('buildLocator').string
            pipeline_name = self.extract_pipeline_name(full_pipeline_name)
            job_name = job_xml['name']

            pipeline = Pipeline(pipeline_name)

            job = Job(job_name)
            job.add_resources_from_xml(job_xml)

            if pipeline in scheduled_pipelines:
                index = scheduled_pipelines.index(pipeline)
                pipeline = scheduled_pipelines[index]
            else:
                scheduled_pipelines.append(pipeline)

            pipeline.add_job(job)

        return scheduled_pipelines
