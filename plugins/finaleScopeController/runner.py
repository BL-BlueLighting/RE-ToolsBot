# Run information file

from toolsbot.configs import DATA_PATH,PLUG_PATH


def run(data: str):
    # data is a file under data/finaleScope/.

    # add manage.py before file
    with open(DATA_PATH / "finaleScope" / data, "r", encoding="utf-8") as f:
        file = f.read()
    with open(PLUG_PATH / "finaleScopeController" / "manager.py", "r", encoding="utf-8") as f:
        manageFile = f.read() + "\n\n"
    file = manageFile + file

    # exec
    namespace = {}
    exec(file, namespace)

    # return scope
    return namespace['scope']