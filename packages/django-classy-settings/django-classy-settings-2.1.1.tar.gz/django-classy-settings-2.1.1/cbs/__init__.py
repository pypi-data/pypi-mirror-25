
from functools import partial
import importlib
from inspect import ismethod
import os

from .utils import as_bool


DEFAULT_ENV_PREFIX = ''


class env:
    '''
    Decorator to make environ based settings simpler.

    @env
    def SOMETHING_KEY(self):
        return 'default'

    You can override the key to use in the env:


    @env(key='OTHER_NAME')
    def SETTINGS_NAME(self):
        ...

    Or, if you want the env to have a prefix not in settings:

    @env(prefix='MY_')
    def SETTING(self):
        ...

    ``key`` and ``prefix`` can be used together.

    You can pass a caster / validator:

    @env(cast=int)
    def SETTING(self):
    '''
    def __new__(cls, *args, **kwargs):
        if 'type' in kwargs and 'cast' not in kwargs:
            kwargs['cast'] = kwargs.pop('type')
        if not args:
            return partial(cls, **kwargs)
        return object.__new__(cls)

    def __init__(self, getter, key=None, cast=None, prefix=None):
        self.getter = getter
        self.cast = cast
        self.key = key or getter.__name__
        if prefix is None:
            prefix = DEFAULT_ENV_PREFIX
        self.var_name = ''.join([prefix, self.key])

    def __get__(self, obj, klass=None):
        if obj is None:
            return self
        try:
            value = os.environ[self.var_name]
        except KeyError:
            if self.getter is None:
                raise RuntimeError(
                    'You must set the %s environment variable.' % self.var_name
                )
            value = self.getter(obj)
        else:
            if self.cast:
                value = self.cast(value)
        obj.__dict__[self.key] = value
        return value


class envbool(env):
    '''
    A special case of env that returns a boolean.
    '''
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('cast', as_bool)
        super().__init__(*args, **kwargs)


def apply(name, to):
    '''
    Apply settings to ``to``, which is expected to be globals().

    Place at the end of settings.py / settings/__init__.py to apply a given
    settings class.

    Pass a settings class:
        cbs.apply(MySettings, globals())

    Pass a class name:
        cbs.apply('MySettings', globals())

    Pass an import path:
        cbs.apply('settings.my.MySettings', globals())

    '''
    if isinstance(name, str):
        if '.' in name:
            module, obj_name = name.rsplit('.', 1)
            module = importlib.import_module(module)
            obj = getattr(module, obj_name)
        else:
            obj = to.get(name)
    else:
        obj = name

    if obj is None:
        raise ValueError('Could not find settings class: %r', name)

    settings = obj()

    def resolve_callable(value):
        if ismethod(value):
            return value()
        return value

    to.update({
        key: resolve_callable(getattr(settings, key))
        for key in dir(settings)
        if key.isupper()
    })
