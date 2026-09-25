from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

Window.clearcolor = get_color_from_hex('#000000')


class CalculatorRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.current = '0'
        self.previous = None
        self.operation = None
        self.reset_next = False

        # Дисплей
        self.display = Label(
            text='0',
            font_size='60sp',
            color=(1, 1, 1, 1),
            halign='right',
            valign='bottom',
            size_hint_y=0.25,
        )
        self.display.bind(size=self._update_display_size)
        self.add_widget(self.display)

        # Кнопки
        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['0', '.', '='],
        ]

        for row in buttons:
            row_layout = GridLayout(
                cols=len(row) if row[0] != '0' else 4,
                spacing=8,
                size_hint_y=0.15,
            )
            for text in row:
                btn = Button(
                    text=text,
                    font_size='28sp',
                    background_normal='',
                    background_color=self._button_color(text),
                    color=self._text_color(text),
                )
                if text == '0':
                    btn.size_hint_x = 2
                btn.bind(on_press=self.on_button)
                row_layout.add_widget(btn)
            self.add_widget(row_layout)

    def _update_display_size(self, instance, value):
        instance.text_size = (value[0] - 20, value[1])

    def _button_color(self, text):
        if text in ('AC', '+/-', '%'):
            return get_color_from_hex('#A5A5A5')
        if text in ('÷', '×', '−', '+', '='):
            return get_color_from_hex('#FF9500')
        return get_color_from_hex('#333333')

    def _text_color(self, text):
        if text in ('AC', '+/-', '%'):
            return (0, 0, 0, 1)
        return (1, 1, 1, 1)

    def on_button(self, instance):
        text = instance.text
        if text in '0123456789':
            self._input_digit(text)
        elif text == '.':
            self._input_dot()
        elif text in ('+', '−', '×', '÷'):
            self._set_operation(text)
        elif text == '=':
            self._calculate()
        elif text == 'AC':
            self._clear()
        elif text == '+/-':
            self._toggle_sign()
        elif text == '%':
            self._percent()
        self.display.text = self.current

    def _input_digit(self, d):
        if self.reset_next or self.current == '0':
            self.current = d
            self.reset_next = False
        elif len(self.current) < 12:
            self.current += d

    def _input_dot(self):
        if self.reset_next:
            self.current = '0.'
            self.reset_next = False
        elif '.' not in self.current:
            self.current += '.'

    def _set_operation(self, op):
        if self.operation and not self.reset_next:
            self._calculate()
        try:
            self.previous = float(self.current)
        except ValueError:
            return
        self.operation = op
        self.reset_next = True

    def _calculate(self):
        if self.operation is None or self.previous is None:
            return
        try:
            curr = float(self.current)
        except ValueError:
            return
        try:
            if self.operation == '+':
                result = self.previous + curr
            elif self.operation == '−':
                result = self.previous - curr
            elif self.operation == '×':
                result = self.previous * curr
            elif self.operation == '÷':
                if curr == 0:
                    self.current = 'Ошибка'
                    self.operation = None
                    self.previous = None
                    self.reset_next = True
                    return
                result = self.previous / curr
            self.current = self._fmt(result)
        except Exception:
            self.current = 'Ошибка'
        self.previous = None
        self.operation = None
        self.reset_next = True

    def _clear(self):
        self.current = '0'
        self.previous = None
        self.operation = None
        self.reset_next = False

    def _toggle_sign(self):
        if self.current in ('0', 'Ошибка'):
            return
        if self.current.startswith('-'):
            self.current = self.current[1:]
        else:
            self.current = '-' + self.current

    def _percent(self):
        try:
            self.current = self._fmt(float(self.current) / 100)
        except ValueError:
            pass

    @staticmethod
    def _fmt(num):
        if num == int(num) and abs(num) < 1e15:
            return str(int(num))
        return f'{num:.10g}'


class CalculatorApp(App):
    def build(self):
        self.title = 'Калькулятор'
        return CalculatorRoot()


if __name__ == '__main__':
    CalculatorApp().run()
