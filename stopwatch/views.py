from wagtail.admin.views.reports import PageReportView
from wagtail.models import Page
from django.http import HttpResponse
import csv
import openpyxl
from django.utils import timezone
from datetime import timedelta
from stopwatch.forms import AgingPagesFilterForm
from wagtail.models import Page
from django.urls import reverse

from wagtail.models import Page
from django.utils.timezone import make_naive


class CustomAgingPagesReportView(PageReportView):
        template_name = "reports/custom_aging_pages_report.html"
        model = Page  
        index_url_name = "custom_aging_pages_report"
        index_results_url_name = "custom_aging_pages_report_results"
        header_icon = 'time'
        page_title = "Custom Aging Pages Report"
        export_headings = dict(
            page_title='Page Title',
            first_published_at='First Published At',
            last_updated_at='Last Updated At',
            status='Status',
            page_type='Page Type', 
        )

        def get_queryset(self):
            queryset = self.model.objects.all()
            # Apply the aging filter (pages older than 3 years)
            three_years_ago = timezone.now() - timedelta(days=3 * 365)
            queryset = queryset.filter(first_published_at__lte=three_years_ago)

            last_updated_before = self.request.GET.get('last_updated_before')
            status = self.request.GET.get('status')
            page_type = self.request.GET.get('page_type')

            # Apply date filters
            if last_updated_before:
                queryset = queryset.filter(last_published_at__lte=last_updated_before)

            # Apply status filter
            if status == 'live':
                queryset = queryset.filter(live=True)
            elif status == 'draft':
                queryset = queryset.filter(live=False)

            # Apply page type filter
            if page_type:
                queryset = queryset.filter(content_type__model__icontains=page_type)

            return queryset


        def format_status(self, page):
            """Return the status of the page."""
            if page.live:
                if page.has_unpublished_changes:
                    return "Live + Draft"
                return "Live"
            return "Draft"

        def format_page_type(self, page):
            """Return the specific type of the page."""
            return page.specific_class.__name__

        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            annotated_data = []
            for page in self.get_queryset():
                last_updated_user = (
                    page.latest_revision.user
                    if page.latest_revision and page.latest_revision.user
                    else "Unknown"
                )

                annotated_data.append({
                    'title': page.title,
                    'edit_url': reverse('wagtailadmin_pages:edit', args=[page.id]),
                    'first_published_at': page.first_published_at,
                    'last_updated_at': page.latest_revision_created_at,
                    'updated_by': last_updated_user,  
                    'status': self.format_status(page),
                    'page_type': self.format_page_type(page),
                })

            context['annotated_pages'] = annotated_data
            context['filter_form'] = AgingPagesFilterForm(self.request.GET)
            return context
            
        def format_status(self, page):
                """Return the status of the page."""
                if page.live:
                    if page.has_unpublished_changes:
                        return "Live + Draft"
                    return "Live"
                return "Draft"

        def export_to_csv(self):
                queryset = self.get_queryset()
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="custom_aging_pages_report.csv"'

                writer = csv.writer(response)
                writer.writerow(self.export_headings.values())

                for page in queryset:
                    row = [
                        page.title,
                        self.format_datetime(page.first_published_at),
                        self.format_datetime(page.latest_revision_created_at),
                        self.format_status(page),
                        self.format_page_type(page),  
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
                    # Convert datetime fields to naive
                    first_published_at = page.first_published_at
                    latest_revision_created_at = page.latest_revision_created_at

                    if first_published_at:
                        first_published_at = make_naive(first_published_at)

                    if latest_revision_created_at:
                        latest_revision_created_at = make_naive(latest_revision_created_at)

                    row = [
                        page.title,
                        first_published_at,
                        self.latest_revision_created_at,
                        self.format_status(page),
                        self.format_page_type(page),
                    ]
                    sheet.append(row)

                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = 'attachment; filename="custom_aging_pages_report.xlsx"'

                workbook.save(response)
                return response
                    
        def dispatch(self, request, *args, **kwargs):
                export_format = request.GET.get('export')
                if export_format == 'csv':
                    return self.export_to_csv()
                elif export_format == 'xlsx':
                    return self.export_to_xlsx()

                return super().dispatch(request, *args, **kwargs)
            
        def format_datetime(self, datetime_obj):
                """Format the datetime object to 'd F Y' format."""
                if datetime_obj:
                        return datetime_obj.strftime('%d %B %Y')  
                return ''