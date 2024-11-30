import random
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock


class ConsoleWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(ConsoleWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Поле для вывода (консоль)
        self.output = TextInput(readonly=True, font_size=14)
        self.add_widget(self.output)

        # Поле для ввода
        self.input = TextInput(multiline=False, font_size=14)
        self.input.bind(on_text_validate=self.on_enter)
        self.add_widget(self.input)

        self.input_disabled = True
        self.input.disabled = True  # Отключаем ввод до тех пор, пока не потребуется
        self.input_buffer = ''
        self.input_callback = None

    def write(self, text):
        # Обновляем вывод в главном потоке
        Clock.schedule_once(lambda dt: self._update_output(text))

    def _update_output(self, text):
        self.output.text += text

    def flush(self):
        pass

    def on_enter(self, instance):
        if not self.input_disabled and self.input_callback:
            self.input_buffer = self.input.text
            self.input.text = ''
            self.input_disabled = True
            self.input.disabled = True
            callback = self.input_callback
            self.input_callback = None
            callback(self.input_buffer)


class DebateGameApp(App):
    def build(self):
        self.console = ConsoleWidget()
        sys.stdout = self.console
        sys.stdin = self
        # Запускаем игру
        Clock.schedule_once(lambda dt: self.run_game())
        return self.console

    def run_game(self):
        # Начинаем генератор основной функции
        self.game_iter = main(self)
        # Выполняем первый шаг
        self.run_next_step(None)

    def run_next_step(self, input_value):
        try:
            # Выполняем до следующего запроса ввода
            prompt = self.game_iter.send(input_value)
            # Если требуется ввод, показываем поле ввода
            self.console.write(prompt)
            self.console.input_disabled = False
            self.console.input.disabled = False
            self.console.input.focus = True
            self.console.input_callback = self.run_next_step
        except StopIteration:
            pass

    def input(self, prompt=''):
        # Этот метод теперь не используется
        pass


def main(app):
    def print_centered(text, width=50):
        app.console.write(text.center(width) + "\n")

    def show_intro():
        print_centered("FATHER")
        print_centered("CREATIVE COMPUTING")
        print_centered("MORRISTOWN, NEW JERSEY")
        app.console.write('\n' * 3)
        app.console.write("WANT TO HAVE A DEBATE WITH YOUR FATHER, EH??\n")

    def show_instructions():
        app.console.write("YOU ARE GOING TO PLAY IN A GAME IN WHICH YOU WILL DISCUSS\n")
        app.console.write("A PROBLEM WITH YOUR FATHER AND ATTEMPT TO GET HIM TO\n")
        app.console.write("AGREE WITH YOU IN THREE TRIES.\n\n")
        app.console.write("FOR EACH STATEMENT YOU MAKE, I WILL TELL YOU WHAT\n")
        app.console.write("YOUR FATHER REPLIED.\n\n")
        app.console.write("YOU MUST SELECT YOUR STATEMENT FROM ONE\n")
        app.console.write("OF THE FOLLOWING SIX.\n")

    def show_statements():
        app.console.write("**********\n")
        app.console.write("1.     O.K. I WILL STAY HOME.\n")
        app.console.write("2.     BUT I'D REALLY LIKE TO GO. ALL MY FRIENDS ARE GOING.\n")
        app.console.write("3.     IF ALL MY WORK IS DONE, I SHOULD BE ABLE TO GO.\n")
        app.console.write("4.     IF YOU LET ME GO OUT I'LL BABYSIT ALL NEXT WEEK\n")
        app.console.write("5.     YOU NEVER LET ME DO WHAT I WANT TO DO.\n")
        app.console.write("6.     I'M GOING ANYWAY!\n")
        app.console.write("**********\n\n")

    def get_valid_input(prompt, valid_range):
        app.console.write(prompt)
        response = yield ''
        while True:
            try:
                value = int(response)
                if value in valid_range:
                    return value
                else:
                    app.console.write("INVALID RESPONSE. PLEASE CHOOSE A NUMBER BETWEEN 1 AND 6.\n")
            except ValueError:
                app.console.write("INVALID INPUT. PLEASE ENTER A NUMBER.\n")
            response = yield ''

    def play_game():
        points = 0
        responses = [
            "NO, YOU CAN'T GO OUT ON A DATE SAT. NITE AND THAT'S THAT.",
            "I DON'T THINK YOU DESERVE TO GO OUT SAT. NITE.",
            "NO, I'M SORRY, BUT YOU REALLY DON'T DESERVE TO GO SAT. NIGHT.",
            "WELL, MAYBE, BUT I DON'T THINK YOU SHOULD GO.",
            "O.K. IF YOU DO THAT YOU CAN GO OUT SAT. NIGHT."
        ]
        points_dict = {1: -1, 2: 2, 3: -1, 4: 2, 5: -1, 6: -2}

        app.console.write(responses[0] + "\n")

        for attempt in range(3):
            response = yield from get_valid_input("WHAT WOULD YOU SAY FIRST (CHOOSE 1-6): ", range(1, 7))
            points += points_dict[response]

            if response == 1:
                app.console.write("AGREEMENT REACHED\n")
                break
            else:
                app.console.write("YOUR FATHER SAID:\n")
                app.console.write(responses[1 if response == 2 else 3] + "\n")
                app.console.write(f"YOUR SCORE IS NOW {points} POINTS.\n")

        app.console.write(f"ON A SCALE OF -7 TO 4, YOUR SCORE WAS {points} POINTS.\n")
        return points

    def final_decision(points):
        app.console.write("IT IS NOW SAT. NIGHT, WHICH DO YOU DO?\n")
        app.console.write("1. GO OUT.\n")
        app.console.write("2. STAY HOME.\n")
        decision = yield from get_valid_input("", [1, 2])

        if decision == 1:
            if random.random() > 0.5:
                app.console.write("YOUR FATHER CHECKED UP ON YOU.\n")
            else:
                app.console.write("YOUR FATHER DIDN'T CHECK UP ON YOU.\n")

        if points >= 2:
            app.console.write("WELL DONE!\n")
        elif points > -4:
            app.console.write("YOU CONVINCED YOUR FATHER BUT IT TOOK TOO MANY TRIES.\n")
        else:
            app.console.write("YOU DIDN'T SUCCEED IN CONVINCING YOUR FATHER.\n")

    show_intro()
    if (yield from get_valid_input("DO YOU WANT INSTRUCTIONS (1=YES, 2=NO): ", [1, 2])) == 1:
        show_instructions()
        show_statements()

    while True:
        score = yield from play_game()
        yield from final_decision(score)
        play_again = yield from get_valid_input("WOULD YOU LIKE TO TRY AGAIN (1=YES, 2=NO): ", [1, 2])
        if play_again == 2:
            break

    app.console.write("THANK YOU FOR PLAYING!\n")
    App.get_running_app().stop()


if __name__ == '__main__':
    DebateGameApp().run()
