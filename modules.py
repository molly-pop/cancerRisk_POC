from typing import Callable

import pandas as pd
import matplotlib.pyplot as plt

from shiny import Inputs, Outputs, Session, module, render, ui


# UI for Cancer Risk Calculator
@module.ui
def risk_ui():
    return ui.nav_panel(
        "Risk Calculator",
        ui.layout_columns(
            # Input form
            ui.card(
                ui.card_header("Cancer Risk Calculator"),
                ui.input_numeric("age", "Age", value=30, min=0),
                ui.input_select(
                    "sex",
                    "Sex",
                    choices=["Male", "Female"],
                ),
                ui.input_checkbox("smoking", "Do you smoke?"),
                ui.input_checkbox("alcohol", "Do you drink alcohol?"),
                ui.input_numeric("physical_activity", "Physical Activity (hours/week)", value=0, min=0),
                ui.input_text("diet", "Diet Quality (e.g., balanced, unhealthy)", value="balanced"),
                ui.input_action_button("submit", "Calculate Risk"),
            ),
            # Output card for risk result
            ui.card(
                ui.card_header("Your Cancer Risk"),
                ui.output_text_verbatim("risk_result"),
                ui.output_plot("risk_chart"),
            ),
        ),
    )


# Server logic for Cancer Risk Calculator
@module.server
def risk_server(input: Inputs, output: Outputs, session: Session):
    # Function to calculate a dummy cancer risk score based on input data
    def calculate_risk(age, sex, smoking, alcohol, physical_activity, diet):
        # Dummy risk calculation based on user input
        risk_score = age * 0.05
        if smoking:
            risk_score += 0.2
        if alcohol:
            risk_score += 0.1
        if physical_activity < 3:
            risk_score += 0.1
        if diet.lower() == "unhealthy":
            risk_score += 0.1
        return risk_score

    # Rendering the risk result
    @output
    @render.text
    def risk_result():
        # When the submit button is clicked, calculate the risk score
        if input.submit() > 0:
            risk_score = calculate_risk(
                input.age(),
                input.sex(),
                input.smoking(),
                input.alcohol(),
                input.physical_activity(),
                input.diet()
            )
            return f"Your estimated cancer risk score is: {risk_score:.2f}"
        else:
            return "Please fill out the form and click 'Calculate Risk'."

    # Plot the dummy risk chart (matplotlib)
    @output
    @render.plot
    def risk_chart():
        if input.submit() > 0:
            risk_score = calculate_risk(
                input.age(),
                input.sex(),
                input.smoking(),
                input.alcohol(),
                input.physical_activity(),
                input.diet(),
            )
            # Generate a simple bar chart for risk score
            categories = ["Base Risk", "Smoking", "Alcohol", "Physical Activity", "Diet"]
            values = [input.age() * 0.05, 0.2 if input.smoking() else 0, 0.1 if input.alcohol() else 0, 0.1 if input.physical_activity() < 3 else 0, 0.1 if input.diet().lower() == "unhealthy" else 0]

            plt.figure(figsize=(6, 4))
            plt.bar(categories, values, color='skyblue')
            plt.title('Risk Contribution Breakdown')
            plt.ylabel('Risk Score')
            plt.ylim(0, 0.3)
            plt.tight_layout()
            return plt.gcf()

@module.ui
def data_view_ui():
    return ui.nav_panel(
        "View Data",
        ui.layout_columns(
            ui.value_box(
                title="Row count",
                value=ui.output_text("row_count"),
                theme="primary",
            ),
            ui.value_box(
                title="Mean score",
                value=ui.output_text("mean_score"),
                theme="bg-green",
            ),
            gap="20px",
        ),
        ui.layout_columns(
            ui.card(ui.output_data_frame("data")),
            style="margin-top: 20px;",
        ),
    )


@module.server
def data_view_server(
    input: Inputs, output: Outputs, session: Session, df: Callable[[], pd.DataFrame]
):
    @render.text
    def row_count():
        return df().shape[0]

    @render.text
    def mean_score():
        return round(df()["training_score"].mean(), 2)

    @render.data_frame
    def data():
        return df()
