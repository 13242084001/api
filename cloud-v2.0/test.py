import functools
def cmp(a,b):
    if a > b:
        return 1
    elif a < b:
        return -1
    else:
        return 0

if __name__ == '__main__':
    nums = [1,3,20,15,0,2,5,7,100,55,66]
    nums.sort(key=functools.cmp_to_key(cmp))
    print(nums)