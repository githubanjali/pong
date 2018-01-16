from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

class PongGame(Widget):
	ball = ObjectProperty(None)

	def serve_ball(self):
		self.ball.center = self.center
		self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))
				
	def update(self, dt):
		self.ball.move()

		# bounce off top and bottom
		if (self.ball.y < 0) or (self.ball.top > self.height):
			self.ball.velocity_y *= -1

		# bounce off left and right
		if (self.ball.x < 0) or (self.ball.right > self.width):
			self.ball.velocity_x *= -1
	def on_touch_move(self, touch):
		if touch.x < self.width/3:
			self.player1.center_y = touch.y
		if touch.x > self.width - self.width/3:
			self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
		game = PongGame()
		game.serve_ball()
		Clock.schedule_interval(game.update, 1.0/60.0)
		return game

class PongBall(Widget):

    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
		
class PongPaddle(Widget):

    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            speedup  = 1.1
            offset = 0.02 * Vector(0, ball.center_y-self.center_y)
            ball.velocity =  speedup * (offset - ball.velocity)		
		
if __name__ == '__main__':
    PongApp().run()