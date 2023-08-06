from terrapin.render_full import render_full
from terrapin.render_simple import render_simple


def render(template, context):
    """ Choose which rendering strategy to use and execute """

    if '{%' in template:
        return render_full(template, context)
    else:
        return render_simple(template, context)
