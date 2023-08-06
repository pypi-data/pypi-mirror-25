#    Thumbnail slider plugin for Django CMS
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

from cms.models import CMSPlugin
from django.db import models


# Create your models here.
class ThumbnailSlider(CMSPlugin):
    enable_thumbnail_carousel = models.BooleanField(blank=False, null=False, default=False)
    items_on_slider = models.IntegerField(blank=True, null=False, default=1)
    loop = models.BooleanField(default=False)
    auto_play = models.BooleanField(default=False)
    additional_classes = models.CharField(blank=True, null=False, max_length=255, default='')
    slide_classes = models.CharField(blank=True, null=False, max_length=255, default='')
    thumbnail_width = models.IntegerField(blank=True, null=False, default=100)
    thumbnail_items = models.IntegerField(blank=True, null=False, default=10)

    def __str__(self):
        return "%s slides" % self.num_children()
