import numpy as np

from bokeh.models import Button, Column, ColumnDataSource, CustomJS, Jitter, LabelSet
from bokeh.plotting import figure, output_file, show

N = 1000

source = ColumnDataSource(data=dict(
    x=np.ones(N), xn=2*np.ones(N), xu=3*np.ones(N), y=np.random.random(N)*10
))

normal = Jitter(width=0.2, distribution="normal")
uniform = Jitter(width=0.2, distribution="uniform")

p = figure(x_range=(0, 4), y_range=(0,10), toolbar_location=None, x_axis_location="above")
p.circle(x='x',  y='y', color='firebrick', source=source, size=5, alpha=0.5)
p.circle(x='xn', y='y', color='olive',     source=source, size=5, alpha=0.5)
p.circle(x='xu', y='y', color='navy',      source=source, size=5, alpha=0.5)

label_data = ColumnDataSource(data=dict(
    x=[1,2,3], y=[0, 0, 0], t=['Original', 'Normal', 'Uniform']
))
label_set = LabelSet(x='x', y='y', text='t', y_offset=-4, source=label_data,
                     text_baseline="top", text_align='center')
p.add_layout(label_set)

callback = CustomJS(args=dict(source=source, normal=normal, uniform=uniform), code="""
    const data = source.data;
    for (let i = 0; i < data.y.length; i++) {
        data.xn[i] = normal.compute(data.x[i] + 1);
    }
    for (let i = 0; i < data.y.length; i++) {
        data.xu[i] = uniform.compute(data.x[i] + 2);
    }
    source.change.emit();
""")

button = Button(label='Press to apply Jitter!', width=300)
button.js_on_click(callback)

output_file("transform_jitter.html", title="Example Jitter Transform")

show(Column(button, p))
