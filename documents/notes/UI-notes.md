# Editing interface

Include (hide-able) fields for displaying orignal values.

When submitting changes, to eTag test - if mismatch, use original value fields to highlight fields whose values changed since the original edit, and conflicts with changes made locally.  This should ensure safe mukltiuser editing.  Also, set flag in data when starting an edit, clear when submitted.  If there is an outstanding edit less than (say) 1 day old, show a warning when starting new edit.

Keep note of most recent record entered for any type/view, and provide option to copy values to new record.


# User interface layout notes

Two popular layout and styling frameworks, Twitter Bootstrap and Zurb Foundation, both appear to provode far more capabilities than I currently know what to do with, and both appear to require Javascript.  They also both use a nestable twelve-column grid structure.

In the first instance, I propose to use a home-grown 12-column grid as the basis for laying out user interface panels.  Later, when I better understand the requirements, and to support mobile devices, I can adopt a more functional layout framework (hopefully retaining the original no-javascript capabilities.)

The basic capabilities, then, are `span1` to `span12` and `offset0` to `offset11`.  These are grouped into rows.  For small displays, the columns may be stacked vertically.  More to come later.

UI "widgets" will be defined to use some given number (1-12) of columns, with optional offset from the preceding widget.


# Web page layout and styling

http://960.gs/
http://www.designinfluences.com/fluid960gs/
http://www.gridsystemgenerator.com/
http://lesscss.org
http://sass-lang.com/guide
http://lessframework.com/
http://blueprintcss.org/
http://bluetrip.org/
http://elasticss.com/
http://twitter.github.com/bootstrap/ (**)
http://foundation.zurb.com (**)

(**) favourites?

Re-evaluate Haystack (**gone)
