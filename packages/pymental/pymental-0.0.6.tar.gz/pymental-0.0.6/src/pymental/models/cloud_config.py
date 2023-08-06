from pymental.meta import Model
from pymental.fields import GenericField, ListField, RelatedField, SKIP


class CloudConfig(Model):
    _tag = 'cloud_config'

    min_cluster_size = GenericField('min_cluster_size')
    max_cluster_size = GenericField('max_cluster_size')
