import sys

elements = [ 'b', 'c', 'f', 'l','o','s','t','z']
count = 0

def getInput():
    key = sys.stdin.read(1)
    print(key)
    return int(key)
    # display(key)
backStep =0 
def permutations(elements, current_permutation = []):
    global count
    count+=1
    global backStep

    if len(elements) == 0:
        # count+=1
        print('permutation',current_permutation)
        # with open('sampple.txt', 'a') as f:
        #     f.write(f"{current_permutation}\n")
        backStep = input()
        backStep= int(backStep)
        # print(backStep)

    else:
        for i in range(len(elements)):
            # print(backStep)
            if(backStep>0): 
                backStep-=1
                return
            # print(i,elements)
            new_permutation = current_permutation + [elements[i]]
            # print(new_permutation)
            remaining_elements = elements[:i] + elements[i+1:]
            # print(remaining_elements)
            # input()
            permutations(remaining_elements, new_permutation)

permutations(elements)
# print(getInput())
print(count)