from pymental.client import Conductor
from pymental.models import CloudConfig, SKIP

client = Conductor()

node_list = client.nodes.list()
total_nodes = len([x for x in node_list.nodes if x.product == 'Server'])
print('\n'.join(['{} - {}'.format(n.name, n.status) for n in node_list.nodes]))
print('\nTotal nodes: {}\nTotal running jobs: {}'.format(
    total_nodes, node_list.total_running_jobs))

job_list = client.jobs.list(filter='pending')
total_pending_jobs = len(job_list.jobs) if job_list.jobs != SKIP else 0
if total_pending_jobs:
    print('\n'.join(['{} - {}'.format(n.id, n.status) for n in job_list.jobs]))
print('Total pending jobs: {}'.format(total_pending_jobs))

if total_pending_jobs / 2 > total_nodes:
    cloud_config = client.cloud_config.create(CloudConfig(min_cluster_size=2))
    print(cloud_config.min_cluster_size)
else:
    print('\nIt\'s fine.')
