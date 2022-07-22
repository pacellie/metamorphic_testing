import pytest

from .helper import change_signature
from .generator import MetamorphicGenerator
from .suite import Suite


# A Suite maps module names with test names to the actual test instance
# Transformations and Relations can be registered as well as System under Tests.
# This needs to be a global, because there's no other way to register them in
# the proposed MT syntax our customer wants to use.
suite = Suite()


# name: name of the metamorphic test
# transform: optional transformation function
# relation: optional relation function
# (1) create a new instance of a metamorphic test
#     for now the transform just receives the default priority 0 -> change later?
# (2) retrieve the module of the caller of this function
# (3) register the test in the global suites variable
# (4) return the name as a handle to the caller
def metamorphic(name, *, transform=None, relation=None):
    """
    Registers a new metamorphic test

    Registering the transform and relation can be done during registration, or
    later by decorating the appropriate transformation / relation functions.

    Parameters
    ----------
    name : str
        Name of the metamorphic test.
    transform : callable
        Optional transformation function. Defaults to None.
    relation : callable
        Optional relation function. Defaults to None.

    Returns
    -------
    out : str
        The identifier of the metamorphic test. This can later be used to invoke
    specific metamorphic test for a system instead of all of them.

    See Also
    --------
    system : register and execute tests for the system under test.
    relation (decorator) : Registers a metamorphic relation for the metamorphic tests
    listed in names.

    Examples
    --------
    mm_test_1 = metamorphic('some_metamorphic_test_name', relation=approximately)

    @system(name=mm_test_1)
    def test_function(input):
        func(input)
    """
    test_id = suite.metamorphic(name)
    if transform is not None:
        suite.add_transform(test_id, transform, priority=0)
    if relation is not None:
        suite.set_relation(test_id, relation)
    return test_id


# randomize the argument arg by the value generated by the generator by setting
# overriding the value of arg in the given kwargs
def randomized(arg, generator: MetamorphicGenerator):
    """
    Assigns a (randomized) value to the parameters of a transformer function.

    For the purpose of metamorphic testing transformations, it is recommended to apply this to
    all but the first argument.

    Parameters
    ----------
    arg : str
        The name of the argument in the transformer function to assign value to.
    generator :
        Either a singular value that will always be assigned to the argument,
        or a function without an argument that generates a value when called.

    Returns
    -------
    wrapper : callable
        A function which will register the random generator to suite

    Examples
    --------
    @randomized('n', randint(1, 10))
    def add(x, n):
        return x + n
    """

    def wrapper(transform):
        return suite.randomized_generator(transform, arg, generator)

    return wrapper


# fix the argument arg to the given value
# overriding the value of arg in the given kwargs
def fixed(arg, value):
    def wrapper(transform):
        return suite.fixed_generator(transform, arg, value)

    return wrapper


# metamorphic_name: name of a metamorphic test
# priority: priority of the transform
# transform: transformation function we are wrapping
# update the metamorphic test in the global suites variable by appending the
# (transform, priority) pair to the already present transformations of the given
# metamorphic test
def transformation(test_id, *, priority=0):
    """
    Registers the decorated function as a transformation for a pre-defined metamorphic test
    given by 'name' parameter.

    Parameters
    ----------
    test_id : str
        Name of the metamorphic test that is supposed to use the decorated function
        as transformation
    priority : int
        Optional priority of the transformation. While using multiple transformations for a
        metamorphic test, use this priority to set a specific order between the transformations
        if order is important for a use case. The higher the value the earlier the
        transformation will be applied. Transformations with equal priority will be executed in
        a randomly shuffled order. Please note this is a keyword only argument. Default: 0

    Returns
    -------
    wrapper : callable
        A function which would ultimately register the transformation defined
        in the function decorated with this decorator to the suite.

    See Also
    --------
    system : register and execute tests for the system under test.
    metamorphic : register a new metamorphic test
    suite : the object that holds all the metamorphic transformations and relations

    Examples
    --------
    mm_test_1 = metamorphic('some_metamorphic_test_name', relation=approximately)
    mm_test_2 = metamorphic('another_metamorphic_test_name')

    @transformation(mm_test_1)
    @transformation(mm_test_2)
    def negate(x):
        return -x

    @system(name=identifier)
    def test_function(input):
        func(input)
    """

    def wrapper(transform):
        suite.add_transform(test_id, transform, priority=priority)
        return transform

    return wrapper


# metamorphic_name: name of a metamorphic test
# relation: relation function we are wrapping
# update the metamorphic test in the global suites variable by setting the relation
# of the given metamorphic test
def relation(*test_ids):
    """
    Registers a decorated function as a metamorphic relation for the metamorphic tests
    listed in names.

    Parameters
    ----------
    names : str
        Name of the metamorphic test for which the relation needs to be mapped. Please note
        there can be multiple names parameters separated by comma and in such cases the same
        relation is associated to different metamorphic tests.

    Returns
    -------
    wrapper : callable
        returns a function which would ultimately register the relation to suite and associate
        it with the metamorphic tests passed as input parameters to the decorated function with
        this decorator.

    See Also
    --------
    system : register and execute tests for the system under test.
    metamorphic : register a new metamorphic test
    suite : the object that holds all the metamorphic transformations and relations
    transformation : Registers a decorated function as a transformation for a metamorphic test

    Examples
    --------
    mm_test_1 = metamorphic('some_metamorphic_test_name')
    mm_test_2 = metamorphic('another_metamorphic_test_name')

    @transformation(mm_test_1)
    @transformation(mm_test_2)
    def negate(x):
        return -x

    @relation(mm_test_1, mm_test_2)
    def approximately_negate(x, y):
        return approximately(-x, y)

    @system
    def test_function(input):
        func(input)
    """

    def wrapper(relation):
        for test_id in test_ids:
            suite.set_relation(test_id, relation)
        return relation

    return wrapper


# names: the names of the metamorphic tests to be run
# test: the system under test function
# name: the name of the metamorphic test to be run
# x: the actual input
# execute all the tests of this module in the global suites variable by delegating
# the the execute function of the MetamorphicTest class
def system(*names, **kwargs):
    def wrapper(test):
        @change_signature(test)
        def execute(name, *args, **kwargs):
            if kwargs:
                args = tuple(kwargs.values())
            suite.execute(name, test, *args)

        return pytest.mark.metamorphic(
            visualize_input=kwargs.get('visualize_input', None)
        )(
            pytest.mark.parametrize('name', names)(execute)
        )

    return wrapper