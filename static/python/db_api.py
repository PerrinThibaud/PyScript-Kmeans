class Database:
    # noinspection PyDefaultArgument
    def __init__(self, data={}):
        self.number: str = data.get('number')
        self.index: str = data.get('index')
        self.maxLeft: str = data.get('maxLeft')
        self.maxRight: str = data.get('maxRight')

    def check_max(self) -> None:
        if self.index > 0 :
            self.maxLeft = False
        else:
            self.maxLeft = True

        if self.index < self.number -1 :
            self.maxRight = False
        else:
            self.maxRight = True

    def move_next(self) -> None:
        self.index = min(self.index + 1, self.number - 1) 
        self.check_max()

    def move_previous(self) -> None:
        self.index = max(self.index - 1, 0)
        self.check_max()

    def increment_db(self) -> None:
        self.number += 1
        self.check_max()

def get_db() -> dict:
    return {
        "number": 0,
        "index": 0,
        "maxLeft": True,
        "maxRight": True
    }

def download_db() -> Database:
    forecast: dict = get_db()

    return Database(forecast)
