from .models import FooterInfo
from .utils import menu

def footer_context(request):
    footer = FooterInfo.objects.first()
    return {'footer': footer}

def get_pages_menu(request):
    return {'menu': menu}