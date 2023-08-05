from django.dispatch import Signal


job_created = Signal(providing_args=['instance'])
