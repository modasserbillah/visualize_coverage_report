import warnings

warnings.filterwarnings("ignore")

import click
import pandas as pd
import plotly.express as px


@click.command()
@click.option("--path", help="path or url to the html coverage report")
def visualize_coverage(path):
    if not path:
        print(
            """No path provided, using default url: 'https://nedbatchelder.com/files/sample_coverage_html/index.html' 
                You can specify a path using --path flag. For help use --help"""
        )
        path = "https://nedbatchelder.com/files/sample_coverage_html/index.html"
    df = prepare_data(path)
    create_plots(df)


def prepare_data(path):
    # using the example report from Ned's site
    report = pd.read_html(path)[0]
    # Split the path into separate columns to feed into plotly
    path_columns = report["Module"].str.split("/", expand=True)
    df = pd.concat([path_columns, report], axis=1)
    # coverage metric needs to be numeric for plotly
    df["coverage"] = df["coverage"].str.rstrip("%").astype("float")
    return df


def create_plots(df):
    treemap = px.treemap(
        df[:-1],  # excludes the summary row
        path=[0, 1],
        color_continuous_scale=px.colors.sequential.Peach,
        color="coverage",
    )
    treemap.show()
    sunburst = px.sunburst(
        df[:-1],
        path=[0, 1],
        color_continuous_scale=px.colors.sequential.Peach,
        color="coverage",
    )
    sunburst.show()


if __name__ == "__main__":
    visualize_coverage()
