from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

class GamePage(BoxLayout):
    def __init__(self, bpm, **kwargs):
        super(GamePage, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        # Left side for the rhythm game
        self.left_layout = BoxLayout(orientation='vertical')
        self.add_widget(self.left_layout)

        # Label to display total score
        self.total_score_label = Label(text='Total Score: 0', size_hint_y=None, height=40)
        self.left_layout.add_widget(self.total_score_label)

        # Label to display score gained from every press
        self.score_gained_label = Label(text='', size_hint_y=None, height=40)
        self.left_layout.add_widget(self.score_gained_label)

        # Button for the user to press
        self.press_button = Button(text='Press in Rhythm!', on_press=self.on_button_press)
        self.left_layout.add_widget(self.press_button)

        # Variables for rhythm game
        self.bpm = bpm  # Define bpm here
        self.beat_count = 0
        self.total_score = 0
        self.last_beat_time = 0  # Time of the last beat
        self.accuracy_score = 10  # Start with full accuracy
        self.miss_penalty = 2  # Set the penalty for missing a beat

        # Audio cue for the beat
        self.beat_sound = SoundLoader.load('beep-03.wav')  # Change the filename accordingly

        # Schedule the beat based on BPM
        self.schedule_beat()

        # Right side for the heartbeat slider
        self.right_layout = BoxLayout(orientation='vertical')
        self.add_widget(self.right_layout)

        # Label to display the current value of the heartbeat slider
        self.heartbeat_label = Label(text='Heartbeat: 50', size_hint_y=None, height=40)
        self.right_layout.add_widget(self.heartbeat_label)

        # Slider for the heartbeat
        self.heartbeat_slider = Slider(min=50, max=200, orientation='vertical', value=50)
        self.heartbeat_slider.bind(value=self.on_heartbeat_slider_change)
        self.right_layout.add_widget(self.heartbeat_slider)

    def schedule_beat(self):
        # Schedule a beat based on BPM
        beat_interval = 60.0 / self.bpm  # Calculate the interval between beats
        Clock.schedule_interval(self.on_beat, beat_interval)

    def on_beat(self, dt):
        # This method is called on each beat
        self.beat_count += 1
        self.last_beat_time = Clock.get_time()  # Update the time of the last beat
        print(f'Beat {self.beat_count}')

        # Play the beat sound
        if self.beat_sound:
            self.beat_sound.play()

    def on_button_press(self, instance):
        # Handle button press
        if self.beat_count > 0:
            # Calculate accuracy score based on the time difference
            time_difference = abs(Clock.get_time() - self.last_beat_time)
            accuracy = max(0, 1 - min(1, time_difference / (60.0 / self.bpm)))

            # Update accuracy score
            self.accuracy_score = max(0, self.accuracy_score - accuracy)

            # Calculate score gained from this press
            heartbeat_multiplier = 0.01 * self.heartbeat_slider.value
            score_gained = int(accuracy * 10 * heartbeat_multiplier)  # Adjust scoring logic

            # Update total score
            self.total_score += score_gained
            self.total_score_label.text = f'Total Score: {self.total_score}'

            # Update score gained label
            self.score_gained_label.text = f'Score Gained: {score_gained}'

    def on_heartbeat_slider_change(self, instance, value):
        # Update the label text when the heartbeat slider value changes
        self.heartbeat_label.text = f'Heartbeat: {int(value)}'

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

class MyApp(App):
    def build(self):
        return MainPage()

if __name__ == '__main__':
    app = MyApp()
    app.run()
