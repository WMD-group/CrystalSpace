import os
from pathlib import Path
from fire import Fire

import ase
from pymatgen.core import Structure
import pandas as pd

from dash import Dash, html, Input, Output, dcc, dash_table, no_update
import dash_bootstrap_components as dbc

from visualize_embedding import get_plotly_embedding
from visualize_structure import get_plotly_structure
from utils import fn_chemical_check, blank_fig

PARENT_DIR = Path(os.path.dirname(__file__))
# load label data
LABEL_DATA = pd.read_pickle(PARENT_DIR / "assets/df_binary_label.pkl")
LABEL_DATA["label"] = LABEL_DATA["label"].astype(str)
# load materials project data
MP_DATA = pd.read_pickle(PARENT_DIR / "assets/df_binary_mp.pkl")


def main(
    debug: bool = True,
    host: str = "0.0.0.0",
    port: int = 8050,
):
    # initialize the app - incorporate a Dash Bootstrap theme
    external_stylesheets = [dbc.themes.MINTY]
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    # app layout
    app.layout = dbc.Container(
        [
            # set the app title
            dbc.Row(
                [
                    html.H1(
                        "Crystal Space for Binary Compounds 🚀",
                        style={
                            "textAlign": "center",
                            "color": "black",
                        },
                    ),
                    html.Hr(),
                ]
            ),
            # set selector for methods
            dbc.Row(
                [
                    # set selector for dimension reduction method
                    dbc.Col(
                        dbc.Select(
                            id="reduction-method-selelct",
                            options=[
                                {"label": "t-SNE", "value": "tsne"},
                                {"label": "UMAP", "value": "umap"},
                                {"label": "PCA", "value": "pca"},
                            ],
                            value="tsne",
                        ),
                        width=3,
                    ),
                    # set selector for embedding method
                    dbc.Col(
                        dbc.Select(
                            id="embedding-method-select",
                            options=[
                                {"label": "magpie", "value": "magpie"},
                                {"label": "mat2vec", "value": "mat2vec"},
                                {"label": "megnet16", "value": "megnet16"},
                                {"label": "oliynyk", "value": "oliynyk"},
                                {"label": "skipatom", "value": "skipatom"},
                                {"label": "random_200", "value": "random_200"},
                            ],
                            value="skipatom",
                        ),
                        width=3,
                    ),
                ],
                justify="start",
            ),
            html.Br(),
            # set selector for chemical systems
            dbc.Row(
                [
                    # set selector for chemical system 1
                    dbc.Col(
                        dbc.Select(
                            id="chemical-system-select-1",
                            options=[
                                {
                                    "label": ase.data.chemical_symbols[i],
                                    "value": ase.data.chemical_symbols[i],
                                }
                                if i != 0
                                else {"label": "species 1", "value": "default"}
                                for i in range(104)
                            ],
                            value="default",
                        ),
                        width=2,
                    ),
                    # set selector for chemical system 2
                    dbc.Col(
                        dbc.Select(
                            id="chemical-system-select-2",
                            options=[
                                {
                                    "label": ase.data.chemical_symbols[i],
                                    "value": ase.data.chemical_symbols[i],
                                }
                                if i != 0
                                else {"label": "species 2", "value": "default"}
                                for i in range(104)
                            ],
                            value="default",
                        ),
                        width=2,
                    ),
                ],
                justify="start",
            ),
            dcc.Store(id="embedding-data-store", data=None),
            html.Br(),
            # set scatter and crystal structure
            dbc.Row(
                [
                    # set the scatter plot
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H4(
                                        "Scatter Plot",
                                        style={
                                            "textAlign": "center",
                                            "color": "black",
                                        },
                                    )
                                ),
                                dbc.CardBody(
                                    [
                                        dcc.Markdown(
                                            id="method-name",
                                            children="",
                                            style={
                                                "textAlign": "center",
                                                "color": "black",
                                                "fontSize": 20,
                                            },
                                        ),
                                        dcc.Graph(
                                            id="3d-scatter-plot",
                                            figure=blank_fig(),
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        width=6,
                    ),
                    # set the crystal structure
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H4(
                                        "Crystal Structure",
                                        style={
                                            "textAlign": "center",
                                            "color": "black",
                                        },
                                    )
                                ),
                                dbc.CardBody(
                                    [
                                        # name of the crystal structure
                                        dcc.Markdown(
                                            id="crystal-structure-name",
                                            children="Click a point on the scatter plot",
                                            style={
                                                "textAlign": "center",
                                                "color": "black",
                                                "fontSize": 20,
                                            },
                                        ),
                                        # graph
                                        dcc.Graph(
                                            id="crystal-structure",
                                            figure=blank_fig(),
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        width=6,
                    ),
                ],
                justify="start",
            ),
            html.Br(),
            # set a table with properties
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            id="table",
                        ),
                    ]
                ),
                style={"border": "none"},
            ),
        ]
    )

    # set the callback for the scatter plot
    @app.callback(
        [
            Output("method-name", "children"),
            Output("3d-scatter-plot", "figure"),
        ],
        Input("reduction-method-selelct", "value"),
        Input("embedding-method-select", "value"),
        Input("chemical-system-select-1", "value"),
        Input("chemical-system-select-2", "value"),
    )
    def update_3d_scatter_plot(
        reduction_method,
        embedding_method,
        chemical_system_1,
        chemical_system_2,
    ):
        # set default values for reduction_method and embedding_method
        if reduction_method == "default":
            reduction_method = "tsne"
        if embedding_method == "default":
            embedding_method = "magpie"

        # set the path to the embedding
        path_embedding = Path(PARENT_DIR, "assets/reduced_embeddings_3d")
        path_embedding = (
            path_embedding / f"{reduction_method}_{embedding_method}_mean.pkl"
        )
        if not path_embedding.exists():
            raise FileNotFoundError(f"Embedding file {path_embedding} does not exist.")
        # read the embedding
        df_embedding = pd.read_pickle(path_embedding)
        df_embedding.columns = ["x", "y", "z"]
        df_embedding["formula"] = df_embedding.index

        # merge the total data with the embedding
        df_plot = df_embedding.join(LABEL_DATA)

        # check if the chemical system contains the specified species
        mask = fn_chemical_check(df_plot, chemical_system_1, chemical_system_2)

        # get the plotly scatter plot
        new_fig = get_plotly_embedding(
            df_plot[mask],
        )

        new_method_name = f"{reduction_method} plot with {embedding_method} Embedding"

        return new_method_name, new_fig

    # set the callback for the crystal structure
    @app.callback(
        [
            Output("crystal-structure-name", "children"),
            Output("crystal-structure", "figure"),
            Output("table", "children"),
        ],
        Input("3d-scatter-plot", "clickData"),
    )
    def update_hoverdata_scatter(clickData):
        if clickData is None:
            return no_update

        # get origin_idx from hoverData
        formula = clickData["points"][0]["customdata"][0]
        if not formula in MP_DATA.index:
            blank_table = dash_table.DataTable(
                [{"index": "mp_data", formula: "None"}],
                style_cell={
                    "textAlign": "center",
                    "width": "50%",
                    "overflow": "hidden",
                },
            )
            return formula, blank_fig(), blank_table

        # get new structure
        hover_data = MP_DATA.loc[formula]
        new_structure = hover_data["structure"]

        # update structures
        mg_structure = Structure.from_dict(new_structure)
        new_fig = get_plotly_structure(mg_structure)

        # update the table
        new_table = dash_table.DataTable(
            data=hover_data[
                [
                    "formula_anonymous",
                    "volume",
                    "density",
                    "density_atomic",
                    "energy_per_atom",
                    "formation_energy_per_atom",
                    "energy_above_hull",
                    "is_stable",
                    "band_gap",
                    "efermi",
                    "total_magnetization",
                ]
            ]
            .T.reset_index()
            .to_dict("records"),
            selected_rows=[0],
            style_cell={
                "textAlign": "center",
                "width": "50%",
                "overflow": "hidden",
            },
        )
        return formula, new_fig, new_table

    # run the app
    app.run(debug=debug, host=host, port=port)


if __name__ == "__main__":
    Fire(main)
