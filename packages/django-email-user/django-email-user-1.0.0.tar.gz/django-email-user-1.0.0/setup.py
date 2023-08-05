import setuptools
import email_user

setuptools.setup(
    name='django-email-user',
    version=email_user.__version__,
    author='Interaction Consortium',
    author_email='studio@interaction.net.au',
    url='https://github.com/ixc/django-email-user',
    description='Abstract models + utils to replace `django.contrib.auth.User` with a model that uses an email '
                'address instead of a username',
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
)