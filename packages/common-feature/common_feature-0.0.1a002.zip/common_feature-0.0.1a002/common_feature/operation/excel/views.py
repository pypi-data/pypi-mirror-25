#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sample:
class SampleView(SampleClass, TemplateView):

    template_name = ''

    def get_context_data(self, *args, **kwargs):
        context = super(SampleView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
"""