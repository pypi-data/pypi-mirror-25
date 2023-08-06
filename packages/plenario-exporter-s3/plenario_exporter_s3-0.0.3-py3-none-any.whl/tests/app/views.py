from plenario_core.views.export import GenericMetaExportView
from plenario_exporter_s3.services import create_models_and_start_job

from .models import EtlEventMeta

export_meta = GenericMetaExportView.as_view(
    models=[EtlEventMeta],
    async_handler=create_models_and_start_job)
