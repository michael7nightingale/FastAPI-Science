from tortoise.models import Model


class TortoiseModel(Model):
    def as_dict(self):
        schema = self.describe()
        dicted = {field['name']: getattr(self, field['name']) for field in schema['data_fields']}
        dicted[schema['pk_field']['name']] = str(getattr(self, schema['pk_field']['name']))
        return dicted
