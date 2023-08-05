#!/usr/bin/python
# -*- coding: UTF-8 -*-

from base64 import b32encode
from binascii import unhexlify

import datetime
from decimal import Decimal
import hashlib
import json
import math
import sys
import pprint

from time import time, sleep
import traceback
from django.shortcuts import render
import decimal

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache, caches
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseServerError, Http404
from django.template import Context, Template, RequestContext
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import is_safe_url
from django.utils.translation import check_for_language, activate

from django.db import transaction, connection
from django.db.models import F, Sum, Q, Count, Max

from django.shortcuts import redirect, render_to_response

from django.template.response import TemplateResponse

from django.utils.crypto import get_random_string, random
from django.utils.translation import ugettext, ugettext_noop
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView, View
from django.utils.module_loading import import_string #from two_factor.compat import import_by_path <-- this is remove in django 1.9 -- will update soon
from django.core.files.storage import DefaultStorage

#from sx.web.utils.shared_captcha import captcha, validate_captcha
import gettext
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
