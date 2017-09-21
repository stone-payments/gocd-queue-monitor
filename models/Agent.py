class Agent:
    def __init__(self,name, resources, environments, status):
        self.name = name
        self.resources = resources
        self.environments = environments
        self.status = status

    def __str__(self):        
        return self.name        