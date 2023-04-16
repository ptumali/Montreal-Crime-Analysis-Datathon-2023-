import sqlite3
import plotly.express as px
from pathlib import Path

# TODO Line chart showing years and crime amount
# TODO Pie chart proportions of crimes (types)
# TODO Segmentation bar graph of crimes based on precincts
# TODO plotly map
# TODO Bar graph(x-axis=day of time, y-axis=amount of crimes)

connection = sqlite3.connect(Path("D:/UCI/Montreal-Crime-Analysis-Datathon-2023-/crime.db"))
cursor = connection.cursor()

def find_category_amount(categ_name: str) -> int:
    cursor.execute('SELECT categorie ,count(*) '
                    'FROM crime '
                    'WHERE categorie =? '
                    'GROUP BY categorie;',
                    (categ_name,))

    result = cursor.fetchall()
    return result[0][1]

def organize_category_amount() -> dict:
    categ_dict = dict()
    categ_dict['Introduction'] = find_category_amount('Introduction')
    categ_dict['Vol dans / sur véhicule à moteur'] = find_category_amount('Vol dans / sur véhicule à moteur')
    categ_dict['Vol de véhicule à moteur'] = find_category_amount('Vol de véhicule à moteur')
    categ_dict['Méfait'] = find_category_amount('Méfait')
    categ_dict['Vols qualifiés'] = find_category_amount('Vols qualifiés')
    categ_dict['Infractions entrainant la mort'] = find_category_amount('Infractions entrainant la mort')
    return categ_dict

def pie_chart_crime_prop() -> None:
    crime_dict = organize_category_amount()
    fig = px.pie(values=crime_dict.values(), names=crime_dict.keys())
    fig.show()


if __name__ == "__main__":
    pie_chart_crime_prop()