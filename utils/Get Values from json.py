import json
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog

# Load existing JSON file
with open('scenes.json', 'r') as file:
    data = json.load(file)

# Get the keys as a list
keys = list(data.keys())

# Extract x and y values from each key (assumes key format like "x_y")
x_vals = [int(k.split('_')[0]) for k in keys]
y_vals = [int(k.split('_')[1]) for k in keys]

# Set up Matplotlib figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
sc = ax.scatter(x_vals, y_vals, color='blue', s=100)

# Add text labels to the points
texts = []
for i, key in enumerate(keys):
    texts.append(ax.text(x_vals[i], y_vals[i] + 0.2, key,
                         ha='center', fontsize=9))

ax.set_title("Click on a point to enter coordinates")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.grid(True)
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.set_aspect('equal')

# Initialize Tkinter (used for the dialog)
root = tk.Tk()
root.withdraw()  # Hide the main window

# Define the event handler for mouse clicks
def on_click(event):
    # Only process clicks inside the plotting area
    if event.inaxes != ax:
        return

    # Check each label's bounding box to see if the point was clicked
    for i, text in enumerate(texts):
        bbox = text.get_window_extent(renderer=fig.canvas.get_renderer())
        if bbox.contains(event.x, event.y):
            clicked_key = keys[i]
            # Use Tkinter's dialog to ask for input
            answer = simpledialog.askstring("Input", 
                        f"Enter coordinate for key '{clicked_key}' (e.g., 11.029152436812732, 77.02635694395484):",
                        parent=root)
            if answer is not None:
                # Save the entered answer under the key in the JSON data
                data[clicked_key] = answer
                print(f"Updated {clicked_key}: {answer}")
                text.set_color('green')  # Visual cue for updated point
                # Optionally update the label with the new coordinate:
                text.set_text(f"{clicked_key}\n{answer}")
                fig.canvas.draw()
            break

# Connect the click event to the on_click function
fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()

# Save the updated JSON data back to the file
with open('scenes.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Updated 'scenes.json' with the new coordinates.")
