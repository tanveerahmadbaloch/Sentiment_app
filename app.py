import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file_path):
    # Load data from Excel file
    df = pd.read_excel(file_path)
    return df

def generate_pie_charts(df):
    st.title("Pie Charts for Each News Source and Label")

    for news_source in df['news source'].unique():
        source_df = df[df['news source'] == news_source]

        # Count occurrences of each label for the current news source
        label_counts = source_df['label'].value_counts()

        # Create a pie chart using Plotly Express
        fig = px.pie(label_counts, names=label_counts.index, values=label_counts.values,
                     title=f'Pie Chart for {news_source} and Label',
                     color_discrete_sequence=px.colors.qualitative.Set3)

        # Set consistent size for all pie charts
        fig.update_layout(height=400, width=400)

        # Show the pie chart
        st.plotly_chart(fig)

def generate_grouped_bar_chart(df):
    # Convert 'date' column to datetime type
    df['date'] = pd.to_datetime(df['date'])

    # Extract month and year from the 'date' column and convert to strings
    df['MonthYear'] = df['date'].dt.to_period('M').astype(str)

    # Count occurrences of each date, label, and news source triplet
    count_df = df.groupby(['MonthYear', 'label', 'news source']).size().reset_index(name='Count')

    st.title("Grouped Bar Plot with Month-Year, News Source, and Label")

    # Create a grouped bar plot using Plotly Express
    fig = px.bar(count_df, x='MonthYear', y='Count', color='news source', facet_col='label',
                 labels={'Count': 'Number of News'},
                 category_orders={'label': ['neutral', 'positive', 'negative']},
                 width=2000, height=600)

    # Update the layout for better readability (optional)
    fig.update_layout(
        xaxis_title='Month-Year',
        yaxis_title='Number of News',
        hovermode='x',
        showlegend=True,
        legend_title='News Source',
    )

    # Show the plot
    st.plotly_chart(fig)

def generate_date_label_bar_chart(df):
    st.title("Bar chart with labels and date")
    # Define custom colors for each label
    color_map = {'neutral': 'blue', 'positive': 'green', 'negative': 'red'}

    # Create a bar plot using Plotly Express with custom colors
    fig = px.bar(df, x='date', color='label', barmode='group',
                 color_discrete_map=color_map,
                 title='Bar Plot with Date and Label')

    # Update the layout for better readability (optional)
    fig.update_layout(
        xaxis_title='Date',
        hovermode='x',
        showlegend=True,
        legend_title='Label',
        height=600,  # Set the height of the figure
        width=2000
    )

    # Show the plot
    st.plotly_chart(fig)

def generate_sentiment_analysis_chart(df):
    # Calculate Sentiment Mean for each date and news source
    sentiment_mean_df = df.groupby(['date', 'news source'], as_index=False)['score'].mean()

    # Streamlit app
    st.title("Sentiment Analysis Dashboard")

    # Display the DataFrame if needed
    st.write(sentiment_mean_df)

    # Plotting
    fig = px.line(sentiment_mean_df, x='date', y='score', color='news source',
                  title='Sentiment Mean Over Time by News Source')

    # Increase the width of the entire graph
    fig.update_layout(width=2000)

    # Show the plot
    st.plotly_chart(fig)

def main():
    st.title("Newspaper Data Analysis")

    # Upload Excel file
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    if uploaded_file is not None:
        # Load data from the uploaded file
        df = load_data(uploaded_file)

        # Display the loaded data
        st.write("### Displaying Data:")
        st.write(df)

        # Generate the pie charts for each News Source and Label
        generate_pie_charts(df)

        # Generate the grouped bar chart for Month-Year, News Source, and Label
        generate_grouped_bar_chart(df)

        # Generate the bar chart for Date and Label
        generate_date_label_bar_chart(df)

        # Generate the sentiment analysis chart
        generate_sentiment_analysis_chart(df)

if __name__ == "__main__":
    main()



