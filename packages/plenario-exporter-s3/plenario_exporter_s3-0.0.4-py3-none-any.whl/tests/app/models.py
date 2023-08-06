from plenario_core.models import EtlEventMetaBase


class EtlEventMeta(EtlEventMetaBase):
    def get_absolute_url(self):
        return 'derp'
