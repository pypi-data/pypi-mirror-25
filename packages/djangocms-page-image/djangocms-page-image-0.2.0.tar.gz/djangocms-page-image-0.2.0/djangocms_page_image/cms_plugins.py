from django.db.models import Q
from django.template.loader import select_template

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from django.utils.translation import ugettext_lazy as _

from .models import ChildPagePreviewPlugin


class CMSChildPagePreviewPlugin(CMSPluginBase):
    model = ChildPagePreviewPlugin
    name = _("Child Page Preview")

    TEMPLATE_NAME = "djangocms_page_image/plugins/%s.html"
    render_template = TEMPLATE_NAME % 'child_page_preview'

    #Search
    search_fields = []

    def render(self, context, instance, placeholder):
        self.render_template = select_template((
            self.TEMPLATE_NAME % instance.style,
            self.render_template,
        ))
        request = context['request']
        if request.user.has_perm('cms.can_change'):
            subpages = instance.placeholder.page.children.all()
        else:
            subpages = instance.placeholder.page.children.published()
        context['subpages'] = subpages.filter(
            Q(imageextension__show_preview=True) |
            Q(imageextension__isnull=True)
        )
        context['instance'] = instance
        return context

plugin_pool.register_plugin(CMSChildPagePreviewPlugin)
