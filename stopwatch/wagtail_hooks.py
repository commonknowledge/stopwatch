from django.urls import path, reverse
from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail import hooks
from .views import StaleContentAuditReport

@hooks.register('register_reports_menu_item')
def register_stale_content_audit_report_menu_item():
    return AdminOnlyMenuItem("Stale Content Audit – By First Published At", reverse('stale_content_audit'), icon_name=StaleContentAuditReport.header_icon, order=700)

@hooks.register('register_admin_urls')
def register_stale_content_audit_report_url():
    return [
        path('reports/stale-content-audit-by-first-published-at/', StaleContentAuditReport.as_view(), name='stale_content_audit'),
    ]