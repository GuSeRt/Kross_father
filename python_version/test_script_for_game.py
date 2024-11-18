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
    """Reads process output until the specified prompt appears."""
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
    """Sends input to the process."""
    proc.stdin.write(f'{text}\n')
    proc.stdin.flush()

def test():
    print("Starting test...")
    try:
        py_cmd = 'python basic_to_python_conversion.py'  

        
        py_proc = process(py_cmd)

        
        py_output = read_until(py_proc, "DO YOU WANT INSTRUCTIONS (YES/NO):")

        
        if "WANT TO HAVE A DEBATE WITH YOUR FATHER, EH??" not in py_output:
            print("Initial output mismatch.")
            print("Python output:")
            print(repr(py_output))  
            return
        else:
            print("Initial output verified. [+] TEST 1 - PASSED")

        
        write_input(py_proc, "NO")

        
        py_output += read_until(py_proc, "WHAT WOULD YOU SAY FIRST (CHOOSE 1-6):")

        
        user_input = '2'
        write_input(py_proc, user_input)

        
        py_output += read_until(py_proc, "YOUR SCORE IS NOW")

        
        if "YOUR SCORE IS NOW" not in py_output:
            print("Score output mismatch.")
            print("Python output:")
            print(repr(py_output))
            return
        else:
            print("Score output verified. [+] TEST 2 - PASSED")

        
        write_input(py_proc, "1")  
        py_output += read_until(py_proc, "WOULD YOU LIKE TO TRY AGAIN (YES/NO):")

        
        if "IT IS NOW SAT. NIGHT, WHICH DO YOU DO?" not in py_output:
            print("Final decision mismatch.")
            print("Python output:")
            print(repr(py_output))
            return
        else:
            print("Final decision verified. [+] TEST 3 - PASSED")

        
        write_input(py_proc, "NO")
        py_proc.communicate()  

        print("All tests passed successfully.")

    except Exception as ex:
        print(f"Test failed with exception: {ex}")

if __name__ == "__main__":
    test()
