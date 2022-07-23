import pytest
from typing import Optional, TypeVar, Callable, Hashable

from .helper import change_signature
from .generator import MetamorphicGenerator
from .suite import Suite, TestID
from .transform import Transform
from .rel import Relation

A = TypeVar('A')

TransformWrapper = Callable[[Transform], Transform]
RelationWrapper = Callable[[Relation], Relation]
System = Callable

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
def metamorphic(
        name: str, *,
        transform: Optional[Transform] = None,
        relation: Optional[Relation] = None) -> TestID:
    """
    Registers a new metamorphic test

    Registering the transform and relation can be done during registration, or
    later by decorating the appropriate transformation / relation functions.

    Parameters
    ----------
    name : str
        Name of the metamorphic test.
    transform : Optional[Transform]
        Optional transformation function. Defaults to None.
    relation : Optional[Relation]
        Optional relation function. Defaults to None.

    Returns
    -------
    out : TestID
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


def randomized(arg: str, generator: MetamorphicGenerator[A]) -> TransformWrapper:
    """
    Randomize the argument arg by the value generated by the generator by setting
    overriding the value of arg in the given kwargs

    For the purpose of metamorphic testing transformations, it is recommended to
    apply this to all but the first argument.

    Parameters
    ----------
    arg : str
        The name of the argument in the transformer function to assign value to.
    generator : MetamorphicGenerator[A]
        An object of some concrete implementation (concrete child class) of
        MetamorphicGenerator.

    Returns
    -------
    wrapper : TransformWrapper
        A function which will register the random generator to suite

    See Also
    --------
    fixed : fix the argument arg to the given value

    Examples
    --------

    from randint import RandInt

    mm_test = metamorphic('some_metamorphic_test_name')

    @transformation(mm_test)
    @randomized('n', RandInt(1, 10))
    def add(x, n):
        return x + n
    """

    def wrapper(transform: Transform) -> Transform:
        return suite.randomized_generator(transform, arg, generator)

    return wrapper


def fixed(arg: str, value: A) -> TransformWrapper:
    """
    Fix the argument arg to the given value overriding the value of arg
    in the given kwargs

    Parameters
    ----------
    arg : str
        The name of the argument in the transformer function to assign value to.
    value : A
        the fixed value of the arg

    Returns
    -------
    wrapper : TransformWrapper
        A function which will register the fixed value to suite and to the function
        decorated with his decorator.

    See Also
    --------
    randomized : Randomize the argument arg by the value generated by the generator

    Examples
    --------
    from randint import RandInt

    mm_test = metamorphic('some_metamorphic_test_name')

    @transformation(mm_test)
    @randomized('n', RandInt(1, 10))
    @fixed('c', 0)
    def shift(x, n, c):
        return x + 2 * n * math.pi + c
    """

    def wrapper(transform: Transform) -> Transform:
        return suite.fixed_generator(transform, arg, value)

    return wrapper


# metamorphic_name: name of a metamorphic test
# priority: priority of the transform
# transform: transformation function we are wrapping
# update the metamorphic test in the global suites variable by appending the
# (transform, priority) pair to the already present transformations of the given
# metamorphic test
def transformation(test_id: TestID, *, priority: int = 0) -> TransformWrapper:
    """
    Registers the decorated function as a transformation for a pre-defined metamorphic test
    given by 'name' parameter.

    Parameters
    ----------
    test_id : TestID
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
    wrapper : TransformWrapper
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

    def wrapper(transform: Transform) -> Transform:
        suite.add_transform(test_id, transform, priority=priority)
        return transform

    return wrapper


# metamorphic_name: name of a metamorphic test
# relation: relation function we are wrapping
# update the metamorphic test in the global suites variable by setting the relation
# of the given metamorphic test
def relation(*test_ids: TestID) -> RelationWrapper:
    """
    Registers a decorated function as a metamorphic relation for the metamorphic tests
    listed in names.

    Parameters
    ----------
    test_ids : TestID
        Name of the metamorphic test for which the relation needs to be mapped. Please note
        there can be multiple names parameters separated by comma and in such cases the same
        relation is associated to different metamorphic tests.

    Returns
    -------
    wrapper : RelationWrapper
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

    def wrapper(relation: Relation) -> Relation:
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
def system(*names: Hashable, **kwargs) -> Callable[[System], Callable[..., None]]:
    """
    Identifies the function decorated with this decorator as a systemUnderTest and
    executes all the metamorphic tests given by names.

    Parameters
    ----------
    names : Hashable
        Optional names of the metamorphic tests to be performed on the system under
        test. It's a multi-argument, i.e multiple metamorphic tests can be entered
        as comma separated multiple arguments. If these arguments are not passed,
        the framework executes all the metamorphic tests defined in the same file
        on the system under test function.
    kwargs: Any
        Optional key word arguments to pass some additional parameters to the
        tests or transformations.

    Returns
    -------
    wrapper : Callable[[System], Callable[..., None]]
        returns a function which would ultimately register the decorated function
        as the system under test with a number of pre-defined metamorphic tests
        and executes those tests.

    See Also
    --------
    metamorphic : registers a new metamorphic test
    transformation : registers a function as a transformation for a metamorphic test
    relation : registers a function as a relation for a metamorphic test

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

    @system(mm_test_1, mm_test_2)
    def test_function(input):
        func(input)
    """

    def wrapper(test: System) -> Callable[..., None]:
        @change_signature(test)
        def execute(name: str, *args, **kwargs):
            if kwargs:
                args = tuple(kwargs.values())
            suite.execute(name, test, *args)

        return pytest.mark.metamorphic(
            visualize_input=kwargs.get('visualize_input', None),
            visualize_output=kwargs.get('visualize_output', None),
        )(
            pytest.mark.parametrize('name', names)(execute)
        )

    return wrapper
