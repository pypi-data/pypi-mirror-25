import logging
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow_xplenty.client_factory import ClientFactory

"""Operator start a job on an Xplenty cluster
"""
class XplentyStartJobOperator(BaseOperator):
    @apply_defaults
    def __init__(self, package_id, start_cluster_task_id, **kwargs):
        self.package_id = package_id
        self.start_cluster_task_id = start_cluster_task_id
        self.client = ClientFactory().client()

        super(XplentyStartJobOperator, self).__init__(**kwargs)

    def execute(self, context):
        cluster_id = context['task_instance'].xcom_pull(task_ids=self.start_cluster_task_id)
        if cluster_id is None:
            raise Exception('No cluster_id found in XComs')

        job = self.client.add_job(cluster_id, self.package_id, {})
        logging.info('Starting job %d' % job.id)
        return job.id
