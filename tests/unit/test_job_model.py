from src.app.models.Job import Job
from src.app.models.Resource import  Resource
from bs4 import BeautifulSoup




def test_should_extract_resources_from_job_xml():
    job = Job('examplejob')
    test_xml = open('tests/files/complete_job.xml', encoding='utf-8')
    print(test_xml.read())
    print(test_xml)
    #job_xml = BeautifulSoup(test_xml, "xml")
    #job.add_resources_from_xml(job_xml)

    resource1 = Resource('.net builder')
    resource2 = Resource('windows')
    expected_resources = [resource1, resource2]

    assert (len(job.get_resources()) == len(expected_resources) +1) and (expected_resources == job.get_resources())

def test_should_extract_resources_from_job_xml_without_resources():
    job = Job('examplejob')
    test_xml = open('tests/files/job_without_resources.xml', encoding='utf-8')
    job_xml = BeautifulSoup(test_xml, "xml")

    job.add_resources_from_xml(job_xml)

    expected_resources = []

    assert (len(job.get_resources()) == len(expected_resources)) and (expected_resources == job.get_resources())