from future.utils import listitems
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from bokeh.io import curdoc
from bokeh.models.widgets import Select, Button, TableColumn, DataTable, CheckboxGroup, Tabs, Panel

source = ColumnDataSource(data=dict(var_name=[]))
variables = [str(i) for i in range(0, 100)]
include = {name: True for name in variables}


def update_check_box():
    if include[selector.value]:
        include_checkbox.active = [0]
    else:
        include_checkbox.active = []


def prev_action():
    current_index = selector.options.index(selector.value)
    selector.value = selector.options[current_index - 1]
    update_check_box()


def selector_action(atrr, old, new):
    update_check_box()


def check_box_action(attr, old, new):
    if new:
        include[selector.value] = True
    if not new:
        include[selector.value] = False
    included_vars = [key for key, value in listitems(include) if value]
    included_vars.sort()
    source.data = {'var_name': included_vars}


include_checkbox = CheckboxGroup(labels=["Include"], active=[], width=400)
include_checkbox.on_change('active', check_box_action)

prev = Button(label="<", button_type="primary", width=50)
prev.on_click(prev_action)

selector = Select(value=variables[0], options=variables, width=300)
selector.title = "Select a Variable"
selector.on_change('value', selector_action)

columns = [TableColumn(field="var_name", title="Title", width=100)]
data_table = DataTable(source=source, columns=columns, height=175, width=275, row_headers=False)

layout_1 = column(include_checkbox, prev, selector)
layout_2 = column(data_table)

tab1 = Panel(child=layout_1, title='tab1')
tab2 = Panel(child=layout_2, title='tab1')

tabs = Tabs(tabs=[tab1, tab2])

curdoc().add_root(tabs)
curdoc().title = "Bug Test"
