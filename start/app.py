from shiny import App, render, ui, reactive
import pandas as pd
import numpy as np
import ipyleaflet as L
from pathlib import Path
from asyncio import sleep
from plot_funs import plot_country, plot_world
from shinywidgets import output_widget, register_widget, reactive_read

temperature = pd.read_csv(Path(__file__).parent / 'temperatures.csv')

# Values from dropdown
countries = temperature['Country'].unique().tolist()

# CSS
font_style = "font-weight:100";

# Values for slider
temp_years = temperature['Year'].unique()
temp_years_min = temp_years.min()
temp_years_max = temp_years.max()

app_ui = ui.page_fluid(
    
    ui.h2("Climate change", style=font_style),
    ui.row(
        ui.column(
            6, ui.input_select(
                id="country",
                label="Choose a country",
                choices = countries
                )),
        ui.column(
            6,
            ui.row(
                ui.column(
                    6,
                    ui.input_slider(
                        id="year",
                        label="Choose a year",
                        min=temp_years_min,
                        max=temp_years_max,
                        value=temp_years_min,
                        step=1,
                        animate=False
                    )
                ),
                ui.column(6, ui.output_ui("color_map"))
            )
        )
    ),
    ui.row(
        ui.column(6, ui.output_plot("graph_country")),
        ui.column(6, output_widget("map"))
    ),
    ui.br(),
    ui.row(
        ui.column(6, ui.h5("Imprint", style=font_style)),
        ui.column(6, ui.p(f"Learn how this app is develop and deploy", style=font_style))
    ),
        ui.row(
        ui.column(6, ui.row(
            ui.column(2, ui.img(src="developer.png", width="32px"), style="text-align: center;"),
            ui.column(10, ui.p("Mauricio Combariza", style=font_style)),
        ),
                  ui.row(
                ui.column(2, ui.img(src="address2.png", width="32px"), style="text-align: center;"),
                ui.column(10, ui.p('Redderblock 28', style = font_style))
                ),ui.row(
                ui.column(2, ),
                ui.column(10, ui.p('22145 Hamburg', style = font_style))
                ),
                ui.row(
                ui.column(2, ),
                ui.column(10, ui.p('Germany', style = font_style))
                ),
                      ui.row(
                ui.column(2, ui.img(src="mail2.png", width="32px"), style="text-align: center;"),
                ui.column(10, ui.a(ui.p('bert.gollnick@posteo.net'), href="mailto:bert.gollnick@posteo.net", style = font_style))
                ),
                  
                  ),
        ui.column(6, ui.a(ui.img(src="course_logo_300x169.png"), href="https://www.udemy.com"), style="text-align:center;")
    ), 
    ui.p("Data Source: Sevgi Sy. Temperature Change, 2022", ui.a("Kaggle Dataset", href= "https://www.kaggle.com/datasets/sevgisarac/temperature-change"), ", ",ui.a("License: Attribution 3.0 IGO (CC BY 3.0 IGO)", href="https://creativecommons.org/licenses/by/3.0/igo/"), style = font_style),
    style="background-color:#fff"
)


def server(input, output, session):
    map = L.Map(center=(0,0), zoom = 1)
    # Add a distance scale
    map.add_control(L.leaflet.ScaleControl(position="bottomleft"))
    register_widget("map", map)

    # When the year changes, update the map
    @reactive.Effect
    def _():
        layer = plot_world(temp=temperature, year=input.year())
        map.add_layer(layer)

    @output
    @render.plot
    async def graph_country():
        with ui.Progress(min=1, max=15) as p:
            p.set(message = "Calculation in progress", detail="Please wait....")
            for i in range(1, 15):
                p.set(i, message=("Computing"))
                await sleep(0.1)
        g = plot_country(temp=temperature, country=input.country(), year=input.year())
        return g
    
    @output
    @render.ui
    def color_map():
        img = ui.img(src="colormap.png")
        return img

www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=www_dir)
