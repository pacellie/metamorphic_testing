from .transforms import identity
from .relations import equality
from .suite import Suite
from .helper import change_signature


# global two level dictionary which maps module names to test names to the actual test instance
# e.g. suites['test_sin']['A'] retrieves test 'A' from the file 'test_sin'.
suite = Suite()


# name: name of the metamorphic test
# transform: optional transformation function
# relation: optional relation function
# (1) create a new instance of a metamorphic test
#     for now the transform just receives the default priority 0 -> change later?
# (2) retrieve the module of the caller of this function
# (3) register the test in the global suites variable
# (4) return the name as a handle to the caller
def metamorphic(name, *, transform=identity, relation=equality):
    suite.metamorphic(name, transform=transform, relation=relation)
    return name


# arg: the name of a parameter
# generator: either a plain value or a function of the form 'lambda: value'
# transform: transformation function we are wrapping
# randomize the argument arg by the value generated by the generator by setting
# overriding the value of arg in the given kwargs
def randomized(arg, generator):
    def wrapper(transform):
        return suite.randomized_generator(transform, arg, generator)

    return wrapper


# metamorphic_name: name of a metamorphic test
# priority: priority of the transform
# transform: transformation function we are wrapping
# update the metamorphic test in the global suites variable by appending the
# (transform, priority) pair to the already present transformations of the given
# metamorphic test
def transformation(name, *, priority=0):
    def wrapper(transform):
        suite.transformation(name, transform, priority=priority)
        return transform

    return wrapper


# metamorphic_name: name of a metamorphic test
# relation: relation function we are wrapping
# update the metamorphic test in the global suites variable by setting the relation
# of the given metamorphic test
def relation(*names):
    def wrapper(relation):
        for name in names:
            suite.relation(name, relation)
        return relation

    return wrapper


# test: the system under test function
# x: the actual input
# execute all the tests of this module in the global suites variable by delegating
# the the execute function of the MetamorphicTest class
def system(flag=None, *, name=None):
    def wrapper(test):
        @change_signature(test)
        def execute(*args, **kwargs):
            if kwargs:  # to be compatible with both given and pytest
                args = tuple(kwargs.values())
            suite.execute(name, test, *args)

        return execute

    if flag is None:
        return wrapper
    return wrapper(flag)
