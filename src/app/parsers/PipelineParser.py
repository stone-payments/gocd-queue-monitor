from src.app.utils.EnvironmentVariables import EnvironmentVariables
from src.app.parsers.JobParser import JobParser
from src.app.models.Pipeline import Pipeline
from src.app.models.Job import Job


class PipelineParser:

    def extract_pipeline_link(self, pipeline_name):
        env_vars = EnvironmentVariables()
        web_url = env_vars.GOCD_API_URL.replace('-vip','')
        link = web_url + '/admin/pipelines/'+ pipeline_name + '/edit'
        return link

    def extract_pipeline_name(self, full_pipeline_name):
        splitted_build_locator = full_pipeline_name.split('/')
        pipeline_name = splitted_build_locator[0]
        return pipeline_name

    def get_scheduled_pipelines_from_job_xml(self, jobs_xml):
        scheduled_pipelines = []
        job_parser = JobParser()

        for job_xml in jobs_xml:
            full_pipeline_name = job_xml.find('buildLocator').string
            pipeline_name = self.extract_pipeline_name(full_pipeline_name)

            job_name = job_parser.get_name_from_xml(job_xml)
            job = Job(job_name)
            job_resources = job_parser.get_resources_from_xml(job_xml)
            job_environment = job_parser.get_environment_from_xml(job_xml)
            job.set_resources(job_resources)
            job.set_environment(job_environment)

            pipeline = Pipeline(pipeline_name)
            pipeline.link = self.extract_pipeline_link(pipeline_name)
            if pipeline in scheduled_pipelines:
                index = scheduled_pipelines.index(pipeline)
                pipeline = scheduled_pipelines[index]
            else:
                scheduled_pipelines.append(pipeline)

            pipeline.add_job(job)

        return scheduled_pipelines
