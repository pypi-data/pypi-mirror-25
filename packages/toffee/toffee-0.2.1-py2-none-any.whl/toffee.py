# Copyright 2014 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from copy import copy
from functools import partial
from itertools import count
from operator import getitem, setitem
import collections
import inspect

__version__ = '0.2.1'

_creation_order = count()

def _copy_if_factory(ob):
    """
    Return a shallow copy of ``ob`` if it's a partial factory,
    otherwise return ``ob itself.

    Used when copying factory objects, where we want to also shallow copy any
    sub factories (but no need to do a full deep copy).
    """
    if isinstance(ob, Factory) and ob.partial:
        return ob.__copy__()
    return ob

class BaseFactory(object):

    created_order = 0
    extra_operations = None
    partial = False

    def __get__(self, instance, context):
        """
        Factories have magic behaviour in the context of fixtures, so that
        accessing 'my_fixture.foo' auto-delegates to 'my_fixture.o.foo'
        """
        if isinstance(instance, Fixture):
            try:
                return instance.o[instance.factory_names[self]]
            except KeyError:
                raise AttributeError()
        return self

    def create_object(self, context):
        raise NotImplementedError()

    def destroy_object(self, context, ob):
        raise NotImplementedError()

    @classmethod
    def configure(cls):
        """\
        Return a dynamically created Factory subclass.

        In the Factory base class this serves no functional purpose, however
        subclasses may extend this to provide configuration points.
        For example :class:`~toffee.StormFactory` uses this to allow the user
        to supply the getstore method.
        """
        return type(cls.__name__, (cls,), {})

    @classmethod
    def setup_complete(self, context, created):
        """\
        Override this in subclasses to implement custom behaviour after all
        objects have been created (eg flushing to database)
        """

    @classmethod
    def teardown_complete(self, context, created):
        """\
        Override this in subclasses to implement custom behaviour after all
        objects have been torn down (eg flushing to database)
        """


class Factory(BaseFactory):

    class ExtraOperation(object):
        """
        A post-creation operation to perform on the object.
        These objects are created by calling __setitem__ or __setattr__ on a
        factory, and result in the equivalent operation being performed on the
        created object. Operations are run in the same order they are created.
        """
        def __init__(self, factory, fn, *args, **kwargs):
            self.factory = factory
            self.fn = fn
            self.args = args
            self.kwargs = kwargs
            self.created_order = next(_creation_order)

        def bind(self, context, ob):
            self.ob = ob
            self.context = context

        def __call__(self):
            args = tuple(self.context.resolve(a) for a in self.args)
            kwargs = dict((k, self.context.resolve(v))
                          for k, v in self.kwargs.items())
            return self.fn(self.ob, *args, **kwargs)

    def __init__(self, what, *args, **kwargs):
        """
        :param configure_object: A callable to be called after object
                                 creation to configure the new instances
        :param create_object: A callable that replaces the default object
                              creation strategy.
        :param destroy_object: A callable that replaces the default object
                               destruction strategy.
        :param: partial: Boolean. A factory marked as partial does not
                         create and top-level objects, and always
                         produces a new instance when copied.
        """
        reserved = ['configure_object', 'create_object', 'destroy_object',
                    'partial']
        config = {}
        marker = []
        for k in reserved:
            v = kwargs.pop(k, marker)
            if v is not marker:
                config[k] = v

        for k in list(kwargs.keys()):
            if k.endswith('_') and any(k.startswith(r) for r in reserved):
                kwargs[k[:-1]] = kwargs.pop(k)

        for name in ['configure_object', 'create_object', 'destroy_object']:
            meth = config.get(name, None)
            if meth is not None:
                super(Factory, self).__setattr__('_' + name, meth)

        self.__dict__['partial'] = config.get('partial', False)
        self.__dict__['what'] = what
        self.__dict__['args'] = args
        self.__dict__['kwargs'] = AttrDict(kwargs)
        self.__dict__['extra_operations'] = []
        self.__dict__['created_order'] = next(_creation_order)

        # process subfactory__attribute='foo'
        subfactory_updates = collections.defaultdict(dict)
        for k, v in list(self.kwargs.items()):
            if '__' in k:
                head, tail = k.split('__', 1)
                subfactory_updates[head][tail] = v
                del self.kwargs[k]
        for item, attrs in subfactory_updates.items():
            self.kwargs[item] = self.kwargs[item](**attrs)

    def __getitem__(self, attr):
        return LazyRecorderFactory(self)[attr]

    def __getattr__(self, attr):
        return getattr(LazyRecorderFactory(self), attr)

    def __setitem__(self, item, value):
        self.extra_operations.append(self.ExtraOperation(
            self, setitem, item, value))

    def __setattr__(self, attr, value):
        self.extra_operations.append(self.ExtraOperation(
            self, setattr, attr, value))

    def __call__(self, *args, **kwargs):
        args = args or tuple(_copy_if_factory(ob) for ob in self.args)
        kwargs = dict(((k, _copy_if_factory(v))
                    for k, v in self.kwargs.items()),
                    **kwargs)
        return self.__class__(self.what, *args, **kwargs)

    def __copy__(self):

        ob = self.__class__.__new__(self.__class__)
        ob.__dict__.update(self.__dict__)
        ob.__dict__['args'] = tuple(_copy_if_factory(ob) for ob in self.args)
        ob.__dict__['kwargs'] = dict((k, _copy_if_factory(v))
                                      for k, v in self.kwargs.items())
        return ob

    def create_object(self, context):
        try:
            return context.factory_created_objects[self]
        except KeyError:
            pass
        args = tuple(context.resolve(a) for a in self.args)
        kwargs = dict((k, context.resolve(v)) for k, v in self.kwargs.items())

        ob = self._create_object(context, args, kwargs)
        ob = self._configure_object(ob, context)
        context.factory_created_objects[self] = ob
        return ob

    def destroy_object(self, context, ob):
        return self._destroy_object(context, ob)

    def _create_object(self, context, args, kwargs):
        return self.what(*args, **kwargs)

    def _destroy_object(self, context, ob):
        pass

    def _configure_object(self, ob, context):
        return ob



class ListFactory(Factory, collections.Sequence):
    """
    A factory containing a list of other factories
    """
    def __init__(self, items):
        super(ListFactory, self).__init__(None)
        self.__dict__['items'] = items
        self.__dict__['extra_operations'] = sum((i.extra_operations
                                                 for i in items), [])
        self.__dict__['created_order'] = items[0].created_order

    def __len__(self):
        return len(self.items)

    def __getitem__(self, n):
        return self.items[n]

    def __add__(self, other):
        if isinstance(other, ListFactory):
            other = other.items
        return self.__class__(self.items + other)

    def create_object(self, context):
        return self.items.__class__(i.create_object(context)
                                    for i in self.items)

    def destroy_object(self, context, ob):
        for ob, factory in zip(ob, self.items):
            factory.destroy_object(context, ob)


class CallFactory(Factory):
    """\
    A factory that returns the value of a callable function or object.

    Use this to lazily instantiate values that are accessible at setup
    time but not necessarily earlier::

        class fixture(Fixture):

            user = CallFactory(lambda: User.objects.get(username='admin'))
            ...

    """

    def _create_object(self, context, args, kwargs):
        return self.what(*args, **kwargs)

    def _destroy_object(self, context, ob):
        pass


class LazyRecorder(object):
    """
    Records all calls and attribute access for later replay, eg:

        >>> p = LazyRecorder().upper().replace('c', 'm')[0]
        >>> p.replay_with('cat')
        'M'
    """

    def __init__(self):
        self.__dict__['_recorded_events'] = []

    def __call__(self, *args, **kwargs):
        self._recorded_events.append((self._caller, args, kwargs))
        return self

    def __getattr__(self, attr):
        self._recorded_events.append((getattr, (attr,), {}))
        return self

    def __getitem__(self, item):
        self._recorded_events.append((getitem, (item,), {}))
        return self

    def _caller(self, ob, *args, **kwargs):
        return ob(*args, **kwargs)

    def replay_with(self, ob):
        for func, args, kwargs in self._recorded_events:
            ob = func(ob, *args, **kwargs)
        return ob


class LazyRecorderFactory(BaseFactory, LazyRecorder):
    """
    Wraps a factory to record any calls/attribute access
    """
    def __init__(self, factory):
        LazyRecorder.__init__(self)
        BaseFactory.__init__(self)
        self.__dict__['factory'] = factory
        self.__dict__['created_order'] = factory.created_order
        self.__dict__['extra_operations'] = factory.extra_operations

    def __repr__(self):
        s = ''
        for op, args, kwargs in self._recorded_events:
            if op is self._caller:
                f = '(*{args}, **{kwargs})'
            elif op is getitem:
                f = '[{args[0]}]'
            elif op is getattr:
                f = '.{args[0]}'
            else:
                f = ' <unknown>(*{args}, **{kwargs})'
            s += f.format(args=args, kwargs=kwargs)
        return '<{}{}>'.format(self.__class__.__name__, s)

    def __setitem__(self, item, value, setter=setitem):
        events_snapshot = self._recorded_events[:]
        def do_setitem(ob, item, value, setter=setter):
            for func, args, kwargs in events_snapshot:
                ob = func(ob, *args, **kwargs)
            setter(ob, item, value)
        self.extra_operations.append(
            Factory.ExtraOperation(self.factory, do_setitem, item, value))

    def __setattr__(self, attr, value):
        self.__setitem__(attr, value, setattr)

    def create_object(self, context):
        return self.factory.create_object(context)

    def destroy_object(self, context, ob):
        return self.factory.destroy_object(context, ob)

    def replay_with_resolved(self, fixture, ob):
        """
        Like :meth:`LazyRecorder.replay_with`, but resolves any intermediate
        LazyRecorderFactory objects encountered.
        """

        def resolve_ob(n):
            if isinstance(n, LazyRecorderFactory):
                ob = n.factory.create_object(fixture)
                ob = n.replay_with_resolved(fixture, ob)
                return ob
            elif isinstance(n, Factory):
                return n.factory.create_object(fixture)
            else:
                return n

        for func, args, kwargs in self._recorded_events:
            args = tuple(resolve_ob(n) for n in args)
            kwargs = dict((k, resolve_ob(n)) for k, n in kwargs.items())
            ob = func(ob, *args, **kwargs)

        return ob


class DjangoFactory(Factory):

    def _create_object(self, context, args, kwargs):
        ob = self.what.objects.create(*args, **kwargs)
        ob.save()
        return ob

    def _destroy_object(self, context, ob):
        ob.delete()


class _DataMapperFactory(Factory):
    """\
    A factory that requires a data mapper object (eg a storm store or
    sqlalchemy session) in order to bind objects to the database.
    """

    #: Callable that returns the data mapper object
    _getmapper = lambda: None
    mapperkey = '_datamapper'

    default_flush = True
    default_commit = False

    @classmethod
    def _mapper_flush(cls, context):
        mapper = cls._getmapper_cached(context)
        if mapper is not None:
            mapper.flush()

    @classmethod
    def _mapper_commit(cls, context):
        mapper = cls._getmapper_cached(context)
        if mapper is not None:
            mapper.commit()

    def _mapper_add(self, context, ob):
        """
        Ask the datamapper to add ``ob`` to the data store
        """
        mapper = self._getmapper_cached(context)
        if mapper is not None:
            mapper.add(ob)

    def _mapper_remove(self, context, ob):
        """
        Ask the datamapper to remove ``ob`` from the data store
        """
        mapper = self._getmapper_cached(context)
        if mapper is not None:
            mapper.remove(ob)

    @classmethod
    def configure(cls, getmapper, *args, **kwargs):
        classob = super(_DataMapperFactory, cls).configure(*args, **kwargs)
        classob = type(cls.__name__, (classob,),
                       {'_getmapper': staticmethod(getmapper)})

        class MapperAccessFactory(classob):
            """
            Give direct access to the mapper object when creating fixtures,
            eg::

                class fixture(Fixture):
                    user = StormFactory.mapper.find(User, User.id == 1).one()
            """

            def __init__(self):
                super(MapperAccessFactory, self).__init__(None)

            def create_object(self, context):
                return self._getmapper_cached(context)

            def destroy_object(self, context, ob):
                pass

        classob.mapper = MapperAccessFactory()
        return classob

    @classmethod
    def _getmapper_cached(cls, context):
        try:
            return context.factoryoptions[cls.mapperkey]
        except KeyError:
            return context.factoryoptions.setdefault(cls.mapperkey,
                                                     cls._getmapper())

    @classmethod
    def setup_complete(cls, context, created):
        if context.factoryoptions.get('flush', cls.default_flush):
            cls._mapper_flush(context)
        if context.factoryoptions.get('commit', cls.default_commit):
            cls._mapper_commit(context)

    @classmethod
    def teardown_complete(cls, context, created):
        if context.factoryoptions.get('flush', cls.default_flush):
            cls._mapper_flush(context)
        if context.factoryoptions.get('commit', cls.default_commit):
            cls._mapper_commit(context)

    def _create_object(self, context, args, kwargs):
        ob = self.what.__new__(self.what)
        for item, value in kwargs.items():
            setattr(ob, item, value)
        self._mapper_add(context, ob)
        return ob

    def _destroy_object(self, context, ob):
        self._mapper_remove(context, ob)


class StormFactory(_DataMapperFactory):
    """\
    Typically you will need to configure this at the start of your test code,
    like so::

        getstore = lamdba: getUtility(IZStorm).get('main'))
        Factory = StormFactory.configure(getstore)

    You can then use Factory as normal::

        class fixture(Fixture):
            user = Factory(models.User, ...)

    By default, StormFactory calls ``store.flush`` but not ``store.commit``.
    Change this behaviour by passing factory options to setup::

        fixture.setup(flush=False)
        fixture.setup(commit=True)

    Alternatively you can supply factory options in the fixture class:

        class fixture(Fixture):
            factoryoptions = {'commit': True}

    """


class SQLAlchemyFactory(_DataMapperFactory):
    """\

    Typically you will need to configure this at the start of your test code,
    like so::

        Session = sessionmaker(...)
        Factory = SQLAlchemyFactory.configure(Session)

    You can then use Factory as normal::

        class fixture(Fixture):
            user = Factory(models.User, ...)

    By default, SQLAlchemyFactory calls ``session.flush`` but not
    ``session.commit``.
    Change this behaviour by passing factory options to setup::

        fixture.setup(flush=False)
        fixture.setup(commit=True)

    Alternatively you can supply factory options in the fixture class:

        class fixture(Fixture):
            factoryoptions = {'commit': True}

    """

    def _mapper_remove(self, context, ob):
        """
        Ask the datamapper to remove ``ob`` from the data store
        """
        from sqlalchemy.exc import InvalidRequestError
        mapper = self._getmapper_cached(context)
        if mapper is not None:
            try:
                mapper.refresh(ob)
            except InvalidRequestError:
                # The object cannot be refreshed, presumably because it has
                # been deleted by the test code. This should not raise an
                # exception.
                pass
            else:
                # Object is still live and may be deleted
                mapper.delete(ob)
                mapper.flush()

    def _create_object(self, context, args, kwargs):
        from sqlalchemy.orm.attributes import manager_of_class
        ob = manager_of_class(self.what).new_instance()
        for item, value in kwargs.items():
            setattr(ob, item, value)
        self._mapper_add(context, ob)
        return ob


class ArgumentGenerator(object):
    """
    A callable that dynamically generates factory arguments
    """

    def __init__(self, fn):
        self.fn = fn

    def __call__(self):
        return self.fn()


class ArgumentGeneratorFactory(object):
    """
    A factory for producing ``ArgumentGenerator`` objects.

    For an example, see :class:`~toffee.Seq`
    """

    def __init__(self, scope='fixture'):
        assert scope in ('fixture', 'session')
        self.scope = scope
        self._argument_generator = None

    def make_argument_generator(self):
        raise NotImplementedError

    def __call__(self):
        if self.scope == 'session':
            if self._argument_generator is None:
                self._argument_generator = self.make_argument_generator()
            return self._argument_generator

        elif self.scope == 'fixture':
            return self.make_argument_generator()

        else:
            raise ValueError('Invalid scope value: %r', self.scope)


class Seq(ArgumentGeneratorFactory):

    def __init__(self, str_or_fn='%d', start=0, *args, **kwargs):
        self.str_or_fn = str_or_fn
        self.start = start
        super(Seq, self).__init__(*args, **kwargs)

    def make_argument_generator(self):
        counter = count(self.start)

        def seq():
            n = next(counter)
            if callable(self.str_or_fn):
                return self.str_or_fn(n)
            else:
                return self.str_or_fn % (n,)
        return ArgumentGenerator(seq)


class AttrDict(dict):

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, item, value):
        self[item] = value


class FixtureMetaclass(type):
    """
    Metaclass that replaces lists of factory objects with ListFactory instances
    """
    def __new__(cls, name, bases, attrs):
        newattrs = {}
        for attrname, attrvalue in attrs.items():
            if (isinstance(attrvalue, (tuple, list))
                    and len(attrvalue) > 0
                    and all(isinstance(n, BaseFactory) for n in attrvalue)):
                attrvalue = ListFactory(attrvalue)
            newattrs[attrname] = attrvalue
        return super(FixtureMetaclass, cls).__new__(cls, name, bases, newattrs)


_FixtureBaseClass = FixtureMetaclass(str('_FixtureBaseClass'), (), {})

class Fixture(_FixtureBaseClass):

    #: Default factory options. See :class:`~toffee.StormFactory` for an
    #: example of how these are used to control flush and commit options.
    factoryoptions = {}

    def __init__(self, **kwargs):

        #: Factory definitions
        self.d = AttrDict()
        self.factory_names = {}

        #: Named top-level factory created objects
        self.o = AttrDict()

        #: All factory created objects
        self.factory_created_objects = {}

        self.created = None

        self.factoryoptions_defaults = self.factoryoptions.copy()
        self.factoryoptions_defaults.update(kwargs.pop('factoryoptions', {}))

        class_factories = inspect.getmembers(
            self.__class__, lambda ob: isinstance(ob, BaseFactory))
        self.update_factories(dict(class_factories, **kwargs))

    def __getattr__(self, name):
        try:
            return self.o[name]
        except KeyError:
            raise AttributeError(name)

    def update_factories(self, factories):
        for name, factory in factories.items():
            if factory in self.factory_names:
                raise ValueError("Factory %r used more than once (%r and %r)" %
                                 (factory, name, self.factory_names[factory]))
            self.factory_names[factory] = name
        self.d.update(factories)

    def setup(self, force=False, **factoryoptions):
        """
        :param force: allow calls to setup to be nested
        :param **factoryoptions: any factory specific options, for example
                                 passing flags such as ``commit=True``. See
                                 individual factory subclasses for information
        """
        if self.created and not force:
            raise Exception("setup() has already been called on this fixture. "
                            "Call teardown first, or use setup(force=True).")

        self.factoryoptions = dict(self.factoryoptions_defaults,
                                   **factoryoptions)
        self.o = AttrDict()
        self.created = []
        self.factory_created_objects.clear()
        self.argument_generators = {}

        # A list of create/configure operations to perform.
        # Each entry is (<ordering_key>, <function>, <identifier>)
        operations = []

        for name, factory in self.d.items():
            if factory.partial:
                continue
            operations.append((factory.created_order,
                               partial(self._get_or_create_named_object, name),
                               ))

            for op in factory.extra_operations:
                operations.append((op.created_order, op))

        for _, fn in sorted(operations, key=lambda n: n[0]):
            if isinstance(fn, Factory.ExtraOperation):
                fn.bind(self, self.factory_created_objects[fn.factory])
            fn()

        self.setup_complete()
        return self

    def setup_complete(self):
        """\
        Call any setup_complete methods on factory classes to let them know
        that all objects have been created
        """
        factory_created = {}

        for name, ob, factory in self.created:
            factory_created.setdefault(factory.__class__, []).append(ob)

        for f, obs in factory_created.items():
            f.setup_complete(self, obs)

        self.configure()

    def teardown_complete(self, torndown):
        """\
        Call any teardown_complete methods on factory classes to let them know
        that all objects have been torn down
        """
        factory_created = {}

        for name, ob, factory in torndown:
            factory_created.setdefault(factory.__class__, []).append(ob)

        for f, obs in factory_created.items():
            f.teardown_complete(self, obs)

    def configure(self):
        """\
        Subclasses should override this to provide custom post-creation
        configuration
        """

    def _get_or_create_named_object(self, name):
        """\
        Return the object from the named factory, creating it if necessary
        """
        try:
            return self.o[name]
        except KeyError:
            pass
        return self._create_object_from_factory(self.d[name])

    def _create_object_from_factory(self, factory):
        """\
        Invoke ``factory`` to create and configure an object.
        Register the created object so that it may later be referenced and
        torn down.
        """
        name = self.factory_names.get(factory, None)
        ob = factory.create_object(self)
        self.created.append((name, ob, factory))

        if isinstance(factory, LazyRecorderFactory):
            ob = factory.replay_with_resolved(self, ob)

        if name is not None:
            assert name not in self.o
            self.o[name] = ob
        return ob

    def resolve(self, what):

        if isinstance(what, ArgumentGeneratorFactory):
            if what not in self.argument_generators:
                self.argument_generators[what] = what()
            return self.argument_generators[what]()

        if isinstance(what, ArgumentGenerator):
            return what()

        if isinstance(what, Factory):
            return self.resolve(LazyRecorderFactory(what))

        if isinstance(what, LazyRecorderFactory):
            if what.factory in self.factory_names:
                name = self.factory_names[what.factory]
                ob = self._get_or_create_named_object(name)
            else:
                ob = self._create_object_from_factory(what.factory)

            return what.replay_with_resolved(self, ob)

        if isinstance(what, (tuple, list)):
            return what.__class__(map(self.resolve, what))

        if isinstance(what, dict):
            return dict((k, self.resolve(v)) for k, v in what.items())

        return what

    def teardown(self):
        torndown = []
        while self.created:
            name, ob, factory = self.created.pop()
            if name is not None:
                del self.o[name]
            factory.destroy_object(self, ob)
            torndown.append((name, ob, factory))
        self.teardown_complete(torndown)
        self.factoryoptions = {}

    def __enter__(self):
        return self.setup()

    def __exit__(self, type, value, tb):
        if type:
            try:
                self.teardown()
            except Exception:
                pass
        else:
            self.teardown()
        return False

    #: Alias for compatility with unittest names
    setUp = setup

    #: Alias for compatility with unittest names
    tearDown = teardown


class TestWithFixture(object):
    """
    Test class with built-in fixture setup/teardown methods

    Subclass this and initialize 'fixture' or 'class_fixture'::

        import toffee

        class TestSomething(toffee.TestWithFixture):

            class fixture(toffee.Fixture)
                ...

            class class_fixture(toffee.Fixture)
                ...

            def test_something(self):
                fixture = self.f

    If 'fixture' is defined, it will be set up and torn down per test method
    using the regular setUp/tearDown methods.

    If 'class_fixture' is defined it will be set up and torn down using
    nose style class level setUp/tearDown methods.

    In either case, fixture data is available via ``self.f``.
    In addition, class level fixture data is available via ``self.class_f``
    """
    fixture = class_fixture = None

    def setUp(self):
        if self.fixture is not None:
            self.f = self.fixture().setup()

    def tearDown(self):
        if self.fixture is not None:
            self.f.teardown()

    @classmethod
    def setUpClass(cls):
        if cls.class_fixture is not None:
            cls.f = cls.class_f = cls.class_fixture().setup()

    @classmethod
    def tearDownClass(cls):
        if cls.class_fixture is not None:
            cls.class_f.teardown()
