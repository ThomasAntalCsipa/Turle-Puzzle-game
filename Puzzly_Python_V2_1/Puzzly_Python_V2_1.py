# good luck understanding the code
# the game logic loop start at line 1020
# sorry sorry for bad english

#game variables:

import turtle

window = turtle.Screen( )
#turtle.winow_width( ) is set at width=0.5, so it will be autamaticly moved to the right side of the screeen
window.setup(width=0.5, height=1.0, startx = turtle.window_width( ), starty=0)
window.bgcolor("#ffffff")
window.title("Puzzly Python V2_1")

t = turtle.Turtle( )

play_game = True

re_draw_objects_dictonary = { }
# for undoing
previos_map = { }


_map = { }
# for undturdy ground map
map_size_x = int
map_size_y = int
curent_level = int
buffer_array = [ ]
buffer_dictonary = { }

# for when pre-prossesing and optimizing first time map drawing
# and when switching from nice to fast draw type
fast_rendering = True
already_checked_objects_dictonary = { }
biggest_x_value_for_pre_prossesing = -1
biggest_y_value_for_pre_prossesing = -1

already_checked_objects_for_drag_array = [ ]
square_size = 25
square_spacing = 0


# 1 = air, 2 = player, 3 = goal, 4 = box, 5 = wall, 6 = hole, 7 = unsturdy ground(ug), 8 = player on ug, 9 = box on ug, 10 = drag box, 11 = drag box on ug,
# 12 = drag box, 13 = drag box on ug, 14 = final goal (wins game)
object_value_to_color_array = ["#ffffff","#f0f0f0","#0000ff","#ffff00","#ff6969","#696969","#000000","#c0c0c0","#1212c1","#f35252","#00FFFF","#19c6c6",
    "#00dd00","#36af36","#d000ff",]

object_data_dictonary = {
# under value -> 2 = stabel, 1 = unstable, will brakes and leave a hole behi
# [[over_value, under_value], [
# stops movement
# can push
# can be pushed
# can pull
# can be pulled
# can drag
# can be draged
# wins level
# can win level
# wins game
# can win game
# can overlap
# on overlap becomes hole
# on overlap becomes air
# ]]

    1  : [[1,0], []],
    7  : [[1,2], []],
    6  : [[6,0], ["can overlap"]],
    0  : [[1,1], ["stops movement"]],
    5  : [[5,0], ["stops movement"]],
    3  : [[3,0], ["wins level"]],
    14 : [[14,0],["wins game"]],
    2  : [[2,0], ["can push", "can pull", "can drag", "can win level", "can win game", "on overlap becomes hole"]],
    8  : [[2,1], ["can push", "can pull", "can drag", "can win level", "can win game", "on overlap becomes hole"]],
    4  : [[4,0], ["can be pushed", "can drag", "on overlap becomes air"]],
    9  : [[4,1], ["can be pushed", "can drag", "on overlap becomes air"]],
    10 : [[10,0],["can be pushed", "can be pulled", "on overlap becomes air"]],
    11 : [[10,1],["can be pushed", "can be pulled", "on overlap becomes air"]],
    12 : [[12,0],["can be draged", "can pull", "on overlap becomes air"]],
    13 : [[12,1],["can be draged", "can pull", "on overlap becomes air"]],
    
}
# levels are in a dictonary to make it easyer to read them
# two fist values define x and y size of level.
levels = {

"level_1":[5,5,
1,1,1,1,1,
1,2,1,5,1,
1,1,5,5,1,
1,1,5,1,1,
1,1,1,1,3,],

"level_2":[5,4,
1,1,4,1,1,
1,1,6,1,1,
2,1,6,1,3,
1,1,6,1,1],

"level_3":[4,5,
1,1,1,2,
1,5,1,5,
1,1,4,1,
5,5,1,5,
1,5,1,3,],

"level_4":[4,5,
1,1,1,2,
1,5,1,5,
1,1,4,1,
5,5,6,5,
1,5,1,3,],

"level_5":[5,3,
1,1,5,1,1,
2,4,4,1,1,
1,1,5,1,3,],

"level_6":[5,4,
1,1,5,1,1,
1,4,4,6,1,
1,1,5,1,6,
2,1,5,5,3,],

"level_7":[5,3,
1,1,4,1,5,
2,1,4,1,3,
1,1,4,1,5,],

"level_8":[8,5,
5,5,1,1,1,1,5,1,
5,1,1,1,1,1,5,5,
1,1,4,6,1,6,6,3,
2,1,4,1,6,1,5,5,
1,1,4,6,1,1,5,1,],

"level_9":[7,7,
1,3,1,5,5,1,1,
1,1,1,5,5,4,1,
1,6,1,5,5,1,1,
5,6,5,5,1,4,1,
1,6,1,5,1,4,1,
1,1,1,2,1,1,1,
1,1,1,1,1,1,1,],

"level_10":[10,9,
1,1,1,1,5,1,1,1,1,5,
1,1,4,1,6,1,4,1,1,5,
1,1,1,5,5,6,5,5,5,5,
1,5,4,5,1,1,1,5,1,1,
1,5,1,6,1,4,2,6,6,6,
1,4,1,5,1,1,1,5,5,6,
1,4,6,5,5,6,5,5,5,3,
5,5,5,1,4,1,4,1,5,5,
5,5,5,1,1,1,1,1,5,5,],

"level_11":[8,5,
5,1,1,7,1,1,5,1,
1,1,1,5,1,1,5,5,
1,4,1,7,1,2,6,3,
1,1,1,5,1,1,5,5,
5,1,1,7,1,1,5,1,],

"level_12":[9,3,
2,7,1,1,1,5,1,1,1,
5,5,1,5,4,5,1,4,1,
3,6,1,1,1,7,1,1,1,],

"level_13":[6,5,
7,2,1,1,6,3,
7,5,7,5,5,5,
1,1,1,1,1,1,
1,1,4,4,4,1,
1,1,6,1,6,1,],

"level_14":[5,4,
1,8,1,4,1,
1,5,1,1,1,
1,4,1,5,5,
5,1,1,6,3],

"level_15":[7,5,
1 ,1 ,1 ,5 ,1 ,10,1 ,
1 ,10,1 ,5 ,1 ,1 ,1 ,
1 ,1 ,1 ,6 ,1 ,1 ,1 ,
1 ,2 ,1 ,5 ,6 ,6 ,6 ,
1 ,1 ,1 ,5 ,6 ,3 ,6 ,
],

"level_16":[6,3,
1 ,1 ,4 ,10 ,1 ,1 ,
3 ,1 ,5 ,5 ,1 ,2 ,
1 ,1 ,10,4 ,1 ,1 ,],

"level_17":[7,6,
1 ,1 ,1 ,6 ,1 ,1 ,10,
1 ,1 ,1 ,7 ,1 ,1 ,1 ,
1 ,10,1 ,6 ,1 ,2 ,1 ,
1 ,1 ,1 ,6 ,1 ,1 ,6 ,
6 ,6 ,6 ,6 ,6 ,6 ,6 ,
6 ,6 ,6 ,6 ,6 ,6 ,3 ,],

"level_18":[8,8,
6 ,6 ,1 ,6 ,6 ,6 ,6 ,6 ,
6 ,1 ,1 ,1 ,6 ,6 ,3 ,6 ,
6 ,6 ,1 ,6 ,6 ,6 ,6 ,6 ,
6 ,6 ,6 ,6 ,6 ,6 ,6 ,6 ,
6 ,10,10,10,6 ,6 ,1 ,1 ,
6 ,10,2 ,10,6 ,6 ,1 ,1 ,
6 ,10,10,10,6 ,6 ,6 ,6 ,
6 ,6 ,6 ,6 ,6 ,6 ,6 ,6 ,],

"level_19":[10,7,
1 ,1 ,1 ,5 ,1 ,12,5 ,1 ,1 ,1,
1 ,4 ,1 ,1 ,1 ,1 ,1 ,1 ,2 ,1,
1 ,1 ,1 ,5 ,1 ,12,5 ,1 ,1 ,1,
5 ,5 ,5 ,5 ,5 ,5 ,5 ,5 ,6 ,5,
5 ,5 ,1 ,1 ,1 ,1 ,5 ,1 ,1 ,1,
5 ,3 ,1 ,12,1 ,1 ,1 ,1 ,1 ,1,
5 ,5 ,1 ,1 ,1 ,1 ,5 ,1 ,1 ,1,
],

"level_20":[5,5,
1 ,1 ,1 ,5 ,5 ,
1 ,1 ,1 ,1 ,5 ,
5 ,12,1 ,1 ,5 ,
1 ,1 ,5 ,6 ,5 ,
2 ,1 ,5 ,3 ,5 ,
],

"level_21":[4,5,
1 ,1 ,1 ,2 ,
1 ,6 ,12,6 ,
1 ,1 ,12,1 ,
6 ,6 ,6 ,5 ,
1 ,6 ,1 ,3 ,],

"level_22":[6,6,
1 ,1 ,1 ,1 ,5 ,5 ,
5 ,1 ,1 ,1 ,5 ,5 ,
5 ,5 ,1 ,1 ,6 ,6 ,
5 ,12,1 ,1 ,5 ,3 ,
1 ,4 ,1 ,5 ,5 ,5 ,
1 ,2 ,1 ,5 ,5 ,5 ,],

"level_23":[7,6,
1 ,1 ,1 ,5 ,1 ,1 ,1 ,
1 ,1 ,1 ,7 ,1 ,5 ,1 ,
2 ,4 ,4 ,5 ,13,6 ,1 ,
1 ,1 ,1 ,7 ,1 ,5 ,5 ,
5 ,5 ,1 ,7 ,1 ,5 ,5 ,
5 ,5 ,1 ,7 ,6 ,3 ,5 ,],

"level_24":[5,5,
1 ,1 ,12,1 ,1 ,
2 ,1 ,1 ,1 ,6 ,
1 ,1 ,12,1 ,1 ,
6 ,6 ,6 ,5 ,5 ,
6 ,6 ,3 ,5 ,5 ,],

"level_25":[8,5,
1 ,1 ,1 ,7 ,1 ,1 ,5 ,1 ,
12,1 ,1 ,6 ,1 ,1 ,5 ,5 ,
1 ,1 ,1 ,7 ,1 ,2 ,6 ,3 ,
12,1 ,1 ,6 ,1 ,1 ,5 ,5 ,
1 ,1 ,1 ,7 ,1 ,1 ,5 ,1 ,],

"level_26":[3,6,
1 ,3 ,1,
1 ,6 ,1,
5 ,1 ,5,
10,12,1,
1 ,1 ,1,
5 ,2 ,5,],

"level_27":[5,5,
10,5 ,5 ,5 ,3 ,
1 ,12,1 ,5 ,6 ,
1 ,1 ,1 ,5 ,1 ,
5 ,2 ,1 ,1 ,1 ,
5 ,1 ,1 ,1 ,1 ,
],

"level_28":[5,6,
3 ,5 ,1 ,1 ,1 ,
6 ,6 ,1 ,1 ,1 ,
5 ,5 ,7 ,7 ,5 ,
1 ,1 ,10,12,1 ,
1 ,2 ,1 ,1 ,1 ,
1 ,1 ,1 ,1 ,1 ,
],

"level_29":[4,16,
5 ,1 ,1 ,1 ,
5 ,1 ,1 ,1 ,
3 ,6 ,5 ,6 ,
5 ,5 ,5 ,7 ,
1 ,1 ,1 ,6 ,
1 ,1 ,1 ,1 ,
1 ,1 ,1 ,1 ,
1 ,1 ,1 ,1 ,
7 ,7 ,7 ,7 ,
7 ,7 ,7 ,7 ,
7 ,7 ,7 ,7 ,
7 ,7 ,7 ,7 ,
1 ,1 ,1 ,1 ,
1 ,4 ,1 ,1 ,
1 ,1 ,2 ,12,
10,1 ,1 ,1 ,],

"level_30":[7,5,
4 ,1 ,1 ,1 ,1 ,1 ,6 ,
1 ,1 ,1 ,1 ,1 ,1 ,1 ,
1 ,2 ,1 ,1 ,1 ,14,1 ,
1 ,1 ,1 ,1 ,1 ,1 ,1 ,
10,1 ,1 ,1 ,1 ,1 ,12,],

}  

#fuctions:

def load_level(level_number):

    #the global function makes so that the variable can be used in the hole prosject and not just in this fucntion
    global levels
    global curent_level
    global buffer_array

    global _map
    global map_size_x
    global map_size_y

    global previos_map

    # the dictonary makes checking if the level exsists much easyer
    # level_number can also be a name
    if "level_" + str(level_number) in levels:

        # buffer_array alows me to reameber wicth level that is being loaded without having to check every level manuly
        buffer_array = levels.get("level_" + str(level_number))

        curent_level = level_number
    
    else:
        print("error: level_number is invalid")


    if str(level_number) == "2":
    
        print("type z to undo your last move")
        print("or")
        print("type r to restart the level")


    if buffer_array:

        _map.clear( )

        # the variables are just so the code isn't imposible to read
        map_size_x = buffer_array[0]
        map_size_y = buffer_array[1]
        map_max_grid_size_x = map_size_x * square_size + map_size_x * square_spacing
        map_max_grid_size_y = map_size_y * square_size + map_size_y * square_spacing

        #if map_size_x > map_size_y:
        #   
        #    map_ofset_y = (map_size_x - map_size_y) * square_size
        #
        #    turtle.setworldcoordinates(0, -map_ofset_y, map_max_grid_size_x, map_max_grid_size_x + map_ofset_y)
        #
        #elif map_size_y > map_size_x:
        #
        #    map_ofset_x = (map_size_y - map_size_x) * square_size
        #
        #    turtle.setworldcoordinates(-map_ofset_x, 0, map_max_grid_size_y + map_ofset_x, map_max_grid_size_y)
        #
        #else:
        #    
        #    #turtle.setup(map_max_grid_size_x, map_max_grid_size_y)
        #    #turtle.setworldcoordinates(0, -map_max_grid_size_y - square_size / 2 - square_spacing / 2, map_max_grid_size_x + square_size / 2 + square_spacing / 2, 0)
        #    turtle.setworldcoordinates(0, map_max_grid_size_y, map_max_grid_size_x, 0)
        
        turtle.setworldcoordinates(0, map_max_grid_size_y, map_max_grid_size_x, 0)

        t.hideturtle( )
        t.up( )

        
        # takes the map data in the buffer_array and make a dictonary with
        # cordinates and object values so the game can edit it without
        # editing level data directrly and storing the curent map state in memory
        for ny in range(map_size_y):

            for nx in range(map_size_x):

                _map[(nx, ny)] = buffer_array[(nx + (ny * map_size_x)) + 2]
        
        previos_map = _map.copy( )
        
        draw_map( )


def draw_square(square_position_x, square_position_y, square_color = "#xxxxxx"): 

    #uses the square_size and square_spacing variables to get the suqare position in the "grid"
    #square_position_y is fliped so the boxes are renderd in like scann lines
    
    t.goto(square_size * square_position_x + square_spacing * square_position_x, square_size * square_position_y + square_spacing * square_position_y)

    t.down( )
    t.begin_fill( )
    t.pensize(None)
    t.speed(-1)
    t.color(square_color)

    # makes a square with tre lines and fils in the last one (more optimal than making four lines)
    t.setx(t.xcor( ) + square_size)
    t.sety(t.ycor( ) + square_size)
    t.setx(t.xcor( ) - square_size)
    #t.setpos(t.xcor( ) - square_size, t.ycor( ) - square_size)
    #t.setx(t.xcor( ) + square_size)

    t.end_fill( )
    t.up( )


def draw_streched_square(square_position_x, square_position_y, streched_endpoint_x, streched_endpoint_y, square_color = "#xxxxxx"):

    t.goto(square_size * square_position_x + square_spacing * square_position_x, square_size * square_position_y + square_spacing * square_position_y)

    t.down( )
    t.begin_fill( )
    t.pensize(None)
    t.speed(-1)
    t.color(square_color)

    t.goto(square_size * (streched_endpoint_x + 1) + square_spacing * streched_endpoint_x, square_size * square_position_y + square_spacing * square_position_y)
    t.goto(square_size * (streched_endpoint_x + 1) + square_spacing * streched_endpoint_x, square_size * (streched_endpoint_y + 1) + square_spacing * streched_endpoint_y)
    t.goto(square_size * square_position_x + square_spacing * square_position_x, square_size * (streched_endpoint_y + 1) + square_spacing * streched_endpoint_y)

    t.end_fill( )
    t.up( )


def move_player(movment_direction):

    player_found = False

    for object_position, object_value in _map.items( ):
        
        # 2 is normal player and 8 is player on unsturdy ground
        if object_value == 2 or object_value == 8:
            
            player_found = True

            move_object_pre_chain(object_position, movment_direction, True)

            #the brake is to not check more object then nesesery (all maps have just one player)
            break

    if player_found == False:

        print("type z to undo your last move")
        print("or")
        print("type r to restart the level")


def draw_map( ):

    t.clear( )

    if fast_rendering:

        global biggest_x_value_for_pre_prossesing
        global biggest_y_value_for_pre_prossesing

        global already_checked_objects_dictonary
        already_checked_objects_dictonary.clear( )

        #print(type(biggest_x_value_for_pre_prossesing))
        #print(type(biggest_y_value_for_pre_prossesing))

        # all this is for making the map rendering faster, but saddy makes it also more advanced
        for object in _map.items( ):

            object_position = object[0]
            object_position_x = object_position[0]
            object_position_y = object_position[1]
            object_value = object[1]

            #print("-")

            if object_position not in already_checked_objects_dictonary:

                for scouting_object in _map.items( ):

                    scouting_object_position = scouting_object[0]
                    scouting_object_position_x = scouting_object_position[0]
                    scouting_object_position_y = scouting_object_position[1]
                    scouting_object_value = scouting_object[1]

                    #print( )
                    #print(object_position, object_value)
                    #print(scouting_object_position, scouting_object_value)
                    #print(scouting_object_value == object_value)

                    if scouting_object_value == object_value and scouting_object_position_x >= object_position_x and scouting_object_position_y >= object_position_y:
                        
                        #print("yess")
                        already_checked_objects_dictonary[scouting_object_position] = scouting_object_value

                        if scouting_object_position_x > biggest_x_value_for_pre_prossesing:

                            biggest_x_value_for_pre_prossesing = scouting_object_position_x

                        if scouting_object_position_y > biggest_y_value_for_pre_prossesing:

                            biggest_y_value_for_pre_prossesing = scouting_object_position_y
                
                #print( )
                #print(biggest_x_value_for_pre_prossesing)
                #print(biggest_y_value_for_pre_prossesing)

                draw_object(object_position_x, object_position_y, object_value, True, biggest_x_value_for_pre_prossesing, biggest_y_value_for_pre_prossesing)

                for check_object in _map.items( ):
                    
                    if check_object in already_checked_objects_dictonary.items( ):

                        check_object_position = check_object[0]
                        check_object_position_x = check_object_position[0]
                        check_object_position_y = check_object_position[1]
                        check_object_value = check_object[1]

                        #print( )
                        #print(object)
                        
                        if check_object_value != object_value:

                            #print(check_object)
                            #print("!=")

                            if check_object_position_x >= object_position_x:

                                #print(">=x")
                            
                                if check_object_position_y >= object_position_y:

                                    #print(">=y")
                            
                                    if check_object_position_x <= biggest_x_value_for_pre_prossesing:

                                        #print("<=x")

                                        if check_object_position_y <= biggest_y_value_for_pre_prossesing:
                                            
                                            #print("horray")
                                            #print(check_object_position)
                                            already_checked_objects_dictonary.pop(check_object_position)
                
            biggest_x_value_for_pre_prossesing = -1
            biggest_y_value_for_pre_prossesing = -1

    #draw_dot(0,0)
    #draw_dot(map_size_x,0)
    #draw_dot(0,map_size_y)
    #draw_dot(map_size_x,map_size_y)

    elif not fast_rendering:

        # makes it so all the objects are drawn at the right positions
        
        for ny in range(map_size_y):
            
            for nx in range(map_size_x):
        
                draw_object(nx, ny, _map.get((nx, ny)))
                #pass


# makes it easyer to customize the way objects are drawn
def draw_object(object_position_x, object_position_y, object_value, streached = False, streached_endpoint_x = None, streached_endpoint_y = None):

    #object_position_x = int(object_position_x)
    #object_position_y = int(object_position_y)
    # 
    #if object_value == 0:
    #    
    #    draw_square(object_position_x, object_position_y, "f0f0f0")
    #
    #elif object_value == 1:
    #    
    #    draw_square(object_position_x, object_position_y, "0000ff")
    #
    #elif object_value == 2:
    #    
    #    draw_square(object_position_x, object_position_y, "ffff00")
    #
    #elif object_value == 3:
    #    
    #    draw_square(object_position_x, object_position_y, "ff6969")
    #
    #elif object_value == 4:
    #
    #    draw_square(object_position_x, object_position_y, "696969")
    #
    #elif object_value == 5:
    #
    #    draw_square(object_position_x, object_position_y, "000000")
    
    if not streached:
    
        draw_square(int(object_position_x), int(object_position_y), object_value_to_color_array[object_value])
    
    elif streached:

        draw_streched_square(object_position_x, object_position_y, streached_endpoint_x, streached_endpoint_y, object_value_to_color_array[object_value])


# rotation is by 0.5pi radiand (90 degres)
# clockwise and counterclockwise
def matrix_transformation(vector : tuple, operation = "rotate c | rotate cc"):

    # transformations are upsidedown beacuse the y axses is upsidedown

    if operation == "rotate c":

        #[0 -1] [v.x] 
        #[1  0]*[v.y]
        return (0 * vector[0] + -1 * vector[1], 1 * vector[0] + 0 * vector[1])

    elif operation == "rotate cc":
        
        #[ 0 1] [v.x]
        #[-1 0]*[v.y]
        return (0 * vector[0] + 1 * vector[1], -1 * vector[0] + 0 * vector[1])


def win_game( ):

    if curent_level == "30":

        print("you are now smart")
        print("THX for playing! :)")
        print( )
        print("to end the game type: end")


def re_draw_objects(what_to_do, object_position = None, object_value = None, draw_exact = False):
        
    global re_draw_objects_dictonary
    global previos_map
    global _map

    # add all the objects to a buffer so they can be drawn at the "same" time
    if what_to_do == "add":

        re_draw_objects_dictonary[object_position] = object_value
 

    # draws the objcts and updates the _map with the new positions
    elif what_to_do == "draw":
        
        if not re_draw_objects_dictonary:

            return

        previos_map = _map.copy( )
        

        # sorts so all items follow the scan line when redrawning
        if True:
            # it need to flip the x and y in the positions so it
            # priorityses the y value befor the x so it folows the scan line
            # so I just flip the x and y befor and after ordering the positions
            # janky as f ik
            #print(re_draw_objects_dictonary)
            buffer_dictonary.clear( )

            for position in re_draw_objects_dictonary.keys( ):

                buffer_dictonary[(position[1], position[0])] = re_draw_objects_dictonary.get(position)
            
            re_draw_objects_dictonary = buffer_dictonary.copy( )
            buffer_dictonary.clear( )

            for position in sorted(list(re_draw_objects_dictonary.keys( ))):
        
                buffer_dictonary[position] = re_draw_objects_dictonary.get(position)
            
            re_draw_objects_dictonary = buffer_dictonary.copy( )
            buffer_dictonary.clear( )
            
            for position in re_draw_objects_dictonary.keys( ):

                buffer_dictonary[(position[1], position[0])] = re_draw_objects_dictonary.get(position)
            
            re_draw_objects_dictonary = buffer_dictonary.copy( )

            #print(re_draw_objects_dictonary)
            #print( )

        if draw_exact:

            for _object_position, _object_value in re_draw_objects_dictonary.items( ):

                if _map.get(_object_position) != _object_value:
           
                    draw_object(_object_position[0], _object_position[1], _object_value)
        
                    _map[_object_position] = _object_value

        elif not draw_exact:

            for _object_position, _object_value in re_draw_objects_dictonary.items( ):
                
                if _map.get(_object_position) != _object_value:

                    old_layer_data_object_value = object_data_dictonary.get(_map.get(_object_position))[0]
                    new_layer_data_object_value = object_data_dictonary.get(_object_value)[0]

                    #print(old_layer_data_object_value, new_layer_data_object_value, "sus")

                    for check_value, layer_data_check_object in object_data_dictonary.items( ):

                        layer_data_check_object = layer_data_check_object[0]

                        #print(layer_data_check_object, "sy")
                        
                        # just to make overlaping one way from unsturdy
                        # ground to somthing wiht a hole under it
                        if old_layer_data_object_value[1] == 2:

                            check = 1
                        else:

                            check = old_layer_data_object_value[1]

                        if layer_data_check_object[1] == check and layer_data_check_object[0] == new_layer_data_object_value[0]:
                            
                            # so the same thing is not drawn again
                            # and make the game feel laggy
                            if check_value != _map.get(_object_position):

                                if check_value == 0:

                                    check_value = 6

                                draw_object(_object_position[0], _object_position[1], check_value)

                                _map[_object_position] = check_value
            
        re_draw_objects_dictonary.clear( )


    elif what_to_do == "undo":

        re_draw_objects_dictonary.clear( )

        diffrent = False

        for item_postion, item_value in _map.items( ):

            if item_value != previos_map.get(item_postion):

                re_draw_objects_dictonary[item_postion] = previos_map.get(item_postion)

                #print(item_postion, previos_map.get(item_postion))

                diffrent = True

        if diffrent:

            re_draw_objects("draw", None, None, True)

    else:
        
        print("error: re_draw_objects(what_to_do) is an invalid value")


# calkulates all objects that will be pushed at the same time
# so it gose back to the first thing that is gonna be pulled
# the pulled thing is just pushing everything else
# pull things is just having the push origin from the last pull object
def move_object_pre_chain(object_position, movment_direction, draw_when_finished):

    global _map
    global object_data_dictonary
    
    object_value = _map.get(object_position)
    property_data_object_value = object_data_dictonary.get(object_value)[1]

    # object_position[0] gives x and [1] gives y
    # same with movment_direction

    object_behind_position = ((object_position[0] - movment_direction[0]), (object_position[1] - movment_direction[1]))

    can_not_continue = False

    #print(object_behind_position)

    if object_behind_position not in _map:

        #print("outside")

        can_not_continue = True

        property_data_object_behind_value = [ ]

    else:

        object_behind_value = _map.get(object_behind_position)
        property_data_object_behind_value = object_data_dictonary.get(object_behind_value)[1]
        #print(property_data_object_behind_value)
    

    if "can pull" not in property_data_object_value:

        #print(object_value, property_data_object_value)

        #print("to weak object")

        can_not_continue = True
    
    if "can be pulled" not in property_data_object_behind_value:

        #print("dose not like being pulled")

        can_not_continue = True
    
    if can_not_continue:

        if move_object_in_chain(object_position, movment_direction):
            
            re_draw_objects("add", object_position, 1)
            # in can happen that it drags somthing that pulls somthing that can be draged right beind it
            # but as far as im programing it, I belive it will not happen
            # ( logicly imposeble with the code I have so far)
        
        #print(add_objec_to_redraw, "aotr")
        
        if draw_when_finished:
            
            re_draw_objects("draw")

            already_checked_objects_for_drag_array.clear( )

        return True

    move_object_pre_chain(object_behind_position, movment_direction, draw_when_finished)


def move_object_in_chain(object_position, movment_direction):
    
    global _map
    global object_data_dictonary
    
    object_value = _map.get(object_position)
    #print(object_value, object_position)
    property_data_object_value = object_data_dictonary.get(object_value)[1]

    # object_position[0] gives x and [1] gives y

    object_destination_position = ((object_position[0] + movment_direction[0]), (object_position[1] + movment_direction[1]))


    #checks if the object is going outside the map

    if object_destination_position[0] < 0 or object_destination_position[1] < 0:

        #print("object_trys_to_escape")
        return False

    elif object_destination_position[0] > map_size_x - 1 or object_destination_position[1] > map_size_y - 1:

        #print("object_trys_to_escape")
        return False

    object_destination_value = _map.get(object_destination_position)
    #print(object_destination_position, object_destination_value, map_size_x, map_size_y)
    property_data_object_destination_value = object_data_dictonary.get(object_destination_value)[1]
    
    #print(property_data_object_destination_value)

    
    if "can drag" in property_data_object_value:

        #print( )
        #print("drag")

        clockwise_direction = matrix_transformation(movment_direction, "rotate c")
        clockwise_object_position = (object_position[0] + clockwise_direction[0], object_position[1] + clockwise_direction[1])
        
        #print(clockwise_object_position)

        if clockwise_object_position in _map:
            
            #print("c in map")

            property_data_clockwise_object_position = object_data_dictonary.get(_map.get(clockwise_object_position))[1]

            #print(property_data_clockwise_object_position)

            if "can be draged" in property_data_clockwise_object_position:

                #print("can be draged")

                if clockwise_object_position not in already_checked_objects_for_drag_array:

                    #print("have not been draged")

                    already_checked_objects_for_drag_array.append(clockwise_object_position)

                    move_object_pre_chain(clockwise_object_position, movment_direction, False)

        counterclockwise_direction = matrix_transformation(movment_direction, "rotate cc")
        counterclockwise_object_position = (object_position[0] + counterclockwise_direction[0], object_position[1] + counterclockwise_direction[1])

        if counterclockwise_object_position in _map:

            property_data_counterclockwise_object_position = object_data_dictonary.get(_map.get(counterclockwise_object_position))[1]

            if "can be draged" in property_data_counterclockwise_object_position:

                if counterclockwise_object_position not in already_checked_objects_for_drag_array:
                    
                    already_checked_objects_for_drag_array.append(counterclockwise_object_position)

                    move_object_pre_chain(counterclockwise_object_position, movment_direction, False)

    _else = True

    if "stops movement" in property_data_object_destination_value:

        return False
    
    if "wins level" in property_data_object_destination_value:
        
        if "can win level" in property_data_object_value:
            
                load_level(int(curent_level) + 1)

        return False
    
    if "wins game" in property_data_object_destination_value:

        if "can win game" in property_data_object_value:

            win_game( )

        return False

    if "can overlap" in property_data_object_destination_value:

        if "on overlap becomes air" in property_data_object_value:

            re_draw_objects("add", object_destination_position, 1)

            return True

        elif "on overlap becomes hole" in property_data_object_value:

            re_draw_objects("add", object_destination_position, 6)
            
            return True
    
    if "can pull" in property_data_object_destination_value:

        if "can be pulled" in property_data_object_value:

            if move_object_in_chain(object_destination_position, movment_direction):

                re_draw_objects("add", object_destination_position, object_value)

                return True
               
            else:
                
                _else = False
                   
        else:
                
                _else = False

    if "can be pushed" in property_data_object_destination_value:

        if "can push" in property_data_object_value:

            if move_object_in_chain(object_destination_position, movment_direction):
                
                re_draw_objects("add", object_destination_position, object_value)

                return True
        
            else:
                #print("_else !=")
                _else = False
        
        else:
            #print("_else !=")
            _else = False
 
    if _else:
        
        #print("_else")
        re_draw_objects("add", object_destination_position, object_value)

        return True
    
    else:
        #print("!_else")
        return False





# game logic:

#loads the first level of the game (1)
load_level(1)

first_play_dalay = True

print("type \"fast\" to make rendering fast (currently on)")
print("but the tiles will not have a small gap")
print( )
print("or type \"nice\" to have a small gap inbetwen")
print("all the tiles, but rendering is much slower")
print( )
print("rendering only affects when you load or reload a level")

while play_game:

    _input = input( )

    if _input == "end":
        
        play_game = False
        first_play_dalay = False
        
    elif _input == "r":

        load_level(curent_level)
    
    
    elif _input == "w":
        
        # the y directions are fliped beacuse
        # the map rendering is upside down
        # and
        # the flip_re_draw_objects_order is to emulate
        # scanlines (like the thing that moves left to
        # right and from topp to bottom)
        move_player((0, -1))

    
    elif _input == "a":

        move_player((-1, 0))

        
    elif _input == "s":
        
        move_player((0, 1))
        
        
    elif _input == "d":
        
        move_player((1, 0))

    elif _input == "z":

        re_draw_objects("undo")
    
    elif _input == "nice":

        fast_rendering = False

        square_spacing = 5

        map_max_grid_size_x = map_size_x * square_size + map_size_x * square_spacing
        map_max_grid_size_y = map_size_y * square_size + map_size_y * square_spacing

        turtle.setworldcoordinates(0, map_max_grid_size_y, map_max_grid_size_x, 0)

        draw_map( )
    
    elif _input == "fast":

        fast_rendering = True

        square_spacing = 0

        map_max_grid_size_x = map_size_x * square_size + map_size_x * square_spacing
        map_max_grid_size_y = map_size_y * square_size + map_size_y * square_spacing

        turtle.setworldcoordinates(0, map_max_grid_size_y, map_max_grid_size_x, 0)

        draw_map( )
    
    elif _input == "skip":
        
        load_level(int(curent_level)+1)

    elif _input.find("load") == 0 and len(_input) > 4:

        load_level(_input[4:].replace(" ",""))
    
    elif _input == "help":

        print("commands:")
        print("w - move up")
        print("a - move left")
        print("s - move down")
        print("d - move right")
        print("z - undo your last move")
        print("r - restart the current level level")
        print("skip - load the next level")
        print("load - followed by a level number will load that level")
        print("fast - disable gaps betwen tiles and speeds up loading and reloading levels")
        print("nice - enable gaps betwen tiles and slows down loading and reloading levels")
        print("help - show a list with all the commands described")
        print("^Z - written with Ctrl + z will crash the game")
    
    if first_play_dalay:

        first_play_dalay = False

        print("you can always change it when you want")
        print("type \"help\" to get a list with all the commands described")

        print("w")
        print("a")
        print("s")
        print("d")