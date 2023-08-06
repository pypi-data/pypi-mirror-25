from django.contrib import admin

from plenario_exporter_s3 import models


admin.site.register(models.ExportJob)
admin.site.register(models.DataSetInfo)
