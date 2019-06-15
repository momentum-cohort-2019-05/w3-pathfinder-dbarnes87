from PIL import Image

def read_line_of_ints(text):
    ints = []
    ints_as_strs = split_line(text)

    for ints_as_str in ints_as_strs:
        ints.append(int(ints_as_str))
    return ints

def split_line(line):
    return line.split()

def read_file_into_list(filename):
    with open("elevation_small.txt") as file:
        return file.readlines()


def read_file_into_ints(filename):

    lines = read_file_into_list("elevation_small.txt")
    
    list_of_lists = []
    for line in lines:
        list_of_lists.append(read_line_of_ints(line))
    return list_of_lists

class ElevationMap:

    def __init__(self, elevations):
        self.elevations = elevations
    
    def elevation_at_coordinate(self, x, y):
        return self.elevations[y][x]
    
    def min_elevation(self):
        return min([min(row) for row in self.elevations])
    
    def max_elevation(self):
        return max([max(row) for row in self.elevations])
    
    def intensity_at_coordinate(self, x, y):
        elevation = self.elevation_at_coordinate(x, y)
        # min_elevation = self.min_elevation()
        # max_elevation = self.max_elevation()
        # return int((elevation - min_elevation) / (max_elevation - min_elevation) * 255)
        """Plugged in figures to save processor time.  See docstring at bottom of file."""
        return int(( elevation - 3138) / (2509) * 255)

    def draw_grayscale_map(self, width=600, height=600):

        with open("elevation_small.txt") as textFile:
            coordinate = [line.split() for line in textFile]

        image = Image.new("RGBA", (width, height))
        for y in range(height):
            for x in range(width):
                value = self.intensity_at_coordinate(x, y)
                image.putpixel((x, y), (value, value, value))
                # print(value)
        image.save("map.png")

        """Draw path from middle"""

        y_start_value = 300
        step_start_value = int((coordinate[y_start_value][0]))
        x = 1

        """Get elevations for the three next column step options."""           

        for x in range(width):  

            y_up = y_start_value - 1
            y_adjacent = y_start_value
            y_down = y_start_value = 1
        
            step_up = abs(int(coordinate[y_up][x]) - step_start_value)
            step_adjacent = abs(int(coordinate[y_adjacent][x]) - step_start_value)
            step_down = abs(int(coordinate[y_down][x]) - step_start_value)

            if step_up < step_adjacent and step_up < step_down:
                image.putpixel((x, y_up), (0, 255, 255))
                y_start_value = y_up
            elif step_adjacent < step_up and step_adjacent < step_down:
                image.putpixel((x, y_adjacent), (0, 255, 255))
                y_start_value = y_adjacent
            elif step_down < step_up and step_down < step_adjacent:
                image.putpixel((x, y_down), (0, 255,255))
                y_start_value = y_down

            step_start_value = int((coordinate[y_start_value][0]))
        
        image.save("pathfinder_map.png")



elevations = read_file_into_ints("elevation_small.txt") 

e_map = ElevationMap(elevations)

e_map.draw_grayscale_map()



"""
Figures to plug into intensity_at_coordinate function.
Prevents CPU from having to process multiple equations for 
each iteration in "for" loops of draw_grayscale_map function

max_elevation = 5648
min_elevation = 3138
difference    = 2510

Should the difference be 2509?

"""
