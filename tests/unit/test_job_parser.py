from src.app.parsers.JobParser import JobParser
from src.app.models.Resource import Resource
from bs4 import BeautifulSoup


def test_should_extract_resources_from_job_xml():
    test_xml = open('tests/files/complete_job.xml', encoding='utf-8')
    job_parser = JobParser()
    job_xml = BeautifulSoup(test_xml, "xml")
    resources = job_parser.get_resources_from_xml(job_xml)

    resource1 = Resource('.net builder')
    resource2 = Resource('windows')
    expected_resources = [resource1, resource2]

    assert (len(resources) == len(expected_resources)) and (expected_resources == resources)


def test_should_extract_resources_from_job_xml_without_resources():
    job_parser = JobParser()
    test_xml = open('tests/files/job_without_resources.xml', encoding='utf-8')
    job_xml = BeautifulSoup(test_xml, "xml")

    resources = job_parser.get_resources_from_xml(job_xml)

    expected_resources = []

    assert (len(resources) == len(expected_resources)) and (expected_resources == resources)