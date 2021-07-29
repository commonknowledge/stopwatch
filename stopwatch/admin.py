from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from import_export.admin import ImportExportModelAdmin, ImportForm, ConfirmImportForm
from wagtail.core.models import Page

from stopwatch import models, resources


@admin.register(models.StopWatchDocument, models.StopwatchImage)
class GenericAdmin(admin.ModelAdmin):
    pass


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(models.Article)
class NewsItemAdmin(ImportExportModelAdmin):
    class CustomImportForm(ImportForm):
        parent_id = forms.IntegerField()

    class CustomConfirmImportForm(ConfirmImportForm):
        parent_id = forms.IntegerField()

    def get_import_form(self):
        return NewsItemAdmin.CustomImportForm

    def get_confirm_import_form(self):
        return NewsItemAdmin.CustomConfirmImportForm

    def get_form_kwargs(self, form, *args, **kwargs):
        if isinstance(form, NewsItemAdmin.CustomImportForm):
            if form.is_valid():
                kwargs.update({'parent_id': form.cleaned_data['parent_id']})
        return kwargs

    def get_import_resource_kwargs(self, request, form, *args, **kwargs):
        res = super().get_import_resource_kwargs(request, *args, **kwargs)

        if form.is_valid():
            parent_id = form.cleaned_data['parent_id']
            res['parent'] = Page.objects.get(pk=parent_id)

        return res

    resource_class = resources.ArticleResource
