import itertools

def generate_permutations(arrays, current_permutation=[], index=0):
    if index == len(arrays):
        yield tuple(current_permutation)
        return

    for element in arrays[index]:
        # Check if the element is already in the current permutation
        if element not in current_permutation:
            # Add the element to the current permutation
            current_permutation.append(element)
            # Recursively generate permutations for the next array
            yield from generate_permutations(arrays, current_permutation, index + 1)
            # Backtrack by removing the last added element
            current_permutation.pop()

def arrayProduct():
    permutations = list(itertools.product(a,b,c,d))

    for perm in permutations:
        # Check if each element in the permutation comes from a different array
        if len(set(perm)) == len(perm):
            print(perm)

# Define the arrays
a = ['a0', 'a1', 'a2', 'a3']
b = ['b0', 'b1', 'b2', 'b3']
c = ['c0', 'c1', 'c2', 'c3']
d = ['d0', 'd1', 'd2', 'd3']

arrays = [a, b, c, d]



# Generate and print permutations
# for permutation in generate_permutations(arrays):
#     print(permutation)

arrayProduct()
