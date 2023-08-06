
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



