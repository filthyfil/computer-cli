import argparse
import json
import subprocess
from pathlib import Path

from openai import OpenAI

from app.config import config
from app.tools import tools
from app.linter import linter

from rich.console import Console

console = Console()
sandbox = Path(__file__).parent / "sandbox"
sandbox.mkdir(exist_ok=True)

API_KEY = config.API_KEY
BASE_URL = config.BASE_URL
MODEL = config.MODEL

def clean():
    for f in sandbox.iterdir():
        if f.suffix == ".py" and f.is_file():
            f.unlink()

def main():
    parser = argparse.ArgumentParser(prog="computer")
    parser.add_argument("prompt", nargs="+", help="What to ask the computer")

    args = parser.parse_args()
    prompt = " ".join(args.prompt)

    console.print(f"[color(240)]You asked: {prompt}[/color(240)]")

    if not API_KEY:
        raise RuntimeError("API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    system_prompt = """
    You are a computer that answers queries by writing and executing Python scripts.
    Use python3.
    You are already inside a sandbox directory.
    Never use cd. Never change directories.
    Always write files using simple names like a.py, b.py.
    Always execute using: python3 a.py
    Always print the final result using print().
    Combine bash commands when possible.
    Never install packages.
    Prefer sympy for exact math.
    If the query makes no mathematical sense, call the Confusion tool.
    """

    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    while True:
        chat = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools.tools,
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        message = chat.choices[0].message

        if message.tool_calls:
            for tool_call in message.tool_calls:
                console.print(f"[dim][color(240)][{len(messages)}] [/dim][/color(240)]\n")
                console.print(f"[dim][color(240)]TOOL: {tool_call.function.name}({tool_call.function.arguments})[/dim][/color(240)]\n")
        else:
            return

        assistant_msg = {
            "role": "assistant",
            "content": message.content,
        }

        if message.tool_calls:
            assistant_msg["tool_calls"] = [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in message.tool_calls
            ]

        messages.append(assistant_msg)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                args_dict = json.loads(tool_call.function.arguments)

                if tool_call.function.name == "Read":
                    file_path = args_dict["file_path"]
                    with open(sandbox/file_path, 'r') as f:
                        content = f.read()
                    console.print(f"  [dim][color(240)]→ READ {file_path} ({len(content)} chars)[/dim][/color(240)]")

                elif tool_call.function.name == "Write":
                    file_path = args_dict["file_path"]
                    if linter.lint_filepath(file_path):
                        text = args_dict["content"]
                        if linter.lint_write(text):
                            with open(sandbox/file_path, 'w') as f:
                                f.write(text)
                        else:
                            console.print(f"\n\n[yellow]    Potentially unsafe symbols were used by the agent. Terminating.[/yellow]\n\n")
                            return
                    else:
                        console.print(f"\n\n[yellow]    Potentially unsafe symbols were used by the agent. Terminating.[/yellow]\n\n")
                        return
                    content = f"Successfully wrote {len(text)} chars to {file_path}."
                    console.print(f"  [dim][color(240)]→ WRITE {file_path} ({len(text)} chars)[/dim][/color(240)]")

                elif tool_call.function.name == "Bash":
                    command = args_dict["command"]
                    if linter.lint_bash(command):
                        result = subprocess.run(
                            command,
                            shell=True,
                            capture_output=True,
                            text=True,
                            cwd = sandbox
                        )
                        content = json.dumps({
                            "returncode": result.returncode,
                            "stdout": result.stdout,
                            "stderr": result.stderr,
                        })
                        console.print(f"  [dim][color(240)]→ BASH `{command}` (rc={result.returncode})[/dim][/color(240)]")
                    else:
                        console.print(f"\n\n[yellow]    Potentially unsafe symbols were used by the agent. Terminating.[/yellow]\n\n")
                        return
                    if result.stdout:
                        console.print(f"\n\n[bold][color(240)]   STDOUT → {result.stdout.strip()} [/color(240)][/bold]\n\n")
                    if result.stderr:
                        console.print(f"\n\n[bold]   STDERR → {result.stderr.strip()} [/bold]\n\n")
                    if linter.check_python(command):
                        answer = result.stdout.strip()
                        if (answer == ""):
                            answer = "ERROR"
                        console.print(f"\n\n[bold][green]   COMPUTED → {answer}[/green][/bold]\n\n")
                        return

                elif tool_call.function.name == "Confusion":
                    if args_dict["confused"]:
                        console.print(f"\n\n[yellow]    Agent is confused. Terminating.[/yellow]\n\n")
                    return
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": content,
                    }
                )
        else:
            break


if __name__ == "__main__":
    try:
        main()
    finally:
        clean()
