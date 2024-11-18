import subprocess
import time
import sys

def process(command):
    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )

def read_until(proc, prompt):
    """Читает вывод процесса до появления указанного приглашения."""
    output = ''
    while True:
        char = proc.stdout.read(1)
        if not char:
            break
        output += char
        if output.endswith(prompt):
            break
    return output

def write_input(proc, text):
    """Отправляет ввод в процесс."""
    proc.stdin.write(f'{text}\n')
    proc.stdin.flush()

def test():
    print("Starting test...")
    try:
        # Команда для запуска игры на Python
        py_cmd = 'python basic_to_python_conversion.py'  # Убедитесь, что путь корректен
        # Запуск процесса
        py_proc = process(py_cmd)

        # Чтение начального вывода игры
        py_output = read_until(py_proc, "DO YOU WANT INSTRUCTIONS (YES/NO):")
        
        # Проверка начального вывода
        if "WANT TO HAVE A DEBATE WITH YOUR FATHER, EH??" not in py_output:
            print("Начальный вывод не совпадает.")
            print("Вывод Python игры:")
            print(repr(py_output))  # Печать с учётом специальных символов
            return
        else:
            print("Начальный вывод проверен. [+] ТЕСТ 1 - ПРОШЕЛ")

        # Ответ "NO" для пропуска инструкций
        write_input(py_proc, "NO")
        
        # Чтение до следующего приглашения
        py_output += read_until(py_proc, "WHAT WOULD YOU SAY FIRST (CHOOSE 1-6):")
        
        # Выбор варианта ответа (например, вариант 2)
        user_input = '2'
        write_input(py_proc, user_input)
        
        # Чтение до вывода счета
        py_output += read_until(py_proc, "YOUR SCORE IS NOW")
        
        # Проверка вывода счета
        if "YOUR SCORE IS NOW" not in py_output:
            print("Вывод счета не совпадает.")
            print("Вывод Python игры:")
            print(repr(py_output))
            return
        else:
            print("Вывод счета проверен. [+] ТЕСТ 2 - ПРОШЕЛ")

        # Ответ "1" или "2" для окончательного решения
        write_input(py_proc, "1")  # Предполагаем, что "1" означает "пойти гулять"
        
        # Чтение до следующего приглашения
        py_output += read_until(py_proc, "WOULD YOU LIKE TO TRY AGAIN (YES/NO):")
        
        # Финальная проверка
        if "IT IS NOW SAT. NIGHT, WHICH DO YOU DO?" not in py_output:
            print("Финальное решение не совпадает.")
            print("Вывод Python игры:")
            print(repr(py_output))
            return
        else:
            print("Финальное решение проверено. [+] ТЕСТ 3 - ПРОШЕЛ")

        # Ответ "NO" для завершения игры
        write_input(py_proc, "NO")
        
        # Завершение процесса
        py_proc.communicate()  # Ожидаем завершения процесса
        print("Все тесты прошли успешно.")

    except Exception as ex:
        print(f"Тест не прошел из-за исключения: {ex}")

if __name__ == "__main__":
    test()
