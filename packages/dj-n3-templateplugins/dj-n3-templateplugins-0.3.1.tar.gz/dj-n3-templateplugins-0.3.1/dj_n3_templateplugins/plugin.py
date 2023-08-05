

class BasePlugin(object):
    pass


class TemplatePlugin(BasePlugin):
    def render_html(self):
        raise NotImplementedError('You must define a .render_html() method for your plugin')

    def get_context_data(self):
        raise NotImplementedError('You must define a .get_context_data() method for your plugin')
