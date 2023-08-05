import time
import requests


class Client(object):
    """
    Azkaban client class for interacting with Azkaban server
    """

    def __init__(self, host, username, password, logger):
        """
        intialise the Azkbana client
        :param logger: logger
        :param env: variables coming from conf file
        """
        self.logger = logger
        self.host = host
        self.username = username
        self.password = password

    def run_pipeline(self, project, flow, params, concurrent_option='ignore'):
        """
        Run the pipeline on Azkaban

        :param project: pipeline project
        :param flow: pipeline flow
        :param params: pipeline params
        :param concurrent_option: 'ignore' by default
        :return: the execution id
        """

        session_id = self.login()

        data = {
            'session.id': session_id,
            'ajax': 'executeFlow',
            'project': project,
            'flow': flow,
            'concurrentOption': concurrent_option
        }

        for key, value in params.iteritems():
            data['flowOverride[{key}]'.format(key=key)] = value

        response = requests.get('{host}/executor'.format(host=self.host), params=data).json()

        if 'error' in response:
            raise Exception('Azkaban: {error}'.format(error=response['error']))
        else:
            return response['execid']

    def check_pipeline(self, exec_id):
        """
        Check the status of the pipeline

        :param exec_id: execution id
        :return: True if the pipeline succeeded otherwise False
        """

        while True:

            session_id = self.login()

            self.logger.info('Waiting   {exec_id}'.format(exec_id=exec_id))

            params = {
                'session.id': session_id,
                'ajax': 'fetchexecflow',
                'execid': exec_id
            }

            response = requests.get('{host}/executor'.format(host=self.host), params=params).json()

            status = response['status']

            if status == 'SUCCEEDED':
                return True
            elif status == 'FAILED':
                return False
            else:
                time.sleep(10)

    def login(self):
        """
        Authentication with Azkaban

        :return: the sessions id
        """

        # Create a session with the scheduler
        params = {
            'action': 'login',
            'username': self.username,
            'password': self.password
        }

        response = requests.post(self.host, params=params).json()

        if 'error' in response:
            raise Exception('Azkaban: {error}'.format(error=response['error']))
        else:
            return response['session.id']
