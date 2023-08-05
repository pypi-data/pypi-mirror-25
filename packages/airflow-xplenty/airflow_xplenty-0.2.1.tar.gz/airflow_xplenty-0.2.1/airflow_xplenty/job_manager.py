import os
import time
from client_factory import ClientFactory

class JobManager:
    FINAL_STATUSES = ['completed', 'failed', 'stopped']

    def __init__(self, client, poll_interval=10):
        self.client = client
        self.poll_interval = poll_interval

    def run(self, cluster_id, package_id):
        job = self.client.add_job(cluster_id, package_id, {})
        self.job_id = job.id

        while job.status not in self.FINAL_STATUSES:
            time.sleep(self.poll_interval)
            job = self.client.get_job(self.job_id)

        if job.status == 'failed':
            raise Exception('Job for package_id %d failed: %s' % (self.package_id, job.errors))

    def stop(self):
        if self.job_id is not None:
            self.client.terminate_job(self.job_id)
