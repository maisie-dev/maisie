class NestedResponse:
    def __init__(self, schema=None, many=False, pagination=None, **kwargs):
        self.schema = schema
        self.many = many
        self.pagination = pagination
        self.kwargs = kwargs

    def gather_pagination_info(self):
        pagination = self.pagination

        return {
            "has_next": self.pagination.has_next,
            "has_prev": self.pagination.has_prev,
            "page": self.pagination.page,
            "per_page": self.pagination.per_page,
            "total_pages": self.pagination.pages,
            "total_items": self.pagination.total,
        }

    def dump(self, data):
        response = {}
        if self.schema != None:
            data = self.schema(many=self.many, **self.kwargs).dump(data)
        response["data"] = data
        if self.pagination != None:
            response["pagination"] = self.gather_pagination_info()

        return response


def str_type(min_length=None, max_length=None):
    def validate(str_to_check):
        if len(str_to_check) == 0:
            raise ValueError(f"String must be at least 1 character long")
        if min_length and len(str_to_check) < min_length:
            raise ValueError(f"String must be at least {min_length} characters long")
        if max_length and len(str_to_check) > max_length:
            raise ValueError(f"String must be at most {max_length} characters long")
        return str_to_check

    return validate
