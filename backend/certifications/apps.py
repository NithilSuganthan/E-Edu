from django.apps import AppConfig


class CertificationsConfig(AppConfig):
    name = 'certifications'

    def ready(self):
        import certifications.signals
