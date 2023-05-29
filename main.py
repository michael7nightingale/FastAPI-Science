import sys
import os
sys.path.append(os.getcwd())
import uvicorn

from package.database import dump_database
from configuration.server import create_app


def runserver():
    uvicorn.run(
        app="main:create_app",
        port=8000,
        host='localhost',
        reload=True,

     )


if __name__ == "__main__":
    args = sys.argv[1:]
    assert len(args) == 1, "Only one option is allowed."

    options = {'runserver', 'dumpdata'}
    opt = args[0]

    assert opt in options, "There is not such an option: {}. \nAllowed:\n\t-{}".format(opt, "\n\t-".join(options))

    match opt:
        case "runserver":
            runserver()
        case "dumpdata":
            dump_database()


