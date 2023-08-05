from django.conf import settings

ORG_MODEL = getattr(settings, 'ORGANIZATION_MODEL', 'report.Organization')
REPORT_PACKAGES = getattr(settings, 'REPORT_PACKAGES', [])
