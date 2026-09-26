from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.config import Config
from kivy.utils import platform
import datetime, json, os

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'resizable', True)
if platform != 'android':
    Window.size = (400, 700)

STORAGE = 'tasks.json'


class AssistantRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.add_widget(Label(
            text='[b]🤖 Мой Помощник[/b]', markup=True,
            font_size='24sp', size_hint_y=0.08
        ))

        self.clock_label = Label(text='', font_size='15sp', size_hint_y=0.07)
        self.add_widget(self.clock_label)
        Clock.schedule_interval(self.update_clock, 1)

        inp = BoxLayout(size_hint_y=0.10, spacing=5)
        self.task_input = TextInput(
            hint_text='Новая задача...', multiline=False, font_size='16sp'
        )
        self.task_input.bind(on_text_validate=self.add_task)
        add_btn = Button(text='➕', size_hint_x=0.22, font_size='20sp',
                         background_color=(0.2, 0.7, 0.3, 1))
        add_btn.bind(on_press=self.add_task)
        inp.add_widget(self.task_input)
        inp.add_widget(add_btn)
        self.add_widget(inp)

        scroll = ScrollView(size_hint=(1, 0.62))
        self.tasks_layout = GridLayout(cols=1, spacing=4,
                                       size_hint_y=None, padding=4)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))
        scroll.add_widget(self.tasks_layout)
        self.add_widget(scroll)

        self.status_label = Label(text='Задач: 0', font_size='13sp',
                                  size_hint_y=0.07, color=(0.3, 0.8, 0.3, 1))
        self.add_widget(self.status_label)

        clr = Button(text='🗑 Очистить всё', size_hint_y=0.09, font_size='14sp',
                     background_color=(0.85, 0.25, 0.25, 1))
        clr.bind(on_press=self.clear_all)
        self.add_widget(clr)

        self.tasks = []
        self.load_tasks()

    def update_clock(self, dt):
        self.clock_label.text = datetime.datetime.now().strftime(
            '📅 %d.%m.%Y  🕐 %H:%M:%S')

    def add_task(self, instance):
        text = self.task_input.text.strip()
        if not text:
            return
        task_box = BoxLayout(size_hint_y=None, height=48, spacing=4)
        d = Button(text='☐', size_hint_x=0.14, font_size='20sp',
                   background_color=(0.5, 0.5, 0.5, 1))
        l = Label(text=text, font_size='15sp', halign='left', valign='middle')
        l.bind(size=lambda s, w: setattr(s, 'text_size', (w[0], None)))
        x = Button(text='✖', size_hint_x=0.14, font_size='18sp',
                   background_color=(0.9, 0.3, 0.3, 1))
        task_box.add_widget(d)
        task_box.add_widget(l)
        task_box.add_widget(x)

        t = {'text': text, 'done': False, 'box': task_box,
             'done_btn': d, 'label': l}
        d.bind(on_press=lambda _: self.toggle_task(t))
        x.bind(on_press=lambda _: self.delete_task(t))

        self.tasks.append(t)
        self.tasks_layout.add_widget(task_box)
        self.task_input.text = ''
        self.update_status()
        self.save_tasks()

    def toggle_task(self, t):
        t['done'] = not t['done']
        if t['done']:
            t['done_btn'].text = '☑'
            t['done_btn'].background_color = (0.2, 0.8, 0.2, 1)
            t['label'].color = (0.6, 0.6, 0.6, 1)
            t['label'].text = '[s]%s[/s]' % t['text']
            t['label'].markup = True
        else:
            t['done_btn'].text = '☐'
            t['done_btn'].background_color = (0.5, 0.5, 0.5, 1)
            t['label'].color = (1, 1, 1, 1)
            t['label'].text = t['text']
            t['label'].markup = False
        self.update_status()
        self.save_tasks()

    def delete_task(self, t):
        self.tasks_layout.remove_widget(t['box'])
        self.tasks.remove(t)
        self.update_status()
        self.save_tasks()

    def clear_all(self, instance):
        self.tasks_layout.clear_widgets()
        self.tasks.clear()
        self.update_status()
        self.save_tasks()

    def update_status(self):
        total = len(self.tasks)
        done = sum(1 for x in self.tasks if x['done'])
        self.status_label.text = '📋 %d  |  ✅ %d' % (total, done)

    def save_tasks(self):
        try:
            with open(STORAGE, 'w', encoding='utf-8') as f:
                json.dump([{'text': t['text'], 'done': t['done']}
                           for t in self.tasks], f, ensure_ascii=False)
        except Exception:
            pass

    def load_tasks(self):
        if not os.path.exists(STORAGE):
            return
        try:
            with open(STORAGE, encoding='utf-8') as f:
                for item in json.load(f):
                    self.task_input.text = item['text']
                    self.add_task(None)
                    if item['done']:
                        self.toggle_task(self.tasks[-1])
        except Exception:
            pass


class AssistantApp(App):
    def build(self):
        self.title = 'Помощник'
        return AssistantRoot()


if __name__ == '__main__':
    AssistantApp().run()
