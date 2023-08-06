from typecheck import *
from typing import *

Person = NamedTuple('Person', [('name', str), ('age', int)])

@typecheck
def majority_age(p: Person) -> bool:
    return p.name  # incorrect: typechecker should error out

try:
    majority_age(123)  # incorrect arg type: should error
except Exception as e:
    print(e)

try:
    majority_age(Person('Gerald', 23))  # should give ReturnError above
except Exception as e:
    print(e)

@typecheck
def noop() -> None:
	return

try:
	noop()
except Exception as e:
	print(e)
