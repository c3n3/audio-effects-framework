import os
from aef.tree.node import Node
from aef.io.out import Out
from aef.tools.type import Type
from aef.apps.presets.preset import Preset
from aef.tools.editable_node import EditableNode
from aef.pd.pd_handler import PdHandler
from aef.messaging.central_router import CentralRouter
from aef.messaging.msg_list import PresetMessage
class Presets(Node):
    """Represents the Presets menu item
    """
    inited = False
    presetsFolder = "./presets/"
    def __init__(self):
        """Simple init
        """
        self.title = "Presets"
        self.c = ''
        self.child = None
        self.parent = None
        self.right = None
        self.left = None

    def hover(self):
        """Called when user hovers on menu item
        """
        Out.clearSetTop("Presets")

    def init(self):
        """Called fist when somebody presses enter on item
        """
        self.editing = None
        self.creating = False
        self.index = 0
        self.child = EditableNode(Preset())
        self.child.parent = self
        cur = self.child
        for root, dirs, files in os.walk("./presets/", topdown=False):
            for name in files:
                cur.right = EditableNode(Preset("./presets/{}".format(name)))
                cur.right.left = cur
                cur = cur.right
                cur.parent = self
        self.child.left = cur
        cur.right = self.child

if (not Presets.inited):
    CentralRouter.addConsumer([PresetMessage.msgId], CentralRouter.GLOBAL_SUBSCRIPTION, Presets)
    Presets.inited = True
