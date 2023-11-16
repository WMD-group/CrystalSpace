import re
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def fn_chemical_check(
    df_embedding: pd.DataFrame, species_1: str, species_2: str
) -> np.array:
    """
    Check if the chemical system contains the specified species.

    Args:
        df_embedding (pd.DataFrame): Embedding dataframe.
        species_1 (str): Chemical species 1.
        species_2 (str): Chemical species 2.

    Returns:
        np.array: Boolean array for the chemical systems that contain the specified species.
    """

    chemicals = np.array(df_embedding.index)

    # regular expression patterns
    pattern_1 = r"{}(?:(?={})|(?![a-zA-Z]))".format(species_1, species_2)
    pattern_2 = r"{}(?:(?={})|(?![a-zA-Z]))".format(species_2, species_1)
    # get the mask
    mask = np.array(
        [
            True
            if re.search(pattern_1, chemical)
            and re.search(pattern_2, chemical)
            else True
            if re.search(pattern_1, chemical) and species_2 == "default"
            else True
            if re.search(pattern_2, chemical) and species_1 == "default"
            else True
            if species_1 == "default" and species_2 == "default"
            else False
            for chemical in chemicals
        ]
    )

    return mask


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig
