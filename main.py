import sqlite3
import plotly.express as px
import pandas as pd
from pathlib import Path

# TODO plotly map
# TODO Bar graph(x-axis=day of time, y-axis=amount of crimes)

connection = sqlite3.connect(Path("D:/UCI/Montreal-Crime-Analysis-Datathon-2023-/crime.db"))
cursor = connection.cursor()

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
    categ_amt_precinct_df = _find_category_amount_precinct_dataframe()
    fig = px.bar(categ_amt_precinct_df,
                 x= "PDQ",
                 y= "count",
                 color= "CATEGORIE",
                 title= "The number of crimes in a specific precinct")
    fig.show()

def _find_category_amount_precinct_dataframe() -> pd.DataFrame:
    df = pd.read_sql_query("SELECT PDQ, categorie, COUNT(categorie) AS count "
                           "FROM crime "
                           "GROUP BY PDQ, categorie;", connection)
    # df = pd.read_sql_query("SELECT PDQ, categorie, COUNT(categorie) AS count "
    #                        "FROM crime "
    #                        "GROUP BY PDQ;", connection)
    return df

if __name__ == "__main__":
    print(_find_category_amount_precinct_dataframe())
    # segmentation_graph_crimes_and_precincts()
