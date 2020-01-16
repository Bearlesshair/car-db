import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
import plotly.express as px
from cardb.models import Listing
import pandas as pd


def money_to_float(x):
    return float(x)


df = pd.DataFrame(list(Listing.objects.filter(car=4).values()))
drop_A=df.index[df["price"] == 0].tolist()
# drop_B=df.index[df["mileage"] == 0].tolist()
# c=drop_A+drop_B
df=df.drop(df.index[drop_A])
df = df.dropna(axis=0, how='any', thresh=None, subset=['mileage'], inplace=False)
df['price'] = df['price'].astype('float')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
col_options = [dict(label=x, value=x) for x in df.columns]
dimensions = ["x", "y", "color", "facet_col", "facet_row"]

app = DjangoDash('Scatterplot', external_stylesheets=external_stylesheets)
app.layout = html.Div(
    [
        html.H1("Demo: All the data!"),
        html.Div(
            [
                html.P([d + ":", dcc.Dropdown(id=d, options=col_options)])
                for d in dimensions
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="graph", style={"width": "75%", "display": "inline-block"}),
    ]
)


@app.callback(Output("graph", "figure"), [Input(d, "value") for d in dimensions])
def make_figure(x, y, color, facet_col, facet_row):
    return px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        facet_col=facet_col,
        facet_row=facet_row,
        height=700,
        marginal_x='box',
        marginal_y='violin',
    )

