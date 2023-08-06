
from bootstrap.myapp import bootstrap
from app.console.manager import Manager

app = bootstrap()
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
