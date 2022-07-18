import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.TestReport, call: pytest.CallInfo):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        print(report, report.user_properties, report.__dict__)
        print("Result:", call.result)
        print("excinfo:", call.excinfo)
        extra.append(pytest_html.extras.html("<div>Additional HTML</div>"))
        report.extra = extra