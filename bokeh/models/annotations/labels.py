#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2021, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
'''

'''

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import annotations

import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Bokeh imports
from ...core.enums import (
    AngleUnits,
    FontStyle,
    SpatialUnits,
    TextAlign,
    VerticalAlign,
)
from ...core.has_props import abstract
from ...core.properties import (
    Alpha,
    Angle,
    AngleSpec,
    Color,
    Datetime,
    Enum,
    Float,
    Include,
    NonNullable,
    NumberSpec,
    Override,
    String,
    StringSpec,
    field,
)
from ...core.property_mixins import (
    FillProps,
    LineProps,
    ScalarFillProps,
    ScalarLineProps,
    ScalarTextProps,
    TextProps,
)
from ...util.serialization import convert_datetime_type
from .annotation import Annotation, DataAnnotation

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    "Label",
    "LabelSet",
    "Title",
    "TextAnnotation",
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

@abstract
class TextAnnotation(Annotation):
    ''' Base class for text annotation models such as labels and titles.

    '''

class Label(TextAnnotation):
    ''' Render a single text label as an annotation.

    ``Label`` will render a single text label at given ``x`` and ``y``
    coordinates, which can be in either screen (pixel) space, or data (axis
    range) space.

    The label can also be configured with a screen space offset from ``x`` and
    ``y``, by using the ``x_offset`` and ``y_offset`` properties.

    Additionally, the label can be rotated with the ``angle`` property.

    There are also standard text, fill, and line properties to control the
    appearance of the text, its background, as well as the rectangular bounding
    box border.

    See :ref:`userguide_annotations_labels` for information on plotting labels.

    '''

    x = NonNullable(Float, help="""
    The x-coordinate in screen coordinates to locate the text anchors.

    Datetime values are also accepted, but note that they are immediately
    converted to milliseconds-since-epoch.
    """).accepts(Datetime, convert_datetime_type)

    x_units = Enum(SpatialUnits, default='data', help="""
    The unit type for the x attribute. Interpreted as |data units| by
    default.
    """)

    y = NonNullable(Float, help="""
    The y-coordinate in screen coordinates to locate the text anchors.

    Datetime values are also accepted, but note that they are immediately
    converted to milliseconds-since-epoch.
    """).accepts(Datetime, convert_datetime_type)

    y_units = Enum(SpatialUnits, default='data', help="""
    The unit type for the y attribute. Interpreted as |data units| by
    default.
    """)

    text = String(default="", help="""
    The text value to render.
    """)

    angle = Angle(default=0, help="""
    The angle to rotate the text, as measured from the horizontal.
    """)

    angle_units = Enum(AngleUnits, default='rad', help="""
    Acceptable values for units are ``"rad"`` and ``"deg"``
    """)

    x_offset = Float(default=0, help="""
    Offset value to apply to the x-coordinate.

    This is useful, for instance, if it is desired to "float" text a fixed
    distance in |screen units| from a given data position.
    """)

    y_offset = Float(default=0, help="""
    Offset value to apply to the y-coordinate.

    This is useful, for instance, if it is desired to "float" text a fixed
    distance in |screen units| from a given data position.
    """)

    text_props = Include(ScalarTextProps, help="""
    The {prop} values for the text.
    """)

    background_props = Include(ScalarFillProps, prefix="background", help="""
    The {prop} values for the text bounding box.
    """)

    background_fill_color = Override(default=None)

    border_props = Include(ScalarLineProps, prefix="border", help="""
    The {prop} values for the text bounding box.
    """)

    border_line_color = Override(default=None)

class LabelSet(DataAnnotation):
    ''' Render multiple text labels as annotations.

    ``LabelSet`` will render multiple text labels at given ``x`` and ``y``
    coordinates, which can be in either screen (pixel) space, or data (axis
    range) space. In this case (as opposed to the single ``Label`` model),
    ``x`` and ``y`` can also be the name of a column from a
    :class:`~bokeh.models.sources.ColumnDataSource`, in which case the labels
    will be "vectorized" using coordinate values from the specified columns.

    The label can also be configured with a screen space offset from ``x`` and
    ``y``, by using the ``x_offset`` and ``y_offset`` properties. These offsets
    may be vectorized by giving the name of a data source column.

    Additionally, the label can be rotated with the ``angle`` property (which
    may also be a column name.)

    There are also standard text, fill, and line properties to control the
    appearance of the text, its background, as well as the rectangular bounding
    box border.

    The data source is provided by setting the ``source`` property.

    '''

    x = NumberSpec(default=field("x"), help="""
    The x-coordinates to locate the text anchors.
    """)

    x_units = Enum(SpatialUnits, default='data', help="""
    The unit type for the ``xs`` attribute. Interpreted as |data units| by
    default.
    """)

    y = NumberSpec(default=field("y"), help="""
    The y-coordinates to locate the text anchors.
    """)

    y_units = Enum(SpatialUnits, default='data', help="""
    The unit type for the ``ys`` attribute. Interpreted as |data units| by
    default.
    """)

    text = StringSpec(default=field("text"), help="""
    The text values to render.
    """)

    angle = AngleSpec(default=0, help="""
    The angles to rotate the text, as measured from the horizontal.
    """)

    x_offset = NumberSpec(default=0, help="""
    Offset values to apply to the x-coordinates.

    This is useful, for instance, if it is desired to "float" text a fixed
    distance in |screen units| from a given data position.
    """)

    y_offset = NumberSpec(default=0, help="""
    Offset values to apply to the y-coordinates.

    This is useful, for instance, if it is desired to "float" text a fixed
    distance in |screen units| from a given data position.
    """)

    text_props = Include(TextProps, help="""
    The {prop} values for the text.
    """)

    background_props = Include(FillProps, prefix="background", help="""
    The {prop} values for the text bounding box.
    """)

    background_fill_color = Override(default=None)

    border_props = Include(LineProps, prefix="border", help="""
    The {prop} values for the text bounding box.
    """)

    border_line_color = Override(default=None)

class Title(TextAnnotation):
    ''' Render a single title box as an annotation.

    See :ref:`userguide_annotations_titles` for information on plotting titles.

    '''

    text = String(default="", help="""
    The text value to render.
    """)

    vertical_align = Enum(VerticalAlign, default='bottom', help="""
    Alignment of the text in its enclosing space, *across* the direction of the text.
    """)

    align = Enum(TextAlign, default='left', help="""
    Alignment of the text in its enclosing space, *along* the direction of the text.
    """)

    text_line_height = Float(default=1.0, help="""
    How much additional space should be allocated for the title. The value is provided
    as a number, but should be treated as a percentage of font size. The default is
    100%, which means no additional space will be used.
    """)

    offset = Float(default=0, help="""
    Offset the text by a number of pixels (can be positive or negative). Shifts the text in
    different directions based on the location of the title:

        * above: shifts title right
        * right: shifts title down
        * below: shifts title right
        * left: shifts title up

    """)

    standoff = Float(default=10, help="""
    """)

    text_font = String(default="helvetica", help="""
    Name of a font to use for rendering text, e.g., ``'times'``,
    ``'helvetica'``.

    """)

    text_font_size = String(default="13px")

    text_font_style = Enum(FontStyle, default="bold", help="""
    A style to use for rendering text.

    Acceptable values are:

    - ``'normal'`` normal text
    - ``'italic'`` *italic text*
    - ``'bold'`` **bold text**

    """)

    text_color = Color(default="#444444", help="""
    A color to use to fill text with.
    """)

    text_alpha = Alpha(help="""
    An alpha value to use to fill text with.
    """)

    background_props = Include(ScalarFillProps, prefix="background", help="""
    The {prop} values for the text bounding box.
    """)

    background_fill_color = Override(default=None)

    border_props = Include(ScalarLineProps, prefix="border", help="""
    The {prop} values for the text bounding box.
    """)

    border_line_color = Override(default=None)

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
