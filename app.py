from pathlib import Path

import pandas as pd
from modules import data_view_server, data_view_ui, risk_server, risk_ui

from shiny import App, Inputs, Outputs, Session, reactive, ui

app_ui = ui.page_navbar(
    risk_ui("tab1"),
    data_view_ui("tab2"),
    sidebar=ui.sidebar(
        "This is a proof-of-concept for the Cancer Risk tool for CIS 3296 ",
        ui.input_select(
            "type",
            "Type of Cancer",
            choices=[
                "Breast Cancer",
                "Lung Cancer",
                "Prostate Cancer",
                "Colon Cancer",
                "Pancreatic Cancer",
            ],
        ),
        width="300px",
    ),
    header=ui.include_css(Path(__file__).parent / "styles.css"),
    id="tabs",
    title="Cancer Risk Calculator",
    fluid="true"
)


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Calc()
    def filtered_data() -> pd.DataFrame:
        return df.loc[df["account"] == input.account()]

    risk_server(id="tab1")
    data_view_server(id="tab2", df=filtered_data)


app = App(app_ui, server)
