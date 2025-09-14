# Run information file

def run(data: str):
    # data is a file under data/finaleScope/.
    
    # add manage.py before file
    file = open("./data/finaleScope/" + data, "r", encoding="utf-8").read()
    manageFile = "import toolsbot.plugins.finaleScopeController.manager as manager\n"
    file = manageFile + file
    
    # exec
    namespace = {}
    exec(file, namespace)
    
    # return scope
    return namespace['scope']