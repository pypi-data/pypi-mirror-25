#    Full page slider plugin for Django CMS
#    Copyright (C) 2017 Dmitriy Selischev
#    The MIT License (MIT)
#    
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files
#    (the "Software"), to deal in the Software without restriction,
#    including without limitation the rights to use, copy, modify, merge,
#    publish, distribute, sublicense, and/or sell copies of the Software,
#    and to permit persons to whom the Software is furnished to do so,
#    subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from djangocms_fullslider.models import FullSlider, FullSlide
from djangocms_fullslider.settings import app_settings
from djangocms_fullslider.forms import SlideForm


class FullSliderPlugin(CMSPluginBase):
    model = FullSlider
    cache = False
    name = _("Slider")
    module = _("Fullslider plugin")
    allow_children = True
    child_classes = ["FullSlidePlugin"]
    render_template = "djangocms_fullslider/slider.html"
    fieldsets = (
        (None, {
            "fields": [
                "autoplay",
                "loop"
            ]
        }),
        (_("Advanced settings"), {
            "classes": ("collapse",),
            "fields": [
                "slide",
                "timer",
                "delay",
                "transitionDuration"
            ]
        })
    )

    def render(self, context, instance, placeholder):
        context = super(FullSliderPlugin, self).render(context, instance, placeholder)
        context['app_settings'] = app_settings
        return context


plugin_pool.register_plugin(FullSliderPlugin)


class FullSlidePlugin(CMSPluginBase):
    model = FullSlide
    cache = False
    name = _("Slide")
    module = _("Fullslider plugin")
    require_parent = True
    allow_children = False
    parent_classes = ["FullSliderPlugin"]
    form = SlideForm
    render_template = "djangocms_fullslider/slide.html"

    def render(self, context, instance, placeholder):
        context = super(FullSlidePlugin, self).render(context, instance, placeholder)
        context['url'] = instance.image.url if instance.image is not None else instance.link
        return context


plugin_pool.register_plugin(FullSlidePlugin)
