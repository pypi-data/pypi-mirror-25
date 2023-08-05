from django.contrib.gis import admin


from .models import Job


class JobAdmin(admin.GeoModelAdmin):  # NOQA
    pass


admin.site.register(Job, JobAdmin)  # NOQA