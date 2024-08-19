import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", message="The figure layout has changed to tight")

def plot_distance_per_day(data, time_col, distance_col, num_segments=15, filename=None):
    # Get the unique days in the dataset
    unique_days = data[time_col].dt.date.unique()
    num_days = len(unique_days)

    # Create a color map for the gradient (Cool-Warm, where red is closer, blue is further)
    cmap = plt.cm.coolwarm.reversed()
    
    # Normalize the color map
    norm = plt.Normalize(vmin=data[distance_col].min(),
                         vmax=data[distance_col].max())

    # Replace 0 distances with NaN
    data[distance_col] = data[distance_col].replace(0, np.nan)

    # Create the subplots with additional space between them
    fig, axes = plt.subplots(nrows=num_days, ncols=1, figsize=(12, 4 * num_days), layout="none")
    # fig.subplots_adjust(hspace=0.4, top=0.01, bottom=0.03)  # Add space between subplots, change top and bottom margins
    
    # Ensure axes is iterable if there's only one day (only one subplot)
    if num_days == 1:
        axes = [axes]
    
    for i, day in enumerate(unique_days):
        ax = axes[i]
        
        # Filter data for the current day and make a copy to avoid SettingWithCopyWarning
        day_data = data[data[time_col].dt.date == day].copy()
        
        # Calculate hours elapsed since midnight
        day_data['hours_elapsed'] = (day_data[time_col] - pd.to_datetime(day)).dt.total_seconds() / 3600

        # Plot the distance as a gradient line
        for j in range(1, len(day_data)):
            x_vals = [day_data['hours_elapsed'].iloc[j-1], day_data['hours_elapsed'].iloc[j]]
            y_vals = [day_data[distance_col].iloc[j-1], day_data[distance_col].iloc[j]]
            color_start = cmap(norm(day_data[distance_col].iloc[j-1]))
            color_end = cmap(norm(day_data[distance_col].iloc[j]))
            
            # Create a linear gradient between the two colors
            lc = mcolors.LinearSegmentedColormap.from_list("segment_gradient", [color_start, color_end])
            
            # Adjust the number of segments between two points to create a smoother or rougher transition
            for k in range(num_segments):
                segment_start_x = x_vals[0] + (x_vals[1] - x_vals[0]) * (k / num_segments)
                segment_end_x = x_vals[0] + (x_vals[1] - x_vals[0]) * ((k + 1) / num_segments)
                segment_start_y = y_vals[0] + (y_vals[1] - y_vals[0]) * (k / num_segments)
                segment_end_y = y_vals[0] + (y_vals[1] - y_vals[0]) * ((k + 1) / num_segments)
                
                # Only plot if both start and end of the segment are not NaN
                if not np.isnan(segment_start_y) and not np.isnan(segment_end_y):
                    ax.plot([segment_start_x, segment_end_x], 
                            [segment_start_y, segment_end_y], 
                            color=lc(k / num_segments), linewidth=2)

        # Plot the points with the color gradient (only non-NaN distances)
        sc = ax.scatter(day_data['hours_elapsed'][~day_data[distance_col].isna()], 
                        day_data[distance_col][~day_data[distance_col].isna()], 
                        c=day_data[distance_col][~day_data[distance_col].isna()], 
                        cmap=cmap, norm=norm, s=50, edgecolor='none')
        
        # Add a horizontal line at y=0
        ax.axhline(y=0, color='black', linewidth=2)
        
        # Set the grid for both axes
        ax.grid(True, which='both', axis='both', color='gray', linestyle='--', linewidth=0.5)
        ax.set_xticks(np.arange(0, 25, 1))  # Vertical grid lines every hour
        ax.set_yticks(np.arange(0, data[distance_col].max() + 1, 1))  # Horizontal grid lines every meter
        
        # Set the title for the subplot, adjusted to the left and smaller size
        ax.set_title(f'Day {i + 1}', fontsize=12, loc='left')
        
        # Set the y-axis label and ticks to match x-axis style
        ax.set_ylabel('Distance (m)', fontsize=10, color='gray')
        ax.tick_params(axis='y', labelsize=10, colors='gray')
        
        # Set the x-axis ticks to represent hours elapsed since midnight
        ax.set_xticks(np.arange(0, 25, 1))  # Ticks every hour
        ax.set_xlim(-0.5, 24.5)  # Extend the x-axis to make it less crowded
        ax.set_xticklabels([str(int(hour)) for hour in np.arange(0, 25, 1)],
                           fontsize=10, color='gray')
    
    # Set a common x-axis label
    plt.xlabel('Hours Elapsed Since Midnight', fontsize=12, color='gray')
    
    plt.tight_layout()
    
    if filename is not None:
        plt.savefig(filename, dpi=300)
    else:
        plt.show()

