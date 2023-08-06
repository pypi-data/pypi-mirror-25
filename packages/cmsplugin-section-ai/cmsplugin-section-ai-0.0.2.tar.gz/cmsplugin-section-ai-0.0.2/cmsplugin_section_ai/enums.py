# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from enumfields import Enum


class SectionType(Enum):
    SINGLE_COLUMN = 1
    TWO_COLUMNS = 2
    THREE_COLUMNS = 3
    FOUR_COLUMNS = 4

    class Labels:
        SINGLE_COLUMN = _("Single column")
        TWO_COLUMNS = _("Two columns")
        THREE_COLUMNS = _("Three columns")
        FOUR_COLUMNS = _("Four columns")


class BackgroundColor(Enum):
    TRANSPARENT = "bg-color-transparent"
    LIGHT_GRAY = "bg-color-light-gray"
    PRIMARY = "bg-color-primary"
    SECONDARY = "bg-color-secondary"

    class Labels:
        TRANSPARENT = _("Transparent")
        LIGHT_GRAY = _("Light Gray")
        PRIMARY = _("Primary Color")
        SECONDARY = _("Secondary Color")


class ButtonStyle(Enum):
    PRIMARY = "btn-primary"
    SECONDARY = "btn-secondary"
    WHITE = "btn-white"
    DARK = "btn-dark"

    class Labels:
        PRIMARY = _("Primary Background")
        SECONDARY = _("Secondary Background")
        WHITE = _("White Background")
        DARK = _("Dark Background")
