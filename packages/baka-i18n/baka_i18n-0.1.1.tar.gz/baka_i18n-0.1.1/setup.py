# -*- coding: utf-8 -*-
"""
baka_i18n for baka framework or pyramid
------------------------------------------


Management locale 118n for baka framework and Pyramid


Basic usage
```````````

.. code:: yaml
package: {your_root_package_or_egg}
armor:
    config: configs # config folder
    assets: assets # assets folder
    bundles: assets.yaml # filename assets config
    url: static
    debug: False
    manifest: file
    cache: False
    auto_build: True


in assets.yaml

.. code::

    css-vendor:
        filters: scss,cssmin
        depends: '**/*.scss'
        output: {your_root_package_or_egg}:public/vendor.%(version)s.css
        contents: styles/app.scss


    js-vendor:
        config:
          UGLIFYJS_BIN: ./node_modules/.bin/uglifyjs
        filters: uglifyjs
        output: {your_root_package_or_egg}:public/vendor.%(version)s.js
        contents:
          - javascripts/pace.js
          - javascripts/moment-with-locales.js
          - javascripts/jquery.js
          - javascripts/handlebars.js
          - javascripts/handlers-jquery.js
          - javascripts/cookies.js
          - javascripts/lodash.js
          - javascripts/materialize.js


setup to config
```````````````
in python code


.. code:: python

    config.include('baka_armor')


in development.ini


.. code::

    pyramid.includes =
        pyramid_debugtoolbar
        baka_armor


Usage in mako template
```````````````````````

.. code::
    % for url in request.web_env['js-vendor'].urls():
      <script src="${request.static_url(url)}" />
    % endfor


.. code:: python

    js = Bundle('js/main.js', filters='uglifyjs', output='bundle.js',
                depends='js/**/*.js')

"""
from setuptools import setup, find_packages


setup(name='baka_i18n',
      version='0.1.1',
      description='i18n localization for Baka and Pyramid',
      long_description=__doc__,
      author='Nanang Suryadi',
      license='MIT',
      author_email='nanang.jobs@gmail.com',
      url='https://github.com/baka-framework/baka_i18n',
      packages=find_packages(),
      keywords=['baka framework', 'i18n', 'baka i18n', 'pyramid i18n'],
      install_requires=['pyramid',
                        'Babel',
                        'trafaret',
                        'WebHelpers2',
                        'pytz',
                        'python-dateutil',
                        'bitmath',
                        'Babel',
                        'pyScss',
                        'PyExecJS',
                        'jsmin',
                        'cssmin',
                        'plim'],
      test_suite='',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
      ])
