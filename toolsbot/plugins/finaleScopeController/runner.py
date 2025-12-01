# Run information file

def run(data: str):
    # data is a file under data/finaleScope/.

    # add manage.py before file
    with open("./data/finaleScope/" + data, "r", encoding="utf-8") as f:
        file = f.read()
    with open("./toolsbot/plugins/finaleScopeController/manager.py", "r", encoding="utf-8") as f:
        manageFile = f.read() + "\n\n"
    file = manageFile + file

    # exec
    namespace = {}
    exec(file, namespace)

    # return scope
    return namespace['scope']