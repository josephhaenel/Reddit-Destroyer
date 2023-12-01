import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sentiment_dir = 'Data/Sentiments'
graph_dir = 'Data/Plots'

def process_file(file_path):
    comments = []
    sentiments = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            comment_line = lines[i].strip()
            sentiment_line = lines[i + 1].strip()
            comment = comment_line.split("Comment: ")[1] if "Comment: " in comment_line else ""
            sentiment = sentiment_line.split("Sentiment: ")[1].lower() if "Sentiment: " in sentiment_line else ""
            if sentiment in ["positive", "negative", "neutral"]:
                comments.append(comment)
                sentiments.append(sentiment)
            i += 3  # Move to the next set of comment and sentiment

    return pd.DataFrame({'Comment': comments, 'Sentiment': sentiments})

def count_sentiments(dataFrame):
    unique_sentiments = dataFrame['Sentiment'].unique()
    print("Unique sentiments:", unique_sentiments)
    sentiment_counts = dataFrame['Sentiment'].value_counts()
    totalComments = len(dataFrame)
    return sentiment_counts, totalComments

def plot_and_save_sentiments(sentiment_counts, title, save_path, totalComments):
    plt.figure(figsize=(10, 6))
    colors = {'positive': 'green', 'negative': 'red', 'neutral': 'black'}
    sentiment_counts = sentiment_counts.reindex(['positive', 'negative', 'neutral'])
    ax = sentiment_counts.plot(kind='bar', color=[colors.get(x, '#333333') for x in sentiment_counts.index])
    
    plt.xlabel('Sentiment')
    plt.ylabel('Sentiment Count')
    plt.title(title + "\nTotal Comments: " + str(totalComments))
    
    # Convert the max count to an integer and then use it in range
    max_count = int(sentiment_counts.max())
    plt.yticks(range(0, max_count + 6, 5))  # Adjust the range to include the max count

    # Add dashed lines across the y-axis corresponding to the labels
    for label in ax.get_yticklabels():
        plt.axhline(y=label.get_position()[1], color='gray', linestyle='--', alpha=0.6)

    # Create a legend with colors corresponding to the bars
    legend_colors = [mpatches.Patch(color=color, label=label.capitalize()) for label, color in colors.items()]
    plt.legend(handles=legend_colors)

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


if __name__ == '__main__':
    for file in os.listdir(sentiment_dir):
        if file.endswith('.txt'):
            file_path = os.path.join(sentiment_dir, file)
            dataFrame = process_file(file_path)
            sentiment_counts, totalComments = count_sentiments(dataFrame)
            plot_title = 'Sentiment Analysis for ' + file
            save_path = os.path.join(graph_dir, file.replace('.txt', '.png'))
            plot_and_save_sentiments(sentiment_counts, plot_title, save_path, totalComments)
