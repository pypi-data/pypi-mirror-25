import logging
import six
import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder


logger = logging.getLogger(__file__)

register = template.Library()


@register.filter
def json_dump(object):
    return json.dumps(object, indent=2, cls=DjangoJSONEncoder)


# NOTE: from https://stackoverflow.com/a/1242107
@register.filter
def oxford_join(obj_list):
    """Takes a list of objects and returns their unicode representations,
    seperated by commas and with 'and' between the penultimate and final items
    For example, for a list of fruit objects:
    [<Fruit: apples>,<Fruit: oranges>,<Fruit: pears>] ->
     'apples, oranges, and pears'
    """
    if not obj_list:
        return ""
    l = len(obj_list)
    if l == 1:
        return u"%s" % obj_list[0]
    else:
        return (", ".join(six.u(obj) for obj in obj_list[:l - 1]) +
                ", and " + six.u(obj_list[l - 1]))
