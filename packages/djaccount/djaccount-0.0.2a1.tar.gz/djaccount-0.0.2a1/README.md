# Django Account

Account app for the Django framework provides an email based user object

## Simple usage

1. Install by running `pip install djaccount`

2. Add the following settings to your `settings.py` file
    ```python
    INSTALLED_APPS = [
        # contrib and other apps here
        'account',
        # some more custom apps here
    ]
    AUTH_USER_MODEL = 'account.Account'
    LOGIN_URL = '/account/login/'
    LOGIN_REDIRECT_URL = '/account/'
    LOGOUT_REDIRECT_URL = '/'
    ```

3. Add the account URLs to your `urls.py` file
    ```python
    urlpatterns = [
        url(r'^account/', include('account.urls', namespace='account')),
    ]
    ```

4. Run `django-admin migrate`

## Integrated usage

**TBD**

## License

See [LICENSE](LICENSE)

Some of the work was made as part of my job at [Sync.me](https://sync.me)
