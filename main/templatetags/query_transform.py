from django import template

register = template.Library()

@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    updated["time_after"], updated["time_before"] = kwargs['time_after'], kwargs['time_before']
    return updated.urlencode()