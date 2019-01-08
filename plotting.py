from capture import df  #if I call plotting, capture.py will be executed and df createRadialGradient

from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource  #need to convert some things into column data source,
# ^ standardized way to add data to bokeh plots

df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")  #dt for datetime
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)

p = figure(x_axis_type = 'datetime', height = 100, width = 500, sizing_mode='scale_width', title = "Motion Graph")
#sizing_mode instead of responsive now. It worked FUCKING yesterday
p.yaxis.minor_tick_line_color = None
p.ygrid[0].ticker.desired_num_ticks = 1  #to get rid of the grid, accessing the first item of the list

hover = HoverTool(tooltips = [("Start", "@Start_string"), ("End", "@End_string")])  #gets as argument a list of tuples, every tuple - lines of popup window
#Start string and array from the Start column, accessed by the descriptor
p.add_tools(hover)
q = p.quad(left = "Start", right = "End", bottom = 0, top = 1, color = "green", source = cds)  #added source, and now I don't have to write
#df["Start"], but just "Start"

output_file("Graph.html")
show(p)
