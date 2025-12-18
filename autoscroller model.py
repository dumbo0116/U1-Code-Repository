# Import the packages needed to process data (pandas and matplotlib)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time

# Function definitions will be defined at the top of the python 
def main():

	# Present the User with a Menu to explore options

    # Use Pandas to open up each of the datafiles based on user selection
    data1 = pd.read_csv("share-of-adults-who-are-overweight.csv")
    data2 = pd.read_csv("share-of-adults-defined-as-obese.csv")
    choice = input("Welcome! Which country's data would you like to explore today?: ")

    # Convert each column in the dataset into a list
    columns_as_lists1 = {col: data1[col].tolist() for col in data1.columns}
    columns_as_lists2 = {col: data2[col].tolist() for col in data2.columns}

    # print them out for visual verification
    # for col, lst in columns_as_lists.items():
    #     print(f"{col}: {lst}")

    # Place each column into its own list
    entity1 = data1["Entity"].tolist()
    rates_temp1 = data1["Prevalence of overweight among adults, BMI >= 25 (age-standardized estimate) (%) - Sex: both sexes - Age group: 18+  years of age"]
    rates1 = []
    entity2 = data2["Entity"].tolist()
    rates_temp2 = data2["Prevalence of obesity among adults, BMI >= 30 (crude estimate) (%) - Sex: both sexes - Age group: 18+  years of age"]
    rates2 = []
    years = data1["Year"].tolist()
    while True:
        for i in range(6798):
            if (entity1[i].lower() == choice.lower()):
                rates1.append(rates_temp1[i])
        if (not rates1):
            print("\nSorry, that is not a existing country. Please enter the name of a valid country.")
            choice = input("Which country's data would you like to explore today?: ")
            continue

        for i in range(6798):
            if (entity2[i].lower() == choice.lower()):
                rates2.append(rates_temp2[i])
                name = entity2[i]
        break
        print("\nSorry, that is not an existing country abbreviation. Please enter a valid country abbreviation.")
        choice = input("Which country's data would you like to explore today? (Input a country abbreviation e.g. CAN, CHN, USA): ")
			
    # Create a figure and ax`is for the plot
    fig, ax = plt.subplots(figsize=(6, 6))

    # Initialize pie chart
    sizes1 = rates1[0:1]  # Start with the first value
    sizes2 = rates2[0:1]
    labels = ['Start']
    colors = ['#ff9999']

    # Create a pie chart
    wedges, texts, autotexts = ax.pie(sizes1, sizes2, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)

    # Function to update the pie chart for each frame in the animation
    def update(frame):
        ax.clear()  # Clear the axis before drawing new pie chart
        
        # Update the sizes, labels, and colors for the current frame
        sizes = [rates2[frame], rates1[frame] - rates2[frame], 100 - rates1[frame]]  # Get the current slice of percentages up to the frame index
        labels = ["Obese", "Overweight", "Healthy"]  # Create labels for the percentages
        colors = plt.cm.Paired([0.3, 0.5, 0.7])  # Generate a range of colors
        
        # Create a new pie chart with updated data
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        
        # Set title
        ax.set_title(f"Obesity Rates of {name} ({years[frame]})")
        if (years[frame] == 1990):
            time.sleep(0.5)
        
        return wedges, texts, autotexts
    
    # Create an animated pie chart with FuncAnimation
    ani = FuncAnimation(fig, update, frames=len(rates1), interval=200, repeat=True)

    # Show the animation
    plt.show()

main()
