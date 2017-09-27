from src.app.models.Agent import Agent


class AgentParser:

    def __init__(self, agents_json_dict):
        self.agents_json_dict = agents_json_dict

    def get_active_agents(self):
        agents = []
        for agent in self.agents_json_dict:
            if self.is_agent_active(agent) and not self.is_elastic_agent(agent):
                agent_name = agent['hostname']
                agent_envs = self.get_agent_environments(agent)
                agent_resources = self.get_agent_resources(agent)
                agent_status = self.get_agent_status(agent)
                agent_obj = Agent(agent_name, agent_resources, agent_envs, agent_status)
                agents.append(agent_obj)

        return agents

    @staticmethod
    def is_elastic_agent(agent):
        if 'elastic_agent_id' in agent:
            return True
        else:
            return False

    @staticmethod
    def is_agent_active(agent):
        if agent['build_state'] != 'Unknown':
            return True
        else:
            return False

    @staticmethod
    def get_agent_resources(agent):
        agent_resources = []
        for resource in agent['resources']:
            agent_resources.append(resource)
        return agent_resources

    @staticmethod
    def get_agent_environments(agent):
        agent_envs = []
        for environment in agent['environments']:
            agent_envs.append(environment)
        return agent_envs

    @staticmethod
    def get_agent_status(agent):
        return agent['build_state']