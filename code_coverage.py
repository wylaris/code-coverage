import time


class Function:
    def __init__(self, name, start):
        self.name = name
        self.start = start
        self.end = 1
        self.lines = []
        self.covered = False

    def add_line(self, lineNumb):
        self.lines.append(lineNumb)

    def remove_line(self, lineNumb):
        if lineNumb in self.lines:
            self.lines.remove(lineNumb)

    def set_end(self):
        self.end = self.start + len(self.lines)

    def check_coverage(self):
        if len(self.lines) == 0:
            self.covered = True

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

def get_all_functions(lines):
    functions = {}
    lineNumb = 1
    inFunc = False
    curr = None
    for line in lines:
        if (not line.startswith("#") and "test_" not in line and "main()" not in line and "__main" not in line):
            if "def" in line:
                inFunc = True
                func = Function(line.split("def ")[1].split("(")[0], lineNumb)
                curr = func.name
                functions[curr] = func
            elif line != "" and line != "\n" and inFunc:
                functions[curr].add_line(lineNumb)
            elif inFunc:
                functions[curr].set_end()
                inFunc = False
                curr = None
        lineNumb += 1
    return functions

def print_functions(functions):
    print("\nFunctions found:")
    for func in functions:
        print("  " + func)
    print("\n\n")

def coverage_check(lines,functions):
    inTest = False
    currTest = None
    for line in lines:
        if "def test_" in line:
            inTest = True
            currTest = line.split("def ")[1].split("(")[0]
        elif inTest and "assert" in line:
            localVars = {}
            asserted = functions[line.split("assert ")[1].strip().split("(")[0]]
            rec_traverse_func(asserted, functions, lines, localVars)
            inTest = False
    for func in functions.values():
        func.check_coverage()

def rec_traverse_func(function, functions, lines, localVars):
    skipStatement = False
    returnedVars = []
    for i in range(function.start, function.end):
        line = lines[i]
        if ")" in line and line.split("(")[0].split(" ")[-1] in functions.keys():
            func = functions[line.split("(")[0].split(" ")[-1].strip()]
            vars = line.strip().split("=")[0]
            if isinstance(vars, str):
                vars = [vars]
            localVars = add_returned_vars(localVars, vars, rec_traverse_func(func, functions, lines, localVars))
        elif "=" in line:
            parts = line.strip().split("=")
            localVars[parts[0].strip()] = parts[1].strip()
        elif "if" in line or "elif" in line:
            logic = line.split("if")[1].strip().replace(":", "")
            if logic in localVars.keys():
                if not localVars[logic] == 'True':
                    skipStatement = True
                    continue
                else:
                    skipStatement = False
        elif skipStatement:
            continue
        elif "return " in line:
            var = line.split("return ")[1].strip()
            if var in localVars.keys():
                returnedVars.append(localVars[var])
            else:
                returnedVars.append(var)
            function.remove_line(i + 1)
            break
        function.remove_line(i + 1)
    return returnedVars

def add_returned_vars(dict, vars, list):
    for i in range(0, len(list)):
        dict[vars[i]] = list[i]
    return dict

def print_uncovered(functions):
    covered = []
    uncovered = []
    for func in functions.values():
        if func.covered:
            covered.append(func)
        else:
            uncovered.append(func)
    print("\nFunctions with full coverage:")
    for func in covered:
        print("  " + func.name)
    print("\nFunctions with missing coverage")
    for func in uncovered:
        print("  " + func.name + ". Lines:")
        for line in func.lines:
            print("    " + str(line))



def main():
    start = time.process_time()
    lines = get_lines_from_file("test.py")
    functions = get_all_functions(lines)
    print_functions(functions)
    coverage_check(lines, functions)
    print_uncovered(functions)
    print("Time taken for coverage: " + str(time.process_time() - start) + " seconds")


def get_lines_from_file(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    return lines

if __name__ == "__main__":
    main()
