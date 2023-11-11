from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.slider import Slider
from kivy.properties import NumericProperty
from kivy.core.audio import SoundLoader

class MainPage(BoxLayout):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20

        # Create a label to display the current value
        self.value_label = Label(text='Selected Value: 40', size_hint_y=None, height=40)
        self.add_widget(self.value_label)

        # Create a slider with values ranging from 40 to 180 with increments of 5
        self.slider = Slider(min=40, max=180, step=5, value=40)
        self.slider.bind(value=self.on_slider_value_change)  # Bind the value property to the callback
        self.add_widget(self.slider)

        # Create a "Go" button
        self.go_button = Button(text='Go', on_press=self.on_go_button_press)
        self.add_widget(self.go_button)

    def on_slider_value_change(self, instance, value):
        # Update the label text when the slider value changes
        self.value_label.text = f'Selected Value: {value}'

    def on_go_button_press(self, instance):
        # Handle the "Go" button press
        selected_value = self.slider.value
        print(f'Go button pressed with value: {selected_value}')

        # Open the GamePage with the selected BPM
        app.root.clear_widgets()
        app.root.add_widget(GamePage(bpm=selected_value))


class GamePage(BoxLayout):
    current_bpm = NumericProperty(80)
    beep_sound = SoundLoader.load('beep-03.wav')  # Replace with the actual path

    def __init__(self, bpm, **kwargs):
        super(GamePage, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20

        self.bpm = bpm
        self.beeps_per_minute = 80

        self.bpm_label = Label(text=f'Current BPM: {self.bpm}\nBeeps per Minute: {self.beeps_per_minute}', size_hint_y=None, height=60)
        self.add_widget(self.bpm_label)

        self.bpm_slider = Slider(min=50, max=200, step=5, value=self.current_bpm)
        self.bpm_slider.bind(value=self.on_slider_value_change)
        self.add_widget(self.bpm_slider)

        self.back_button = Button(text='Back', on_press=self.on_back_button_press)
        self.add_widget(self.back_button)

        # Schedule the initial sound playback
        self.schedule_sound()

        # Schedule the periodic update every 10 seconds
        Clock.schedule_interval(self.periodic_update, 10)

    def on_slider_value_change(self, instance, value):
        self.current_bpm = value
        self.bpm_label.text = f'Current BPM: {self.current_bpm}\nBeeps per Minute: {self.beeps_per_minute}'

    def periodic_update(self, dt):
        # Update the beeps per minute every 10 seconds
        self.beeps_per_minute = self.calculate_beeps_per_minute(self.current_bpm)
        self.bpm_label.text = f'Current BPM: {self.current_bpm}\nBeeps per Minute: {self.beeps_per_minute}'

        # Reschedule the sound playback with the new interval
        self.schedule_sound()

    def update(self, dt):
        current_bpm = self.calculate_current_bpm()
        self.beeps_per_minute = self.calculate_beeps_per_minute(current_bpm)
        self.bpm_label.text = f'Current BPM: {current_bpm}\nBeeps per Minute: {self.beeps_per_minute}'

    def calculate_current_bpm(self):
        # Implement how to get the current heart rate here
        # For example, you might use a sensor or simulate it for testing
        # For demonstration purposes, returning a constant value
        return self.current_bpm

    def calculate_beeps_per_minute(self, current_bpm):
        difference = current_bpm - self.bpm

        if difference > 0:
            return max(60, self.beeps_per_minute - (difference // 10) * 5)
        elif difference < 0:
            return min(100, self.beeps_per_minute + (-difference // 10) * 5)
        else:
            return self.beeps_per_minute

    def schedule_sound(self):
        Clock.unschedule(self.play_sound)
        interval = 60 / self.beeps_per_minute if self.beeps_per_minute > 0 else 0
        Clock.schedule_interval(self.play_sound, interval)

    def play_sound(self, dt):
        if self.beep_sound:
            self.beep_sound.volume = 1.0
            self.beep_sound.play()

    def on_back_button_press(self, instance):
        Clock.unschedule(self.play_sound)
        Clock.unschedule(self.periodic_update)  # Unschedule the periodic update
        app.root.clear_widgets()
        app.root.add_widget(MainPage())

# The rest of the code remains unchanged

class MyApp(App):
    def build(self):
        return MainPage()

if __name__ == '__main__':
    app = MyApp()
    app.run()
