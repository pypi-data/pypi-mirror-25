from django.template import Library, Context, Template
import importlib
from dj_n3_templateplugins.utils import get_plugin_instance


register = Library()


@register.simple_tag(takes_context=True)
def render_plugin(context, plugin_obj):
    plugin_instance = get_plugin_instance(plugin_obj)
    t = Template(plugin_instance.render_html())
    return t.render(Context(context))
