import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_plotly_embedding(
    df: pd.DataFrame = None,
    opacity: float = 0.5,
    **kwargs,
) -> go.Figure:
    """
    Plot the embedding of a dataframe with plotly.

    Args:
        df: dataframe with columns x, y, z, smact_allowed, mp_data.
        opacity: opacity of the markers. Default is 0.8.
        kwargs: additional keyword arguments.
    Returns:
        fig: plotly figure object.
    """
    # check if the dataframe is empty
    if df is None:
        return go.Figure()

    fig = px.scatter_3d(
        df,
        x="x",
        y="y",
        z="z",
        template="plotly_white",
        color="label",
        color_discrete_map={
            "0": "#D9D9D9",
            "1": "#22E000",
            "2": "#FF1201",
            "3": "#002FFF",
        },
        opacity=opacity,
        hover_data=[
            "formula",
        ],
    )

    # update hovertemplate
    fig.update_traces(
        hovertemplate="<br>".join(
            [
                "formula: %{customdata[0]}",
            ]
        )
    )

    # remove the background grid and axes and ticks and tick labels
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                showticklabels=False,
                title="",
            ),
            yaxis=dict(
                showticklabels=False,
                title="",
            ),
            zaxis=dict(
                showticklabels=False,
                title="",
            ),
        ),
    )

    # set title
    if "title" in kwargs:
        fig.update_layout(
            title=dict(
                text=kwargs["title"],
                font=dict(size=20),
                x=0.5,
                y=0.95,
                xanchor="center",
                yanchor="top",
            )
        )

    # update the legend labels
    legend_label_map = {
        "0": "Unlikely (False, False)",
        "1": "Interesting (False, True)",
        "2": "Missing (True, False)",
        "3": "Standard (True, True)",
    }

    for trace in fig.data:
        trace.name = legend_label_map[trace.name]

    # update the marker

    fig.update_traces(
        marker=dict(
            size=8,
            # line=dict(width=0.5, color="Grey"),
        ),
        selector=dict(mode="markers"),
    )

    # update the legend title
    fig.update_layout(
        legend_title_text="(smact_allowed, mp_data)",
    )

    return fig
