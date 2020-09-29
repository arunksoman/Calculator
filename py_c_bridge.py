import lupa
from lupa import LuaRuntime
lua = LuaRuntime(unpack_returned_tuples=True)
# lua_code = '''
#     function(num1, num2)
#         return num1 - num2
#     end
# '''
# result = LuaRuntime(unpack_returned_tuples=True).eval(lua_code)
# print(result)

# lua_func = lua.eval('function(f, n) return f(n) end')

# def py_add1(n):
#     return n-1
# result = lua_func(py_add1, 1.2)
# print(result)