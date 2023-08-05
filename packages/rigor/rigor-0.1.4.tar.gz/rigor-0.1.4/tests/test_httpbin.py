from rigor import Suite, Namespace, Validator, Runner, ReportEngine
from collections import OrderedDict

import tempfile
import pytest
import os

ROOT_DIR = os.path.join(os.path.dirname(__file__), "httpbin")


@pytest.fixture
def suite():
    directories = [ROOT_DIR]
    return Suite(directories=directories, tags_excluded=["broken"])


def test_collect(suite):
    assert suite.tags_excluded == ["broken"]
    assert len(suite.skipped) == 3
    assert len(suite.queued) == 8


def test_execute(suite):
    result = suite.execute()
    assert result.success
    assert len(result.passed) == 8

    with tempfile.TemporaryDirectory() as tmpdir:
        print(tmpdir)
        engine = ReportEngine(report_types=["json"], output_path=tmpdir,
                              suite_result=result)
        engine.generate()


def test_case_get(suite):
    case = suite.get_case(ROOT_DIR, "get.rigor")

    # check case root
    assert case.name == "Get"
    assert case.format == "1.0"
    assert case.domain == "https://httpbin.org"
    assert case.tags == ["working"]
    assert len(case.steps) == 1

    # check case steps
    step = case.steps[0]
    assert step.description == "Get call with no parameters"
    assert step.request.path == "/get"
    assert step.validate == [
        Validator(expect="{response.url}", actual="https://httpbin.org/get"),
        Validator(expect="{response.args}", actual=OrderedDict()),
        Validator(expect="{response.headers.Accept}", actual="*/*"),
        Validator(expect="{response.headers.Connection}", actual="close"),
    ]


def test_case_params(suite):
    case = suite.get_case(ROOT_DIR, "params.rigor")

    # check case root
    assert case.name == "Params"
    assert case.format == "1.0"
    assert case.domain == "https://httpbin.org"
    assert case.tags == ["working"]
    assert len(case.steps) == 1
    assert len(case.scenarios) == 3

    # check scenarios
    assert case.scenarios[0] == Namespace(value=1, __name__="Scenario #1")
    assert case.scenarios[1] == Namespace(value=2, __name__="Override!")
    assert case.scenarios[2] == Namespace(value=['a', 'b', 'c'],
                                          __name__="Scenario #3")


def test_case_http_status(suite):
    case = suite.get_case(ROOT_DIR, "http_status.rigor")

    # check case root
    assert case.name == "HTTP Status"
    assert case.format == "1.0"
    assert case.domain == "https://httpbin.org"
    assert len(case.steps) == 4
    assert len(case.scenarios) == 1  # default empty scenario

    # check step
    assert case.steps[0].request.status == []
    assert case.steps[1].request.status == [200]
    assert case.steps[2].request.status == [404]
    assert case.steps[3].request.status == [418]


def test_case_iterate(suite):
    case = suite.get_case(ROOT_DIR, "iterate.rigor")
    assert len(case.steps) == 4
    step = case.steps[0]
    namespace = Runner(case=case).namespace

    assert list(step.iterate.iterate(namespace)) == [
        dict(show_env=0, other="A"),
        dict(show_env=1, other="B"),
    ]
    step = case.steps[2]
    assert list(step.iterate.iterate(namespace)) == [
        dict(show_env=0, other="A"),
        dict(show_env=0, other="B"),
        dict(show_env=0, other="C"),
        dict(show_env=0, other="D"),
        dict(show_env=0, other="E"),
        dict(show_env=0, other="F"),
        dict(show_env=1, other="A"),
        dict(show_env=1, other="B"),
        dict(show_env=1, other="C"),
        dict(show_env=1, other="D"),
        dict(show_env=1, other="E"),
        dict(show_env=1, other="F"),
    ]


def test_case_load_yaml(suite):
    case = suite.get_case(ROOT_DIR, "load_yaml.rigor")
    assert len(case.scenarios) == 2
    assert len(case.steps) == 1

    scenario = case.scenarios[0]
    assert scenario.keys() == {"data", "__name__"}
    assert scenario['__name__'] == "same"

    scenario = case.scenarios[1]
    assert scenario.keys() == {"data", "__name__"}
    assert scenario['__name__'] == "same"


def test_case_conditional():
    directories = [os.path.join(ROOT_DIR, "conditional.rigor")]
    suite = Suite(directories=directories)
    assert len(suite.skipped) == 0
    assert len(suite.queued) == 1
    result = suite.execute()
    assert not result.success  # test fails, checking # of steps
    assert len(result.failed) == 1
    scenario_result = result.failed[0].failed[0]
    assert len(scenario_result.step_results) == 2
