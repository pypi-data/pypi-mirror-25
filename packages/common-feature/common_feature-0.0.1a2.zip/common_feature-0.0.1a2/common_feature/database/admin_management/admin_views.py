#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import models
from ...operation.dict import utils
from ..._import_lib import *


class AdminSQL(TemplateView):
    template_name = "admin/AdminSQL.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        sql = request.GET.get('word')
        errors = []
        msg = ""
        records = ''
        ranking = models.Sqlcode.objects.all().order_by("id")
        excel = request.GET.get('excel')

        if request.GET.get('display'):
            for rankings in ranking:
                if (request.GET.get("dropdown")) == rankings.name:
                    sql = rankings.code

        elif request.GET.get('save'):
            if sql == request.GET.get('word') and len(sql) > 0:
                code = models.Sqlcode(
                    name='SQL'+str(models.Sqlcode.objects.all().count()),
                    code=sql,
                )
                code.save()
                msg = 'SQL is saved'
            else:
                errors.append('SQL is NOT save')
                sql = None

        elif request.GET.get('check'):
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    records = utils.dict_fetchall(cursor)

            except:
                errors.append("invalid sql command")

            if len(records) > 0:
                values = []
                keys = []
                for record in records:
                    keys = record.keys()
                    values.append(record.values())
                context['keys'] = keys
                context['values'] = values
            elif not errors:
                msg = "no record"

        if excel and sql:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    records = utils.dict_fetchall(cursor)
                return HttpResponse(
                    excel._create_excel(
                        querys=records,
                        save_internal=False
                    )
                    , content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )

            except:
                errors.append("invalid sql command")

        context['errors'] = errors
        context['message'] = msg
        context['ranking'] = ranking
        context['SQL'] = sql if sql and not errors else ""
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)