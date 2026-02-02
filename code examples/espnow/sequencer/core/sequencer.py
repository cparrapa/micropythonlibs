from time import sleep

class Sequencer:
    def __init__(self):
        self.functions = {}

    def execute(self, program, context=None):
        i = 0
        stack = []
        context = context or {}

        while i < len(program):
            step = program[i]
            cmd = step["cmd"]

            if cmd == "DEF FUNC":
                fname = step["name"]
                body = []
                i += 1
                while program[i]["cmd"] != "END FUNC":
                    body.append(program[i])
                    i += 1
                self.functions[fname] = body

            elif cmd == "CALL FUNC":
                fname = step["name"]
                if fname in self.functions:
                    self.execute(self.functions[fname], context)

            elif cmd == "REPEAT":
                stack.append({"i": i, "times": step.get("times", 2)})

            elif cmd == "END":
                top = stack[-1]
                top["times"] -= 1
                if top["times"] > 0:
                    i = top["i"]
                    continue
                else:
                    stack.pop()

            elif cmd == "WAIT":
                sleep(step.get("time", 1))

            elif cmd == "LED ON":
                print("LED ON")

            elif cmd == "LED OFF":
                print("LED OFF")

            i += 1