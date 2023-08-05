"""
hudai.resources.domain
"""
from ..helpers.resource import Resource


class DomainResource(Resource):
    def __init__(self, client):
        Resource.__init__(
            self, client, base_path='/companies/{company_id}/domains')
        self.resource_name = 'Domain'

    def list(self, company_id, page=None):
        query_params = self._set_limit_offset({'page': page})

        return self.http_get('/', params={'company_id': company_id},
                             query_params=query_params)

    def create(self, company_id, hostname):
        return self.http_post('/', params={'company_id': company_id},
                              data={'hostname': hostname})

    def fetch(self, company_id, entity_id):
        return self.http_get('/{id}',
                             params={'company_id': company_id, 'id': entity_id})

    def delete(self, company_id, entity_id):
        return self.http_delete('/{id}',
                                params={'company_id': company_id, 'id': entity_id})
