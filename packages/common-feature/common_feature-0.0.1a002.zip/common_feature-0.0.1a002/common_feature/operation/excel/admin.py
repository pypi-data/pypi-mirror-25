#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
import datetime

from . import utils
from ..._import_lib import *


class ImportExportBase(object):
    user_field_lists = None
    user_display_lists = None
    user_filter_lists = None

    def get_fields_list(self):
        """
        :param user_field_lists: user input
        :return:
        """
        fields = self.model._meta.fields
        fields_list = []
        for field in fields:
            fields_list.append(field.name)

        # check valid or not
        if self.user_field_lists:
            for user_field_list in self.user_field_lists:
                if user_field_list not in fields_list:
                    raise Exception('%s not in the fields of %s models' %(user_field_list, self.model.__name__))

        return fields_list

    def get_display_field(self):
        """
        if not field input
        :return: display field for excel easy reading
        """
        if self.user_display_lists:
            fields = self.get_fields_list()
            display_field = []

            for field in fields:
                display_field.append(field.replace('_', ' '))
        else:
            display_field = self.user_display_lists
        return display_field

    def verify_field_display_field(self):
        display_list = self.get_display_field()
        fields_list = self.get_fields_list()

        if len(display_list) != len(fields_list):
            raise Exception('Fields List and Display List must be same length')

    def get_filter(self):
        if self.user_filter_lists:
            new_filter_list = []
            fields = self.get_fields_list()
            for user_filter_list in self.user_filter_lists:
                if user_filter_list in fields:
                    new_filter_list.append(user_filter_list)
                else:
                    raise Exception('%s not in the field list.' % user_filter_list)
            return new_filter_list
        else:
            return []


class ImportFeature(ImportExportBase):
    change_list_template = 'admin/import_export/import_export.html'


class ExportFeature(ImportExportBase):
    change_list_template = 'admin/import_export/import_export.html'

    def get_filename(self):
        """
        :return: filename
        """
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        filename = "%s_%s_%s.%s" % ('Export',
                                    self.model.__name__,
                                    date_str,
                                    'xlsx')
        return filename

    def get_urls(self):
        urls = super(ExportFeature, self).get_urls()

        excel_urls = [
            url(r'^Export/$', self.admin_site.admin_view(self.do_export))
        ]
        return excel_urls + urls

    def get_query(self):
        if self.get_filter() is not []:
            return self.model.objects.filter(*self.get_filter()).values(*self.get_fields_list())
        else:
            return self.model.objects.all().values(*self.get_fields_list())

    def get_export_context_data(self, **kwargs):
        return self.get_context_data(**kwargs)

    def do_export(self, request, *args, **kwargs):
        context = self.get_export_context_data()
        utils.create_excel(
            query=self.get_query(),
            fields=self.get_fields_list(),
            display_fields=self.get_display_field(),
            filename1=self.get_filename(),
        )

        return TemplateResponse(request, [self.change_list_template],
                                context)