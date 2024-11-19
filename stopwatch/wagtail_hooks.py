from django.urls import path, reverse
from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail import hooks
from .views import CustomAgingPagesReportView

@hooks.register('register_reports_menu_item')
def register_custom_aging_pages_report_menu_item():
    return AdminOnlyMenuItem("Custom aging pages", reverse('custom_aging_pages_report'), icon_name=CustomAgingPagesReportView.header_icon, order=700)

@hooks.register('register_admin_urls')
def register_custom_aging_pages_report_url():
    return [
        path('reports/custom-aging-pages/', CustomAgingPagesReportView.as_view(), name='custom_aging_pages_report'),
    ]