# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from varlet.views import PageViewSet

__all__ = ['page_detail_url', 'page_root_url', 'urlpatterns']

page_detail_url = PageViewSet.as_detail_url()
page_root_url = PageViewSet.as_root_url()

urlpatterns = [
    page_detail_url,
    page_root_url,
]
