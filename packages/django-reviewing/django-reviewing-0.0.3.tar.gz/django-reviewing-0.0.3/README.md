# Django Reviewing

[![Build Status](https://travis-ci.org/JostCrow/django-reviewing.svg?branch=master)](https://travis-ci.org/JostCrow/django-reviewing)
[![codecov](https://codecov.io/gh/JostCrow/django-reviewing/branch/master/graph/badge.svg)](https://codecov.io/gh/JostCrow/django-reviewing)
[![Lintly](https://lintly.com/gh/JostCrow/django-reviewing/badge.svg)](https://lintly.com/gh/JostCrow/django-reviewing/)

## Installation

Install with pip

```shell
pip install django-reviewing
```

Add *'django-reviewing'* to the installed apps

```python
# settings.py

INSTALLED_APPS = [
    ...
    'reviews',
    ...
]
```

<!-- ```python
# urls.py

urlpatterns = [
    ...
    url(r'^reviews/', include('reviews.urls', namespace='reviews')),
    ...
]
``` -->

## Settings

There are several settings which you can use within settings.py:

```python
    REVIEWS_IS_MODERATED = False
    # If True the admin has to publish a review manually. Otherwise a review is public right after it has been added.

    REVIEWS_SHOW_PREVIEW = False
    # If True a preview is displayed to the user before he can submit the review.

    REVIEWS_IS_EMAIL_REQUIRED = False
    # If True the e-mail field of the review is mandatory. (if the user is anonymous)

    REVIEWS_IS_NAME_REQUIRED = False
    # If True the name field of the review is mandatory. (if the user is anonymous)
```

## Usage

Add the provided tags to your templates

```html
    {% load reviews_tags %}

    <html>
        <head>
            <title>{{ flatpage.title }}</title>
        </head>
        <body>
            {{ flatpage.content }}
            {% average_for_instance flatpage %}

            <hr>
            {% reviews_for_instance flatpage %}

        </body>
    </html>
```

## Example

There is a simple example provided with this product.

To install it just make sure *django.contrib.flatpages* has been installed (a
flatpage will serve as our test content) and add reviews.example to
*INSTALLED_APPS*.

Now add a flatpage and browse to it. You should be able to add reviews to the
flatpage now.
