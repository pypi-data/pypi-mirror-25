from django.template import Library, Context, Template
import importlib


register = Library()


@register.simple_tag(takes_context=True)
def render_plugin(context, plugin_obj):
    pmod = importlib.import_module(plugin_obj.pythonpath)
    p = pmod.Plugin()
    t = Template(p.render_html())
    return t.render(Context(context))
