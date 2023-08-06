from django.contrib.postgres.fields import JSONField
from django.db.models import Lookup


class JSONDateLookup(Lookup):
    """
    Abstract lookup class for working with dates inside JSON field.
    """
    def get_op(self):
        raise NotImplementedError

    def as_sql(self, compiler, connection):
        """Generates a piece of SQL code for date strings comparison."""
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 'to_date(%s #>> \'{}\', \'YYYY-MM-DD\') %s to_date(trim(both \'"\' from %s), \'YYYY-MM-DD\')' % (
            lhs, self.get_op(), rhs), params


class JSONDateLTLookup(JSONDateLookup):
    """
    'Less then' lookup for dates inside JSON fields.
    """
    lookup_name = 'json_date_lt'

    def get_op(self):
        return '<'


class JSONDateGTLookup(JSONDateLookup):
    """
    'Greater then' lookup for dates inside JSON fields.
    """
    lookup_name = 'json_date_gt'

    def get_op(self):
        return '>'


JSONField.register_lookup(JSONDateLTLookup)
JSONField.register_lookup(JSONDateGTLookup)
