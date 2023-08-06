import django.dispatch

schema_uploaded_signal = django.dispatch.Signal(providing_args=["instance"])
