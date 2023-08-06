from .apps import BaseApp, BaseAppManager
import json


class ModelEndpoint(BaseApp):
    def predict(self, params):
        return self.act(['predict', 'create'], {
            'object_id': self.object_id, 'input_json': json.dumps(params)})

    def pre_save(self):
        for param in ['enrich', 'store', 'workspace']:
            if self._data.get(param, None) is not None and \
                    not isinstance(self._data[param], str):
                self._data[param] = self._data[param].object_id


class ModelEndpointManager(BaseAppManager):
    model = ModelEndpoint
    namespace = ['serve']

    def pre_create(self, **params):
        params['workspace'] = self.workspace.object_id
        params['enrich'] = params['enrich'].object_id
        if params.get('store', None) is not None:
            params['store'] = params['store'].object_id
        return params
