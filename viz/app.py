import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("../data/global_land_temperatures_by_country.csv")
data["Date"] = pd.to_datetime(data["dt"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Temperature Data"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Temperature Data", className="header-title"
                ),
                html.P(
                    children="Analyze the temperature changes from 1750 until today",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Country", className="menu-title"),
                        dcc.Dropdown(
                            id="country-filter",
                            options=[
                                {"label": country, "value": country}
                                for country in np.sort(data.Country.unique())
                            ],
                            value="Åland",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="temperature-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="uncertainty-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [Output("temperature-chart", "figure"), Output("uncertainty-chart", "figure")],
    [
        Input("country-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(country, start_date, end_date):
    mask = (
        (data.Country == country)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    temperature_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AverageTemperature"],
                "type": "lines",
                "hovertemplate": "%{y:.2f}°C<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Temperature by Country",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksuffix": "°C", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    uncertainty_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AverageTemperatureUncertainty"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Average Temperature Uncertainty by Country", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return temperature_chart_figure, uncertainty_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)