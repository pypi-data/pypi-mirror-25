from typing import List

from django.db import transaction

from plenario_exporter_s3.models import DataSetInfo, ExportJob


def create_models_and_start_job(
        requestor_email: str,
        ds_info: List[dict]) -> None:

    job = ExportJob(requestor=requestor_email)
    data_sets = [
        DataSetInfo(job=job, **info)
        for info in ds_info
    ]

    with transaction.atomic():
        job.save()
        for data_set in data_sets:
            data_set.save()

    job.start_job()
    job.save()

    return job.pk
