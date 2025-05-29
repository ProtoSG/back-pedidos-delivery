from config import confi
from src import init_app

configuration = confi['development']
app = init_app(configuration)

if __name__=='__main__':
    app.run()
