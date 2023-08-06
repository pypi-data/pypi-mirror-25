from .api import BaseModelManager, BaseModel


class BaseApp(BaseModel):
    @property
    def credentials(self):
        return self.act(['credentials', 'read'], {'object_id': self.object_id})


class BaseAppManager(BaseModelManager):
    model = BaseApp
    namespace = ['apps']

    def __init__(self, *args, **kwargs):
        super(BaseAppManager, self).__init__(*args, **kwargs)
        self.workspace = kwargs.pop('workspace', None)

        if self.workspace is None:
            raise AssertionError("Missing workspace parameter on initialization")

    def pre_create(self, **params):
        params['workspace'] = self.workspace.object_id
        return params

    def pre_save(self, **params):
        if not isinstance(self.workspace, str):
            params['workspace'] = params['workspace'].object_id


class Workspace(BaseModel):
    def add_owner(self, email):
        return self.act(['owners', 'create'], {
            'object_id': self.object_id, 'user': email})

    def remove_owner(self, email):
        return self.act(['owners', 'partial_update'], {
            'object_id': self.object_id, 'user': email})

    def add_contributor(self, email):
        return self.act(['contributors', 'create'], {
            'object_id': self.object_id, 'user': email})

    def remove_contributor(self, email):
        return self.act(['contributors', 'partial_update'], {
            'object_id': self.object_id, 'user': email})

    def set_payment_method(self, payment_method_object_id):
        return self.act(['set_payment_method'], {
            'object_id': self.object_id, 'method': payment_method_object_id})

    def notify(self, subject, content):
        return self.act(['notify'], {
            'object_id': self.object_id, 'subject': subject, 'content': content})


class WorkspaceManager(BaseModelManager):
    model = Workspace
    namespace = ['workspaces']
