import sqlite3
import json
import plotly.express as px
import pandas as pd
from pathlib import Path

# TODO plotly map

db_path = Path.cwd()/'crime.db'
connection = sqlite3.connect(db_path)
cursor = connection.cursor()
geojsonPath = Path.cwd()/'limitespdq.geojson'

def organize_category_amount() -> dict:
    categ_dict = dict()
    categ_dict['Breaking and Entering'] = _find_category_amount('Introduction')
    categ_dict['Theft from/to a motor vehicle'] = _find_category_amount('Vol dans / sur véhicule à moteur')
    categ_dict['Theft of a motor vehicle'] = _find_category_amount('Vol de véhicule à moteur')
    categ_dict['Mischief'] = _find_category_amount('Méfait')
    categ_dict['Robbery'] = _find_category_amount('Vols qualifiés')
    categ_dict['Murder resulting death'] = _find_category_amount('Infractions entrainant la mort')
    return categ_dict

def _find_category_amount(categ_name: str) -> int:
    cursor.execute('SELECT categorie ,count(*) '
                    'FROM crime '
                    'WHERE categorie =? '
                    'GROUP BY categorie;',
                    (categ_name,))

    result = cursor.fetchall()
    return result[0][1]

def pie_chart_crime_prop() -> None:
    crime_dict = organize_category_amount()
    fig = px.pie(values=crime_dict.values(), names=crime_dict.keys())
    fig.show()

def line_graph_years_and_crime() -> None:
    year_crime_amount_dict = _find_year_crime_amount()
    fig = px.line(x= year_crime_amount_dict.keys(),
                  y= year_crime_amount_dict.values(),
                  title = 'Amount of crime in Montreal over time (2015-2022)')
    fig.show()
def _find_year_crime_amount() -> dict:
    year_crime_amount_dict = dict()
    cursor.execute("SELECT SUBSTR(DATE, 1, 4) AS year, COUNT(*) AS count "
                   "FROM crime "
                   "WHERE SUBSTR(DATE, 1, 4) <> '2023' "
                   "GROUP BY SUBSTR(DATE, 1, 4);")
    result = cursor.fetchall()
    for i in result:
        year_crime_amount_dict[i[0]] = i[1]
    return year_crime_amount_dict

def segmentation_graph_crimes_and_precincts() -> None:
    categ_amt_precinct_df = _find_categ_amt_precinct_df()
    fig = px.bar(categ_amt_precinct_df,
                 x= "PDQ",
                 y= "count",
                 color= "CATEGORIE",
                 title= "The number of crimes in a specific precinct")
    fig.show()

def _find_categ_amt_precinct_df() -> pd.DataFrame:
    df = pd.read_sql_query("SELECT PDQ, categorie, COUNT(categorie) AS count "
                           "FROM crime "
                           "GROUP BY PDQ, categorie;", connection)
    # df = pd.read_sql_query("SELECT PDQ, categorie, COUNT(categorie) AS count "
    #                        "FROM crime "
    #                        "GROUP BY PDQ;", connection)
    return df

def bar_graph_tof_crime_rate() -> None:
    some_df = _find_categ_amount_tofd()
    fig = px.bar(some_df,
                 x = "QUART",
                 y = "count",
                 title= "Crime rate based on time of day")
    fig.show()

def _find_categ_amount_tofd() -> pd.DataFrame:
    query = """
            SELECT QUART, COUNT(categorie) AS count
            FROM crime
            GROUP BY QUART
            ORDER BY CASE
                    WHEN QUART = 'jour' then 1
                    WHEN QUART = 'soir' then 2
                    WHEN QUART = 'nuit' then 3
                    END;
            """
    df = pd.read_sql_query(query, connection)
    return df

def make_map(category: str, color_scheme: str) -> None:
    geojson = json.load(open(geojsonPath, "r"))
    some_df = _find_spec_categ_in_precinct(category)
    fig = px.choropleth_mapbox(some_df, geojson=geojson,
                               color="count",
                               locations="PDQ", featureidkey="properties.PDQ",
                               center={'lat': 45.508888, 'lon': -73.561668},
                               mapbox_style="carto-positron",
                               zoom=9,
                               color_continuous_scale=color_scheme,)
    fig.show()

def _find_spec_categ_in_precinct(category: str) -> pd.DataFrame:
    query = "SELECT PDQ, COUNT(categorie) AS count " + "FROM crime " + f'WHERE categorie = "{category}" ' + "GROUP BY PDQ;"
    df = pd.read_sql_query(query, connection)
    return df

if __name__ == "__main__":
    introduction = ("Introduction", "reds")
    vol_dans = ("Vol dans / sur véhicule à moteur", "blues")
    vol_vehicle = ("Vol de véhicule à moteur", "purples")
    mefait = ("Méfait", "greens")
    vol_qualif = ("Vols qualifiés", "oranges")
    infraction = ("Infractions entrainant la mort", "teal")

    make_map(*introduction)
    make_map(*vol_dans)
    make_map(*vol_vehicle)
    make_map(*mefait)
    make_map(*vol_qualif)
    make_map(*infraction)