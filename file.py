from functools import wraps
from tokenize import Number 

def greeter(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        txt = func(*args, **kwargs)
        return "Aloha " + txt.title()
    return inner_func

def count_sum(num_txt):
    num_list = list(num_txt)
    if num_list[0] == "-":
        list_sum = sum(map(int, num_list[1:]))
        list_sum *= -1
    else:
        list_sum = sum(map(int, num_list))
    return list_sum
    
def sums_of_str_elements_are_equal(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        num_to_compare = func(*args, **kwargs)
        num1, num2 = num_to_compare.split()
        element_sum_num1 = count_sum(num1)
        element_sum_num2 = count_sum(num2)
        if element_sum_num1 == element_sum_num2:
            return f"{element_sum_num1} == {element_sum_num2}"
        else:
            return f"{element_sum_num1} != {element_sum_num2}"
    return inner_func


def get_keys(raw_key_list):
    key_list = []
    for el in raw_key_list:
        if "__" in el:
            merged_keys = el.split("__")
            for merged_key in merged_keys:
                key_list.append(merged_key)
        else:
            key_list.append(el)
    print(key_list)
    return key_list
    
    
def get_result_from_dict(dict_to_check, key_to_check):
    try: 
        if dict_to_check[key_to_check] == "":
            return "Empty value"
        else:
            return dict_to_check[key_to_check] 
    except:
        raise ValueError

   
def format_output(*required_keys):
    # ta funkcja ma za zadanie przechwycić argumenty i zwrócić
    # "prawdziwy" dekorator
    def real_decorator(to_be_decorated):
        # Ta funkcja ma za zadanie przechwycić to co zostanie udekorowane.
        def wrapper(*args, **kwargs):
            # args i kwargs to argumenty funkcji dekorowanej
            raw_dict = to_be_decorated(*args, **kwargs)
            new_dict = {}
            for el in required_keys:
                if "__" in el:
                    result_l = []
                    merged_keys = el.split("__")
                    for merged_key in merged_keys:
                        value_from_dict = get_result_from_dict(raw_dict, merged_key)
                        result_l.append(value_from_dict)
                    result = " ".join(result_l)
                    new_dict[el] = result

                else: 
                    result = get_result_from_dict(raw_dict, el) 
                    new_dict[el] = result
                    
            return new_dict
        return wrapper
    return real_decorator


        
def add_method_to_instance(klass):
    def wrapper(to_be_decorated):
        def inner(*args, **kwargs):
            return to_be_decorated()
        setattr(klass, to_be_decorated.__name__, inner)
        return inner
    return wrapper
