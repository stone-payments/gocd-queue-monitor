from app.models.Resource import Resource

class Job:

    def __init__(self, name):
        self.name = name
        self.resources = []
        
    def add_resources_from_xml(self, job_xml):
        resources_xml = job_xml.find('resources')
        if resources_xml != None:
            resources_xml_list = resources_xml.find_all('resource')

            for resource_xml in resources_xml_list:
                resource = Resource(resource_xml.string.strip())
                self.resources.append(resource)

    def get_resources(self):
        return self.resources

    def __str__(self):
        return self.name