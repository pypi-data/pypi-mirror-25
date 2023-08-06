DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
INSTALLED_APPS=(
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'appodeal',
)
SITE_ID=1
SECRET_KEY='this-is-just-for-tests-so-not-that-secret'
DEBUG=True
ROOT_URLCONF='tests.urls'
APPODEAL_REWARD_CREATE_HANDLER='tests.handler.appodeal_reward_create_handler'
APPODEAL_SECRET_ANDROID='qwerty'
APPODEAL_SECRET_IOS='what'
