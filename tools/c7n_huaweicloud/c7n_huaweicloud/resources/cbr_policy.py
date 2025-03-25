import logging
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcbr.v1 import *

from c7n.utils import type_schema
from c7n_huaweicloud.actions.base import HuaweiCloudBaseAction
from c7n_huaweicloud.provider import resources
from c7n_huaweicloud.query import QueryResourceManager, TypeInfo

log = logging.getLogger("custodian.huaweicloud.resources.cbr-policy")


@resources.register('cbr-policy')
class CbrPolicy(QueryResourceManager):
    class resource_type(TypeInfo):
        service = 'cbr-policy'
        enum_spec = ('list_policies', 'policies', 'offset')
        id = 'id'


@CbrPolicy.action_registry.register('delete_policy')
class CbrDeletePolicy(HuaweiCloudBaseAction):
    '''
    Checks if a recovery point is encrypted. Delete the recovery point not encrypted.

    :Example:

    .. code-block:: yaml

        policies:
            - name: delete_policy_unassociated
              resource: huaweicloud.cbr-policy
              filters:
                - and:
                  - type: value
                    key: name
                    value: "weekly_create_backup"
                  - type: value
                    key: associated_vaults
                    value: []
              actions:
                - delete_policy

    '''

    schema = type_schema('delete_policy')

    def perform_action(self, resource):

        client = self.manager.get_client()
        try:
            request = DeletePolicyRequest()
            request.policy_id = resource['id']
            response = client.delete_policy(request)
        except exceptions.ClientRequestException as e:
            log.error(e.status_code, e.request_id, e.error_code, e.error_msg)
            raise
        return response





