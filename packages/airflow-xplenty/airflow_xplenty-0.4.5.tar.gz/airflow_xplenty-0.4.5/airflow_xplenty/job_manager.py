import logging
import time

class JobManager:
    FINAL_STATUSES = ['completed', 'failed', 'stopped']

    def __init__(self, client, poll_interval=10):
        self.client = client
        self.poll_interval = poll_interval

    def run(self, cluster_id, package_id):
        job = self.client.add_job(cluster_id, package_id, {})
        self.job_id = job.id
        logging.info('Starting job %d' % self.job_id)

        prev_progress = None
        while job.status not in self.FINAL_STATUSES:
            time.sleep(self.poll_interval)
            job = self.client.get_job(self.job_id)
            progress = round(job.progress * 100, 1)
            if prev_progress is None or prev_progress != progress:
                logging.info('Job %d in state %s (%.1f%%)' % (self.job_id, job.status, progress))
                prev_progress = progress

        logging.info('Job %d finished in state %s' % (self.job_id, job.status))

        if job.status == 'failed':
            raise Exception('Job for package_id %d failed: %s' % (package_id, job.errors))

    def stop(self):
        if self.job_id is not None:
            self.client.terminate_job(self.job_id)
