#the game logic start down at line ---
#sorry sorry for bad english

#game variables:

import turtle
import winsound

window = turtle.Screen()
window.bgcolor("#ffffff")
window.title("Puzzly_Python_V1_1")
window.setup(width=0.5, height=1.0, startx = turtle.window_width( ), starty=0)

t = turtle.Turtle()

play_game = True

re_draw_objects_dict = {}

_map = {}
map_size_x = int
map_size_y = int
curent_level = int
buffer_array = list

square_size = int(25)
square_spacing = int(5)

#two fist values define x and y size of level. #1 = player, 2 = goal, 3 = box, 4 = wall, 5 = hole
#levels are in a dictonary to make it easyer to read them
levels = {

"level_1":[5,5,
0,0,0,0,0,
0,1,0,4,0,
0,0,4,4,0,
0,0,4,0,0,
0,0,0,0,2,],

"level_2" : [5,4,
0,0,3,0,0,
0,0,5,0,0,
1,0,5,0,2,
0,0,5,0,0],

"level_3":[4,5,
0,0,0,1,
0,4,0,4,
0,0,3,0,
4,4,0,4,
0,4,0,2,],

"level_4":[4,5,
0,0,0,1,
0,4,0,4,
0,0,3,0,
4,4,5,4,
0,4,0,2,],

"level_5":[5,3,
0,0,4,0,0,
1,3,3,0,0,
0,0,4,0,2,],

"level_6":[5,4,
0,0,4,0,0,
0,3,3,5,0,
0,0,4,0,5,
1,0,4,4,2,],

"level_7":[5,3,
0,0,3,0,4,
1,0,3,0,2,
0,0,3,0,4,],

"level_8":[8,5,
4,4,0,0,0,0,4,0,
4,0,0,0,0,0,4,4,
0,0,3,5,0,5,5,2,
1,0,3,0,5,0,4,4,
0,0,3,5,0,0,4,0,],

"level_9":[7,7,
0,2,0,4,4,0,0,
0,0,0,4,4,3,0,
0,5,0,4,4,0,0,
4,5,4,4,0,3,0,
0,5,0,4,0,3,0,
0,0,0,0,1,0,0,
0,0,0,0,0,0,0,],

"level_10":[10,9,
0,0,0,0,4,0,0,0,0,4,
0,0,3,0,5,0,3,0,0,4,
0,0,0,4,4,5,4,4,4,4,
0,4,3,4,0,0,0,4,0,0,
0,4,0,5,0,3,1,5,5,5,
0,3,0,4,0,0,0,4,4,5,
0,3,5,4,4,5,4,4,4,2,
4,4,4,0,3,0,3,0,4,4,
4,4,4,0,0,0,0,0,4,4,],

}  


#fuctions:

def draw_square(square_position_x, square_position_y, square_color):

    #uses the square_size and square_spacing variables to get the suqare position in the "grid"
    t.goto((square_position_x * square_size) + (square_position_x * square_spacing) + square_spacing, -((square_position_y * square_size) + (square_position_y * square_spacing) + square_spacing + square_size))
    
    t.down()
    t.begin_fill()
    t.pensize(1)
    t.speed(-1)
    t.color("#" + str(square_color))

    t.down()
    t.begin_fill()

    #makes a square with tre lines and fils in the last one (more optimal than making four lines)
    t.setx(t.xcor() + square_size)
    t.sety(t.ycor() + square_size)
    t.setx(t.xcor() - square_size)
    
    t.end_fill()
    t.up()



def load_level(level_number):

    #the global function makes so that the variable can be used in the hole prosject and not just in this fucntion
    global levels
    global curent_level
    global buffer_array

    global _map
    global map_size_x
    global map_size_y
    
    curent_level = level_number

    #the dictonary makes checking if the level exsists much easyer
    if "level_" + str(level_number) in levels:

        #buffer_array alows me to reameber wicth level that is being loaded without having to check every level manuly
        buffer_array = levels.get("level_" + str(level_number))

    elif level_number == 11:
        pass
    
    else:
        print("error: level_number is invalid")

    if level_number == 3:
        print("try to type: r")
        
    elif level_number == 11:
        print("you are now smart")
        print("")
        print("if you want, type: load")
        print("and the level number you want to load")
        print("")
        print("or to end the game type: end")

    if buffer_array:

        _map.clear()

        #the variables are just so the code isn't inposible to read
        map_size_x = buffer_array[0]
        map_size_y = buffer_array[1]
        map_max_grid_size_x = (map_size_x * square_size) + (map_size_x * square_spacing)
        map_max_grid_size_y = ((map_size_y) * square_size) + (map_size_y * square_spacing)

        #turtle.setup(map_max_grid_size_x, map_max_grid_size_y)
        turtle.setworldcoordinates(0, -map_max_grid_size_y - square_size / 2 - square_spacing / 2, map_max_grid_size_x + square_size / 2 + square_spacing / 2, 0)

        t.hideturtle()
        t.up()

        
        #takes the map data in the buffer_array and make a dictonary with cordinates and object values so the game can edit it
        for ny in range(map_size_y):

            for nx in range(map_size_x):

                _map[str(nx) + "," + str(ny)] = buffer_array[(nx + (ny * map_size_x)) + 2]
        
        draw_map()
        
def draw_map():

    t.clear()

    #makes it so all the objects are drawn at the right positions
    
    for ny in range(map_size_y):
        
        for nx in range(map_size_x):

            draw_object(nx, ny, _map.get(str(nx) + "," + str(ny)))


#makes it easyer to customize the way objects are drawn
def draw_object(object_position_x, object_position_y, object_value):

    object_position_x = int(object_position_x)
    object_position_y = int(object_position_y)
    
    if object_value == 0:
        
        draw_square(object_position_x, object_position_y, "f0f0f0")

    elif object_value == 1:
        
        draw_square(object_position_x, object_position_y, "0000ff")

    elif object_value == 2:
        
        draw_square(object_position_x, object_position_y, "ffff00")

    elif object_value == 3:
        
        draw_square(object_position_x, object_position_y, "ff6969")

    elif object_value == 4:

        draw_square(object_position_x, object_position_y, "696969")

    elif object_value == 5:

        draw_square(object_position_x, object_position_y, "000000")



def move_player(movment_direction_x, movment_direction_y):

    for object_name, object_value in _map.items():

        if object_value == 1:

            move_object(object_name, movment_direction_x, movment_direction_y)

            #the brake is to not check more object then nesesery (all maps have just one player)
            break


def move_object(object_position, movment_direction_x, movment_direction_y):

    #gets the needed data
    
    object_value = _map[object_position]

    object_destination_position = str(int(object_position[0]) + movment_direction_x) + "," + str(int(object_position[-1]) + movment_direction_y)
    
    object_destination_value = _map.get(object_destination_position)


    #checks if the object is going outside the map

    if int(object_destination_position[:object_destination_position.index(",")]) < 0 or int(object_destination_position[-1]) < 0:

         #print("object_trys_to_escape")
         return False

    elif int(object_destination_position[:object_destination_position.index(",")]) > map_size_x or int(object_destination_position[-1]) > map_size_y:

        #print("object_trys_to_escape")
        return False


    #now it checks for every objct destination

    #if it returns false it means that the object can't be pushed, if true it can
    
    if object_destination_value == 0:

        #add the objcts in to a re_draw_buffer so only the objects that change are drawn again
        
        re_draw_objects("add", object_destination_position, object_value)
        re_draw_objects("add", object_position, object_destination_value)
            
        if object_value != 3:
            
            #if a box is pushed the player has to tell the game to re draw the objcts
            re_draw_objects("draw", 0, 0,)

        return True

    elif object_destination_value == 1:

        #print("object_trys_to_move_in_to_player")

        return False

    elif object_destination_value == 2:

        if object_value == 1:

            load_level(curent_level + 1)

        else:

            #a box can't make you win
            #print("non_player_trys_to_enter_goal")

            return False
                    

    elif object_destination_value == 3:

        #print("box_tuched")

        if object_value == 3:

                #no multipushing
                #print("box_is_tying_to_push_a_box")
                
                return False

        #now the game check if the box has a valid destination
        if move_object(object_destination_position, movment_direction_x, movment_direction_y):

            re_draw_objects("add", object_destination_position, object_value)
            re_draw_objects("add", object_position, 0)

            re_draw_objects("draw", 0, 0)

        else:

            #print("box_is_tying_to_move_in_to_a_wall")
            
            return False


    elif object_destination_value == 4:

        #print("object_walks_in_to_a_wall")

        return False
    
    elif object_destination_value == 5:

        if object_value == 1:

            #re loads the level
            load_level(curent_level)

        elif object_value == 3:

            #makes the hole be filled up
            re_draw_objects("add", object_destination_position, 0)

            return True
        
        else:

            print("error: something non valid move in to a hole")

            return False
            

    else:
        #print("error: object_destination_value is not valid")
        pass



def re_draw_objects(what_to_do, object_position, object_value):
        
    global re_draw_objects_dict

    #add all the objects to a buffer so they can be drawn at the "same" time
    if what_to_do == "add":

        re_draw_objects_dict[object_position] = object_value

        

    #draws the objcts and updates the _map with the new positions
    elif what_to_do == "draw":
        
        for _object_position, _object_value in re_draw_objects_dict.items():

            draw_object(_object_position[0], _object_position[-1], _object_value)

            _map[_object_position] = _object_value

        re_draw_objects_dict.clear()

    else:
        
        print("error: re_draw_objects(what_to_do) is an invalid value")
        



#game logic:

print("w a s d")

#loads the first level of the game
load_level(1)

while play_game:

    _input = input()

    if _input == "end":
        
        play_game = False
        
    elif _input == "r":

        load_level(curent_level)
    
    
    elif _input == "w":

        #the y directions are fliped beacuse the map rendering is upside down
        move_player(0, -1)        

    
    elif _input == "a":
        
        move_player(-1, 0)

        
    elif _input == "s":
        
        move_player(0, 1)
        
        
    elif _input == "d":
        
        move_player(1, 0)
        

    elif _input.find("load") == 0:

        load_level(int(_input[4:]))
