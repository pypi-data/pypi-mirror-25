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

from django.utils.translation import ugettext_lazy as _
from django.db import models
from cms.models import CMSPlugin
from cmsplugin_filer_image.models import FilerImageField


# Create your models here.
class FullSlider(CMSPlugin):
    slide = models.PositiveIntegerField(verbose_name=_("Index number of initial slide"), default=0, blank=False,
                                        null=False)
    timer = models.BooleanField(verbose_name=_("Display timer bar"), default=False, blank=False, null=False)
    autoplay = models.BooleanField(verbose_name=_("Start the Slideshow automatically"), default=True, blank=False,
                                   null=False)
    loop = models.BooleanField(verbose_name=_("Loop the Slideshow"), default=True, blank=False, null=False)
    delay = models.PositiveIntegerField(verbose_name=_("Delay between slides in milliseconds"), default=5000,
                                        blank=False, null=False)
    transitionDuration = models.PositiveIntegerField(verbose_name=_("Transition duration in milliseconds"),
                                                     default=1000, blank=False, null=False)

    def __str__(self):
        return "Slider"


class FullSlide(CMSPlugin):
    image = FilerImageField(verbose_name='Image', null=True, blank=True)
    link = models.URLField(verbose_name='Image link', null=True, blank=True)

    def get_url(self):
        return self.image.url if self.image is not None else self.link

    def __str__(self):
        return "Slide: %s" % self.get_url()
