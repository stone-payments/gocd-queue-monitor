from .Resource import Resource


class Job:
    def __init__(self, name):
        self.environment = ''
        self.name = name
        self.resources = []

    def get_resources(self):
        return self.resources

    def set_resources(self, resources):
        self.resources = resources

    def get_environment(self):
        return self.environment

    def set_environment(self, environment):
        self.environment = environment

    def __str__(self):
        return self.name