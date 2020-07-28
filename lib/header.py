#Basics Requirements
import dash
import dash_html_components as html

header = html.Div(
            children = [
                html.Div(
                    [
                        html.H3("Team 10 - SuperSubsidio"),
                    ],
                    id="title",
                    className="two-thirds column",
                ),
                html.Div(
                    [],
                    id="logo",
                    className="one-third column",
                ),
                
            ],
            id="header",
        )
