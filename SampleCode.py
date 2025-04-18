import matplotlib.pyplot as plt

# Sample data
x = [1, 2, 3, 4, 5]
y = [10, 12, 8, 14, 11]

# Create the plot
plt.plot(x, y, marker='o', linestyle='-', color='blue')
plt.title("Sample Line Chart")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.grid(True)

# Save the plot as an image (since GUI display is not available)
plt.savefig("output_plot.png")

print("✅ Plot saved as 'output_plot.png'")
