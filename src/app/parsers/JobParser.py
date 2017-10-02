from src.app.models.Resource import Resource


class JobParser:
    def get_name_from_xml(self, job_xml):
        return job_xml['name']

    def get_resources_from_xml(self, job_xml):
        resources = []
        resources_xml = job_xml.find('resources')

        if resources_xml != None:
            resources_xml_list = resources_xml.find_all('resource')

            for resource_xml in resources_xml_list:
                resource = Resource(resource_xml.string.strip())
                resources.append(resource)
        return resources

    def get_environment_from_xml(self, job_xml):
        environment = job_xml.find('environment')
        if environment is not None:
            return environment.string
        else:
            return ''
