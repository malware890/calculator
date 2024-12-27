import math
import tkinter as tk
from functools import partial


root = tk.Tk()
root.configure(bg="gray")
root.title("Calculator")
root.geometry("320x450")


class Stream:
    def __init__(self):
        self.memory = []
        self.buff = []

    def str_parse(self):
        for i in range(len(self.buff) - 1, -1, -1):
            if isinstance(self.buff[i], str):
                self.buff[i] = self.buff[i].replace(" ", "")
                if not self.buff[i]:
                    self.buff.pop(i)

        return self.buff

    def float_parse(self):
        for i in range(len(self.buff) - 2, -1, -1):
            if isinstance(self.buff[i], str) and '.' in self.buff[i]:
                self.buff[i] = float(self.buff[i] + str(self.buff[i + 1]))
                self.buff.pop(i + 1)

    def exp_parse(self):
        for i in range(len(self.buff) - 1, -1, -1):
            if isinstance(self.buff[i], str) and "i" in self.buff[i]:
                num = self.buff[i][4:len(self.buff[i]) - 1]
                if '.' in num:
                    self.buff[i] = round(1 / float(num), 5)
                else:
                    self.buff[i] = 1 / int(num)

            elif isinstance(self.buff[i], str) and "^" in self.buff[i]:
                num = self.buff[i][:len(self.buff[i]) - 2]
                if '.' in num:
                    self.buff[i] = round(float(num) ** 2, 5)
                else:
                    self.buff[i] = int(num) ** 2

            elif isinstance(self.buff[i], str) and "s" in self.buff[i]:
                num = self.buff[i][5:len(self.buff[i]) - 1]
                if '.' in num:
                    self.buff[i] = round(math.sqrt(float(num)), 5)
                else:
                    self.buff[i] = math.sqrt(int(num))

    @staticmethod
    def mul_div(op1, operation, op2):
        if operation == '*':
            return op1 * op2
        elif operation == '/':
            return op1 / op2

    def compute(self, data: list):
        for i in range(len(data) - 1, -1, -1):
            if data[i] == '$':
                data.pop(i)

        while '*' in data:
            m_idx = data.index('*')
            x = self.mul_div(data.pop(m_idx - 1), data.pop(m_idx - 1), data.pop(m_idx - 1))
            data.insert(m_idx - 1, x)
        while '/' in data:
            m_idx = data.index('/')
            x = self.mul_div(data.pop(m_idx - 1), data.pop(m_idx - 1), data.pop(m_idx - 1))
            data.insert(m_idx - 1, x)

        result = data[0]
        for i in range(1, len(data), 2):
            if data[i] == '+':
                result += data[i + 1]
            elif data[i] == '-':
                result -= data[i + 1]

        result = round(result, 5) if isinstance(result, float) else result
        return result

    def par_parse(self, data: list):
        pairs = dict()
        count = 0.001

        for i in range(len(data)):
            if data[i] == '(':
                pairs[i] = count
                count += 0.001
            elif data[i] == ')':
                count -= 0.001
                for key in pairs.keys():
                    if pairs[key] == count:
                        pairs[key] = i

        for i in range(len(pairs)):
            data[max(pairs)] = '$'
            data[max(pairs) + 1] = self.compute(data[max(pairs) + 1: pairs[max(pairs)]])
            for j in range(max(pairs) + 2, pairs[max(pairs)] + 1):
                data[j] = '$'
            del pairs[max(pairs)]

        return self.compute(data)

    def eval_parse(self, label: tk.Label):
        self.str_parse()
        self.float_parse()
        self.exp_parse()
        result = self.par_parse(self.buff)

        self.buff = [result]
        label.configure(text=result)
        return result


    def err(self, msg: str):
        self.buff.clear()
        self.buff = msg


for i in range(4):
    root.columnconfigure(i, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=2)
for i in range(2, 8):
    root.rowconfigure(i, weight=1)

stream1 = Stream()
stream_frame = tk.Frame(root, bg="gray")
stream_frame.grid(row=1, column=0, columnspan=5, sticky="NESW")
stream_label = tk.Label(stream_frame, bg="white", text=' '.join(stream1.buff))
stream_label.pack(fill="both", expand=True, padx=3, pady=2)


def op(n: str, stream: Stream, label: tk.Label):
    match n:
        case "C":
            stream.buff.clear()
            stream.memory.clear()
        case "DEL":
            stream.buff = stream.buff[:-1]
        case "(":
            stream.buff.append("(")
        case ")":
            stream.buff.append(")")
        case "1/X":
            stream.buff.append(f"inv({stream.buff.pop()})")
        case "X^2":
            stream.buff.append(f"{stream.buff.pop()}^2")
        case "sqrt(X)":
            stream.buff.append(f"sqrt({stream.buff.pop()})")
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


buttons = ["(", ")", "C", "DEL", "1/X", "X^2", "sqrt(X)", "/", "7", "8", "9", "*", "4", "5", "6", "-", "1", "2", '3', "+", "-X", "0", ".", "="]
for r in range(2, 8):
    for c in range(4):
        idx = (r - 2) * 4 + c
        b = tk.Button(root, text=buttons[idx], bg="blue" if idx == len(buttons) - 1 else "white", fg="white" if idx == len(buttons) - 1 else "black",
                      command=partial(op, buttons[idx], stream1, stream_label))
        b.grid(row=r, column=c, sticky="NESW", padx=1, pady=1)
        buttons[idx] = b


option_frame = tk.Frame(root, bg="gray")
option_frame.grid(row=0, column=0, sticky="EW")
for i in range(4):
    option_frame.columnconfigure(i, weight=1)

option_frame.rowconfigure(0, weight=2)
option_frame.rowconfigure(1, weight=3)

option = tk.Button(option_frame, bg="white")
option.grid(row=0, column=0, columnspan=3, sticky="NESW", padx=10, pady=2)

root.mainloop()
