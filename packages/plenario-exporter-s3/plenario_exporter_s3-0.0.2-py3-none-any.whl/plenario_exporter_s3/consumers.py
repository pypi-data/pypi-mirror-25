import codecs
import csv
import os
import shutil
import zipfile
from typing import List, Tuple

import boto3
from django.apps import apps
from django.core.mail import send_mail
from django.db.models import Q, QuerySet

from plenario_exporter_s3 import defaults
from plenario_exporter_s3.models import ExportJob, DataSetInfo


def export(message: dict) -> None:
    """Asynchronously runs an export job.

    :param message: the channel message containing the job pk
    """
    # get the job from the pk in the message
    pk = str(message['pk'])
    job = ExportJob.objects.get(pk=pk)

    # lay out the dump directories
    try:
        temp_dir, curr_dir, dump_dir, archive_fname, archive_path = \
            _setup_dirs_and_files(pk)
    except Exception as error:
        job.mark_erred(str(error))
        job.save()
        raise

    # for each data set attached to the job, query
    try:
        data_sets = job.data_sets.all()
        querysets = _get_querysets(data_sets)
    except Exception as error:
        job.mark_erred(str(error))
        job.save()
        raise

    # write the querysets to csvs
    try:
        _write_csvs(dump_dir, querysets)
    except Exception as error:
        job.mark_erred(str(error))
        job.save()
        raise

    # create a zipfile of the query result csvs
    try:
        _create_zipfile(temp_dir, pk, archive_fname, curr_dir)
    except Exception as error:
        job.mark_erred(str(error))
        job.save()
        raise

    # remove the temp results dir
    try:
        shutil.rmtree(dump_dir)
    except Exception as error:
        job.mark_erred(str(error))
        job.save()
        raise

    # ensure the s3 bucket exists
    try:
        _ensure_s3_bucket()
    except Exception as error:
        job.mark_erred(str(error))
        job.save()
        raise

    # upload the zipfile to s3
    try:
        archive_link = _upload_to_s3(archive_path, archive_fname)
    except Exception as error:
        job.mark_erred(str(error))
        job.save()
        raise

    # notify the requesting user via email
    try:
        _email_requestor(archive_link, job.requestor)
    except Exception as error:
        job.mark_erred(str(error))
        job.save()
        raise

    # finally remove zipfile
    try:
        os.remove(archive_path)
    except Exception as error:
        job.mark_erred(str(error))
        job.save()
        raise

    # set the complete time and bucket
    job.mark_completed()
    job.bucket = archive_link
    job.save()


def _setup_dirs_and_files(job_pk: str) -> Tuple[str]:
    """Sets up temp directories and file names.

    :param job_pk: the export job pk to be used as the archive name
    :return: the created directory names and file names
    """
    curr_dir = os.getcwd()

    root_dir = os.path.abspath(os.sep)
    temp_dir = os.path.join(root_dir, 'tmp')
    dump_dir = os.path.join(temp_dir, job_pk)

    archive_fname = f'{job_pk}.zip'
    archive_path = os.path.join(temp_dir, archive_fname)

    os.mkdir(dump_dir)

    return temp_dir, curr_dir, dump_dir, archive_fname, archive_path


def _get_querysets(
        data_sets: List[DataSetInfo]
        ) -> List[Tuple['MetaModel', QuerySet, List[str]]]:
    """Creates a list querysets to be later iterated to write the export files.

    :param data_sets: the list of data set info objects related to the job
    :return: tuples of the meta model, queryset, and field names
    """
    querysets = []
    for data_set in data_sets:
        meta_model_class = apps.get_model(
            data_set.meta_model_app_label, data_set.meta_model_class_name)
        meta_model = meta_model_class.objects.get(pk=data_set.meta_model_pk)
        ds_model = meta_model.get_ds_model()

        geo_q = Q(**{
            f'{data_set.point_field}__coveredby': data_set.bbox,
        })
        time_q = Q(**{
            f'{data_set.date_field}__contained_by': data_set.timerange,
        })

        results = ds_model.objects\
            .filter(geo_q, time_q)\
            .values(*data_set.fields)
        querysets.append((meta_model, results, data_set.fields))

    return querysets


def _write_csvs(
        dump_dir: str,
        querysets: List[Tuple['MetaModel', QuerySet, List[str]]]
        ) -> List[str]:
    """Iterates the querysets and writes the results to CSVs.

    :param dump_dir: the path to the directory to write the files
    :param querysets: the output of ``_get_querysets``
    :return: a list of created file names
    """
    fnames = []
    for meta_model, queryset, fields in querysets:
        fname = os.path.join(dump_dir, f'{meta_model.name}.csv')
        with codecs.open(fname, mode='w', encoding='utf8') as fh:
            writer = csv.DictWriter(fh, fields)
            writer.writeheader()
            for row in queryset:
                writer.writerow(row)
        fnames.append(fname)
    return fnames


def _create_zipfile(
        temp_dir: str,
        dump_dirname: str,
        archive_fname: str,
        curr_dir: str) -> None:
    """Creates a zipfile from the directory of exported CSVs.

    :param temp_dir: the path the temp directory
    :param dump_dirname: the name of the dump directory (not the full path)
    :param archive_fname: the name of the archive file
    :param curr_dir: the current executing directory
    """
    os.chdir(temp_dir)
    zfile = zipfile.ZipFile(
        archive_fname, mode='w', compression=zipfile.ZIP_DEFLATED)
    for dirname, _, fnames in os.walk(dump_dirname):
        for fname in fnames:
            path = os.path.join(dirname, fname)
            zfile.write(path)
    zfile.close()
    os.chdir(curr_dir)


def _ensure_s3_bucket():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(defaults.S3_BUCKET)
    if not bucket.creation_date:
        bucket.create()


def _upload_to_s3(archive_path: str, archive_fname: str) -> str:
    """Uploads the archive to S3.

    :param archive_path: the full path to the archive
    :param archive_fname: the name of the archive file
    :return: the URL of the archive
    """
    s3 = boto3.resource('s3')
    data = open(archive_path, mode='rb')
    bucket = defaults.S3_BUCKET
    s3.Bucket(bucket).put_object(
        Key=archive_fname, Body=data, ACL=defaults.S3_OBJECT_ACL)
    data.close()
    return f'https://s3.amazonaws.com/{bucket}/{archive_fname}'


def _email_requestor(archive_link: str, email_address: str) -> None:
    """Sends an email to the export requestor with a link to the archive.

    :param archive_link: the link to the archive on S3
    :param email_address: the email address of the requestor
    """
    message = \
        'Your exported data set is ready for download:\n\n' \
        f'{archive_link}\n\n' \
        'Please note that the file will be automatically removed after 7 days.'
    send_mail(
        subject='Plenario Export Ready',
        message=message,
        from_email=defaults.EMAIL_SENDER_ADDRESS,
        recipient_list=[email_address])
