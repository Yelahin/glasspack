from .models import FooterContent
from .utils import menu

def footer_context(request):
    footer = FooterContent.objects.first()
    return {'footer': footer}

def get_pages_menu(request):
    return {'menu': menu}