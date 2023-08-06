from pymental.client import Conductor
from pymental.models import CloudConfig

client = Conductor()
# job = client.jobs.get(210)
# stat = client.jobs.status(268)
#
# poll_status(client=client, job_id=job.id)
node_list = client.nodes.list()
total_nodes = len(node_list.nodes)
print('\n'.join(['{} - {}'.format(n.name, n.status) for n in node_list.nodes]))
print('Total nodes: {}\tTotal running jobs: {}'.format(
    total_nodes, node_list.total_running_jobs))
# node = client.nodes.get(3)
# print(node.status)

job_list = client.jobs.list(filter='pending')
total_jobs = len(job_list.jobs)
print('\n'.join(['{} - {}'.format(n.id, n.status) for n in job_list.jobs]))
print('Total jobs: {}'.format(total_jobs))

if total_jobs / 2 > total_nodes:
    cloud_config = CloudConfig(min_cluster_size=3)
    cloud_config.min_cluster_size = 3 if str(cloud_config.min_cluster_size) == '2' else 2
print(client.cloud_config.create(cloud_config).min_cluster_size)
print('ff')
