from blogo import *
from blogo_utils import *

BlogoUtils.start_fresh()
BlogoUtils.add_light_area()

turtle = Blogo()
turtle.set_texture("yellow")
for i in range(10):
    turtle.circle(6)
    turtle.rt(36)