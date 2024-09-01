from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
    CursorPagination,
)
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    """重写PageNumberPagination, 实现ModelViewSet可调用、自定义返回样式、实现size控制"""

    page_size = 10  # 设置默认每页返回数据量
    page_size_query_param = "size"  # 自定义page_size在链接中的参数名称
    max_page_size = 50  # 设置每页最大数据返回量

    # 重写数据分页返回样式
    def get_paginated_response(self, data):
        currentPage = int(self.get_page_number(self.request, self.page.paginator)) or 1
        limit = int(self.get_page_size(self.request)) or 10
        total = self.page.paginator.count if self.page else 0
        return Response(
            {
                "page": currentPage,
                "limit": limit,
                "total": total,
                "results": data,
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
            }
        )


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 50

class CustomCursorPagination(CursorPagination):
    page_size = 10
    page_size_query_param = "page_size"
    cursor_query_param = "cursor"
    ordering = "id" # 默认采用“created”进行排序，故自定义排序字段