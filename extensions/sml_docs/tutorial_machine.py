from docutils import nodes
from sphinx.util.docutils import SphinxRole
from sphinx.writers.html5 import HTML5Translator


class tutorial_machine(nodes.container):
    pass


def visit_tutorial_machine(self: HTML5Translator, node: tutorial_machine):
    label = node['label']
    hint = node['hint']
    html = f'<span class="tutorial-machine md-tag" title="{hint}">{label}</span>'
    self.body.append(html)
    raise nodes.SkipNode()


class TutorialMachine(SphinxRole):
    MACHINES = {
        'Vivado': {
            'label': 'Vivado',
            'hint': 'Perform these steps on machine with AMD Vivado Design Suite',
        },
        'Yocto': {
            'label': 'Yocto',
            'hint': 'Perform these steps on machine with Yocto project',
        },
        'EGSE Host': {
            'label': 'EGSE Host',
            'hint': 'Perform these steps on EGSE Host within Smart Mission Lab network',
        },
        'DPU Board': {
            'label': 'DPU Board',
            'hint': 'Perform these steps on a DPU board ',
        },
        'Machine Learning Workstation': {
            'label': 'Machine Learning Workstation',
            'hint': 'Perform these steps on machine with Machine Learning Workstation setup',
        },
        'Vitis AI Deployment Container': {
            'label': 'Vitis AI Deployment Container',
            'hint': 'Perform these steps on machine with Xilinx Vitis AI Deployment Container',
        }
    }
    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        machine = self.text
        info = self.MACHINES.get(machine, None)
        if info is None:
            raise ValueError(f'Unknown machine: {machine}')
        node = tutorial_machine(label=info['label'], hint=info['hint'])
        return [node], []
