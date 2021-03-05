import sys
from malleablec2 import Profile

p = Profile.from_file(
    sys.argv[1] 
    if len(sys.argv) == 2 else 
    "amazon.profile"
)

print("++ Dumping AST\n")
print(p.ast.pretty())

print('-------------------\n')

print("++ Source Reconstructed from AST\n")
print(p) # shortcut for p.reconstruct()