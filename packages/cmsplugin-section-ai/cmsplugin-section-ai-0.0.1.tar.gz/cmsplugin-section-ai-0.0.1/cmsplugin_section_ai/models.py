# -*- coding: utf-8 -*-
from cms.models import CMSPlugin, Page
from cmsplugin_section.enums import SectionType, BackgroundColor, ButtonStyle
from django.db import models
from django.utils.translation import ugettext_lazy as _
from enumfields import EnumIntegerField, EnumField
from filer.fields.file import FilerFileField


class Section(CMSPlugin):
    type = EnumIntegerField(SectionType, verbose_name=_("section type"), default=SectionType.SINGLE_COLUMN)
    title = models.CharField(
        verbose_name=_("title"),
        max_length=75,
        blank=True,
        help_text=_("Visible title for this section")
    )
    background_color = EnumField(
        BackgroundColor,
        verbose_name=_("background color"),
        max_length=50,
        default=BackgroundColor.TRANSPARENT
    )
    background_image = FilerFileField(
        verbose_name=_(u"background image"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("This overrides any given background color")
    )
    full_width = models.BooleanField(verbose_name=_("make the content 100% wide"), default=False)
    no_top_margin = models.BooleanField(verbose_name=_("remove top margin from this section"), default=False)
    no_bottom_margin = models.BooleanField(verbose_name=_("remove bottom margin from this section"), default=False)
    extra_margin = models.BooleanField(verbose_name=_("add extra vertical margin for content"), default=False)
    text_center = models.BooleanField(verbose_name=_("align content text to center"), default=False)
    anchor = models.CharField(
        verbose_name=_("anchor identifier"),
        max_length=50,
        blank=True,
        help_text=_("Set anchor identifier for this section to be used with anchor links.")
    )

    def __str__(self):
        return "%s - %s" % (self.type.label, self.title)

    @property
    def section_classes(self):
        classes = ""
        if self.no_top_margin and self.no_bottom_margin:
            classes = "no-top-margin no-bottom-margin"
        elif self.no_top_margin:
            classes = "no-top-margin"
        elif self.no_bottom_margin:
            classes = "no-bottom-margin"

        if self.background_image:
            classes += " bg-image"
        else:
            classes += " " + self.background_color.value
        return classes

    @property
    def container_classes(self):
        classes = "container"
        if self.full_width:
            classes += "-fluid"
        if self.text_center:
            classes += " text-center"
        return classes

    def copy_relations(self, oldinstance):
        for button in oldinstance.section_buttons.all():
            button.pk = None
            button.id = None
            button.section = self
            button.save(force_insert=True)


class Link(models.Model):
    text = models.CharField(verbose_name=_("button text"), max_length=75)
    url = models.CharField(verbose_name=_("url"), max_length=250, blank=True)
    page_link = models.ForeignKey(
        Page,
        verbose_name=_("link to a page"),
        null=True,
        blank=True,
        limit_choices_to={"publisher_is_draft": True},
        on_delete=models.SET_NULL,
        help_text=_("Page link overrides any given URL."),
        related_name="section"
    )
    style = EnumField(ButtonStyle, verbose_name=_("Button style"), max_length=50, default=ButtonStyle.PRIMARY)
    anchor = models.CharField(
        verbose_name=_("bind to anchor"),
        max_length=30,
        blank=True,
        help_text=_("Set the anchor identifier of an element. Leave out the # prefix.")
    )

    def __str__(self):
        return self.text

    @property
    def link(self):
        link = ""
        if self.page_link:
            link = self.page_link.get_absolute_url()
        elif self.url:
            link = self.url
        if self.anchor:
            return "%s#%s" % (link, self.anchor)
        return link or "#"


class SectionButton(Link):
    section = models.ForeignKey(Section, verbose_name=_("section"), related_name="section_buttons")
