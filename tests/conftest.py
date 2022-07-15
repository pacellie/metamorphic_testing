from metamorphic_test import suite

def pytest_generate_tests(metafunc):
    if "meta" in metafunc.fixturenames:
        module = metafunc.function.__module__
        metafunc.parametrize("meta", suite.get_tests(module))
