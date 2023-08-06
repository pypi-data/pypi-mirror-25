import time

class ClusterFactory:
    TERMINATING_STATUSES = ['pending_terminate', 'terminating', 'terminated', 'error']
    READY_STATUSES = ['available', 'idle']

    def __init__(self, client, env, poll_interval=10):
        self.client = client
        self.env = env
        self.poll_interval = poll_interval

    def find_or_start(self):
        cluster = self.__find() or self.__start()

        while cluster.status not in self.READY_STATUSES + self.TERMINATING_STATUSES:
            time.sleep(self.poll_interval)
            cluster = self.client.get_cluster(cluster.id)

        if cluster.status not in self.READY_STATUSES:
            raise Exception('Error starting cluster: %s' % cluster.status)

        return cluster

    def __find(self):
        for cluster in self.client.clusters:
            if cluster.type == self.env and cluster.status not in self.TERMINATING_STATUSES:
                return cluster

    def __start(self):
        return self.client.create_cluster(self.env, 1, 'airflow-%s-cluster' % self.env,
            'Cluster to run Airflow packages')
