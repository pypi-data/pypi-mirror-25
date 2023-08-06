from django.db.models import Func


class JSONExtractPathText(Func):
    function = 'json_extract_path_text'
    template = '%(function)s(to_json(%(expressions)s), \'%(path)s\')'


class JSONExtractPathDate(Func):
    function = 'json_extract_path_text'
    template = 'to_date(%(function)s(to_json(%(expressions)s), \'%(path)s\'), \'YYYY-MM-DD\')'
