from tkinter import*

import kivy
from kivy.app import App
from kivy.uix.behaviors import button
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class Cell:
    
    def __init__(self, value, hidden):
        self.value = value
        self.hidden = hidden
    
    def representation(self):
        if self.hidden == True:
            return " "
        elif self.hidden == False:
            return self.value
        else:
            return "error"

testCell = Cell("2", False)

print("testprint")
print(testCell.representation())
print(Cell.representation(testCell))

class Grid(GridLayout):
    
    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        self.cols = 10
        for i in range(0,100):
            self.button=Button()
            self.button(on_press=self.press)
            self.add_widget(self.button)

    def press(self, instance):
        self.button=self.Button(text="P")

class MinesweeperApp(App):
    def build(self):
        #return Label(text="Hello, Arvid!")
        #return Button(text="Testbutton",size_hint=(0.1,0.1))
        return Grid()

if __name__ == "__main__":
    MinesweeperApp().run()

#print(help(App))