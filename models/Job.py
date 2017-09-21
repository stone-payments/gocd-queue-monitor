from models.Resource import Resource

class Job:

    def __init__(self, name):
        self.name = name
        self.resources = []
        
    def add_resources_from_xml(self, job_xml):
        resources_xml = job_xml.find('resources')
        resources_xml_list = resources_xml.find_all('resource')

        for resource_xml in resources_xml_list:
            resource = Resource(resource_xml.string.strip())
            self.resources.append(resource)

    def __str__(self):
        name = 'Job: ' + self.name        
        name += ' | Resources: [ '
        for resource in self.resources:
            name +=  '%s ' % (resource)
        name += ' ] '    
        return name