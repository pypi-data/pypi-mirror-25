# ----------------电影赋值----------------

# movies = [
#     "The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91,
#         ["Graham chapman",
#             ["Michael Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]]]
# each_item = movies
# print(each_item)
# print(movies[4][def函数使用][3])
# print(movies)
# for each_item in movies:
#     print(each_item)
# names = ["Michael","Terry"]
# print(names)
# isinstance(names,list)
# num_name = len(names)
# isinstance(num_name,list)
# for each_item in movies:
#     if isinstance(each_item,list):
#         for nested_item in each_item:
#             print(nested_item)
#     else:
#         print(each_item)

# for each_item in movies:
#     if  isinstance(each_item,list):
#         for nested_item in each_item:
#             if  isinstance(nested_item,list):
#                 for deeper_item in nested_item:
#                     print(deeper_item)
#             else:
#                 print(nested_item)
#     else:
#         print(each_item)
#         print(each_item)

# ----------------def函数学习使用（递归）----------------
# def print_lol(the_list):
#     for each_item in the_list:
#         if isinstance(each_item,list):
#             print_lol(each_item)
#         else:
#             print(each_item)

# 导入range使用
import Test01

def print_lol(the_list,level):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
    else:
        for tab_stop in range(level):
                print("\t",end="")
        print(each_item)