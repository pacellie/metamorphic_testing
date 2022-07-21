from typing import Callable, List
import traceback
from .report_generator import ReportGenerator


class RelationDoesNotHoldError(Exception):
    pass


def error_html(error: Exception) -> str:
    if isinstance(error, RelationDoesNotHoldError):
        return '<span class="error">does not hold</span>'
    error_str = traceback.format_tb(error.__traceback__)[-1].replace("\n", "<br />")
    return f'<span class="error">{error_str}</span>'


def placeholder_html(s: str) -> str:
    return f'<i>{s}</i>'


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
        column = [self.visualize_input(self.report.input_x)]
        previous_fail = False
        for transform_index, transform_result in enumerate(self.report.transform_results):
            column.append(
                f"⇩ {self.report.transforms[transform_index].get_name()}"
            )
            if previous_fail:
                column.append(placeholder_html("(skipped)"))
            elif transform_result.error:
                column.append(error_html(transform_result.error))
                previous_fail = True
            else:
                column.append(self.visualize_input(transform_result.output))
        return column
    
    @staticmethod
    def _add_column(to: List[List], fill=""):
        for x in to:
            x.append(fill)
    
    def _transform_error_occurred(self) -> bool:
        return any(
            transform_result.error is not None
            for transform_result in self.report.transform_results
        )
    
    def _add_system_name(self, rows: List[List[str]]):
        """Put the system name in the second column of the first & last row."""
        system_name = self.report.system.__name__
        rows[0][1] = f"⇨ {system_name} ⇨"
        if self._transform_error_occurred():
            system_name += placeholder_html(" (skipped)")
        rows[-1][1] = f"⇨ {system_name} ⇨"
    
    def _add_outputs(self, rows: List[List[str]]):
        """Add the outputs in the last column of the first & last row."""
        x_err = self.report.output_x.error is not None
        y_err = self.report.output_y.error is not None
        if x_err:
            output_x_str = f"""
                {error_html(self.report.output_x.error)}
                <br />
                (⇨ Transformations skipped)
            """
        else:
            output_x_str = self.visualize_output(self.report.output_x.output)
        rows[0][-1] = output_x_str
        if not x_err:
            if self._transform_error_occurred():
                output_y_str = placeholder_html("(skipped)")
            elif y_err:
                output_y_str = error_html(self.report.output_y.error)
            else:
                output_y_str = self.visualize_output(self.report.output_y.output)
            rows[-1][-1] = output_y_str
    
    def _add_relation(self, rows: List[List[str]]):
        """Add the relation in the last row in the middle."""
        if self.report.output_x.error is not None:
            # Everything just stopped, no relation annotation
            return
        if self._transform_error_occurred() or self.report.output_y.error is not None:
            holds_str = placeholder_html("(skipped)")
        elif self.report.relation_result.error:
            holds_str = "<br />" + error_html(self.report.relation_result.error)
        elif self.report.relation_result.output:
            holds_str = "holds"
        else:
            holds_str = error_html(RelationDoesNotHoldError())
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