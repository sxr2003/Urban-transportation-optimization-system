def data_processing(data):
    data3 = []
    data4 = []
    data2 = list(map(int,str(data).split(","))) # 将数据转换为字符串，按逗号分割，再转换为整数列表
    for i in range(0,len(data2)-2,3): # 从0开始，每隔3个元素，循环到倒数第三个元素
        data3.append(data2[i:i+3]) # 将列表中的三个元素切片出来，作为一个子列表，添加到data3中
    for i in range(0,len(data3)-3,4): # 从0开始，每隔4个元素，循环到倒数第四个元素
        data4.append(data3[i:i+4]) # 将列表中的四个元素切片出来，作为一个子列表，添加到data4中
    # print(data)
    #print(len(data4))
    return data4 # 返回data4，是一个二维列表

def adjust_Crossing(list_data:list):
    list_return = []
    data = list(map(int,str(list_data).split(","))) # 将数据转换为字符串，按逗号分割，再转换为整数列表
    for i in range(0,len(data)-2,3): # 从0开始，每隔3个元素，循环到倒数第三个元素
        list_return.append(data[i:i+3]) # 将列表中的三个元素切片出来，作为一个子列表，添加到list_return中
    return list_return # 返回list_return，是一个二维列表

def adjust_old(time):
    file = open("old.txt","r") # 打开文件old.txt，以读取模式
    list_data = list(file.read().split("\n")) # 读取文件内容，按换行符分割，转换为列表
    file.close() # 关闭文件
    return data_processing(list_data[time]) # 调用data_processing函数，传入列表中的第time个元素，返回一个二维列表

def adjust_today(time):
    file = open("today.txt","r") # 打开文件today.txt，以读取模式
    list_data = list(file.read().split("\n")) # 读取文件内容，按换行符分割，转换为列表
    file.close() # 关闭文件
    print(data_processing(list_data[time])) # 调用data_processing函数，传入列表中的第time个元素，打印一个二维列表
    
def adjust_list(list_data:list):
    return data_processing(list_data) # 调用data_processing函数，传入列表，返回一个二维列表

def adjust_Crossing_time(list_data:list,num:int):
    temp = []
    for i in range(16*4):
        temp.append([list_data[i],num-list_data[i]])
    return  temp # 调用data_processing函数，传入列表，返回一个二维列表
