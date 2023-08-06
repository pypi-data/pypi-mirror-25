import logging

from ..utils import WaitCompletion
from .command import Command
logger = logging.getLogger(__name__)


class Nodes(Command):
    def __init__(self, *args, **kwargs):
        self._logger = logger
        super(Nodes, self).__init__(*args, **kwargs)

    def list(self):
        self.columns = ['ip', 'created']
        logger.debug('Going to list nodes..')
        uri = 'nodes/{0}/'.format(self.application)
        all = self.api.get(uri=uri)
        return all

    def get(self, ip):
        uri = 'nodes/{0}/{1}'.format(self.application, ip)
        response = self.api.get(uri=uri)
        return response

    @WaitCompletion(logger=logger)
    def add(self, provider=None, availability_zone=None, **kwargs):
        logger.info('Please wait while FaaSpot creating a VM for you..')
        uri = 'nodes/{0}/'.format(self.application)
        data = {'region': availability_zone or None,
                'provider': provider or None}
        task_id = self.api.put(uri=uri, data=data)
        return "Execution id: {0}".format(task_id)

    @WaitCompletion(logger=logger)
    def remove(self, ip=None, **kwargs):
        logger.debug('Going to delete a node')
        ip = ip if ip else ''
        uri = 'nodes/{0}/{1}'.format(self.application, ip)
        task_id = self.api.delete(uri=uri)
        return "Execution id: {0}".format(task_id)

    def update(self, min, max):
        if min > max:
            raise Exception('Bad arguments. min should be lower than max')
        if any(not self._is_number(x) for x in [min, max]):
            raise Exception('Bad arguments. min & max should be numbers')
        logger.debug('Going to update node workers amount: {0} - {1}'.format(min, max))
        uri = 'nodes/{0}/'.format(self.application)
        data = {'min_workers': min,
                'max_workers': max}
        response = self.api.patch(uri=uri, data=data)
        return response

    @WaitCompletion(logger=logger)
    def refresh_ip(self, ip=None, **kwargs):
        uri = 'nodes/{0}/'.format(self.application)
        data = {'refresh_ip': ip if ip else 'all'}
        task_id = self.api.patch(uri=uri, data=data)
        return "Execution id: {0}".format(task_id)

    def replace(self, ip):
        uri = 'nodes/{0}/replace/{1}'.format(self.application, ip)
        result = self.api.get(uri=uri)
        return result

    @staticmethod
    def _is_number(num):
        return isinstance(num, int) or num.isdigit()
