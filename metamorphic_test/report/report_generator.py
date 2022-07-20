from abc import ABCMeta, abstractmethod

from .execution_report import MetamorphicExecutionReport


class ReportGenerator(metaclass=ABCMeta):
    report: MetamorphicExecutionReport
    def __init__(self, report: MetamorphicExecutionReport):
        self.report = report

    @abstractmethod
    def generate(self):
        ...