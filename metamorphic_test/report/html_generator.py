from typing import Callable, List
from .report_generator import ReportGenerator


def error_html(error_message: str) -> str:
    return f'<span class="error">{error_message}</span>'


class HTMLReportGenerator(ReportGenerator):
    """
    Produces an HTML table like this:

    input_x              -> system -> output_x
    | (transform 0)                       |
    transform_result[0]                   |
    | (transform 1)                       | (relation) (holds?)
    transform_result[1]                   |
    | ...                                 |
    transform_result[-1] -> system -> output_y
    """

    # a function to change how the inputs look (left side, before system)
    visualize_input: Callable[..., str] = str
    # a function to change how the outputs look (right side, after system)
    visualize_output: Callable[..., str] = str

    def _generate_transform_column(self) -> List[str]:
        """
        Generates the first column of the table, which shows the transformations
        and their results.
        """
        # start with initial input
        rows = [self.visualize_input(self.report.input_x)]
        for transform_index, transform_result in enumerate(self.report.transform_results):
            rows.append(
                f"⇩ {self.report.transforms[transform_index].get_name()}"
            )
            if transform_result.error:
                rows.append(error_html(transform_result.error))
            else:
                rows.append(self.visualize_input(transform_result.output))
        return rows
    
    @staticmethod
    def _add_column(to: List[List], fill=""):
        for x in to:
            x.append(fill)
    
    def _add_system_name(self, rows: List[List[str]]):
        """Put the system name in the second column of the first & last row."""
        system_name = self.report.system.__name__
        rows[0][1] = rows[-1][1] = f"⇨ {system_name} ⇨"
    
    def _add_outputs(self, rows: List[List[str]]):
        """Add the outputs in the last column of the first & last row."""
        rows[0][-1] = self.visualize_output(self.report.output_x)
        rows[-1][-1] = self.visualize_output(self.report.output_y)
    
    def _add_relation(self, rows: List[List[str]]):
        """Add the relation in the last row in the middle."""
        if self.report.relation_result.error:
            holds_str = error_html(self.report.relation_result.error)
        elif self.report.relation_result.output:
            holds_str = "holds"
        else:
            holds_str = error_html("does not hold")
        rows[len(rows) // 2][-1] = (
            f"⇵ {self.report.relation.__name__} {holds_str}"
        )
    
    @staticmethod
    def _list_to_table(rows: List[List[str]]):
        table_inner = ""
        for row in rows:
            table_inner += "<tr>"
            for entry in row:
                table_inner += f"<td>{entry}</td>"
            table_inner += "</tr>"
        return f"<table>{table_inner}</table>"

    def generate(self) -> str:
        rows = [[c] for c in self._generate_transform_column()]
        self._add_column(rows)
        self._add_system_name(rows)
        self._add_column(rows, fill="|")
        self._add_outputs(rows)
        self._add_relation(rows)
        return self._list_to_table(rows) + "<br/>"