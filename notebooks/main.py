
from data_analysis import MyClass
from module2 import my_function

# Now you can use the imported classes and functions
if __name__ == "__main__":
    # Create an instance of MyClass and call its method
    my_class_instance = MyClass()
    my_class_instance.my_method()

    # Call the function from module2
    my_function()