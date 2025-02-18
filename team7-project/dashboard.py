import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the dataset
df = pd.read_csv("/home/ubuntu/ad688-employability-sp25A1-group7/data/analytics_jobs.csv")

# Initialize Dash App
app = dash.Dash(__name__)

# App Layout
app.layout = html.Div([
    html.H1("Data & Analytics Job Market Dashboard", style={'textAlign': 'center'}),
    
    html.Label("Filter by Job Title:"),
    dcc.Dropdown(
        id='job-filter',
        options=[{'label': job, 'value': job} for job in df['job_title'].unique()],
        multi=True,
        placeholder="Select Job Titles",
    ),
    
    html.Div(dcc.Graph(id='salary-histogram')),
    html.Div(dcc.Graph(id='job-title-bar')),
    html.Div(dcc.Graph(id='skills-bar'))
])

# Callback Function to Update Graphs
@app.callback(
    [Output('salary-histogram', 'figure'),
     Output('job-title-bar', 'figure'),
     Output('skills-bar', 'figure')],
    [Input('job-filter', 'value')]
)
def update_graphs(selected_jobs):
    filtered_df = df if not selected_jobs else df[df['job_title'].isin(selected_jobs)]
    
    fig_salary = px.histogram(
        filtered_df, x="salary", nbins=30, title="Salary Distribution",
        labels={'salary': 'Salary (USD)'}, color_discrete_sequence=['blue']
    )
    
    top_jobs = filtered_df['job_title'].value_counts().nlargest(10).reset_index()
    fig_job = px.bar(
        top_jobs, x="index", y="job_title", title="Top 10 Most Common Job Titles",
        labels={'index': 'Job Title', 'job_title': 'Count'}, color="index"
    )
    
    skills_expanded = filtered_df.assign(skills=filtered_df['skills'].str.split(",")).explode("skills")
    top_skills = skills_expanded['skills'].value_counts().nlargest(10).reset_index()
    fig_skills = px.bar(
        top_skills, x="index", y="skills", title="Top 10 In-Demand Skills",
        labels={'index': 'Skill', 'skills': 'Count'}, color="index"
    )
    
    return fig_salary, fig_job, fig_skills

# Run the Dash App
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8050)
