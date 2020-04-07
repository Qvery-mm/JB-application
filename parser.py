import sys

def findLines(filename, _methodName, previousStart):
    methodname = ''.join(_methodName.split('|'))
    start = 0
    end = 0	
    counter = 0
    flag = True
    flag2 = True
    stack = 0
    with open(filename) as source:
        for line in source:
            line = line.lower()
            line = line.replace("{", "\n{")
            line = line.replace("}", "\n}")
            #print(line)
            counter += 1
            if flag and line.find(methodname) >= 0 and previousStart < counter:
                j = line.find(methodname)
                if not line[j-1] == ' ' or line[j-3] == ' ' or not ( line[j-2] in '_$]*>' or line[j-2].isalnum()):
                    continue
                try:
                    #print(line[j - 6:j - 1])
                    if(line[j - 6:j - 1] == 'class'):
                        continue
                except Exception:
                    continue
                flag = False
                start = counter
                for i in range(j, len(line)):
                    if line[i] == '{':
                        flag2 = False
                        stack += 1
                        #print('stack~~~~~', stack)
                    elif line[i] == '}':
                        stack -= 1
                        #print('stack~~~~~', stack)
                    if not flag2 and stack == 0:
                        end = counter
                        return (start, end)
                continue
            if not flag:
                for i in range(len(line)):
                    if line[i] == '{':
                        flag2 = False
                        stack += 1
                        #print('stack~~~~~', stack)
                    elif line[i] == '}':
                        stack -= 1
                        #print('stack~~~~~', stack)
                    if not flag2 and stack == 0:
                        end = counter
                        return (start, end)
        return (start, end)


if __name__ == "__main__":
    print(findLines("Input.java", "f"))

