import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load the data
file_path = 'furniture.xlsx'
df = pd.read_excel(file_path)

# Preprocess data to aggregate by month and year
df['order_date'] = pd.to_datetime(df['order_date'])
df['month_year'] = df['order_date'].dt.to_period('M').dt.to_timestamp()

# Calculate KPIs
total_sales = df['total_sales'].sum()
total_orders = df['order_date'].count()
avg_sales_per_order = total_sales / total_orders
most_profitable_month = df.groupby(df['order_date'].dt.to_period('M'))['total_sales'].sum().idxmax()

# Initialize the app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Furniture Store Sales Dashboard"),
    html.Div([
        html.Div([
            html.H3("Total Sales"),
            html.P(f"${total_sales:,.2f}")
        ], style={"display": "inline-block", "width": "24%", "text-align": "center"}),
        html.Div([
            html.H3("Total Orders"),
            html.P(f"{total_orders:,}")
        ], style={"display": "inline-block", "width": "24%", "text-align": "center"}),
        html.Div([
            html.H3("Avg Sales/Order"),
            html.P(f"${avg_sales_per_order:,.2f}")
        ], style={"display": "inline-block", "width": "24%", "text-align": "center"}),
        html.Div([
            html.H3("Most Profitable Month"),
            html.P(f"{most_profitable_month}")
        ], style={"display": "inline-block", "width": "24%", "text-align": "center"})
    ], style={"margin-bottom": "20px"}),
    html.Label("Select Sub-Category:"),
    dcc.Dropdown(
        id='sub_category_dropdown',
        options=[{'label': sub, 'value': sub} for sub in df['sub_category'].unique()],
        value=df['sub_category'].unique()[0],
        clearable=False
    ),
    dcc.Graph(id='sales_graph'),
    dcc.Graph(id='cumulative_sales_graph')
])

# Callback
@app.callback(
    [Output('sales_graph', 'figure'), Output('cumulative_sales_graph', 'figure')],
    [Input('sub_category_dropdown', 'value')]
)
def update_graphs(selected_sub_category):
    filtered_df = df[df['sub_category'] == selected_sub_category]
    
    # Area plot for total sales
    sales_fig = px.area(
        filtered_df, 
        x='order_date', 
        y='total_sales', 
        title=f"Total Sales for {selected_sub_category}",
        labels={'total_sales': 'Total Sales', 'order_date': 'Order Date'},
        template='ggplot2'
    )
    
    # Aggregate data for cumulative sales by month/year
    monthly_sales = filtered_df.groupby('month_year', as_index=False).agg({'total_sales': 'sum'})
    cumulative_sales_fig = px.bar(
        monthly_sales, 
        x='month_year', 
        y='total_sales', 
        title=f"Monthly Total Sales for {selected_sub_category}",
        labels={'total_sales': 'Total Sales', 'month_year': 'Month/Year'},
        template='ggplot2'
    )
    
    return sales_fig, cumulative_sales_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
