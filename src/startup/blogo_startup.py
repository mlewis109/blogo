import inspect
from functools import wraps
from pprint import pprint
from console_python import replace_help
import console_python


@wraps(replace_help)
def custom_convenience(namspace):
    """Add custom convenience definitions."""
    replace_help(namspace)
    import blogo
    import blogo_utils
    members = inspect.getmembers(blogo_utils) + inspect.getmembers(blogo)
    for (member_name, member_object) in members:
        if ((member_name not in ["register", "unregister"])
                and (inspect.isfunction(member_object) or inspect.isclass(member_object))
                and (member_name not in namspace)):
            namspace[member_name] = member_object
    
    

def register():
    console_python.replace_help = custom_convenience

def unregister():
    console_python.replace_help = replace_help
    
if __name__ == "__main__":
    register()