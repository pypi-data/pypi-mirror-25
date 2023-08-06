# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cmsplugin_section.enums import SectionType
from cmsplugin_section.models import Section, SectionButton
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class SectionButtonAdmin(admin.StackedInline):
    model = SectionButton
    extra = 1


class SectionPlugin(CMSPluginBase):
    model = Section
    name = _("Section")
    inlines = (SectionButtonAdmin,)
    allow_children = True
    templates = {
        SectionType.SINGLE_COLUMN: "cmsplugin_section/section_types/single_column.html",
        SectionType.TWO_COLUMNS: "cmsplugin_section/section_types/two_columns.html",
        SectionType.THREE_COLUMNS: "cmsplugin_section/section_types/three_columns.html",
        SectionType.FOUR_COLUMNS: "cmsplugin_section/section_types/four_columns.html",
    }

    def get_render_template(self, context, instance, placeholder):
        return self.templates.get(instance.type, "cmsplugin_section/empty.html")

    def render(self, context, instance, placeholder):
        context["section"] = instance
        return context


plugin_pool.register_plugin(SectionPlugin)
