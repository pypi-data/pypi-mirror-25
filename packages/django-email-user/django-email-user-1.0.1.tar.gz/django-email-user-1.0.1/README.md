# django-email-user

Abstract models + utils to replace `django.contrib.auth.User` with a model that uses an email
address instead of a username.


## Installation

```
pip install django-email-user
```


## Usage:

```python
# my_auth/models.py

from email_user.models import EmailBasedUser


class User(EmailBasedUser):
    pass
```

```python
# my_auth/admin.py

from email_user.admin import EmailBasedUserAdmin
from django.contrib.admin import register
from . import models


@register(models.User)
class UserAdmin(EmailBasedUserAdmin):
    pass
```

```python
# in project settings

INSTALLED_APPS = (
    # '...',
    'my_auth',
)

AUTH_USER_MODEL = 'my_auth.User'
```


## History

This codebase is largely derived from [django-generic](https://bitbucket.org/drmeers/django-generic/) and
[django-polymorphic-auth](https://github.com/ixc/django-polymorphic-auth).
