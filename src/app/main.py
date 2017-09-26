import json
import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from src.app.models.Agent import Agent
from src.app.models.Job import Job

from src.app.models.Pipeline import Pipeline

load_dotenv('./.env')
from flask import Flask, render_template
app = Flask(__name__)

GOCD_API_URL = os.environ.get("GOCD_API_URL")
GOCD_USER = os.environ.get("GOCD_USER")
GOCD_PASSWORD = os.environ.get("GOCD_PASSWORD")


@app.route('/')
def main():

    return render_template('works.html')

@app.route('/home')
def home():
    scheduled_jobs_xml = get_scheduled_jobs_xml()
    scheduled_pipelines = get_scheduled_pipelines_from_job_xml(scheduled_jobs_xml)
    active_agents = get_active_agents()
    pipelines_with_updated_status = update_pipelines_status(scheduled_pipelines)

    return render_template('index.html', pipelines=pipelines_with_updated_status, agents=active_agents)


def get_scheduled_jobs_xml():
    response = requests.get(GOCD_API_URL + '/jobs/scheduled.xml', auth=(GOCD_USER, GOCD_PASSWORD), verify=False)
    xml = response.text
    # xml = open("./test.xml")
    soup = BeautifulSoup(xml, "xml")
    scheduled_jobs_xml = soup.find_all('job')    
    return scheduled_jobs_xml


def get_scheduled_pipelines_from_job_xml(jobs_xml):
    scheduled_pipelines = []
    
    for job_xml in jobs_xml:        
        full_pipeline_name = job_xml.find('buildLocator').string
        pipeline_name = Pipeline.extract_pipeline_name(full_pipeline_name)
        job_name = job_xml['name']
        
        pipeline = Pipeline(pipeline_name)
            
        job = Job(job_name)
        job.add_resources_from_xml(job_xml)

        if(pipeline in scheduled_pipelines):
            index = scheduled_pipelines.index(pipeline)                      
            pipeline = scheduled_pipelines[index]
        else:            
            scheduled_pipelines.append(pipeline)
            
        pipeline.add_job(job)
        
    return scheduled_pipelines


def update_pipelines_status(pipelines):
    for pipeline in pipelines:
        pipeline.update_pipeline_status_from_api()
    return pipelines    


@app.route('/agents')
def get_active_agents():

    headers = {'accept': "application/vnd.go.cd.v4+json"}

    response = requests.get(GOCD_API_URL + '/agents',auth=(GOCD_USER, GOCD_PASSWORD), headers=headers, verify=False)

    response_json = json.loads(response.text)
    agents_list = response_json['_embedded']['agents']
    agents=[]
    
    for agent in agents_list:        
        if(is_agent_active(agent) and not is_elastic_agent(agent)):        
            agent_name = agent['hostname']
            agent_envs = get_agent_environments(agent)
            agent_resources = get_agent_resources(agent)
            agent_status = get_agent_status(agent)
            agent_obj = Agent(agent_name,agent_resources,agent_envs,agent_status)
            agents.append(agent_obj)

    return agents


def is_elastic_agent(agent):
    if 'elastic_agent_id' in agent:
        return True
    else:
        return False


def is_agent_active(agent):
    if agent['build_state'] != 'Unknown':
        return True
    else: 
        return False


def get_agent_resources(agent):
    agent_resources = []
    for resource in agent['resources']:
        agent_resources.append(resource)
    return agent_resources            


def get_agent_environments(agent):
    agent_envs = []    
    for environment in agent['environments']:
        agent_envs.append(environment)
    return agent_envs


def get_agent_status(agent):
    return agent['build_state']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
