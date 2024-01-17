import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
import numpy as np
from PIL import Image

# Data Preparation
data = {
    "Astronaut": ["Anatoly Solovyev", "Michael Lopez-Alegria", "Stephen G. Bowen", "Andrew J. Feustel", 
                  "Bob Behnken", "Peggy Whitson", "Fyodor Yurchikhin", "Shane Kimbrough", "Jerry L. Ross", 
                  "John M. Grunsfeld", "Sergey Prokopyev", "Christopher Cassidy", "Oleg Artemyev", 
                  "Richard Mastracchio", "Sunita Williams", "Steven L. Smith", "Michael Fincke", 
                  "Michael E. Fossum", "Scott E. Parazynski", "Joseph R. Tanner", "Andrew Morgan", 
                  "Robert L. Curbeam", "Nikolai Budarin", "Douglas H. Wheelock", "James H. Newman", 
                  "Yuri Onufrienko", "Christina Koch", "Richard Linnehan", "Sergey Avdeev", "David Wolf"],
    "Agency": ["RSA", "NASA", "NASA", "NASA", "NASA", "NASA", "RSA", "NASA", "NASA", "NASA", "RSA", 
               "NASA", "RSA", "NASA", "NASA", "NASA", "NASA", "NASA", "NASA", "NASA", "NASA", "NASA", 
               "RSA", "NASA", "NASA", "RSA", "NASA", "NASA", "RSA", "NASA"],
    "EVA Count": [16, 10, 10, 9, 10, 10, 9, 9, 9, 8, 8, 10, 8, 9, 7, 7, 9, 7, 7, 7, 7, 7, 8, 6, 6, 8, 6, 6, 10, 7],
    "EVA Time": ["82:22", "67:40", "65:57", "61:48", "61:10", "60:21", "59:28", "59:28", "58:32",   
                 "58:30", "55:15", "54:51", "53:32", "53:04", "50:40", "49:48", "48:37", "48:32", "47:05", "46:29", "45:48", "45:34", "44:25", "43:30", "43:13", "42:33", "42:15", "42:12", "42:02", "41:57"]
}

df = pd.DataFrame(data)

# Converting EVA Time to minutes for plotting
def time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(":"))
    return hours * 60 + minutes

df["EVA Time (min)"] = df["EVA Time"].apply(time_to_minutes)

# Sorting the DataFrame by EVA Time in ascending order
df_sorted_asc = df.sort_values(by="EVA Time (min)", ascending=True)

# Setting the colors for the agencies
color_mapping = {"NASA": "blue", "RSA": "red"}
df_sorted_asc["color"] = df_sorted_asc["Agency"].map(color_mapping)

# Plotting
plt.figure(figsize=(10, 10), facecolor="black")
plt.subplots_adjust(top=0.8)  # Adjusting space for the updated chart title

# Create EVA Time primary axis bars 
ax1 = plt.gca()
eva_time_bars = ax1.barh(df_sorted_asc["Astronaut"], df_sorted_asc["EVA Time (min)"], color=df_sorted_asc['color'], alpha=0.7)

# Create EVA Time primary axis bar data labels
for bar in eva_time_bars:
    bar_width = bar.get_width()
    # Find the corresponding HH:MM value for the bar
    hh_mm_value = df_sorted_asc[df_sorted_asc["EVA Time (min)"] == bar_width]["EVA Time"].values[0]
    ax1.text(bar_width + 10, bar.get_y() + bar.get_height()/2, hh_mm_value, 
             va='center', ha='left', color="white", fontsize=8)

# Create EVA Count secondary axis bars
ax2 = ax1.twiny()
eva_count_bars = ax2.barh(df_sorted_asc["Astronaut"], df_sorted_asc["EVA Count"], height=0.3, color="white", alpha=0.7)

# Create EVA Count secondary axis bar data labels
for bar in eva_count_bars:
    label_x_pos = .5  # Position to the right of the y-axis
    label_str = f"{bar.get_width():<2}"  # Format the label with whitespace padding
    # Decrease the height of the background box by adjusting the padding
    bbox_props = dict(facecolor='black', edgecolor='none', boxstyle='square,pad=0.05', alpha=0.7)
    ax2.text(label_x_pos, bar.get_y() + bar.get_height()/2, label_str,
             ha='center', va='center', color="white", fontsize=8, bbox=bbox_props)

# Create agency legend
legend_elements = [Patch(facecolor='blue', edgecolor='blue', label='NASA', alpha=0.7),
                   Patch(facecolor='red', edgecolor='red', label='RSA', alpha=0.7)]
ax1.legend(handles=legend_elements, title="", loc='center right', bbox_to_anchor=(1, 0.5))

# Modify primary and secondary x-axis
for ax in [ax1, ax2]:
    # Hide spines for top, bottom, and right
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # Hide axis ticks and labels for x-axis
    ax.tick_params(bottom=False, labelbottom=False, top=False, labeltop=False)
    # Hide grid lines
    ax.grid(False)
    ax.set_facecolor('black')

# Keep the y axis left labels
ax1.tick_params(left=True, labelleft=True)  # Show y-axis ticks and labels
ax1.tick_params(axis='y', labelcolor='white')

# Load an image
image = Image.open('jwst_background.jpg')
image = np.array(image)
# Get the current limits of the plot
x_min, x_max = ax1.get_xlim()
y_min, y_max = ax1.get_ylim()
# Set image as the background with correct extent
ax1.imshow(image, aspect='auto', extent=[x_min, x_max, y_min, y_max], zorder=-1)

# Main title
plt.text(0.5, 1.03, "Top 30 Spacewalk Records by Cumulative EVA Time\n", horizontalalignment='center', fontsize=14, transform=ax1.transAxes, color='white')
# Subtitle
plt.text(0.5, 1.01, "EVA Time (HH:MM) (colored bars), EVA Count (white bars)\n", horizontalalignment='center', fontsize=10, transform=ax1.transAxes, color='white')
# Source
plt.text(0.5, 0.99, "Data from https://en.wikipedia.org/wiki/List_of_cumulative_spacewalk_records\ncreated by @curtispokrant", horizontalalignment='center', fontsize=8, transform=ax1.transAxes, color='white')

# Adjust the layout
plt.subplots_adjust(top=0.85)
plt.tight_layout(pad=3.0)
plt.show()
