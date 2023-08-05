import re

ASSIGNMENT_REGEX = re.compile("!{(.+)=(.+)}") # Regex to find assignment blocks.
INTERP_REGEX = re.compile("\$(\w+)")

class VariableFilter():
    def __init__(self):
        pass

    def Process(self, engine, text):
        value = text
        variable_block = engine.variable_bin

        # register and delete each !{assignment=variable}
        for (name, val) in ASSIGNMENT_REGEX.findall(value):
            variable_block[name] = val
            value = value.replace("!{"+name+"="+val+"}", '').strip("\n").strip(' ')

        if INTERP_REGEX.search(value) is None:
            return value

        # Replace each $var with its variable block value.
        for varname in INTERP_REGEX.findall(value):
            if varname in variable_block:
                value = value.replace("$"+varname, variable_block[varname])

        return value