from cement.core.foundation import CementApp
from config import NAME, BANNER
from controllers import (
    BaseController,
    GenerateController
)

class App(CementApp):
    class Meta:
        label = NAME
        base_controller = BaseController
        handlers = [
            GenerateController
        ]

def main():
    with App() as app:
        print(BANNER)
        app.run()

if __name__ == '__main__':
    main()
