import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Define the directories for sentiment data and where to save the graphs
sentiment_dir = 'Data/Sentiments'
graph_dir = 'Data/Plots'

# Function to process a sentiment file and extract comments and sentiments
def process_file(file_path):
    comments = []
    sentiments = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            # Extract comment and sentiment from each line in the file
            comment_line = lines[i].strip()
            sentiment_line = lines[i + 1].strip()
            comment = comment_line.split("Comment: ")[1] if "Comment: " in comment_line else ""
            sentiment = sentiment_line.split("Sentiment: ")[1].lower() if "Sentiment: " in sentiment_line else ""
            # Filter out invalid sentiments
            if sentiment in ["positive", "negative", "neutral"]:
                comments.append(comment)
                sentiments.append(sentiment)
            i += 3  # Move to the next set of comment and sentiment
    # Create a DataFrame to store comments and corresponding sentiments
    return pd.DataFrame({'Comment': comments, 'Sentiment': sentiments})

# Function to count sentiment occurrences and return unique sentiments
def count_sentiments(dataFrame):
    sentiment_counts = dataFrame['Sentiment'].value_counts()
    totalComments = len(dataFrame)
    return sentiment_counts, totalComments

# Function to plot and save sentiment counts as a bar chart
def plot_and_save_sentiments(sentiment_counts, title, save_path, totalComments):
    plt.figure(figsize=(10, 6))
    colors = {'positive': 'green', 'negative': 'red', 'neutral': 'black'}
    sentiment_counts = sentiment_counts.reindex(['positive', 'negative', 'neutral'])
    ax = sentiment_counts.plot(kind='bar', color=[colors.get(x, '#333333') for x in sentiment_counts.index])
    
    plt.xlabel('Sentiment')
    plt.ylabel('Sentiment Count')
    plt.title(title + "\nTotal Comments: " + str(totalComments))
    
    # Adjust the y-axis ticks to include the max count
    max_count = int(sentiment_counts.max())
    plt.yticks(range(0, max_count + 6, 5))

    # Add dashed lines across the y-axis corresponding to the labels
    for label in ax.get_yticklabels():
        plt.axhline(y=label.get_position()[1], color='gray', linestyle='--', alpha=0.6)

    # Create a legend with colors corresponding to the bars
    legend_colors = [mpatches.Patch(color=color, label=label.capitalize()) for label, color in colors.items()]
    plt.legend(handles=legend_colors)

    plt.tight_layout()
    # Save the plot as an image file
    plt.savefig(save_path)
    plt.close()

if __name__ == '__main__':
    # Iterate through sentiment files in the sentiment directory
    for file in os.listdir(sentiment_dir):
        if file.endswith('.txt'):
            file_path = os.path.join(sentiment_dir, file)
            # Process the sentiment file and extract data
            dataFrame = process_file(file_path)
            # Count sentiment occurrences and get total comments
            sentiment_counts, totalComments = count_sentiments(dataFrame)
            # Create a title for the plot and specify the save path
            plot_title = 'Sentiment Analysis for ' + file
            save_path = os.path.join(graph_dir, file.replace('.txt', '.png'))
            # Generate and save the sentiment plot
            plot_and_save_sentiments(sentiment_counts, plot_title, save_path, totalComments)
