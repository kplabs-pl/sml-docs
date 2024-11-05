from datetime import datetime
import os

project = 'Smart Mission Lab'
author = 'KP Labs Sp. z o.o'
copyright = f'{datetime.now().year}, {author}'

primary_domain = None
numfig = True
language = 'en'

extensions = [
    'sphinx_immaterial',
    'sml_docs',
]

html_theme = 'sphinx_immaterial'
html_logo = 'images/logo-kplabs.png'
html_favicon = 'images/favicon.ico'
html_static_path = ['_static']
templates_path = ['_templates']
html_css_files = [
    'custom.css',
]
html_theme_options = {
    'features': [
        'toc.follow',
    ],
    'palette': [
        {
            'media': '(prefers-color-scheme: light)',
            'scheme': 'default',
            'toggle': {
                'icon': 'material/toggle-switch-off-outline',
                'name': 'Switch to dark mode',
            }
        },
        {
            'media': '(prefers-color-scheme: dark)',
            'scheme': 'slate',
            'toggle': {
                'icon': 'material/toggle-switch',
                'name': 'Switch to light mode',
            }
        },
    ],
    'social': [
        {
            'icon': 'fontawesome/brands/twitter',
            'link': 'https://twitter.com/labs_kp/',
            'name': 'KP Labs on X',
        },
    ],
}

google_analytics_token = os.environ.get('GA_TOKEN', None)

if google_analytics_token is not None:
    html_theme_options['analytics'] = {
        'provider': 'google',
        'property': google_analytics_token,
    }
    html_theme_options['consent'] = {
        'title': 'Cookie consent',
        'description': '''
      We use cookies to recognize your repeated visits and preferences, as well
      as to measure the effectiveness of our documentation and whether users
      find what they're searching for. With your consent, you're helping us to
      make our documentation better.
        '''
    }
