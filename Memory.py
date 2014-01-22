

class Memory:

    def __init__(self, name): # memory name
    	self.name = name
    	self.table = dict()

    def has_key(self, name):  # variable name
    	return name in self.table

    def get(self, name):         # get from memory current value of variable <name>
    	return self.table.get(name)

    def put(self, name, value):  # puts into memory current value of variable <name>
    	self.table[name] = value

class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
    	self.stack = [  memory ]

    def get(self, name):             # get from memory stack current value of variable <name>
    	return self.stack[-1].get(name)

    def put(self, name, value): # puts into memory stack current value of variable <name>
    	self.stack[-1].put(name, value)

    def push(self, memory): # push memory <memory> onto the stack
    	self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
    	self.stack.pop()

