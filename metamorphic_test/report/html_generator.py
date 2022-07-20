from typing import Callable
from .report_generator import ReportGenerator


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

    visualize_input: Callable[..., str] = str

    def generate(self) -> str:
        rows = []
        rows.append([self.visualize_input(self.report.input_x)])
        # add transform names
        for transform_index, transform_result in enumerate(self.report.transform_results):
            rows.append(
                [f"⇩ {self.report.transforms[transform_index].get_name()}", "", "", "", "|"]
            )
            rows.append([str(transform_result), "", "", "", "|"])
            last_transform_result = transform_result
        if last_transform_result.error is None:
            rows[-1][0] = self.visualize_input(last_transform_result.output)
        # add system name with arrows
        system_name = self.report.system.__name__
        rows[0][1:4] = ["⇨", system_name, "⇨"]
        rows[-1][1:4] = ["⇨", system_name, "⇨"]
        # add outputs
        rows[0].append(str(self.report.output_x ))
        rows[-1][-1] = str(self.report.output_y)
        # add relation in the middle on the right
        holds_str = "does not hold"
        if self.report.relation_result.error:
            holds_str = f"error: {self.report.relation_result.error}"
        elif self.report.relation_result.output:
            holds_str = "holds"
        rows[len(rows) // 2][-1] = (
            f"⇵ {self.report.relation.__name__} {holds_str}"
        )
        table_inner = ""
        for row in rows:
            table_inner += "<tr>"
            for entry in row:
                table_inner += f"<td>{entry}</td>"
            table_inner += "</tr>"
        return f"<table>{table_inner}</table><br/>"