import turtle

window_height = 600
window_width = 600
window_margin = 50
update_interval = 25   

player_size = 50        
player_init_x = 0
player_init_y = -window_height / 2 + window_margin
player_speed = 10       

enemy_number = 21       
enemy_size = 50
enemy_init_x = -window_width / 2 + window_margin
enemy_init_y = window_height / 2 - window_margin
enemy_min_x = enemy_init_x
enemy_max_x = window_width / 2 - enemy_size * enemy_number
enemy_kill_player_distance = 30
    
enemy_speed = 2
enemy_speed_increment = 1
enemy_direction = 1

enemies = []

laser_speed = 20
laser_kill_enemy_distance = 20
laser_kill_special_enemy_distance = 30

cheat_mode = 0
score = 0

def show_special_enemy():
    global special_enemy
    special_enemy.goto(window_width / 2 + 20, window_height / 2 - 30)
    special_enemy.showturtle()

def update_cheat_mode():
    global cheat_mode
    if cheat_mode == 0:
        cheat_mode = 1
    else:
        cheat_mode = 0

def decrease_enemy_number(x, y):
    global enemy_number
    if enemy_number > 1:
        enemy_number -= 1
        enemy_number_text.clear()
        enemy_number_text.write(str(enemy_number), font=("System", 18, "bold"), align="center")
        
def increase_enemy_number(x, y):
    global enemy_number
    if enemy_number < 49:
        enemy_number += 1
        enemy_number_text.clear()
        enemy_number_text.write(str(enemy_number), font=("System", 18, "bold"), align="center")
        
def playermoveleft():
    x, y = player.position()
    if x - player_speed > -window_width / 2 + window_margin:
        player.goto(x - player_speed, y)

def playermoveright():
    x, y = player.position()
    if x + player_speed < window_width / 2 - window_margin:
        player.goto(x + player_speed, y)

def updatescreen():
    global cheat_mode, special_enemy, score

    for enemy in enemies:
        if laser.isvisible() and laser.distance(enemy) <= laser_kill_enemy_distance:
            if enemy.isvisible():
                laser.hideturtle()
                enemy.hideturtle()
                score += 20
                break

    if laser.isvisible() and laser.distance(special_enemy) <= laser_kill_special_enemy_distance:
        if special_enemy.isvisible():
            laser.hideturtle()
            special_enemy.hideturtle()
            score += 100
            turtle.ontimer(show_special_enemy, 5000)
            
    labels.clear()
    labels.goto(-window_width / 2 + 10, window_height / 2 - 35)
    labels.write("Score: " + str(score), font=("System", 18, "bold"))

    if laser.isvisible():
        x, y = laser.position()
        laser.goto(x, y + laser_speed)
    if laser.ycor() > window_height / 2:
        laser.hideturtle()

    for enemy in enemies:
        if (enemy.ycor()-player.ycor() < enemy_kill_player_distance) and (enemy.isvisible()):
            gameover("You lose!")
            return

    count = 0
    for enemy in enemies:
        if enemy.isvisible():
            count += 1
    if count == 0:
        gameover("You win!")
        return

    if cheat_mode == 0:
        global enemy_direction, enemy_speed
        dx = enemy_speed * enemy_direction
        dy = 0

        x0 = enemies[0].xcor()
        if x0 + dx > enemy_max_x or x0 + dx < enemy_min_x:
            enemy_direction = -enemy_direction
            dx = -dx
            dy = -enemy_size / 2
            if enemy_direction == 1:
                enemy_speed = enemy_speed + enemy_speed_increment

        for enemy in enemies:
            x, y = enemy.position()
            enemy.goto(x + dx, y + dy)
            if (x // 20) % 2 == 0:
                enemy.shape("pig_enemy1.gif")
            else:
                enemy.shape("pig_enemy2.gif")

        x, y = special_enemy.position()
        if special_enemy.isvisible() and x <= -window_width / 2 - 20:
            special_enemy.hideturtle()
            turtle.ontimer(show_special_enemy, 5000)
        else:
            special_enemy.goto(x - 5, y)
        
           
    turtle.update()
    turtle.ontimer(updatescreen, update_interval)

def reset_slingshot():
    player.shape("slingshot.gif")

def shootlaser():
    if not laser.isvisible():
        laser.goto(player.position())
        laser.showturtle();
        player.shape("slingshot2.gif")
        turtle.ontimer(reset_slingshot, 200)

def gamestart(x, y):
    global player, laser, enemy_max_x, labels
    
    start_button.clear()
    start_button.hideturtle()
    labels.clear()
    enemy_number_text.clear()
    arrow_left.hideturtle()
    arrow_right.hideturtle()

    labels.goto(-window_width / 2 + 10, window_height / 2 - 35)
    labels.write("Score: " + str(score), font=("System", 18, "bold"))

    if enemy_number < 7:
        enemy_max_x = window_width / 2 - enemy_size * enemy_number
    else:
        enemy_max_x = window_width / 2 - enemy_size * 7;
    
    turtle.addshape("slingshot.gif")
    turtle.addshape("slingshot2.gif")

    player = turtle.Turtle()
    player.shape("slingshot.gif")
    player.up()
    player.goto(player_init_x, player_init_y)

    turtle.listen()
    turtle.onkeypress(playermoveleft, "Left")
    turtle.onkeypress(playermoveright, "Right")
   
    turtle.addshape("pig_enemy1.gif")
    turtle.addshape("pig_enemy2.gif")
    turtle.addshape("special_enemy.gif")
    turtle.addshape("bomb.gif")

    special_enemy.shape("special_enemy.gif")
    special_enemy.up()
    special_enemy.hideturtle()
    turtle.ontimer(show_special_enemy, 5000)

    for i in range(enemy_number):
        enemy = turtle.Turtle()
        enemy.shape("pig_enemy1.gif")
        enemy.up()
        enemy.goto(enemy_init_x + enemy_size * (i % 7), enemy_init_y - enemy_size * (i // 7))
        enemies.append(enemy)

    laser = turtle.Turtle()
    laser.shape("bomb.gif")
    laser.up()

    laser.hideturtle()
    turtle.onkeypress(shootlaser, "space")
    turtle.ontimer(updatescreen, update_interval)
    turtle.onkeypress(update_cheat_mode, "c")

def gameover(message):
    sentence = turtle.Turtle()
    sentence.hideturtle()
    sentence.pencolor("green")
    sentence.write(message, align="center", font=("System", 30, "bold"))
    turtle.update()

turtle.setup(window_width, window_height)
turtle.bgpic("background.gif")
turtle.up()
turtle.hideturtle()
turtle.tracer(False)

start_button = turtle.Turtle()
start_button.up()
start_button.goto(-80, -220)
start_button.color("white", "yellowgreen")
start_button.begin_fill()
for _ in range(2):
    start_button.forward(160)
    start_button.left(90)
    start_button.forward(50)
    start_button.left(90)
start_button.end_fill()

start_button.color("blue")
start_button.goto(0, -215)
start_button.write("Start", font=("System", 24, "bold"), align="center")

start_button.goto(0, -195)
start_button.shape("square")
start_button.shapesize(2.5, 8)
start_button.color("")

labels = turtle.Turtle()
labels.pencolor("blue")
labels.up()
labels.goto(0,200)
labels.write("Defend from Pigs", font=("System", 40, "bold"), align="center")
labels.goto(0,-120)
labels.write("""
It's a bright sunny day, and you are
bathing under the warm sunlight.
Suddenly the green pigs come to attack you!
Luckily, you have prepared your slingshot.
Use left and right arrow keys to control it.
Press space bar to shoot an angry bird!
Click Start below to defend yourself!
Since the game is too hard, press c
button to freeze the screen.
""", font=("System", 18, "bold"), align="center")
labels.goto(-200, -140)
labels.write("Number of Pigs:", font=("System", 18, "bold"))
labels.hideturtle()

enemy_number_text = turtle.Turtle()
enemy_number_text.pencolor("blue")
enemy_number_text.up()
enemy_number_text.goto(80, -140)
enemy_number_text.write(str(enemy_number), font=("System", 18, "bold"), align="center")
enemy_number_text.hideturtle()

arrow_left = turtle.Turtle()
arrow_left.shape("arrow")
arrow_left.color("blue")
arrow_left.shapesize(1, 2)
arrow_left.left(180)
arrow_left.up()
arrow_left.goto(40, -125)
arrow_left.onclick(decrease_enemy_number)

arrow_right = turtle.Turtle()
arrow_right.shape("arrow")
arrow_right.color("blue")
arrow_right.shapesize(1, 2)
arrow_right.up()
arrow_right.goto(120, -125)
arrow_right.onclick(increase_enemy_number)

special_enemy = turtle.Turtle()
special_enemy.hideturtle()

turtle.update()

start_button.onclick(gamestart)

turtle.done()
