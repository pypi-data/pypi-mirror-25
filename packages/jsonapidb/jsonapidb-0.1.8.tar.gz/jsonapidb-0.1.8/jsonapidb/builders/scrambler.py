import inspect


def egg(cls):
    cls.__is_egg = True
    return cls


# TODO uproscic
class EggFactory:
    EXISTING_EGGS = {}

    @classmethod
    def create(cls, egg_cls):
        if egg_cls.__name__ not in cls.EXISTING_EGGS:
            cls.EXISTING_EGGS[egg_cls.__name__] = Egg(egg_cls)
        return cls.EXISTING_EGGS[egg_cls.__name__]

    @classmethod
    def create_from_instance(cls, instance):
        if instance.__class__.__name__ not in cls.EXISTING_EGGS:
            new_egg = Egg(instance.__class__)
            new_egg.instance = instance
            cls.EXISTING_EGGS[instance.__class__.__name__] = new_egg
        return cls.EXISTING_EGGS[instance.__class__.__name__]


class Egg:
    def __init__(self, egg_cls):
        self.egg_cls = egg_cls
        self.instance = None
        self._egg_factory = EggFactory()
        self.dependencies = self._get_dependencies()

    @property
    def name(self):
        return self.egg_cls.__name__

    @property
    def is_built(self):
        return self.instance is not None

    def _get_dependencies(self):
        egg_parameters = map(lambda p: p.annotation, inspect.signature(self.egg_cls.__init__).parameters.values())
        dependencies = filter(self.is_dependency, egg_parameters)
        return list(map(self._egg_factory.create, dependencies))

    @classmethod
    def is_dependency(cls, parameter: inspect.Parameter):
        return parameter.__name__ != '_empty'

    def build(self):
        if self.instance is None:
            self.instance = self.egg_cls(*[d.instance for d in self.dependencies])


class SingleModuleEggsExtractor:
    def __init__(self, module):
        self._module = module
        self.egg_factory = EggFactory()

    def get_eggs(self):
        eggs = []
        for module_member_name in dir(self._module):
            potential_egg_cls = getattr(self._module, module_member_name)
            if self._is_egg(potential_egg_cls):
                eggs.append(self.egg_factory.create(potential_egg_cls))
        return eggs

    @staticmethod
    def _is_egg(potential_egg):
        return inspect.isclass(potential_egg) and hasattr(potential_egg, '__is_egg')


class MultipleModulesEggsExtractor:
    def __init__(self, modules):
        self._modules = modules

    def get_eggs(self):
        result = []
        for module in self._modules:
            module_eggs = SingleModuleEggsExtractor(module).get_eggs()
            result.extend(module_eggs)
        return result


class EggsBuilder:
    def __init__(self, eggs):
        self._eggs = eggs

    def build(self):
        for egg in self._eggs:
            self._build_egg(egg)
        return self._eggs

    def _build_egg(self, egg):
        for dependency in egg.dependencies:
            self._build_egg(dependency)
        egg.build()


class ModulesBuilder:
    def __init__(self, modules, initial_eggs=None):
        if initial_eggs is None:
            initial_eggs = []
        self._modules = modules
        self._initial_eggs = initial_eggs

    def build(self):
        eggs_extractor = MultipleModulesEggsExtractor(self._modules)
        eggs = eggs_extractor.get_eggs()
        eggs.extend(self._initial_eggs)

        eggs_builder = EggsBuilder(eggs)
        built_eggs = eggs_builder.build()
        return {e.name: e.instance for e in built_eggs}