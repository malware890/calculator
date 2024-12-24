import math
import tkinter as tk
from functools import partial

root = tk.Tk()
root.configure(bg="gray")
root.title("Calculator")
root.geometry("320x400")


class Stream:
    def __init__(self):
        self.memory = []
        self.buff = []

    def str_parse(self):
        stream_copy = self.buff.copy()
        for i in range(len(stream_copy) - 1, -1, -1):
            if isinstance(stream_copy[i], str):
                stream_copy[i] = stream_copy[i].replace(" ", "")
                if not stream_copy[i]:
                    stream_copy.pop(i)

        return stream_copy

    def float_parse(self):
        stream_copy = self.str_parse()

        for i in range(len(stream_copy) - 2, -1, -1):
            if isinstance(stream_copy[i], str) and '.' in stream_copy[i]:
                stream_copy[i] = float(stream_copy[i] + str(stream_copy[i + 1]))
                stream_copy.pop(i + 1)
        return stream_copy

    def exp_parse(self):
        stream_copy = self.float_parse()
        for i in range(len(stream_copy) - 1, -1, -1):
            if stream_copy[i] == "%":
                stream_copy[i - 1] *= 0.01
                stream_copy.pop(i)

            elif isinstance(stream_copy[i], str) and "i" in stream_copy[i]:
                num = stream_copy[i][4:len(stream_copy[i]) - 1]
                if '.' in num:
                    stream_copy[i] = round(1 / float(num), 5)
                else:
                    stream_copy[i] = 1 / int(num)

            elif isinstance(stream_copy[i], str) and "^" in stream_copy[i]:
                num = stream_copy[i][:len(stream_copy[i]) - 2]
                if '.' in num:
                    stream_copy[i] = round(float(num) ** 2, 5)
                else:
                    stream_copy[i] = int(num) ** 2

            elif isinstance(stream_copy[i], str) and "s" in stream_copy[i]:
                num = stream_copy[i][5:len(stream_copy[i]) - 1]
                if '.' in num:
                    stream_copy[i] = round(math.sqrt(float(num)), 5)
                else:
                    stream_copy[i] = math.sqrt(int(num))

        return stream_copy

    # FIX FOR PEMDAS
    def eval_parse(self, label: tk.Label):
        stream_copy = self.exp_parse()
        result = stream_copy[0]

        for i in range(1, len(stream_copy), 2):
            if stream_copy[i] == '+':
                result += stream_copy[i + 1]
            elif stream_copy[i] == '-':
                result -= stream_copy[i + 1]
            elif stream_copy[i] == '*':
                result *= stream_copy[i + 1]
            elif stream_copy[i] == '/':
                result /= stream_copy[i + 1]

        result = round(result, 5) if isinstance(result, float) else result
        self.buff = [result]
        label.configure(text=result)
        return result

    def err(self, msg: str):
        self.buff.clear()
        self.buff = msg


for i in range(4):
    root.columnconfigure(i, weight=1)
root.rowconfigure(0, weight=2)
root.rowconfigure(1, weight=3)
for i in range(2, 8):
    root.rowconfigure(i, weight=1)

stream1 = Stream()
stream_frame = tk.Frame(root, bg="gray")
stream_frame.grid(row=1, column=0, columnspan=5, sticky="NESW")
stream_label = tk.Label(stream_frame, bg="white", text=' '.join(stream1.buff))
stream_label.pack(fill="both", expand=True, padx=3, pady=2)


def op(n: str, stream: Stream, label: tk.Label):
    match n:
        case "CE":
            stream.buff.clear()
        case "C":
            stream.buff.clear()
            stream.memory.clear()
        case "DEL":
            stream.buff = stream.buff[:-1]
        case "%":
            stream.buff.append("%")
        case "1/X":
            stream.buff.append(f" inv({stream.buff.pop()})")
        case "X^2":
            stream.buff.append(f" {stream.buff.pop()}^2")
        case "sqrt(X)":
            stream.buff.append(f" sqrt({stream.buff.pop()})")
        case "-X":
            stream.buff.append("-")
        case "+":
            stream.buff.append(" + ")
        case "-":
            stream.buff.append(" - ")
        case "*":
            stream.buff.append(" * ")
        case "/":
            stream.buff.append(" / ")
        case ".":
            stream.buff[-1] = str(stream.buff[-1]) + "."
        case "=":
            stream.eval_parse(stream_label)
        case _:
            if stream.buff and stream.buff[-1] == '-':
                stream.buff[-1] = -int(n)
            elif stream.buff and isinstance(stream.buff[-1], int):
                stream.buff[-1] = stream.buff[-1] * 10 + int(n)
            else:
                stream.buff.append(int(n))

    label.configure(text=str(''.join(map(str, stream.buff))), font=("Arial", 25), anchor='w', padx=5)


buttons = ["%", "CE", "C", "DEL", "1/X", "X^2", "sqrt(X)", "/", "7", "8", "9", "*", "4", "5", "6", "-", "1", "2", '3', "+", "-X", "0", ".", "="]
for r in range(2, 8):
    for c in range(4):
        idx = (r - 2) * 4 + c
        b = tk.Button(root, text=buttons[idx], bg="blue" if idx == len(buttons) - 1 else "white", fg="white" if idx == len(buttons) - 1 else "black",
                      command=partial(op, buttons[idx], stream1, stream_label))
        b.grid(row=r, column=c, sticky="NESW", padx=1, pady=1)
        buttons[idx] = b


root.mainloop()
