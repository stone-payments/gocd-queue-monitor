from os import path
from app.parsers.AgentParser import AgentParser
from app.parsers.PipelineParser import PipelineParser
from app.services.APIConsumer import APIConsumer
from dotenv import load_dotenv
from app.utils.EnvironmentVariables import EnvironmentVariables
from flask import Flask, render_template

from apscheduler.schedulers.background import BackgroundScheduler


load_dotenv(path.dirname(__file__) + '/../' + '.env')
env_vars = EnvironmentVariables()
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

@app.route('/version')
def version():
    return "Api version" + APIConsumer.get_api_version()


scheduler = BackgroundScheduler()
job = scheduler.add_job(version, 'interval', seconds=3)
# scheduler.start()

@app.route('/works')
def main():
    return render_template('works.html')


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=env_vars.port())
