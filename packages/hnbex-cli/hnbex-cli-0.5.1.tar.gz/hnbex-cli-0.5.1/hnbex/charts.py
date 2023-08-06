import tempfile

from subprocess import call

from hnbex.output import print_err


# A template for rendering a text chart
TEMPLATE_DUMB = """set terminal dumb

set title "{currency} Exchange Rate"

set timefmt "%Y-%m-%d"

set xdata time
set xrange [ "{start_date:%Y-%m-%d}":"{end_date:%Y-%m-%d}" ]
set xlabel "Date"

plot '{data_file}' using 1:2 title "" with linespoints pt "x"
"""

# A template for rendering a graphical chart
TEMPLATE_QT = """set terminal qt

set title "{currency} Exchange Rate"

set timefmt "%Y-%m-%d"

set xdata time
set xrange [ "{start_date:%Y-%m-%d}":"{end_date:%Y-%m-%d}" ]
set xlabel "Date"

set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 ps 1.5
plot '{data_file}' using 1:2 title "" with linespoints ls 1
"""


def get_template(name):
    if name == 'qt':
        return TEMPLATE_QT
    if name == 'dumb':
        return TEMPLATE_DUMB
    raise ValueError("Unknown template: {}".format(name))


def plot(currency, rates, start_date, end_date, template):
    plot_data = "\n".join(["{} {}".format(rate['date'], rate['median_rate'])
        for rate in rates])

    with tempfile.NamedTemporaryFile() as script_file:
        with tempfile.NamedTemporaryFile() as data_file:
            script_template = get_template(template)
            script = script_template.format(
                currency=currency,
                start_date=start_date,
                end_date=end_date,
                data_file=data_file.name,
            )

            script_file.write(script.encode('utf-8'))
            script_file.flush()

            data_file.write(plot_data.encode('utf-8'))
            data_file.flush()

            try:
                call(['gnuplot', '-c', script_file.name, '-p'])
            except FileNotFoundError as ex:
                print_err(ex)

                from hnbex.commands import CommandError
                raise CommandError("Charting failed. Do you have gnuplot installed?")
