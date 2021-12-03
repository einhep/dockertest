def funa(fn):
    print("processing funa")
    fn()
    print("after processing funa")
    return "return funca"

@funa
def funb():
    print("processing funb")
    return "return funcb"

if __name__ == '__main__':
    print(funb())