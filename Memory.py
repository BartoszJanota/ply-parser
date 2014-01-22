

class Memory:

    def __init__(self, name): # memory name

    def has_key(self, name):  # variable name

    def get(self, name):         # get from memory current value of variable <name>

    def put(self, name, value):  # puts into memory current value of variable <name>


class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>

    def get(self, name):             # get from memory stack current value of variable <name>

    def put(self, name, value): # puts into memory stack current value of variable <name>

    def push(self, memory): # push memory <memory> onto the stack

    def pop(self):          # pops the top memory from the stack


