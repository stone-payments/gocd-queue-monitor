import os
import requests
import json

from app.services.APIConsumer import APIConsumer

GOCD_API_URL = os.environ.get("GOCD_API_URL")
GOCD_USER = os.environ.get("GOCD_USER")
GOCD_PASSWORD = os.environ.get("GOCD_PASSWORD")

class Pipeline:

    def __init__(self, name):
        self.name = name
        self.jobs = []
        self.status = 'unknown'
    
    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_name(self):
        return self.name

    def add_job(self, job):
        self.jobs.append(job)
    
    def get_jobs(self):
        return self.jobs

    def update_pipeline_status_from_api(self):
        self.status = APIConsumer.get_pipeline_status_from_api(self.name)

    def __hash__(self):
        return hash((self.name))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.name == other.name
    
    def __str__(self):
        name = self.name + ' Jobs: ' 
        for job in self.jobs:
            name +=  '"%s", ' % (job)
        return name