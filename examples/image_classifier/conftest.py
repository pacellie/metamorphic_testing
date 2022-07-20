from typing import Callable
import pytest

from metamorphic_test.suite import TestID
from metamorphic_test.decorator import suite
from metamorphic_test.report.html_generator import HTMLReportGenerator


@pytest.hookimpl(hookwrapper=True)
# call param is needed for the hook signature to be correct
# pylint: disable=unused-argument
def pytest_runtest_makereport(item: pytest.TestReport, call: pytest.CallInfo):
    # just hacked together for now
    # pylint: disable=too-many-locals
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        extra_html = "<b>Reports</b><br/>"
        # find the metamorphic mark
        m_mark = None
        for mark in item.own_markers:
            if mark.name == "metamorphic":
                m_mark = mark
                break
        assert m_mark is not None, \
            "pytest marker should have been added by the system decorator"
        test_id: TestID = m_mark.kwargs["test_id"]
        module: str = m_mark.kwargs["module"]
        visualize_input: Callable = m_mark.kwargs["visualize_input"]
        if visualize_input is None:
            # pylint: disable=unnecessary-lambda-assignment
            visualize_input = lambda x: x
        if test_id is None:
            # means all tests in the module
            # TODO: implement
            print("Not implemented:", module)
            extra_html += "<div>(Not yet implemented)</div>"
        else:
            m_test = suite.get_test(test_id)
            # Using `for report in m_test.reports:` breaks
            # the code in some very mysterious way:
            # There will be no report any more and even
            # just `for report in m_test.reports: pass` will
            # break the reporting. I have absolutely no idea 
            # what's happening.
            # pylint: disable=consider-using-enumerate
            for i in range(len(m_test.reports)):
                generator = HTMLReportGenerator(
                    m_test.reports[i],
                )
                generator.visualize_input = visualize_input  # type: ignore
                html = generator.generate()
                extra_html += f"<div>{html}</div>"
        extra_html = "<div>" + extra_html + "</div>"
        extra.append(pytest_html.extras.html(extra_html))
        report.extra = extra


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "metamorphic(name, module): mark test as metamorphic, adding report metadata to it"
    )