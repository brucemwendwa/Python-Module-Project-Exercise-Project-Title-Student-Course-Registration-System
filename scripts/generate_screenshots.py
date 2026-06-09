import os
import pty
import select
import subprocess
import sys
import tempfile
import textwrap
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


SCENARIOS = [
    (
        "01_add_student.png",
        "Add a student and view students",
        "\n".join(
            [
                "1",
                "S001",
                "Mary Wanjiku",
                "mary@example.com",
                "0711111111",
                "",
                "2",
                "",
                "0",
            ]
        )
        + "\n",
    ),
    (
        "02_add_course.png",
        "Add a course and view courses",
        "\n".join(
            [
                "4",
                "PY101",
                "Python Fundamentals",
                "Mr. Joseph",
                "2",
                "",
                "5",
                "",
                "0",
            ]
        )
        + "\n",
    ),
    (
        "03_register_student.png",
        "Register a student to a course",
        "\n".join(
            [
                "1",
                "S001",
                "Mary Wanjiku",
                "mary@example.com",
                "0711111111",
                "",
                "4",
                "PY101",
                "Python Fundamentals",
                "Mr. Joseph",
                "2",
                "",
                "6",
                "S001",
                "PY101",
                "",
                "7",
                "PY101",
                "",
                "0",
            ]
        )
        + "\n",
    ),
    (
        "04_duplicate_registration.png",
        "Prevent duplicate registration",
        "\n".join(
            [
                "1",
                "S001",
                "Mary Wanjiku",
                "mary@example.com",
                "0711111111",
                "",
                "4",
                "PY101",
                "Python Fundamentals",
                "Mr. Joseph",
                "2",
                "",
                "6",
                "S001",
                "PY101",
                "",
                "6",
                "S001",
                "PY101",
                "",
                "0",
            ]
        )
        + "\n",
    ),
    (
        "05_course_full.png",
        "Prevent registering into a full course",
        "\n".join(
            [
                "4",
                "PY101",
                "Python Fundamentals",
                "Mr. Joseph",
                "1",
                "",
                "1",
                "S001",
                "Mary Wanjiku",
                "mary@example.com",
                "0711111111",
                "",
                "1",
                "S002",
                "John Mwangi",
                "john@example.com",
                "0712222222",
                "",
                "6",
                "S001",
                "PY101",
                "",
                "6",
                "S002",
                "PY101",
                "",
                "0",
            ]
        )
        + "\n",
    ),
]


def run_terminal_session(input_text):
    with tempfile.TemporaryDirectory() as data_dir:
        environment = os.environ.copy()
        environment["SCHOOL_DATA_DIR"] = data_dir
        master_fd, slave_fd = pty.openpty()
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            cwd=PROJECT_ROOT,
            env=environment,
            close_fds=True,
        )
        os.close(slave_fd)

        output_parts = []

        def read_available(timeout):
            while True:
                readable, _, _ = select.select([master_fd], [], [], timeout)
                if not readable:
                    break
                try:
                    chunk = os.read(master_fd, 4096)
                except OSError:
                    break
                if not chunk:
                    break
                output_parts.append(chunk)
                timeout = 0

        for line in input_text.splitlines(keepends=True):
            read_available(0.08)
            os.write(master_fd, line.encode("utf-8"))
            time.sleep(0.03)

        deadline = time.time() + 8
        while process.poll() is None and time.time() < deadline:
            read_available(0.1)

        read_available(0.1)
        os.close(master_fd)

    return b"".join(output_parts).decode("utf-8", errors="replace").replace("\r", "")


def prepare_lines(title, output, width=95, max_lines=54):
    wrapped_lines = [f"$ python3 main.py    # {title}", ""]
    for raw_line in output.splitlines():
        if not raw_line:
            wrapped_lines.append("")
            continue
        wrapped = textwrap.wrap(raw_line.rstrip(), width=width) or [""]
        wrapped_lines.extend(wrapped)

    if len(wrapped_lines) > max_lines:
        wrapped_lines = (
            [wrapped_lines[0], "", "... earlier terminal output omitted ...", ""]
            + wrapped_lines[-max_lines:]
        )
    return wrapped_lines


def render_png(file_name, title, output):
    if Path(FONT_PATH).exists():
        font = ImageFont.truetype(FONT_PATH, 18)
    else:
        font = ImageFont.load_default()
    lines = prepare_lines(title, output)
    line_height = 24
    padding = 28
    width = 1240
    height = padding * 2 + line_height * len(lines)

    image = Image.new("RGB", (width, height), "#111827")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 48), fill="#0f172a")
    draw.text((padding, 15), "Terminal", font=font, fill="#e5e7eb")

    y_position = 62
    for line in lines:
        fill = "#f8fafc"
        if line.startswith("$ "):
            fill = "#93c5fd"
        elif line.startswith("---") or line.startswith("====="):
            fill = "#86efac"
        elif "Error:" in line or "failed" in line.lower():
            fill = "#fca5a5"
        elif "successfully" in line.lower() or "Loaded" in line:
            fill = "#bbf7d0"
        draw.text((padding, y_position), line, font=font, fill=fill)
        y_position += line_height

    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    image.save(SCREENSHOTS_DIR / file_name)


def main():
    for file_name, title, input_text in SCENARIOS:
        output = run_terminal_session(input_text)
        render_png(file_name, title, output)
        print(f"Created screenshots/{file_name}")


if __name__ == "__main__":
    main()
