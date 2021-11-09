from django import template

register = template.Library()


@register.filter
def censor(bad):
    wordfilter_list = [
        'хрень', 'Fuck', 'FUCK',
    ]

    for c in wordfilter_list:
        bad = bad.replace(c, '***')

    return bad