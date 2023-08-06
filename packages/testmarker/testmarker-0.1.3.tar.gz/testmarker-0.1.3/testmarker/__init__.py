import logging
import os
from collections import OrderedDict
import unittest
from unittest.loader import _FailedTest
logger = logging.getLogger(__name__)


def lookup_environ_skip_status(marker, default=False):
    name = marker.name.upper()
    is_not_skip = os.environ.get(name)
    if is_not_skip is not None:
        return not bool(is_not_skip)
    is_skip = os.environ.get("NO_" + name)
    if is_skip is not None:
        return bool(is_skip)
    return default


class _Marker:
    def __init__(self, name, fn, *, description=None, skip=False):
        self.name = name
        self.reason = description or name
        self.fn = fn
        self.default = skip
        self.is_skip = None

    def skip_activate(self):
        logger.debug("skip activate marker=%s", self)
        self.is_skip = True

    def skip_deactivate(self):
        logger.debug("skip deactivate marker=%s", self)
        self.is_skip = False

    def __str__(self):
        return "<{self.__class__.__name__} name='{self.name}'>".format(self=self)

    def __call__(self, test_item):
        setattr(test_item, _MARKED_ATTR_NAME, self.name)  # xxx
        if self.is_skip is None:
            self.is_skip = self.fn(self, default=self.default)
        return unittest.skipIf(self.is_skip, self.reason)(test_item)


_MARKED_ATTR_NAME = "_marked"


def _apply_force_skip_testcase(fmt, cls=unittest.TestCase):
    originalSetupClass = cls.setUpClass.__func__

    @classmethod
    def setup_class(cls):
        if issubclass(cls, _FailedTest):
            return originalSetupClass(cls)

        if _MARKED_ATTR_NAME not in cls.__dict__:
            skip_class = True
            for name, attr in cls.__dict__.items():
                if name.startswith("test") and callable(attr):
                    if hasattr(attr, _MARKED_ATTR_NAME):
                        skip_class = False
                    else:
                        setattr(cls, name, unittest.skip(fmt.format("{}.{}".format(cls.__name__, name)))(attr))
            if skip_class:
                raise unittest.SkipTest(fmt.format(cls.__name__))
        return originalSetupClass(cls)

    cls.setUpClass = setup_class


class Repository:
    def __init__(self, fn):
        self.pool = OrderedDict()
        self.fn = fn
        self.registered_actions = {}

    def __getitem__(self, name):
        return self.pool[name]

    @property
    def markers(self):
        return self.pool.values()

    def create_marker(self, name, *, description=None, skip=False):
        marker = self.pool[name] = _Marker(name, fn=self.fn, description=description, skip=skip)
        if name in self.registered_actions:
            getattr(marker, self.registered_actions[name])()
        elif "" in self.registered_actions:
            getattr(marker, self.registered_actions[""])()
        return marker

    def register_action(self, name, action):
        self.registered_actions[name] = action


class Manager:
    def __init__(self, repository):
        self.repository = repository

    def __getattr__(self, name):
        try:
            return self.repository[name]
        except KeyError:
            raise AttributeError(name)

    def create_marker(self, name, *, description=None, skip=False):
        return self.repository.create_marker(name, description=description, skip=skip)

    __call__ = create_marker

    def only(self, names, *, skip_unmarked=False, fmt="{} is skipped by --only option"):
        for name in names:
            self.repository.register_action(name, "skip_deactivate")
        self.repository.register_action("", "skip_activate")
        for marker in self:
            if marker.name in names:
                marker.skip_deactivate()

        if skip_unmarked:
            _apply_force_skip_testcase(fmt)

    def ignore(self, names):
        for name in names:
            self.repository.register_action(name, "skip_activate")
        for marker in self:
            if marker.name in names:
                marker.skip_activate()

    def __iter__(self):
        return iter(self.repository.markers)


class FluffyManager(Manager):
    def __getattr__(self, name):
        try:
            return self.repository[name]
        except KeyError:
            return self.create_marker(name)

    def freeze(self):
        self.__class__ = Manager


mark = FluffyManager(Repository(lookup_environ_skip_status))
