from django.shortcuts import render
import subprocess
import sys
import os

GPP_PATH = r"C:\msys64\mingw64\bin\g++.exe"

def code_editor(request):
    return render(request, 'compiler/editor.html')

def run_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        user_input = request.POST.get('input')
        language = request.POST.get('language')

        output = ""
        error = ""

        if language == 'python':
            with open("user_code.py", "w") as f:
                f.write(code)

            try:
                result = subprocess.run(
                    [sys.executable, "user_code.py"],
                    input=user_input.encode(),
                    capture_output=True,
                    timeout=5
                )
                output = result.stdout.decode()
                error = result.stderr.decode()
            except subprocess.TimeoutExpired:
                error = "TLE: Time Limit Exceeded!"

        elif language == 'cpp':
            with open("user_code.cpp", "w") as f:
                f.write(code)

            compile_result = subprocess.run(
                [GPP_PATH, "user_code.cpp", "-o", "user_code.exe"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            compile_stdout = compile_result.stdout.decode()
            compile_stderr = compile_result.stderr.decode()

            print("== COMPILATION STDOUT ==")
            print(compile_stdout)
            print("== COMPILATION STDERR ==")
            print(compile_stderr)
            print("== COMPILATION RETURN CODE ==")
            print(compile_result.returncode)

            if compile_result.returncode != 0:
                error = "Compilation failed:\n" + compile_stderr
            else:
                try:
                    run_result = subprocess.run(
                        ["user_code.exe"],
                        input=user_input.encode(),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=5
                    )
                    output = run_result.stdout.decode()
                    error = run_result.stderr.decode()
                except subprocess.TimeoutExpired:
                    error = "TLE: Time Limit Exceeded!"

        elif language == 'java':
            with open("user_code.java", "w") as f:
                f.write(code)

            # Compile Java code
            compile_result = subprocess.run(
                ["javac", "user_code.java"],
                capture_output=True
            )

            if compile_result.returncode != 0:
                error = compile_result.stderr.decode()
            else:
                try:
                    run_result = subprocess.run(
                        ["java", "user_code"],
                        input=user_input.encode(),
                        capture_output=True,
                        timeout=5
                    )
                    output = run_result.stdout.decode()
                    error = run_result.stderr.decode()
                except subprocess.TimeoutExpired:
                    error = "TLE: Time Limit Exceeded!"



        return render(request, 'compiler/editor.html', {
            'code': code,
            'input': user_input,
            'language': language,
            'output': output,
            'error': error,
        })

    return render(request, 'compiler/editor.html')
