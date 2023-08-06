import re
from django import template
from django.utils.translation import ugettext_lazy as _


register = template.Library()


# Copied from https://www.djangosnippets.org/snippets/9/

class ExprNode(template.Node):
    def __init__(self, expr_string, var_name):
        self.expr_string = expr_string
        self.var_name = var_name

    def render(self, context):
        from django.template.context import RequestContext, Context
        try:
            clist = list(context)
            clist.reverse()
            d = {}
            d['_'] = _
            for c in clist:
                if isinstance(c, RequestContext) or isinstance(c, Context):
                    for item in c:
                        if isinstance(item, dict):
                            d.update(item)
                else:
                    d.update(c)
            if self.var_name:
                context[self.var_name] = eval(self.expr_string, d)
                return ''
            else:
                return str(eval(self.expr_string, d))
        except:
            raise


r_expr = re.compile(r'(.*?)\s+as\s+(\w+)', re.DOTALL)


def do_expr(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents[0])
    m = r_expr.search(arg)
    if m:
        expr_string, var_name = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError(
                "%r tag at least require one argument" % tag_name)

        expr_string, var_name = arg, None
    return ExprNode(expr_string, var_name)


do_expr = register.tag('expr', do_expr)


class ImportObjectNode(template.Node):
    def __init__(self, import_string, var_name):
        self.import_string = import_string
        self.var_name = var_name

    def render(self, context):
        from apps.core.utils import load_object
        try:
            if self.var_name:
                context[self.var_name] = load_object(self.import_string)
                return ''
            else:
                return str(load_object(self.import_string))
        except:
            raise


r_expr = re.compile(r'(.*?)\s+as\s+(\w+)', re.DOTALL)


def do_load_object(parser, token):
    """
    Syntax:
    {% load_object apps.equipment.models.Equipment as equipment %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents[0])
    m = r_expr.search(arg)
    if m:
        expr_string, var_name = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError(
                "%r tag at least require one argument" % tag_name)

        expr_string, var_name = arg, None
    return ImportObjectNode(expr_string, var_name)


do_load_object = register.tag('load_object', do_load_object)
