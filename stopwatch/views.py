from wagtail.admin.views.reports import PageReportView
from wagtail.models import Page
from django.http import HttpResponse
import csv
import openpyxl
from django.utils import timezone
from datetime import timedelta



class CustomAgingPagesReportView(PageReportView):
    index_url_name = "custom_aging_pages_report"
    index_results_url_name = "custom_aging_pages_report_results"
    header_icon = 'time'
    results_template_name = 'stopwatch/reports/custom_aging_pages_results.html'
    page_title = "Custom aging pages report"

    export_headings = dict(
        page_title='Page Title',
        first_published_at='First Published at',
        last_updated_at='Last Updated At',
        live='Status',
        content_type='Type',
    )

    def get_queryset(self):
        # Fetch pages older than 3 years
        three_years_ago = timezone.now() - timedelta(days=3 * 365)
        queryset = Page.objects.filter(first_published_at__lte=three_years_ago).order_by('-first_published_at')
        return queryset
    
    
    # Custom spreadsheet export set up
    def export_to_csv(self):
        queryset = self.get_queryset()  
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="custom_aging_pages_report.csv"'

        writer = csv.writer(response)
        writer.writerow(self.export_headings.values())

        for page in queryset:
            row = [
                page.title,
                page.first_published_at,
                self.format_datetime(page.latest_revision_created_at),
                'Live' if page.live else 'Draft',
                page.specific_class.__name__,
            ]
            writer.writerow(row)

        return response

    def export_to_xlsx(self):
        queryset = self.get_queryset()  

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Custom Aging Pages"

        headers = list(self.export_headings.values())
        sheet.append(headers)

        for page in queryset:
            row = [
                page.title,
                page.first_published_at,
                self.format_datetime(page.latest_revision_created_at),
                'Live' if page.live else 'Draft',
                page.specific_class.__name__,
            ]
            sheet.append(row)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="custom_aging_pages_report.xlsx"'

        workbook.save(response)
        return response

    def dispatch(self, request, *args, **kwargs):
        export_format = request.GET.get('format', 'csv')
        if 'export' in request.GET:
            if export_format == 'xlsx':
                return self.export_to_xlsx()
            else:
                return self.export_to_csv()
        return super().dispatch(request, *args, **kwargs)

    def format_datetime(self, datetime_obj):
        """
        Format the datetime object to 'Y-m-d H:i:s' format.
        Returns an empty string if datetime_obj is None.
        """
        if datetime_obj:
            return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
        return ''