import matplotlib.pyplot as plt
import plotly_express as px

class SportFig:
    """The SportFig class is used to make different figures for showing the gender, medal and age to one of the OS sport"""

    def __init__(self, df, name) -> None:
        self.name = name 
        self.df = df

    def sport_gender(self):
        gender = self.df[["NOC", "Sex", "Team", "Medal"]][self.df["Sport"] == self.name].value_counts().reset_index()
        gender = gender.rename(columns={0:"Number"})
        fig = px.scatter(gender, x="Team", y="Medal", size="Number", color="Sex", title="Medals for counties in gender")
        fig.show()
    
    def sport_country(self):
        country = self.df[["NOC", "Sex", "Team", "Medal"]][self.df["Sport"] == self.name].value_counts().reset_index()
        country = country.rename(columns={0:"Number"})
        country = country.groupby(["NOC"]).sum().reset_index()
        fig = px.choropleth(country, locations="NOC",
                    color="Number",
                    title="Total medals in OS (M & F)",
                    color_continuous_scale=px.colors.sequential.Plasma)
        fig.show()

    def sport_age(self):
        age = self.df[["Team", "Age"]][self.df["Sport"] == self.name]
        fig = px.box(age, x="Team", y="Age", title="Plot box for ages which the teams who won the OS medals")
        fig.show()
        
