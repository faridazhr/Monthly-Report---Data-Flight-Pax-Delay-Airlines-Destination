
### get info ----
def highest_and_lowest_value(data, column_name):
    min_data = data.loc[data[f"{column_name}"].idxmin()]
    max_data = data.loc[data[f"{column_name}"].idxmax()]

    print(f"Lowest {column_name}:\n", min_data)
    print("\n")
    print(f"Highest {column_name}:\n", max_data)