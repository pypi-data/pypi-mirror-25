from lib import client, downtime, host, hostgroups, notifications, service, servicegroups, usergroups, users
from pprint import pprint
import logging
import sys

class Icinga2API(object):
    """
    Main Class to implement the Icinga2 API
    """

    def __init__(self, username=None, password=None, url=None, debug=False):
        """
        Initialize all needed Classes
        """
        self.log = logging.getLogger('Icinga2API')
        streamhandler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(logging.BASIC_FORMAT)
        streamhandler.setFormatter(formatter)
        self.log.addHandler(streamhandler)

        if debug:
            self.log.setLevel(logging.DEBUG)

        self.client = client.Icinga2APIClient()
        self.client.setconfig(username, password, url)
        self.downtimes = downtime.Downtime(client=self.client)
        self.hosts = host.Hosts(client=self.client)
        self.hostgroups = hostgroups.Hostgroups(client=self.client)
        self.notifications = notifications.Notification(client=self.client)
        self.services = service.Service(client=self.client)
        self.servicegroups = servicegroups.Servicegroups(client=self.client)
        self.usergroups = usergroups.Usergroups(client=self.client)
        self.users = users.Users(client=self.client)


if __name__ == '__main__':
    api = Icinga2API(username="root", password="1a15f273bf8c908d", url="https://icinga.mw-krz-swd.de:5665", debug=True)
    pprint(api.hosts.problem_count())
