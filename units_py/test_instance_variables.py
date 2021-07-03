class Foo:

    def __init__(self) -> None:
        super().__init__()
        self.name = "Foo"

    def get_foo_name(self):
        print("Foo: ", self.name)


class Bar(Foo):

    def __init__(self) -> None:
        super().__init__()
        self.name = "Bar"

    def get_bar_name(self):
        print("Bar: ", self.name)


if __name__ == '__main__':
    test = Bar()
    test.get_foo_name()
    test.get_bar_name()