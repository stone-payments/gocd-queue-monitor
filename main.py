from os import path
from src.app.parsers.AgentParser import AgentParser
from src.app.parsers.PipelineParser import PipelineParser
from src.app.services.APIConsumer import APIConsumer
from dotenv import load_dotenv
from src.app.utils.EnvironmentVariables import EnvironmentVariables
from flask import Flask, render_template


load_dotenv(path.dirname(__file__) + './.env')
env_vars = EnvironmentVariables()
app = Flask(__name__, template_folder='src/app/templates', static_folder='src/app/static')


@app.route('/')
def home():
    scheduled_jobs_xml = APIConsumer.get_scheduled_jobs_xml()
    pipeline_parser = PipelineParser()
    scheduled_pipelines = pipeline_parser.get_scheduled_pipelines_from_job_xml(scheduled_jobs_xml)

    pipelines_with_updated_status = []
    for pipeline in scheduled_pipelines:
        pipeline.update_pipeline_status_from_api()
        pipelines_with_updated_status.append(pipeline)

    agents_json = APIConsumer.get_agents_json()
    agent_parser = AgentParser(agents_json)
    active_agents = agent_parser.get_active_agents()

    return render_template('index.html', pipelines=pipelines_with_updated_status, agents=active_agents)


@app.route('/agents')
def agents():
    return 'agents'


@app.route('/version')
def version():
    return "Api version" + APIConsumer.get_api_version()


@app.route('/works')
def main():
    return render_template('works.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=env_vars.port())
