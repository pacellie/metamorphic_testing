from .report_generator import ReportGenerator


def shorten(value):
    value = str(value)
    if len(value) > 25:
        return value[:25] + "..."
    return value


class StringReportGenerator(ReportGenerator):
    """
    Produces output like this:

    input_x ---------------- system ------> output_x
    | (transform 0)                            |
    transform_result[0]                        |
    | (transform 1)                            | (relation) (holds?)
    transform_result[1]                        |
    | ...                                      |
    transform_result[-1] --- system ------> output_y
    """

    def generate(self) -> str:
        # This pretty much just builds the ASCII image above:
        output_lines = []
        output_lines.append(f"{self.report.input_x} ")
        # add transform names
        for transform_index, transform_result in enumerate(self.report.transform_results):
            output_lines.append(
                f"| {shorten(self.report.transforms[transform_index].get_name())} "
            )
            output_lines.append(shorten(str(transform_result).replace("\n", "\\n")) + " ")
        chars_left_of_system = max(len(line) for line in output_lines) + 2
        # add "---" for system arrows
        output_lines[0] = output_lines[0].ljust(chars_left_of_system, "-")
        output_lines[-1] = output_lines[-1].ljust(chars_left_of_system, "-")
        # add system name
        system_name = shorten(self.report.system.__name__)
        output_lines[0] += f" {system_name} --->"
        output_lines[-1] += f" {system_name} --->"
        # pad lines in between with spaces
        max_chars = max(len(line) for line in output_lines)
        for i in range(1, len(output_lines) - 1):
            output_lines[i] = output_lines[i].ljust(max_chars, " ") + " | "
        # add outputs
        output_lines[0] += f" {shorten(self.report.output_x)}"
        output_lines[-1] += f" {shorten(self.report.output_y)}"
        # add relation in the middle on the right
        holds_str = "does not hold"
        if self.report.relation_result.error:
            holds_str = f"error: {self.report.relation_result.error}"
        elif self.report.relation_result.output:
            holds_str = "holds"
        output_lines[len(output_lines) // 2] += (
            f" {shorten(self.report.relation.__name__)} {holds_str}"
        )
        return "\n".join(output_lines)