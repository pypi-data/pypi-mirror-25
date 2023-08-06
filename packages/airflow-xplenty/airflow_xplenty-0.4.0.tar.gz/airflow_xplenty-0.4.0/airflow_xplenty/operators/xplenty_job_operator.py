from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow_xplenty.client_factory import ClientFactory
from airflow_xplenty.cluster_factory import ClusterFactory
from airflow_xplenty.job_manager import JobManager
from airflow_xplenty.package_finder import PackageFinder

"""Operator to run an Xplenty package on a cluster

Spin-up or re-use a cluster in the given environment ('sandbox' or 'production')
and execute the named package as a job. If the job completes normally or is
stopped, this operator will finish successfully. If the job fails, then this
operator will fail.
"""
class XplentyJobOperator(BaseOperator):
    @apply_defaults
    def __init__(self, package_id=None, package_name=None, env='sandbox', **kwargs):
        if package_id is None and package_name is None:
            raise TypeError('__init__ requires either package_id or package_name')

        if package_id is not None and package_name is not None:
            raise TypeError('Do not supploy both package_id and package_name')

        self.package_id = package_id
        self.package_name = package_name

        # Setting all of these instance variables in the constructor,
        # rather than where they are used to facilitate testing.
        self.client = ClientFactory().client()
        self.cluster_factory = ClusterFactory(self.client, env)
        self.package_finder = PackageFinder(self.client)
        self.job_manager = JobManager(self.client)

        super(XplentyJobOperator, self).__init__(**kwargs)

    def execute(self, context):
        cluster = self.cluster_factory.find_or_start()

        if self.package_id is not None:
            package = self.client.get_package(self.package_id)
        else:
            package = self.package_finder.find(self.package_name)

        if package is None:
            raise Exception('Package %s not found' % self.package_name)

        self.job_manager.run(cluster.id, package.id)

    def on_kill(self):
        self.job_manager.stop()
