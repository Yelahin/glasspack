menu = [
    {"title": "Home", "name": "home"},
    {"title": "About us", "name": "about"},
    {"title": "Products", "name": "products"},
    {"title": "Contact us", "name": "contact"},
]


class DataMixin:
    menu = None
    title = None
    page_content = None
    extra_context = {}

    def __init__(self):
        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

        if self.title is not None:
            self.extra_context['title'] = self.title

        if self.page_content is not None:
            self.extra_context['page_content'] = self.page_content


    def get_mixin_content(self, context, **kwargs):
        context['menu'] = menu
        context['title'] = self.title
        context['page_content'] = self.page_content
        context.update(kwargs)
        return context