#-*-coding:utf-8-*-
__author__ = 'Administrator'

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty,NumericProperty
from kivy.clock import Clock
from kivy.graphics import Color,Rectangle,InstructionGroup
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.button import Button
import random
from kivy.lang import Builder
Builder.load_string("""
<Direction>:
    canvas:
        Color:
            rgba: .1, .1, 1, .9
        Line:
            width: 2.
            rectangle: (self.x, self.y, self.width, self.height)
<Options>:
    canvas:
        Color:
            rgba: .1, .1, 1, .9
        Line:
            width: 2.
            rectangle: (self.x, self.y, self.width, self.height)
""")
class Controls(Widget):
    direction = "right" #前进方向

    def __init__(self, **kwargs):
        super(Controls, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self,"text")
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):

        if keycode[0] == 273:
            if self.direction != "down":
                self.direction = "up"
        elif keycode[0] == 276:
            if self.direction != "right":
                self.direction = "left"
        elif keycode[0] == 275:
            if self.direction != "left":
                self.direction = "right"
        elif keycode[0] == 274:
            if self.direction != "up":
                self.direction = "down"

class Main(FloatLayout):
    snake = ListProperty([(0,0)])
    rangeSnake = ListProperty([0,0,Window.width,Window.height])
    startSpeed = NumericProperty(30)

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.keyboard = Controls()
        self.count = 0
        self.bind(size=self.up,pos=self.up)

    def up(self,*args):
        self.rangeSnake[0] = self.pos[0]
        self.rangeSnake[1] = self.pos[1]
        self.rangeSnake[2] = self.pos[0] + self.size[0]
        self.rangeSnake[3] = self.pos[1] + self.size[1]
        self.snake[0] = self.pos

    def start(self,*dt):
        self.canvas.clear()
        Clock.unschedule(self.move)
        self.food()
        Clock.schedule_interval(self.move,1./(self.startSpeed+self.count))

    def restart(self, *dt):
        self.canvas.clear()
        self.clear_widgets()
        Clock.unschedule(self.move)

        self.foods()
        self.snake = [ self.pos]
        self.keyboard.direction = "right"
        Clock.schedule_interval(self.move,1./(self.startSpeed+self.count))

    def stop(self,*dt):
        Clock.unschedule(self.move)

    def continue_move(self):
        Clock.unschedule(self.move)
        Clock.schedule_interval(self.move,1./(self.startSpeed+self.count))

    def food(self,*args):
        self.foodblue = InstructionGroup()
        self.foodblue.add(Color(1, 0, 0, 1))
        x = random.randint(int(self.rangeSnake[0]), int(self.rangeSnake[2]-10))
        y = random.randint(int(self.rangeSnake[1]), int(self.rangeSnake[3]-10))
        self.food = Rectangle(pos=(x,y), size=(10,10))
        self.foodblue.add(self.food)

    def foods(self):
        self.count += 1
        x = random.randint(int(self.rangeSnake[0]), int(self.rangeSnake[2]-10))
        y = random.randint(int(self.rangeSnake[1]), int(self.rangeSnake[3]-10))
        for a,b in self.snake:
            if x > a+10 or y >b+10 or x < a- 10 or y<b-10:
                pass
            else:
                self.foods()
                return
        self.food.pos = (x,y)

    def move(self,*dt):
        self.canvas.clear()
        self.canvas.add(self.foodblue)
        x,y = self.snake[-1]
        if abs(self.snake[-1][0] -self.food.pos[0])<10 and abs(self.snake[-1][1] -self.food.pos[1])<10:#吃到食物
            x,y = self.snake[-1]
            if self.keyboard.direction == "left":
                for i in range(1,11):
                    x1,y1 = x-i,y
                    self.snake.append((x1,y1))
            elif self.keyboard.direction == "right":
                 for i in range(1,11):
                    x1,y1 = x+i,y
                    self.snake.append((x1,y1))
            elif self.keyboard.direction == "up":
                for i in range(1,11):
                    x1,y1 = x,y+i
                    self.snake.append((x1,y1))
            elif self.keyboard.direction == "down":
                for i in range(1,11):
                    x1,y1 = x,y-i
                    self.snake.append((x1,y1))
            self.foods()
        else:
            if self.keyboard.direction == "left":
                x,y = x-1,y
                if x < self.rangeSnake[0] :
                    self.gameover()
                for a,b in self.snake:
                    if x >a and x-a<10 and abs(b-y)<10:
                        self.gameover()
                        break
            elif self.keyboard.direction == "right":
                x,y = x+1,y
                if x+10 > self.rangeSnake[2]:
                    self.gameover()
                for a,b in self.snake:
                    if a>x and a-x < 10 and abs(b-y)< 10:
                        self.gameover()
                        break
            elif self.keyboard.direction == "up":
                x,y = x,y+1
                if y+10 >self.rangeSnake[3]:
                    self.gameover()
                for a,b in self.snake:
                    if b>y and b-y < 10 and abs(x-a)<10:
                        self.gameover()
                        break
            elif self.keyboard.direction == "down":
                x,y = x,y-1
                if y < self.rangeSnake[1]:
                    self.gameover()
                for a,b in self.snake:
                    if y >b and y-b>10 and abs(x-a)<10:
                        self.gameover()
                        break
            self.snake.append((x,y))
            del self.snake[0]
        for i in self.snake:
            snake = InstructionGroup()
            snake.add(Color(0, 0, 1, 1))
            snake.add(Rectangle(pos=i, size=(10,10)))
            self.canvas.add(snake)
    def gameover(self):
        Clock.unschedule(self.move)
        btn = Button(text="Game is over",size_hint=(1,1),pos_hint={"center_x":.5,"center_y":.5})
        self.add_widget(btn)
        btn.bind(on_release=self.restart )

class Direction(GridLayout):
    def __init__(self, **kwargs):
        super(Direction, self).__init__(**kwargs)
        self.cols = 3
        self.add_widget(Label())
        btnUp = DirectionButton(text="up")
        self.add_widget(btnUp)
        self.add_widget(Label())
        btnLeft = DirectionButton(text="left")
        self.add_widget(btnLeft)
        btnDown = DirectionButton(text="down")
        self.add_widget(btnDown)
        btnRight = DirectionButton(text="right")
        self.add_widget(btnRight)
class DirectionButton(Button):
    def __init__(self, **kwargs):
        super(DirectionButton, self).__init__(**kwargs)

    def on_press(self):
        app = App.get_running_app().root.children[1]
        if self.text == "up":
            if app.keyboard.direction != "down":
                 app.keyboard.direction = "up"
        elif self.text == "down":
            if app.keyboard.direction != "up":
                 app.keyboard.direction = "down"
        elif self.text == "left":
            if app.keyboard.direction != "right":
                 app.keyboard.direction = "left"
        elif self.text == "right":
            if app.keyboard.direction != "left":
                 app.keyboard.direction = "right"




class Options(GridLayout):
    def __init__(self, **kwargs):
        super(Options, self).__init__(**kwargs)
        self.rows = 1
        self.spinner = Spinner(text='Easy',values=('Easy', 'Medium', 'Hard'))
        self.add_widget(self.spinner)
        self.spinner.bind(text=self.show_selected_value)
        startBtn = Button(text = "start")
        self.add_widget(startBtn)
        startBtn.bind(on_release=self.start)
        stopBtn = Button(text = "stop")
        self.add_widget(stopBtn)
        stopBtn.bind(on_press=self.stop)

    def stop(self,*args):
        App.get_running_app().root.children[1].stop()

    def start(self,ins,*args):
        app = App.get_running_app().root.children[1]
        if ins.text == "continue":
            app.continue_move()
        elif ins.text == "start":
            app.start()
            ins.text = "continue"


    def show_selected_value(self, ins,text):
        if text == 'Easy':
            pass
        elif text == 'Medium':
            pass
        elif text == 'Hard':
            pass



if __name__ == "__main__":

    from kivy.uix.boxlayout import BoxLayout

    class Z(App):
        def build(self):
            root = BoxLayout(orientation='vertical')
            root.add_widget(Options(size_hint_y=.5))
            root.add_widget(Main(size_hint_y=7))
            root.add_widget(Direction())
            return root
    Z().run()