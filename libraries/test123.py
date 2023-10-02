

sum_list = []
sum_list2 = []

def read_usint_data( input1,input2 , first=True):
    num = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    if input1 <= 255:
        input1 = input1
    if input2 < 256 and input2 != 0:
        for i in range(7):
            if num[i] >= input2:
                if first and input2 >1:
                    a = i-1
                elif num[i-1] < input2 < num[i] and not first:
                    a = i-1
                else:
                    a = i
                remain = input2 - num[a]
                b = 2**(8+a)
                sum_list2.append(b)
                # print(sum_list2)
                if remain == 0:
                    sum_list2.append(remain)
                    print(sum(sum_list2))
                    c = sum(sum_list2,input1)
                    print(c)
                    return c
                else:
                    return read_usint_data(input1,remain,False)
    print(input1)
    return input1

read_usint_data(221,0)