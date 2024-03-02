import crossing # 导入crossing模块，定义了交叉路口类
import adjust # 导入adjust模块，用于调整交叉路口数据
from typing import List # 导入typing模块中的List类型别名
Coefficient_list = [[0,1,3],[0,1,2],[1,2,3],[2,3,0]] # 定义一个二维列表，存储每个方向的系数
Coefficient_list2 = [2,1,0] # 定义一个一维列表，存储每个方向的系数
def TF_list(i):
    """
    根据给定的索引i返回对应的列表list1。
    """
    # 定义一个字典，存储 i 和 list1 的对应关系
    dict1 = {0: [-1,-1,4,1],
             1: [-1,0,5,2],
             2: [-1,1,6,3],
             3: [-1,2,7,-1],
             4: [0,-1,8,5],
             7: [3,6,11,-1],
             8: [4,-1,12,9],
             11:[7,6,11,-1],
             12:[8,-1,-1,13],
             13:[9,12,-1,14],
             14:[10,13,-1,15],
             15:[11,14,-1,-1]}
    
    # 使用列表推导式生成 list1 的默认值
    list1 = [i-4,i-1,i+4,i+1]
    
    # 使用字典的 get 方法返回 list1 的值，如果 i 不在字典中，就返回默认值
    return dict1.get(i, list1)
    

def incoming_vehicles_Number(position:int,towards_datadata:list):#计算单个路口
    """
    计算单个路口的进入车辆数量。
    参数：
    - position: 路口位置
    - towards_datadata: 车辆数据列表
    返回值：
    - Increased_quantity: 增加的车辆数量列表
    """
    data = TF_list(position) # 调用TF_list函数，根据路口位置返回一个列表
    Increased_quantity = [] # 定义一个空列表，用于存储增加的车辆数量
    for i in range(4): # 循环4次，即每个路口的方向数
        sun = 0 # 定义一个变量，用于累加车辆数量
        if data[i] >= 0 : # 如果列表中的值大于等于0，表示有车辆进入
            for j in range(3): # 循环3次，即每个方向的车辆数
                sun += towards_datadata[data[i]][Coefficient_list[i][j]][Coefficient_list2[j]] # 根据系数列表，从车辆数据列表中取出相应的值，加到sun上
        Increased_quantity.append(sun) # 将sun的值添加到增加的车辆数量列表中
    return Increased_quantity # 返回增加的车辆数量列表
def update_data(a_list:List[crossing.Crossing]):
    """
    更新数据。
    参数：
    - a_list: Crossing对象列表
    - list_data: 上次车辆走向数据列表
    结果：
    保存在old.txt
    """

    list_data  = ",".join(str(i) for i in crossing.Crossing.quantity_direction)
    Current_data = adjust.adjust_list(list_data) # 调用adjust_list函数，对上次车辆走向数据列表进行处理，返回一个二维列表
    file = open("old.txt","a") # 打开文件old.txt，以追加模式写入
    for i in range(16): # 循环16次，即每个区域的路口数
        temp:List[crossing.Crossing] = a_list[i*4:i*4+4] # 从Crossing对象列表中切片出一个子列表，存储当前区域的四个路口对象
        incoming_list = incoming_vehicles_Number(i,Current_data) # 调用incoming_vehicles_Number函数，传入区域索引和当前车辆数据列表，返回一个增加的车辆数量列表

            
        for j in range (4): # 循环4次，即每个区域的路口数
            if i == 15 and j == 3: # 如果是最后一个区域的最后一个路口
                temp[j].data_preparation(incoming_list[j]) # 调用路口对象的data_preparation方法，传入增加的车辆数量，返回一个字符串，写入文件，并换行
            else : # 如果不是最后一个区域的最后一个路口
                temp[j].data_preparation(incoming_list[j]) # 调用路口对象的data_preparation方法，传入增加的车辆数量，返回一个字符串，写入文件，并用逗号分隔
    file.close() # 关闭文件
    crossing.Crossing.quantity_direction_copy = crossing.Crossing.quantity_direction[:]
    crossing.Crossing.quantity_direction.clear()

def update_data_main(a_list:List[crossing.Crossing]):
    """
    更新数据。
    参数：
    - a_list: Crossing对象列表
    - list_data: 上次车辆走向数据列表
    结果：
    保存在old.txt
    """

    list_data  = ",".join(str(i) for i in crossing.Crossing.quantity_direction)
    Current_data = adjust.adjust_list(list_data) # 调用adjust_list函数，对上次车辆走向数据列表进行处理，返回一个二维列表
    file = open("old.txt","a") # 打开文件old.txt，以追加模式写入
    for i in range(16): # 循环16次，即每个区域的路口数
        temp:List[crossing.Crossing] = a_list[i*4:i*4+4] # 从Crossing对象列表中切片出一个子列表，存储当前区域的四个路口对象
        incoming_list = incoming_vehicles_Number(i,Current_data) # 调用incoming_vehicles_Number函数，传入区域索引和当前车辆数据列表，返回一个增加的车辆数量列表

            
        for j in range (4): # 循环4次，即每个区域的路口数
            if i == 15 and j == 3: # 如果是最后一个区域的最后一个路口
               file.write(temp[j].data_preparation(incoming_list[j])+"\n") # 调用路口对象的data_preparation方法，传入增加的车辆数量，返回一个字符串，写入文件，并换行
            else : # 如果不是最后一个区域的最后一个路口
                file.write(temp[j].data_preparation(incoming_list[j])+",") # 调用路口对象的data_preparation方法，传入增加的车辆数量，返回一个字符串，写入文件，并用逗号分隔
    file.close() # 关闭文件
    crossing.Crossing.quantity_direction_copy = crossing.Crossing.quantity_direction[:]
    crossing.Crossing.quantity_direction.clear()