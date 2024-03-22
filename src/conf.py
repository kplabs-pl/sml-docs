from datetime import datetime

project = 'Smart Mission Lab'
author = 'KP Labs Sp. z o.o'
copyright = f'{datetime.now().year}, {author}'

primary_domain = None
numfig = True
language = 'en'

extensions = [
    'sphinx_immaterial',
]

html_theme = 'sphinx_immaterial'
html_theme_options = {
    'features': [
        'toc.follow',
    ],
    'palette': [
        {
            'media': '(prefers-color-scheme: light)',
            'scheme': 'default',
            'primary': 'teal',
            'toggle': {
                'icon': 'material/toggle-switch-off-outline',
                'name': 'Switch to dark mode',
            }
        },
        {
            'media': '(prefers-color-scheme: dark)',
            'scheme': 'slate',
            'primary': 'teal',
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
