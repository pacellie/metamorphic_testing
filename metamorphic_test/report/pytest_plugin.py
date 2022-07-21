from typing import Callable
import pytest

from metamorphic_test.suite import TestID
from metamorphic_test.decorator import suite
from metamorphic_test.report.html_generator import HTMLReportGenerator


class NoMetamorphicMarkError(ValueError):
    pass


def find_metamorphic_mark(item):
    for mark in item.iter_markers(name='metamorphic'):
        return mark
    raise NoMetamorphicMarkError('No metamorphic mark found')


@pytest.hookimpl(hookwrapper=True)
# call param is needed for the hook signature to be correct
# pylint: disable=unused-argument
def pytest_runtest_makereport(item: pytest.TestReport, call: pytest.CallInfo):
    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html is None:
        return  # skip if no HTML plugin is available
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":
        try:
            m_mark: pytest.Mark = find_metamorphic_mark(item)
        except NoMetamorphicMarkError:
            # This is a non-metamorphic test
            return
        test_id: TestID = item.funcargs['name']
        m_test = suite.get_test(test_id)
        # generate report
        generator = HTMLReportGenerator(m_test.reports[-1])
        visualize_input: Callable = m_mark.kwargs["visualize_input"] or str
        setattr(generator, "visualize_input", visualize_input)
        extra_html = generator.generate()
        # add report to pytest-html output
        extra.append(pytest_html.extras.html(f"""
            <b>Report:</b><br />
            {extra_html}
        """))
        report.extra = extra


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "metamorphic(name, module): mark test as metamorphic, adding report metadata to it"
    )