from django import template
from django.conf import settings
from freemix.canvas.models import Canvas
from django.template.loader import render_to_string
from django.template import Variable

register = template.Library()

def canvases(context):
    return {'STATIC_URL': settings.STATIC_URL,
            'canvases': Canvas.objects.filter(enabled=True)}
canvas_chooser=canvases
@register.inclusion_tag("canvas/chooser.html")
def canvas_chooser(base_url):
    return {'STATIC_URL': settings.STATIC_URL,
            'canvases': Canvas.objects.filter(enabled=True),
            'base_url': base_url}


@register.tag
def canvas_html ( parser, token ):
    try:
        tag_name, option = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents[0]
    return CanvasNode( option, "html" )

@register.tag
def canvas_css(parser, token):
    try:
        tag_name, option = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents[0]
    return CanvasNode( option, "css" )

class CanvasNode ( template.Node ):
    def __init__ ( self, option, type="html" ):
        self.slug = option
        self.type = type

    def render ( self, context ):
        # try:
        if self.type == "css":
            return render_to_string("canvas/canvas.css", {})
        elif self.type == "html":
            slug = Variable(self.slug).resolve(context)
            canvas = Canvas.objects.get(slug=slug)
            return canvas.get_html()

