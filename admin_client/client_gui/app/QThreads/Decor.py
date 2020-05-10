def Attempt(func):
    try:
        return func
    except Exception as e:
        print(e)
        print("----------")
