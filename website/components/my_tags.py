from django import template

register = template.Library()

@register.inclusion_tag('button.html')
def styled_button(text, extra_classes=''):
    return {'text': text, 'extra_classes': extra_classes}