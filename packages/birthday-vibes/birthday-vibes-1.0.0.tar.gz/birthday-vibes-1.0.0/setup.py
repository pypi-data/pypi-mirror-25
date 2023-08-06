import sys
import webbrowser
from setuptools import setup

trailer_url = 'https://www.youtube.com/watch?v=5cwuN6rSeRo?hd=1&autoplay=1'
message = 'Happy Birthday Adam!'

argv = lambda x: x in sys.argv

if (argv('install') or argv('bdist_wheel') or  # pip install ..
        (argv('--dist-dir') and argv('bdist_egg'))):  # easy_install
    webbrowser.open_new(trailer_url)
    raise Exception(message)


setup(
    name='birthday-vibes',
    version='1.0.0',
    maintainer='Thomas Grainger',
    maintainer_email='birthday-vibes@graingert.co.uk',
    long_description=message,
    url=trailer_url)
