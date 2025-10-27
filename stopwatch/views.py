from wagtail.admin.views.reports import PageReportView
from wagtail.models import Page
from django.http import HttpResponse
import csv
import openpyxl
from django.utils import timezone
from datetime import timedelta
from stopwatch.forms import AgingPagesFilterForm
from django.urls import reverse
from django.utils.timezone import make_naive


class StaleContentAuditReport(PageReportView):
    """
    Content audit report for identifying pages published 3+ years ago.
    
    This report identifies potentially stale content by filtering pages based on their
    first_published_at date. Note that first_published_at can be:
    - Imported from legacy systems (see ArticleResource)
    - Manually set by editors via the Wagtail admin
    - Automatically set by Wagtail when a page is first published
    
    The report provides:
    - Filtering by publication date, status (live/draft), and page type
    - Display of both original publication date and last revision date
    - Export functionality to CSV and Excel formats
    
    All aging calculations are based exclusively on first_published_at to ensure
    imported content with historic dates is correctly identified as stale.
    """
        template_name = "reports/custom_aging_pages_report.html"
        model = Page  
        index_url_name = "stale_content_audit"
        index_results_url_name = "stale_content_audit_results"
        header_icon = 'time'
        page_title = "Stale Content Audit – By First Published At"
        export_headings = dict(
            page_title='Page Title',
            first_published_at='First Published At',
            last_updated_at='Last Updated At',
            status='Status',
            page_type='Page Type', 
        )

        def get_queryset(self):
            """
            Build queryset of pages published 3+ years ago.
            
            Applies base aging filter using first_published_at, then applies any
            user-specified filters for date, status, and page type.
            """
            queryset = self.model.objects.all()
            three_years_ago = timezone.now() - timedelta(days=3 * 365)
            queryset = queryset.filter(first_published_at__lte=three_years_ago)

            first_published_before = self.request.GET.get('first_published_before')
            status = self.request.GET.get('status')
            page_type = self.request.GET.get('page_type')

            if first_published_before:
                queryset = queryset.filter(first_published_at__lte=first_published_before)

            if status == 'live':
                queryset = queryset.filter(live=True)
            elif status == 'draft':
                queryset = queryset.filter(live=False)

            if page_type:
                queryset = queryset.filter(content_type__model__icontains=page_type)

            return queryset


        def format_status(self, page):
            """Format page status as human-readable string."""
            if page.live:
                if page.has_unpublished_changes:
                    return "Live + Draft"
                return "Live"
            return "Draft"

        def format_page_type(self, page):
            """Return the specific page type class name."""
            return page.specific_class.__name__

        
        def get_context_data(self, **kwargs):
            """
            Prepare display data for the report template.
            
            Enriches page data with edit URLs, formatted status, last update info,
            and user who made the last update. Uses first_published_at for original
            publication date and latest_revision_created_at for last update tracking.
            """
            context = super().get_context_data(**kwargs)

            annotated_pages = []
            for page in self.get_queryset():
                page_data = type('PageData', (), {
                    'title': page.title,
                    'edit_url': reverse('wagtailadmin_pages:edit', args=[page.id]),
                    'first_published_at': page.first_published_at,
                    'last_updated_at': page.latest_revision_created_at or page.last_published_at,
                    'updated_by': page.latest_revision.user if page.latest_revision and page.latest_revision.user else "Unknown",
                    'status': self.format_status(page),
                    'page_type': self.format_page_type(page),
                })()
                annotated_pages.append(page_data)

            context['annotated_pages'] = annotated_pages
            context['filter_form'] = AgingPagesFilterForm(self.request.GET)
            return context

        def export_to_csv(self):
                """
                Export report data to CSV format.
                
                Includes all filtered pages with their publication date, last update,
                status, and page type in a downloadable CSV file.
                """
                queryset = self.get_queryset()
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="stale_content_audit.csv"'

                writer = csv.writer(response)
                writer.writerow(self.export_headings.values())

                for page in queryset:
                    last_updated = page.latest_revision_created_at or page.last_published_at
                    row = [
                        page.title,
                        self.format_datetime(page.first_published_at),
                        self.format_datetime(last_updated),
                        self.format_status(page),
                        self.format_page_type(page),  
                    ]
                    writer.writerow(row)

                return response

        def export_to_xlsx(self):
                """
                Export report data to Excel format.
                
                Creates an Excel workbook with datetime values properly formatted.
                Converts timezone-aware datetimes to naive for Excel compatibility.
                """
                queryset = self.get_queryset()

                workbook = openpyxl.Workbook()
                sheet = workbook.active
                sheet.title = "Stale Content Audit"

                headers = list(self.export_headings.values())
                sheet.append(headers)

                for page in queryset:
                    first_published_at = page.first_published_at
                    last_updated_at = page.latest_revision_created_at or page.last_published_at

                    if first_published_at:
                        first_published_at = make_naive(first_published_at)
                    
                    if last_updated_at:
                        last_updated_at = make_naive(last_updated_at)

                    row = [
                        page.title,
                        first_published_at,
                        last_updated_at,
                        self.format_status(page),
                        self.format_page_type(page),
                    ]
                    sheet.append(row)

                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = 'attachment; filename="stale_content_audit.xlsx"'

                workbook.save(response)
                return response
                    
        def dispatch(self, request, *args, **kwargs):
                """
                Route requests to appropriate export methods or display view.
                
                Handles export query parameters to trigger CSV or Excel downloads.
                """
                export_format = request.GET.get('export')
                if export_format == 'csv':
                    return self.export_to_csv()
                elif export_format == 'xlsx':
                    return self.export_to_xlsx()

                return super().dispatch(request, *args, **kwargs)
            
        def format_datetime(self, datetime_obj):
                """Format datetime object as 'd Month YYYY' string for display."""
                if datetime_obj:
                        return datetime_obj.strftime('%d %B %Y')  
                return ''