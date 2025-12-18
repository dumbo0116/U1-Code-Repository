import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def main():
    # Load data
    data1 = pd.read_csv("share-of-adults-who-are-overweight.csv")
    data2 = pd.read_csv("share-of-adults-defined-as-obese.csv")
    name = input("Welcome! Which country's data would you like to explore today?: ")

    # Extract relevant columns
    entity1 = data1["Entity"].tolist()
    rates_temp1 = data1["Prevalence of overweight among adults, BMI >= 25 (age-standardized estimate) (%) - Sex: both sexes - Age group: 18+  years of age"]
    entity2 = data2["Entity"].tolist()
    rates_temp2 = data2["Prevalence of obesity among adults, BMI >= 30 (crude estimate) (%) - Sex: both sexes - Age group: 18+  years of age"]
    years = data1["Year"].tolist()
    rates1 = []
    rates2 = []

    while True:
        for i in range(6798):
            if (entity1[i].lower() == name.lower()):
                rates1.append(rates_temp1[i])
        if (not rates1):
            print("\nSorry, that is not a existing country. Please enter the name of a valid country.")
            name = input("Which country's data would you like to explore today?: ")
            continue

        for i in range(6798):
            if (entity2[i].lower() == name.lower()):
                rates2.append(rates_temp2[i])
                name = entity2[i]
        break

    years_country = [years[i] for i in range(len(entity1)) if entity1[i].lower() == name.lower()]

    # Create figure and axis
    fig, ax_pie = plt.subplots(figsize=(6, 6))
    plt.subplots_adjust(bottom=0.25)

    # Initial pie chart
    initial_index = 0
    sizes = [rates2[initial_index], rates1[initial_index] - rates2[initial_index], 100 - rates1[initial_index]]
    labels = ["Obese", "Overweight", "Healthy"]
    colors = ["#b91e1e", "#f39229", "#6eaa40"]
    ax_pie.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax_pie.set_title(f"Obesity Rates of {name} ({years_country[initial_index]})")

    # Slider axis
    ax_slider = plt.axes([0.15, 0.1, 0.7, 0.03])
    year_slider = Slider(ax_slider, 'Year', min(years_country), max(years_country), valinit=years_country[0], valstep=1)
    fig.text(0.5, 0.18, "Use the slider or the left and right arrow keys to change the year",ha='center', va='center', fontsize=10)

    # Update function ()
    def update(val):
        year_val = int(year_slider.val)
        if year_val in years_country:
            idx = years_country.index(year_val)
            ax_pie.clear()
            sizes = [rates2[idx], rates1[idx] - rates2[idx], 100 - rates1[idx]]
            ax_pie.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            ax_pie.set_title(f"Obesity Rates of {name} ({year_val})")
            fig.canvas.draw_idle()

    year_slider.on_changed(update)

    # Add arrow-key navigation
    def on_key(event):
        current_val = int(year_slider.val)
        if event.key == 'right':
            new_val = min(current_val + 1, max(years_country))
            year_slider.set_val(new_val)

        elif event.key == 'left':
            new_val = max(current_val - 1, min(years_country))
            year_slider.set_val(new_val)

    fig.canvas.mpl_connect('key_press_event', on_key)

    plt.show()

main()