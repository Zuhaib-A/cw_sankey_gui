#!/usr/bin/env python3 

#Student Number: 19083919

"""Draw a sankey diagram using data from a given input file.
"""
import sys
from ezgraphics import GraphicsWindow
import random
import math

WIDTH = 1000        # Width of the window in pixels
HEIGHT = 700        # Height of the window in pixels
GAP = 25        # Gap between disagram arrows in pixels
COLOURS = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200),
(245,	130,	48),	(145,	30, 180), (70, 240,	240),	(240, 50, 230),
(210,	245,	60),	(250,	190, 212), (0, 128,	128),	(220, 190, 255),
(170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195),
(128,	128,	0), (255, 215, 180), (0, 0, 128), (128, 128, 128)]

def read_file(file_name):
    """Opens and reads the file. Returns the title, left-hand axis label and 
    the data values in the file.

    Args:
        file_name (str): file containing the data.

    Raises:
        FileNotFoundError: If file not found or is not readable, 
                            this exception is raised.

    Returns:
        title (string): diagram title.
        axis (string): left-hand axis label.
        raw_list (list): Each element contains one line of data from the file.
    """
    
    #Adds ".txt" if the user did not write it.
    if ".txt" not in file_name:
        file_name = file_name + str(".txt")
    file = open(file_name, "r")
    nth_line = file.readlines()
    #The first two lines are designated as the window title and the data label.
    title = nth_line[0]
    axis = nth_line[1]
    current_line = 0
    number_lines = len(nth_line)
    #All the lines after the first two are considered to be data lines and are
    ##added to a list.
    raw_list = []
    for x in range(2, number_lines):
        raw_list.append(nth_line[x].strip("/n"))
    return title, axis, raw_list

def set_up_graph(title):
    """Creates a window and canvas. Displays the title, left-hand axis label.
    Returns a reference to the window. 

    Args:
        title (str): title for the window.
        
    Returns:
        win (GraphicsWindow): reference to the window.
    """
    
    win = GraphicsWindow(WIDTH, HEIGHT)
    win.setTitle(title)
    return win

def parse_value (value, line_number) :
    """Parses and returns a floating point value from a string, cleaning
       required characters (e.g. white spaces).
       
    Args:
        str: string from which the value must be read
        line_number: line in the file, required in case errors neet to be
                     notified.
        
    Raises: 
        ValueError: raised if the string cannot be read as a float, datailing
                    content and line number.
                    
    Returns:
        value (float): The number read as a float.     
    """
    
    #The value attached to each data key is checked to see if it is a float.
    try:
        float(value)
    except ValueError:
        print(f"Error in line {line_number}: Value provided is not a number "
              f"({value})")
    return float(value)
    
def process_data(data_list):
    """Returns a dictionary produced by processing the data in the list. 

    Args:
        data_list (list): list containing the data read from the file

    Raises:
        ValueError: raised if there are errors in the data values in the file

        Exception: raised if there are issues with the RGB selection or if
                   data is missing.

    Returns:
        dictionaries (list): contains two dictionaries, one for any user
                           specified colours and the other for information
                           about the flows.
    """
    
    #Only lines after the first two are looked at:
    current_line = 2
    #Two dictionaries are created, one for any custom colours, one for the data.
    values_dict = {}
    colours_dict = {}
    dictionaries = []
    for i in data_list:
        current_line = current_line + 1
        #The entries in each line have any new line characters removed.
        cleaned = i.replace("\n", "")
        #The entries are then split by using commas as a divider.
        cleaned = ((cleaned.split(",")))
        value_name = str((cleaned[0]))
        value_before_check = (cleaned[1]).replace(" ", "")
        #Here the entries are checked to ensure that they are not empty and that
        ##they are not full of only whitespaces. The program will stop if they
        ###are.
        if (value_name.isspace()):
            raise Exception(f"\nError in line {current_line}: The key provided"
                            " is empty.")
        elif value_name == "" or value_before_check == "":
           raise Exception(f"\nError in line {current_line}: Entries are "
                           "missing for either one of, or both the key "
                           "and value.")
        #The value is checked to ensure it is a float:
        final_value = parse_value(value_before_check, current_line)
        
        #If after the data value, there are RGB selections made, they will need
        ##to be checked that they are integers before being added to the colours
        ##dictionary.
        if len(cleaned) > 2:
            temp_colours = []
            for remaining in range(2, (len(cleaned))):
                try:
                    int(cleaned[remaining])
                except ValueError:
                    print(f"\nError in line {current_line}: Ensure that the "
                          "values entered to select the RGB are all integers.")
                temp_colours.append(int(cleaned[remaining].replace(" ", "")))
        #If no RGB selection has been made, the colour value will be defined as
        ##being empty for that line/value.
        else:
            temp_colours = []
        colours_dict[value_name] = temp_colours
        value_of_key = final_value
        values_dict[value_name] = value_of_key
    dictionaries.append(values_dict)
    dictionaries.append(colours_dict)
    return dictionaries

def colours_select(colours_initial):
    #The extended version of this function can be found below.
    #Please see line 770 (draw_sankey function) to enable/disable.
    """Default function to choose the colours of the arrows and title.

    Args:
        colours_initial (list): List containing any elements after
                                the data values after line 2, or
                                the label from line 2 in the text file.

    Raises:
        Exception: If the text file contains incorrect RGB values not in
                   the range 0-255, or the index used to select it has
                   exceeded the length of the COLOURS list.
                   If the number of RGB elements is greater than 3.
                   An exception is also raised if all the colours in the
                   COLOURS list have been used up.

    Returns:
        rgb (tuple): Contains the final RGB selection.
        inv_rgb (tuple): Contains theinverse of the final RGB selection.
        is_colours_extended (boolean): True or False. Indicates if the extended
                                       function for colours select was called.
    """

    #While loop which checks that a randomly selected colour is not reselected.
    #If the colour is reselected, the while loop will not break until a new one
    ##is selected. 
    loop_break = False
    exceeded_colours_check = 0
    while loop_break == False:
        random_colour = random.randint(0, len(COLOURS) - 1)
        if COLOURS[random_colour] == "used":  
            exceeded_colours_check = exceeded_colours_check + 1
            if exceeded_colours_check == len(COLOURS) - 1:
                raise Exception("\nError: There are not enough colours in "
                                "the list COLOURS, please add more to "
                                "fix the program.")
        else:
            loop_break = True

    #An already selected colour will be replaced with "used" to prevent it from
    ##being reused.
    rgb = COLOURS[random_colour]
    COLOURS[random_colour] = "used"
    #The RGB selection is inverted to produce the inverse colour tuple.
    inv_rgb = ()
    for number in rgb:
        inv_rgb = inv_rgb + (abs(255 - number), )
    #The boolean variable below will be used by the source_title_write function.
    is_colours_extended = False
    return rgb, inv_rgb, is_colours_extended

def colours_select_extended(colours_initial, current_line):
    #Additional Challenge 2:
    #Please see line 770 (draw_sankey function) to enable/disable.
    """Part of Addition Challenge 2. Allows for user specification as to what
    the colours of the arrows (and arrow labels) will be.

    (For the BlueHatGreenHat.txt file, this function will read line 2 and see
    that the source block label is "Words, 96, 96, 96". It will treat
    "96, 96, 96" as the RGB colour of the label rather than just parsing the
    label as "Words, 96, 96, 96", meaning that the label will be just "Words".)

    Args:
        colours_initial (list): List containing any elements after
                                the data values after line 2, or
                                the label from line 2 in the text file.

        current_line (integer): Stores current position in text file.

    Raises:
        Exception: If the text file contains incorrect RGB values not in
                   the range 0-255, or the index used to select it has
                   exceeded the length of the COLOURS list.
                   If the number of RGB elements is greater than 3.
                   An exception is also raised if all the colours in the
                   COLOURS list have been used up.

    Returns:
        rgb (tuple): Contains the final RGB selection.
        inv_rgb (tuple): Contains theinverse of the final RGB selection.
        is_colours_extended (boolean): True or False. Indicates if the extended
                                       function for colours select was called.
    """

    #If no RGB colours have been specified by the user, a random one is picked
    ##in the colours_select function:
    if len(colours_initial) == 0:
        rgb, inv_rgb, is_colours_extended = colours_select(colours_initial)
        is_colours_extended = True
        return rgb, inv_rgb, is_colours_extended
    
    #If the first two arguments for RGB colour selection (R and G) have been
    ##given, they will be set to those with B being 0. 
    elif (len(colours_initial) == 2) or (len(colours_initial) == 3):
        for x in colours_initial:
            #A check to see if the RGB inputs are less than or equal to 255.
            ##Also a check to see that the input is positive.
            if (((x) > 255) and ((x) > (len(COLOURS) - 1)) ) or ((x) < 0):
                raise Exception(f"\nError in line {current_line}: Check that "
                                "the values provided for the RGB selection "
                                "are within the correct range of 0 -> 255.")
        if len(colours_initial) == 2:
            rgb = ((colours_initial[0]), (colours_initial[1]), 0)
        #If all 3 (R, G and B) have been given, that is what RGB will be set to.
        elif len(colours_initial) == 3:
            rgb = ((colours_initial[0]), (colours_initial[1]),
                   (colours_initial[2]))
            
    #If only one input for the colours has been given, it is assumed it will be
    ##used to select from the COLOURS list using the index.
    elif (len(colours_initial) == 1):
        if (colours_initial[0]) <= (len(COLOURS) - 1):
            #If the colour selected is used, the while loop seen before in the 
            ##colours_select function is used again to pick a new unused colour.
            if COLOURS[colours_initial[0]] == "used":
                loop_break = False
                exceeded_colours_check = 1
                while loop_break == False:
                    random_colour = random.randint(0, len(COLOURS) - 1)
                    if COLOURS[random_colour] == "used":  
                        exceeded_colours_check = exceeded_colours_check + 1
                        if exceeded_colours_check == len(COLOURS) - 1:
                            raise Exception("\nError: There are not enough "
                                            "colours in the list COLOURS, "
                                            "please add more to fix the "
                                            "program.")
                    else:
                        loop_break = True
                rgb = COLOURS[colours_initial[0]]
                COLOURS[colours_initial[0]] = "used"
                    
            else:
                rgb = COLOURS[colours_initial[0]]
                COLOURS[colours_initial[0]] = "used"

        else:
            raise Exception(f"\nError in line {current_line}: When using just "
                            "the index to specify the RGB from the COLOURS "
                            "list, the index cannot be greater than the "
                            "maximum index of the COLOURS list which is "
                            f"{len(COLOURS) - 1}.")
    else:
        raise Exception(f"\nError in line {current_line}: Check that the "
                        "number of values provided for RGB selection does not "
                        "exceed three.")
    #Creation of the inverse RGB tuple.
    inv_rgb = ()
    for number in rgb:
        inv_rgb = inv_rgb + (abs(255 - (number)), )
    is_colours_extended = True
    return rgb, inv_rgb, is_colours_extended

def create_colour_gradient(rgb, height_poly, i):
    """Creates the colour gradient for the arrow. 

    Args:
        rgb (list): List containing the final RGB colour selection.
        height_poly (integer): The difference in height from the
                               bottom of the source block to the top of the
                               arrow head.
        i (integer): Number representing which key-value pair in the values
                     dictionary we are at. For example, which country.
            

    Returns:
        rgb_gradients (list): A list that contains three lists. These three
                              are the individual colour gradients for each
                              part of the RGB selection.
    """
    
    #An empty list is created for the 3 colour gradients created for
    ##all three components of RGB.
    list_indv_gradients = []
    for indv_rgb in rgb:
        if indv_rgb == 0:
            #If the colour component of RGB is set to 0. It will have no
            ##gradient. It will be repeated for the length of the gradient.
            colour_repeat = height_poly
        else:
            #If the colour component of RGB in question is not 0. A repeat
            ##variable is calculated to see how many times each number, from
            ##0 to the individual RGB component needs to be repeated.
            colour_repeat = round(height_poly / indv_rgb)

        #An empty list is generated each time which will contain each individual
        ##colour gradient. First for R, then G, then finally B.
        indv_rgb_gradient = []
        for n in range(0, indv_rgb + 1):
            indv_rgb_gradient.extend([n] * colour_repeat)

        #The individual gradient has been created but rounded numbers are used
        ##so adjustments are required to ensure the colour gradients length is
        ##equal to the number of lines being drawn.
        while len(indv_rgb_gradient) != height_poly:
            if len(indv_rgb_gradient) > height_poly:
                difference = len(indv_rgb_gradient) - height_poly
                interval = round(len(indv_rgb_gradient) / difference)
                current_index = 0
                for y in range(0, len(indv_rgb_gradient),interval):
                    del indv_rgb_gradient[y - current_index]
                    current_index = current_index + 1   
            elif len(indv_rgb_gradient) < height_poly:
                end=indv_rgb_gradient[-1]
                indv_rgb_gradient.extend([end]*(height_poly -
                                                len(indv_rgb_gradient)))
                
        list_indv_gradients.append(indv_rgb_gradient)

    #The rgb_gradients list will have all three individual gradients added to it
    ##correctly at the right positions so that for each line, there will be
    ##an RGB combination.
    rgb_gradients = []
    for z in range(0, height_poly):
        rgb_gradients.append([list_indv_gradients[0][z],
                              list_indv_gradients[1][z],
                              list_indv_gradients[2][z]])
    return rgb_gradients

def draw_tri_dest(rgb, border_size, current_x1_dest, current_x2_dest,
                  current_x3_dest, tri_height_min, tri_height_max, canvas):
    """Draws the triangles representing the arrow heads. 

    Args:
        rgb (list): List containing the final RGB colour selection.
        border_size (integer): Minimum gap between the diagram ands window edge.
        current_x1_dest (float): x position of the left corner of the triangle
                                 along the destination.
        current_x2_dest (float): x position of the right corner of the triangle
                                 along the destination.
        current_x3_dest (float): x position of the centre of the triangle.
        tri_height_min (float): Absolute height from the top of the window to
                                the bottom of the triangle.
        tri_height_max (float): Absolute height from the top of the window to
                                the top of the triangle.
        canvas: Reference to drawing on the GraphicsWindow.
    """
    
    canvas.setFill(rgb[0], rgb[1], rgb[2])
    canvas.setOutline("black")
    canvas.drawPolygon(current_x1_dest, tri_height_max, current_x2_dest,
                       tri_height_max, current_x3_dest, tri_height_min)    

def write_tri_dest(inv_rgb, current_x3_dest, tri_height_max, dest_names, i,
                   canvas):
    """Writes the data key names on the triangles representing the arrow heads. 

    Args:
        inv_rgb (list): List containing the final inverted RGB colour selection.
        current_x3_dest (float): x position of the centre of the triangle.
        tri_height_max (float): Absolute height from the top of the window to
                                the top of the triangle.
        dest_names (list): List of the data value names, for example, list of
                           countries.
        i (integer): Number representing which key-value pair in the values
                     dictionary we are at. For example, which country.
        canvas: Reference to drawing on the GraphicsWindow.
    """
    
    canvas.setTextAnchor("center")
    canvas.setOutline(inv_rgb[0], inv_rgb[1], inv_rgb[2])
    canvas.drawText(current_x3_dest,tri_height_max, dest_names[i])

def draw_source_block(source_width, border_size, canvas, source_height):
    """Draws the source block. 

    Args:
        source_width (integer): Width of the source block.
        border_size (integer): Minimum gap between the diagram ands window edge.
        canvas: Reference to drawing on the GraphicsWindow.    
        source_height (integer): Height of the source block.
    """
    
    canvas.setOutline("black")
    canvas.setFill("black")
    canvas.drawRect((WIDTH - source_width) / 2, border_size, source_width,
                    source_height)
    
def source_title_write(title, source_width, is_colours_extended, canvas,
                       source_height, border_size):
    """Writes the title on the source block. 

    Args:
        title (string): The axis label to be put on the source block.
        source_width (integer): Width of the source block.
        is_colours_extended (boolean): True or False. Indicates if the extended
                                       function for colours select was called.
        canvas: Reference to drawing on the GraphicsWindow.    
        source_height (integer): Height of the source block.
        border_size (integer): Minimum gap between the diagram ands window edge.
        
    """

    #If the extended colours_select function was used. The program will check
    ##for a RGB specification for the axis label by calling another function.
    if is_colours_extended == True:
        rgb_title, title = src_title_colour_extended(title)
    elif is_colours_extended == False:
        rgb_title = (255, 255, 255)
    canvas.setTextAnchor("center")
    canvas.setOutline(rgb_title[0], rgb_title[1], rgb_title[2])
    canvas.drawText(((WIDTH - source_width) / 2) + (source_width / 2),
                    border_size + (source_height / 2), title)

def src_title_colour_extended(title):
    #This function will be called by default when the extended colours select
    ##function is in use. It works to handle the BlueHatGreenHat.txt file.
    ###Instead of the source label being "Words, 96,96,96,", it will be "Words"
    ####The colour of the title will be (96,96,96).
    """Selects the colour of the the title on the source block. 

    Args:
        title (string): The axis label to be put on the source block.

    Raises:
        Exception: If integers arent used to identify the axis RGB.
                   If integers provided to identify the RGB are not within
                   the range of 0->255.

    Returns:
        rgb_title (tuple): The RGB selection for the source axis label.
        title (string): The axis label to be put on the source block which
                        has now been treated to ensure it contains no list
                        of numbers which would have been used for RGB
                        selection.
    """
    
    #Line 2 contains the axis label so a local line position tracker is created.
    current_line = 2
    #The title is split up by any commas and then treated.
    if "," in title:
        title_ext = title.replace("\n", "")
        title_ext = ((title_ext.split(",")))
        #If the title contains words plus any numbers for RGB selection,
        ##like 96, 96, the word is ignored and everything after the word is
        ###added to a list. For example, the list would be "96,96,96" and
        ####not "Words, 96,96,96".
        title_ext_split = []
        for x in range(1, len(title_ext)):
            try:
                int(title_ext[x])
            except:
                print(f"\nError in line {current_line}: Ensure that the values "
                      "entered to select the RGB for the title are all "
                      "integers.")
            title_ext_split.append(int(title_ext[x].replace(" ", "")))
            
        for y in title_ext_split:
            if ((((int(y)) > 255) and ((int(y)) > (len(COLOURS) - 1)))
                                                      or ((int(y)) < 0)):
                raise Exception(f"\nError in {current_line}: Check that the "
                                "values provided for the RGB selection of the "
                                "title are integers and are within the correct "
                                "range of 0 -> 255.")
        rgb_title = colours_select_extended(title_ext_split, 2)[0]
        title = title_ext[0]
    #If the title did not have an RGB selection given, the colour of the title
    ##will be white.
    else:
        rgb_title = (255,255,255)
    return rgb_title, title

def draw_curve(height_poly, rgb_gradients, dydx_flow, canvas,
               along_source_x, current_height, dest_widths, i, current_x1_dest):
    #Additional Challenge 1: Please see line 800 (draw_sankey function)
    #                        to enable/disable.
    """Draw straight coloured lines connecting the source to the triangles. 

    Args:
        height_poly (integer): The difference in height from the
                               bottom of the source block to the top of the
                               arrow head.
        rgb_gradients (list): A list that contains three lists. These three
                              are the individual colour gradients for each
                              part of the RGB selection.
        dydx_flow (float): Gradient of each line/bar.
        canvas: Reference to drawing on the GraphicsWindow.
        along_source_x (float): Position of left point of each initial coloured
                                line for every arrow.
        current_height (integer): Bottom of the source block.
        dest_widths (list): List of each line width (pixels).
        i (integer): Number representing which key-value pair in the values
                     dictionary we are at. For example, which country.
        current_x1_dest (float): x position of the left corner of the triangle
                                 along the destination.                 
    """
    
    #Postion of the initial x coordinate of the right point of the line:
    along_source_x2 = along_source_x + dest_widths[i]
    #The for loop will go through each pixel down the distance from the
    ##bottom of the source to the top of the arrow head.
    for x in range(0, height_poly):
        #The colour of each line will be related to the position.
        ##The first line for example will have an RGB of 0,0,0 which is
        ###rgb_gradients[0]
        rgb_line = rgb_gradients[x]
        #If the shape of the bar is completely vertical, the x positions
        ##will not change.
        if dydx_flow == 0:  
            if x > height_poly-3:
                along_source_x = along_source_x + 1
                along_source_x2 = along_source_x2 - 0.4
            canvas.setOutline("black")
            canvas.drawLine(along_source_x - 1, current_height,
                                along_source_x2 + 1, current_height)
            canvas.setOutline(rgb_line[0], rgb_line[1], rgb_line[2])
            canvas.drawLine(along_source_x, current_height, along_source_x2,
                            current_height)
        else:
            #The left and right x positions of the coloured line are
            ##determined:
            
            #Additional 1: The given curve equations are used to determine
            ##how much the line should curve as the program goes down the arrow.
            ratio_height = (x / height_poly)
            p = ratio_height
            curve = p * math.pi - math.pi / 2
            curve = (math.sin(curve) + 1) / 2
            curve = (along_source_x - curve * (along_source_x -
                                               current_x1_dest))
            along_source_x2 = (curve + dest_widths[i])
            #This if statement is purely adjusting the last few coloured lines
            ##to make the arrow aesthetically look better by preventing
            ###edges appearing out of place.
            if x > height_poly-3:
                if dydx_flow < 0:
                    curve = curve + 1
                    along_source_x2 = along_source_x2
                elif dydx_flow > 0:
                    curve = curve + 1
                    along_source_x2 = along_source_x2 - 0.8
            #The black outlines are drawn first.
            x1, y1 = curve - 1, current_height
            x2, y2 = along_source_x2 + 1, current_height
            canvas.setOutline("black")
            canvas.drawLine(x1, y1, x2, y2)
            #Then the coloured lines are drawn.
            canvas.setOutline(rgb_line[0], rgb_line[1], rgb_line[2])
            canvas.drawLine(curve, current_height, along_source_x2,
                            current_height)            
        #The height is incremented by 1 pixel (in this case, going down the
        ##arrow)    
        current_height = current_height + 1
    
def draw_straight(height_poly, rgb_gradients, dydx_flow, canvas,
                  along_source_x, current_height, dest_widths, i):
    #Please see line 800 (draw_sankey function) to enable/disable.
    """Draw straight coloured lines connecting the source to the triangles. 

    Args:
        height_poly (integer): The difference in height from the
                               bottom of the source block to the top of the
                               arrow head.
        rgb_gradients (list): A list that contains three lists. These three
                              are the individual colour gradients for each
                              part of the RGB selection.
        dydx_flow (float): Gradient of each line/bar.
        canvas: Reference to drawing on the GraphicsWindow.
        along_source_x (float): Position of left point of each initial coloured
                                line for every arrow.
        current_height (integer): Bottom of the source block.
        dest_widths (list): List of each line width (pixels).
        i (integer): Number representing which key-value pair in the values
                     dictionary we are at. For example, which country.
                                 
    """
    
    #Postion of the initial x coordinate of the right point of the line:
    along_source_x2 = along_source_x + dest_widths[i]
    #The for loop will go through each pixel down the distance from the
    ##bottom of the source to the top of the arrow head.
    for x in range(0, height_poly):
        #The colour of each line will be related to the position.
        ##The first line for example will have an RGB of 0,0,0 which is
        ###rgb_gradients[0]
        rgb_line = rgb_gradients[x]
        #If the shape of the bar is completely vertical, the x positions
        ##will not change.
        if dydx_flow == 0:
            #The black outline is drawn first.
            canvas.setOutline("black")
            canvas.drawLine(along_source_x, current_height,
                            along_source_x2 + 1, current_height)
            #The coloured line is then drawn.
            canvas.setOutline(rgb_line[0], rgb_line[1], rgb_line[2])
            canvas.drawLine(along_source_x + 1, current_height,
                            along_source_x2, current_height)
        else:
            #Delta is equal to the reciprocal of the line gradient.
            delta = (1 / dydx_flow)
            #This if statement is purely adjusting the last few coloured lines
            ##to make the arrow aesthetically look better by preventing
            ###edges appearing out of place.
            if x > height_poly-3:
                if dydx_flow < 0:
                    along_source_x = along_source_x + 1
                    along_source_x2 = along_source_x2
                elif dydx_flow > 0:
                    along_source_x = along_source_x + 1
                    along_source_x2 = along_source_x2 - 0.8
            else:
                #The left and right x positions of the coloured line are
                ##determined:
                along_source_x = along_source_x + delta
                along_source_x2 = along_source_x + dest_widths[i]
            #The black outlines are drawn first.
            x1, y1 = along_source_x - 1, current_height
            x2, y2 = along_source_x2 + 1, current_height
            canvas.setOutline("black")
            canvas.drawLine(x1, y1, x2, y2)
            #Then the coloured lines are drawn.
            canvas.setOutline(rgb_line[0], rgb_line[1], rgb_line[2])
            canvas.drawLine(along_source_x, current_height, along_source_x2,
                            current_height)            
        #The height is incremented by 1 pixel (in this case, going down the
        ##arrow)
        current_height = current_height + 1
  
def draw_sankey(window, title, data_dic, gap_size = 100, border_size = 100):
    """Draw the sankey diagram

    Args:
        window (GraphicsWindow): contains the graph
        title (string): contains the label to overlay on the source arrow
        data_dic (dictionary): contains the data for the graph
        gap_size (int): number of pixels to leave between destination arrows
        border_size (int): Minimum separation to othe edges of the window

    Raises:
        Exception: If the number of available pixels calculated is less than
                   one pixel.
    """

    #The values and keys from the first dictionary in the data_dic list are
    ##added to a list, these values could be country names or sources of
    ###renwable energy. The keys could be the number of goals or power output.
    values_data_dic = data_dic[0].values()
    names_data_dic = data_dic[0].keys()
    #Calculations related to representing the data in the right amount of
    ##pixels.
    total_flow = sum(values_data_dic)
    number_dests = len(values_data_dic)
    avail_pixels = WIDTH - 2 * 100 - (number_dests - 1) * gap_size
    
    #If there are too many value-key data pairs, sankey diagram will be broken
    ##so an exception is raised if this occurs.
    suggested_gap = (1 - WIDTH + 2 * 100)/(- (number_dests - 1))
    if avail_pixels < 1:
        raise Exception("\nError in file: The number of available pixels "
                        "calculated is less than 1 which means the sankey "
                        "diagram will potentially be inverted and/or "
                        "incorrect. This is caused by the user defined "
                        "GAP being too large for the number of data "
                        "entries used. A suggested GAP value is "
                        f"{suggested_gap}.")
                        
    pixels_per_flow = avail_pixels / total_flow

    #A for loop is used to create a list of the exact width of each
    ##arrow/bar measured in pixels by multiplying the pixel:flow ratio by
    ###the flow. 
    dest_widths = []
    for value in values_data_dic:
        dest_widths.append(value * pixels_per_flow)
    
    dest_names = []
    for key in names_data_dic:
        dest_names.append(key)

    #Geomtry defined for the source block and triangle heights.
    source_width = (total_flow * pixels_per_flow)
    source_height = 40
    tri_height_min = HEIGHT - border_size
    tri_height_max = HEIGHT - (border_size + border_size / 3)
    canvas =  window.canvas()
    
    #Source block is drawn.
    draw_source_block(source_width, border_size, canvas, source_height)
    initial_source_x = (WIDTH - avail_pixels) / 2
    current_line = 2
    for i in range(0, number_dests):
        current_line = current_line + 1
        #The x coordinate of the bottom left corner of each bar is defined:
        current_x1_dest = border_size + sum(dest_widths[0:i]) + gap_size * (i)
        #The x coordinate of the top left corner of each bar is defined:
        along_source_x = initial_source_x + sum(dest_widths[0:i])
        #The gradients (dy/dx) of each line is calculated.
        if (along_source_x - current_x1_dest > 0) or (along_source_x -
        current_x1_dest < 0):
            dydx_flow = (((border_size + source_height) - tri_height_max) /
                                         ((along_source_x - current_x1_dest)))
        else:
            dydx_flow = 0
        #The x coordinate of the bottom right corner of each bar is defined:
        current_x2_dest = current_x1_dest + dest_widths[i]
        #The x coordinate of the centre of each triangle connected to each
        ##bar is defined:
        current_x3_dest = (current_x1_dest + dest_widths[i] / 2)

        #Any elements in the text file used to identify the RGB of each
        ##arrow/title are added to a new colours_list.
        colours_list = list(data_dic[1].values())[0:len(data_dic[1].values())]

################################################################################
#######################      Additional Challenge 2:     #######################

          #Enable or disable one of the function calls below please:

        #Challenge (Colours Selected or Randomised) Lines 773 -> 774:
        rgb, inv_rgb, is_colours_extended = colours_select_extended(
                                                 colours_list[i],current_line)

        #Normal (Colours Only Randomised) Line 777:
        #rgb, inv_rgb, is_colours_extended = colours_select(colours_list[i])
        
        
################################################################################

        #The height of the arrow is calculated, from the source bottom to the
        ##triangle top as height_poly: (Used to draw the right number of 
        ###coloured lines for each bar.)
        height_poly = round(tri_height_max - (border_size + source_height)) + 1
        #The current_height is reset during each iteration for each new
        ##destination so that the lines are drawn correctly.
        current_height = border_size + source_height

        #The RGB colour gradients are created:
        rgb_gradients = create_colour_gradient(rgb, height_poly, i)

        #Triangles for each destination are created:
        draw_tri_dest(rgb, border_size, current_x1_dest, current_x2_dest,
                  current_x3_dest, tri_height_min, tri_height_max, canvas)

################################################################################
#######################      Additional Challenge 1:     #######################

          #Enable or disable one of the function calls below please:

        #Challenge (Curved) Lines 803 -> 805:
        draw_curve(height_poly, rgb_gradients, dydx_flow, canvas,
                   along_source_x, current_height, dest_widths, i,
                   current_x1_dest)

        #Normal (Straight) Lines 808 -> 809:
        #draw_straight(height_poly, rgb_gradients, dydx_flow, canvas,
                      # along_source_x, current_height, dest_widths, i)

################################################################################

        #Each triangle/arrow-head titles is written:
        write_tri_dest(inv_rgb, current_x3_dest, tri_height_max, dest_names,
                       i, canvas)

    #The source axis label/title is written. If is_colours_extended is true
    ##and colours were used, the source title will be coloured as well.
    source_title_write(title, source_width, is_colours_extended, canvas,
                       source_height, border_size)   
        
def main():
    # DO NOT EDIT THIS CODE ###
    input_file = "" ###
    file_read = False ###
    # Try to read file name from input commands: ###
    args = sys.argv[1:]  ###
    if len(args) == 0 or len(args) > 1: ###
        print('\n\nUsage\n\tTo visualise data using a sankey diagram type:\
            \n\n\t\tpython sankey.py infile\n\n\twhere infile is the name of the file containing the data.\n') ###
        print('\nWe will ask you for a filename, as no filename was provided')###
       
    else: ###
        input_file = args[0]###
    
    # Use file provided or ask user for valid filename (we will iterate until a valid file is provided) ###
    while not file_read : ###
        # Ask for filename if not available yet ###
        if input_file == "" : ###
            input_file = input("Provide name of the file to load: ") ###
        
        # Try to Read the file contents ###
        try: ###
            title, left_axis_label, data_list = read_file(input_file) ###
            file_read = True ###
        except FileNotFoundError: ###
            print(f"File {input_file} not found or is not readable.") ###
            input_file = "" ###
            
    # Section 2: Create a window and canvas ###
    win = set_up_graph(title) ###

    # Section 3: Process the data ###
    try: ###
        data_dic = process_data(data_list) ###
    except ValueError as error: ###
        print("Content of file is invalid: ") ###
        print(error) ###
        return ###

    # Section 4: Draw the graph ###
    draw_sankey(win, left_axis_label, data_dic, GAP, 100) ###

    win.wait() ###

if __name__ == "__main__": ###
    main() ###
