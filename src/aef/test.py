
class Test():
    @staticmethod
    def contstruct():
        print("This")

    def __init__(self) -> None:
        print("This")

class Der(Test):
    @staticmethod
    def construct(name):
        print(name)

    def __init__(self, name) -> None:
        super().__init__()
        print(name)


Test.contstruct()
Der.construct()
Der.construct("Hello")