from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.clock import Clock
from kivy.vector import Vector
from random import choice

class PongPaddle(Widget):
    score = NumericProperty(0)
    
    def ball_bounce(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1
    
class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
  
class GameWindow(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
     
    def serve_ball(self):
        self.ball.velocity = Vector(4.2, 0).rotate(choice([15, 45, 135, 165, 195, 225, 315, 345]))
        
    def update(self, dt):
        self.ball.move()
        if (self.ball.y < 0) or (self.ball.y > self.height-50):
            self.ball.velocity_y *= -1
            
        if self.ball.x < 0:
            self.ball.velocity_x *= -1.1
            self.player2.score += 1
            self.ball.pos = (self.width/2, self.height/2)
            self.ball.velocity = Vector(0, 0)
            self.serve_ball()
            
        if self.ball.x > self.width-50:
            self.ball.velocity_x *= -1.1
            self.player1.score += 1
            self.ball.pos = (self.width/2, self.height/2)
            self.ball.velocity = Vector(0, 0)
            self.serve_ball()
            
        self.player1.ball_bounce(self.ball)
        self.player2.ball_bounce(self.ball)
             
    def on_touch_move(self, touch):
        if touch.x < self.width * 1/4:
            self.player1.center_y = touch.y
        if touch.x > self.width * 3/4:
            self.player2.center_y = touch.y      
  
class ExitButton(Button):
    pass
             
class MyGame(App):
    def build(self):
        game = GameWindow()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game
   
if __name__ == '__main__':    
    MyGame().run()
