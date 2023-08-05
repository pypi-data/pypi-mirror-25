# Immaterial for Python

Helper functions to integrate [Immaterial UI](https://www.npmjs.com/package/immaterial-ui) with [Bootstrap 3 for Django](https://github.com/dyve/django-bootstrap3) (aka "`django-bootstrap3`").

For now, this module does just one thing: provides a `field_renderer` class for integrating `django-bootstrap3`'s `{% bootstrap_form %}` template tag. This field renderer will output form fields into a markup that's ready for styling by Immaterial.


## Integration

To make this package's `field_renderer` class available to `django-bootstrap3`, add the following to your Django project's `settings.py`  file:

```python
BOOTSTRAP3 = {
    'field_renderers': {
        'default': 'bootstrap3.renderers.FieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
        'immaterial': 'staff.field_renderers.ImmaterialFieldRenderer',
    },

    # ... Additional project-specific django-bootstrap3 settings here.
}
```

Note that the first two values in the `BOOTSTRAP3.field_renderers` dictionary are the default renderers.

You can see a list of other settings for `django-bootstrap3` on [this page](https://django-bootstrap3.readthedocs.io/en/latest/settings.html) of its documentation.

Then, from your template, call the `bootstrap_form` template tag like so:

```html
{% bootstrap_form form_var layout='immaterial' %}
```

where `form_var` is the form you wish to render.
