import logging
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcbr.v1 import *

from c7n.utils import type_schema
from c7n_huaweicloud.actions.base import HuaweiCloudBaseAction
from c7n_huaweicloud.provider import resources
from c7n_huaweicloud.query import QueryResourceManager, TypeInfo

log = logging.getLogger("custodian.huaweicloud.resources.cbr-backup")

@resources.register('cbr-backup')
class CbrBackup(QueryResourceManager):
    class resource_type(TypeInfo):
        service = 'cbr-backup'
        enum_spec = ('list_backups', 'backups', 'offset')
        id = 'id'


@CbrBackup.action_registry.register('delete_backup')
class CbrDeleteBackup(HuaweiCloudBaseAction):
    '''
    Checks if a recovery point is encrypted. Delete the recovery point not encrypted.
    
    :Example:

    .. code-block:: yaml

        policies:
            - name: delete-unencrypted-backup
              resource: huaweicloud.cbr-backup
              filters:
                - or:
                  - type: value
                    key: extend_info.encrypted
                    value: false
                  - type: value
                    key: extend_info.encrypted_algorithm
                    value: null
              actions:
                - delete_backup

    
    '''

    schema = type_schema('delete_backup')

    def perform_action(self, resource):

        client = self.manager.get_client()
        try:
            request = DeleteBackupRequest()
            request.backup_id = resource['id']
            response = client.delete_backup(request)
        except exceptions.ClientRequestException as e:
            log.error(e.status_code, e.request_id, e.error_code, e.error_msg)
            raise
        return response





