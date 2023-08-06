import six

if six.PY2:
    from blogstrap import create_app  # noqa
else:
    from blogstrap.blogstrap import create_app  # noqa
