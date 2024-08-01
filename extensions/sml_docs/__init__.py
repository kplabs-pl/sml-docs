from sphinx.application import Sphinx
from sphinx.util.typing import ExtensionMetadata

from . import tutorial_machine


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_role('tutorial-machine', tutorial_machine.TutorialMachine())
    app.add_node(tutorial_machine.tutorial_machine, html=(tutorial_machine.visit_tutorial_machine, None))

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
