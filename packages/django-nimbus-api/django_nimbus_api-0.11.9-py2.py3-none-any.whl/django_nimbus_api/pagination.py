# -*- coding:utf-8 -*-
from base64 import b64decode, b64encode
from collections import OrderedDict, namedtuple
from django.conf import settings
from django.utils import six
from django.utils.encoding import force_text
from django.core.paginator import InvalidPage, EmptyPage
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import remove_query_param, replace_query_param


class APIPageNumberPagination(PageNumberPagination):
    # Client can control the page using this query parameter.
    page_query_param = settings.PAGE_QUERY_PARAM

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = settings.PAGE_SIZE_QUERY_PARAM

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = settings.MAX_PAGE_SIZE

    #display_page_controls = True

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except EmptyPage as exc:
            pass
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        return Response({
            'meta': {
                'count': self.page.paginator.count,
                # 'next': self.get_next_link(),
                # 'previous': self.get_previous_link(),
                # 'html': self.to_html(),
                # 'context': self.get_html_context(),
                'version': self.request.version,
            },
            'results': data
        })

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        # if page_number == 1:
        #     return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)
