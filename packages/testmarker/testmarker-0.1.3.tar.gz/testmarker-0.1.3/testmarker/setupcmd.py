from setuptools.command.test import test as _test


class test(_test):
    user_options = _test.user_options + [
        ("ignore=", None, "ignore marked"),
        ("only=", None, "only marked"),
    ]

    def initialize_options(self):
        self.ignore = None
        self.only = None
        self.markers = False
        super().initialize_options()

    def get_markers(self):
        from testmarker import mark
        return mark

    def run(self):
        markers = self.get_markers()
        if self.only is not None:
            markers.only([x.strip() for x in self.only.split(",")], skip_unmarked=True)
        elif self.ignore is not None:
            markers.ignore([x.strip() for x in self.ignore.split(",")])
        return super().run()
