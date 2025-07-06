from .models import FooterInfo

def footer_context(request):
    footer = FooterInfo.objects.first()
    return {'footer': footer}