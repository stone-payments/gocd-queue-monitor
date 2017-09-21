import os
import requests
import json
from bs4 import BeautifulSoup
from models.Pipeline import Pipeline
from models.Job import Job

from dotenv import load_dotenv
load_dotenv('./.env')
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def main():         
    scheduled_jobs_xml = get_scheduled_jobs_xml()
    scheduled_pipelines = get_scheduled_pipelines(scheduled_jobs_xml)

    #pipelines_with_updated_status = update_pipelines_status(scheduled_pipelines)

    return render_template('index.html', pipelines=scheduled_pipelines)


def get_scheduled_jobs_xml():
    # response = requests.get(GOCD_API_URL + 'jobs/scheduled.xml', auth=(GOCD_USER, GOCD_PASSWORD), verify=False)
    # xml = response.text
    xml = open("./test.xml")    
    soup = BeautifulSoup(xml, "xml")
    scheduled_jobs_xml = soup.find_all('job')    
    return scheduled_jobs_xml

def extract_pipeline_name(full_pipeline_name):
    splitted_build_locator = full_pipeline_name.split('/')
    pipeline_name = splitted_build_locator[0]    
    return pipeline_name

def get_scheduled_pipelines(jobs_xml):
    scheduled_pipelines = []
    
    for job_xml in jobs_xml:        
        full_pipeline_name = job_xml.find('buildLocator').string
        pipeline_name = extract_pipeline_name(full_pipeline_name)
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

