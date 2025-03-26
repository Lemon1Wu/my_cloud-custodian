import os
import sys

from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcbr.v1 import *
from huaweicloudsdkcbr.v1.region.cbr_region import CbrRegion

from huaweicloudsdkcore.auth.credentials import BasicCredentials

from c7n import utils
from c7n.exceptions import PolicyValidationError
from c7n.filters import OPERATORS, Filter

def register_cbr_filter(filters):
    filters.register('associated_vaults', AssociatedVaultsFilter)


class AssociatedVaultsFilter(Filter):
    schema = utils.type_schema('associated_vaults', op={'enum': list(OPERATORS.keys())})
    schema_alias = True

    def __call__(self, resource):
        op_name = self.data.get('op', 'ni')
        op = OPERATORS.get(op_name)
        id = resource['id']
        request = ListPoliciesRequest()
        request.vault_id = id
        response = self.client.list_policies(request)
        return op(id, self.list_vaults())

    def list_vaults(self):
        region = os.getenv('HUAWEI_DEFAULT_REGION')
        if not region:
            sys.exit(1)

        ak = os.getenv('HUAWEI_ACCESS_KEY_ID')
        if ak is None:
            sys.exit(1)

        sk = os.getenv('HUAWEI_SECRET_ACCESS_KEY')
        if sk is None:
            sys.exit(1)

        credentials = BasicCredentials(ak, sk)

        client = CbrClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(CbrRegion.value_of(region)) \
            .build()

        try:
            request = ListPoliciesRequest()
            response = client.list_policies(request)
            policies = response.to_dict()['policies']
            list_vaults = []
            for policy in policies:
                list_vaults.extend([associated_vault['vault_id'] for associated_vault in policy['associated_vaults']])
        except exceptions.ClientRequestException as e:
            raise
        return list_vaults