import os, sys 
import inspect

# make testset directories

# directory variables
root_dir = os.path.dirname(__file__)
class_dir = os.path.join(root_dir, "class")
test_dir = os.path.join(root_dir, "test")

sys.path.append(class_dir)
sys.path.append(test_dir)

# load classes manually
from matrix import Matrix

excep = ['__init__', '__doc__', '__module__', '__repr__',]
test_list = dict() # dictionary for class - list of class attributes

test_list[Matrix] = [func for func in dir(Matrix) if not func in excep]

# auxillary function for creating directory if not exists.
def createdirs(directory):
    if not os.path.exists(directory):
	os.makedirs(directory)

def removedirs(directory):
    if os.path.exists(directory):
	os.remove(directory)

removedirs(os.path.join(root_dir, "grade_total.txt"))
class_list = set([elem.split(".")[0] for elem in os.listdir(class_dir)])


createdirs(os.path.join(root_dir, "test"))

# directory creation for each classes and functions to be tested
for elem in class_list:
    elem_dir = os.path.join(test_dir, elem)
    createdirs(elem_dir)

    for test_class in test_list:
	if test_class.__name__.lower() == elem:
	    print "Creating directory for class " + elem
	    for test_func in test_list[test_class]:
		createdirs(os.path.join(elem_dir, test_func))
		print test_func + " directory created."
	    print elem + " directory creation complete."

# directory creation finished

print "Directoy creation finished. Testing start...."

# testing start

# load parsing function of each class manually 
for elem in os.listdir(test_dir):
    sys.path.append(os.path.join(test_dir, elem))

from matrix_functions import parse_Matrix, write_Matrix, compare_Matrix


# parser, writer, compare function for each class 
test_dict = {
	Matrix : [parse_Matrix, write_Matrix, compare_Matrix],
	}

def testfunc(cls):
    cls_dir = os.path.join(test_dir, cls.__name__.lower())
    # aux functions parse_cls, write_cls, compare_cls
    parse_cls = test_dict[cls][0]
    write_cls = test_dict[cls][1]
    compare_cls = test_dict[cls][2]

    for test_func in os.listdir(cls_dir):
	func_dir = os.path.join(cls_dir, test_func)

	if os.path.isdir(func_dir):
	    if os.listdir(func_dir) == []:
		print func_dir + " is empty." 
	    else:
		resset = []
		print test_func + " test" 
		testset = parse_cls(os.path.join(func_dir, 
		    test_func + "_testset.txt"))
		func = [func[1] for func 
		    in inspect.getmembers(cls) if func[0]==test_func][0]
		if test_func[0] == "_":
		    for idx, mat in enumerate(testset):
			if idx%2:
			    mat1 = mat
			    mat2 = testset[idx-1]
			    resset.append(func(mat1, mat2))	
		else:
		    resset = [func(mat) for mat in testset]
		write_cls(resset, func_dir, test_func + "_res")

		solset = parse_cls(os.path.join(func_dir, 
		    test_func + "_sol.txt"))
		compare_cls(solset, resset, func_dir, test_func)

# actual testing 
for cls in test_list.keys():
    testfunc(cls)




