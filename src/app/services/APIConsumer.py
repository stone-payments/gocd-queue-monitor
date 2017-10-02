import os
import requests
import json
from ..utils.EnvironmentVariables import EnvironmentVariables
from bs4 import BeautifulSoup

env_vars = EnvironmentVariables()


class APIConsumer:

    @staticmethod
    def get_scheduled_jobs_xml():
        # response = requests.get(env_vars.gocd_api_url() + '/jobs/scheduled.xml',
        #                         auth=(env_vars.gocd_user(), env_vars.gocd_password()), verify=False)
        # xml = response.text

        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(basepath, "..", "..", "..", "tests", "files", "test.xml"))
        xml = open(filepath)
        soup = BeautifulSoup(xml, "xml")
        scheduled_jobs_xml = soup.find_all('job')
        return scheduled_jobs_xml

    @staticmethod
    def get_api_version():
        headers = {'accept': "application/vnd.go.cd.v1+json"}
        response = requests.get(env_vars.gocd_api_url() + '/api/version',
                                auth=(env_vars.gocd_user(), env_vars.gocd_password()), headers=headers, verify=False)
        response_json = json.loads(response.text)
        version = response_json['version']
        print(version)
        return version

    @staticmethod
    def get_agents_json():

        headers = {'accept': "application/vnd.go.cd.v4+json"}

        response = requests.get(env_vars.gocd_api_url() + '/api/agents',
                                auth=(env_vars.gocd_user(), env_vars.gocd_password()), headers=headers, verify=False)

        response_json = json.loads(response.text)
        agents_dict = response_json['_embedded']['agents']

        return agents_dict

    @staticmethod
    def get_pipeline_status_from_api(pipeline_name):
        response = requests.get(env_vars.gocd_api_url() + '/api/pipelines/'+ pipeline_name +'/status',
                                auth=(env_vars.gocd_user(), env_vars.gocd_password()), verify=False)
        statusJson = json.loads(response.text)

        if statusJson['paused'] is True:
            return 'paused'
        elif statusJson['schedulable']:
            return 'schedulable'
        elif statusJson['locked']:
            return 'locked'
        else:
            return 'unknown'
