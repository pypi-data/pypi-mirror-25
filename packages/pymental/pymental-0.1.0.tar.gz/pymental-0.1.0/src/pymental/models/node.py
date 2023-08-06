from pymental.meta import Model
from pymental.fields import GenericField, ListField, SKIP


class Node(Model):
    _tag = 'node'

    name = GenericField('name')
    hostname = GenericField('hostname')
    ip_addr = GenericField('ip_addr')
    public_ip_addr = GenericField('public_ip_addr')
    eth0_mac = GenericField('eth0_mac')
    status = GenericField('status')
    product = GenericField('product')
    version = GenericField('version')
    platform = GenericField('platform')
    variations = GenericField('variations')
    created_at = GenericField('created_at')
    backup_groups = GenericField('backup_groups')
    running_count = GenericField('running_count')
    job = GenericField('job')

    network_config = GenericField('network_config')
    firewall_config = GenericField('firewall_config')
    mount_point_config = GenericField('mount_point_config')
    sequencer_config = GenericField('sequencer_config')


class NodeList(Model):
    _tag = 'node_list'

    nodes = ListField('node', Node)

    def filter(self, **kwargs):
        key, value = kwargs.popitem()
        nodes = [node for node in self.nodes if getattr(node, key, None) == value]
        if kwargs:
            nodes = [node for node in self.filter(**kwargs) if node in nodes]
        return NodeList(nodes=nodes).nodes

    @property
    def total_running_jobs(self):
        try:
            return sum(int(node.running_count) for node in self.nodes
                       if node.running_count != SKIP)
        except ValueError:
            raise ValueError('Could not extract total number of running jobs')
