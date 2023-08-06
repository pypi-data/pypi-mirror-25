from distutils.core import setup
import tests

setup \
(
    name='camel-case-switcher',
    version='1.0',
    packages=['camel_case_switcher'],
    test_suite = 'tests',
    url='https://gitlab.com/Hares/camel-case-switcher',
    download_url='https://gitlab.com/Hares/camel-case-switcher/repository/master/archive.tar.gz',
    license='MIT',
    author='USSX Hares / Peter Zaitcev',
    author_email='ussx.hares@yandex.ru',
    description='Python tool for changing style in name of functions etc. from camelCase/CamelCase to the underscope_style.',
    keywords=['camel_case', 'strings', 'undescope_style'],
)
