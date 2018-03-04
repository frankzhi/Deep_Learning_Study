import turtle

def draw_rhombus(turtle):
    
    for i in range(2):
        turtle.forward(100)
        turtle.right(30)
        turtle.forward(100)
        turtle.right(150)


def draw_flower(turtle):
    for i in range (360/5):
        draw_rhombus(turtle)
        turtle.right(5)
    turtle.right(90)
    turtle.forward(300)
    canvas.exitonclick()

canvas = turtle.Screen()
canvas.bgcolor("pink")
grace= turtle.Turtle()
grace.shape("turtle")
grace.color("white")
grace.speed(100)



   
draw_flower(grace)
