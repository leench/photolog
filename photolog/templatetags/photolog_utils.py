from django import template

register = template.Library()

@register.filter_function
def fix_width(img):
    if img.width > 0:
        return img.width * 180 / img.height
    return 0
