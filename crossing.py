from random import randint # 导入随机数模块

class Crossing:
    # 类变量，记录去往其他路口的车辆数量
    
    
    quantity_direction = [] # 一个列表，存储每个方向的通过车辆数
    quantity_direction_copy = [] # 一个列表，复制每个方向的通过车辆数
    
    def __init__(self, Number, crossingtime):
        """
        初始化交叉路口对象。

        参数:
        - Number: 包含三个元素的列表，表示各方向车辆数量
        - crossingtime: 包含两个元素的列表，表示两个方向的交叉时间
        """

        self.Number = Number # 将参数Number赋值给实例变量Number
        self.immutableNumber = Number # 将参数Number赋值给实例变量Number
        
        self.crossingtime = crossingtime # 将参数crossingtime赋值给实例变量crossingtime
        self.congestion_coefficient = [] # 一个列表，存储每个方向的拥堵系数
        self.Number_before_execution = [] # 一个列表，存储执行绿灯控制前的车辆数
        self.quantity_direction_private = [0,0,0]
        self.remittance = 0
        self.capacity = [5,5,5]

    
    def data_preparation(self, incoming_vehicles_Number):
        """
        数据更新函数，随机生成车辆数量并更新交叉路口的车辆数量。

        参数:
        - incoming_vehicles_Number: 进入交叉路口的总车辆数量
        """
        self.remittance = incoming_vehicles_Number
        new_Number = [0,0,0] # 创建一个新的列表，用于存储更新后的车辆数量
        # 生成随机数c，范围在[-10, incoming_vehicles_Number]
        c = randint(-10, incoming_vehicles_Number+10) # 调用randint函数，生成一个整数c
        incoming_vehicles_Number += c # 将c加到incoming_vehicles_Number上，表示实际进入的车辆数量

        # 处理负值情况
        if incoming_vehicles_Number < 0: # 如果incoming_vehicles_Number小于0
            incoming_vehicles_Number = 0 # 将其设为0，表示没有车辆进入

        # 生成随机数a和b，确保a+b <= incoming_vehicles_Number
        a = randint(0, incoming_vehicles_Number) # 调用randint函数，生成一个整数a，表示第一个方向的进入车辆数
        b = randint(0, incoming_vehicles_Number - a) # 调用randint函数，生成一个整数b，表示第二个方向的进入车辆数

        # 更新交叉路口的各方向车辆数量
        new_Number[0] = self.Number[0] + a # 将第一个方向的原有车辆数和进入车辆数相加，赋值给new_Number[0]
        new_Number[1] = self.Number[1] + b # 将第二个方向的原有车辆数和进入车辆数相加，赋值给new_Number[1]
        new_Number[2] = self.Number[2] + incoming_vehicles_Number - a - b # 将第三个方向的原有车辆数和剩余的进入车辆数相加，赋值给new_Number[2]
        self.Number = new_Number[:]
        a = ","
        return a.join(str(i) for i in new_Number) # 返回更新后的车辆数量字符串
    def Single_green(self, SingleNumber,Singletime):
        """
        计算单个方向的绿灯时间通过的车辆数。

        参数:
        - SingleNumber: 单个方向的车辆数量
        - Singletime: 单个方向的绿灯时间
        """
        i = 0 # 初始化一个计数器i，表示通过的车辆数
        while 5 * i - 2 <= Singletime: # 当5 * i - 2小于等于绿灯时间时，表示还有车辆可以通过
            i += 1 # 将计数器i加1，表示多了一辆车通过
        if SingleNumber > i: # 如果车辆数量大于计数器i，表示还有车辆未通过
            return i # 返回计数器i，表示通过的车辆数
        else : # 否则，表示所有车辆都通过了
            return SingleNumber # 返回车辆数量，表示通过的车辆数

    def crossing_green(self):
        """
        交叉路口的绿灯控制函数，更新各方向车辆数量。
        """
        
        self.Number_before_execution = self.Number.copy() # 将实例变量Number的值复制给实例变量Number_before_execution，表示执行绿灯控制前的车辆数
        temp = 0 # 初始化一个临时变量temp，用于存储通过的车辆数
        # 控制前两个方向的绿灯
        for i in range(2): # 循环两次，分别对应前两个方向
            temp = self.Single_green(self.Number[i],self.crossingtime[i]) # 调用Single_green函数，传入第i个方向的车辆数和绿灯时间，返回通过的车辆数，赋值给temp
            self.Number[i] -= temp # 将第i个方向的车辆数减去temp，表示更新后的车辆数
            self.quantity_direction.append(temp) # 将temp添加到实例变量quantity_direction的末尾，表示记录第i个方向的通过车辆数
            self.quantity_direction_private[i] = temp
        # 控制右转
        temp = self.Single_green(self.Number[2],self.crossingtime[0] + self.crossingtime[1] + 3) # 调用Single_green函数，传入第三个方向的车辆数和前两个方向的绿灯时间之和加3，返回通过的车辆数，赋值给temp
        self.Number[2] -= temp # 将第三个方向的车辆数减去temp，表示更新后的车辆数
        self.quantity_direction.append(temp) # 将temp添加到实例变量quantity_direction的末尾，表示记录第三个方向的通过车辆数
        self.quantity_direction_private[2] = temp
  
    def accumulation_speed(self,previous_Number):
        Lane = [0,0,0] # 创建一个新的列表，用于存储每个方向的车辆积累速度
        for i in range(3): # 循环三次，分别对应三个方向
            if sum(self.Number_before_execution) !=  0:
                Lane[i] = (self.Number_before_execution[i] - previous_Number[i])*0.6 # 计算第i个方向的车辆积累速度，公式为(执行前的车辆数-执行后的车辆数)/执行前的总车辆数*0.6，赋值给Lane[i]
            if Lane[i] < 0 : # 如果Lane[i]小于0，表示没有车辆积累
                Lane[i] = 0 # 将其设为0，表示没有车辆积累
        return Lane # 返回车辆积累速度列表
    
    def congestion_coefficient_fun(self):
        # 计算车辆密度
        vehicle_density = [num / capacity for num, capacity in zip(self.Number, self.capacity)]
        # 计算拥堵系数
        self.congestion_coefficient = [max(0, density - 1) for density in vehicle_density]
        # self.congestion_coefficient = self.accumulation_speed(self.Number) # 调用accumulation_speed函数，传入执行后的车辆数，返回车辆积累速度列表，赋值给实例变量congestion_coefficient
        # for i in range(3): # 循环三次，分别对应三个方向
        #     if sum(self.Number) != 0 :
        #         self.congestion_coefficient[i] += self.Number[i]*0.004 # 计算第i个方向的拥堵系数，公式为车辆积累速度+执行后的车辆数/执行后的总车辆数*0.4，赋值给self.congestion_coefficient[i]
        #     if self.congestion_coefficient[i] < 0: # 如果拥堵系数小于0，表示没有拥堵
        #         self.congestion_coefficient[i] = 0 # 将其设为0，表示没有拥堵
        

        
    def time_adjust(self):
        self.congestion_coefficient_fun()
        for i in range(2):
            self.time_adjust_single(i)

    def return_data(self):
        """
        返回交叉路口的统计数据，包括耗时、通过车辆数、剩余车辆数、车辆去向。
        """
        print("耗时:", sum(self.crossingtime)) # 打印耗时，为交叉时间的和
        print("通过车辆数:", sum(self.quantity_direction)) # 打印通过车辆数，为通过车辆数列表的和
        print("剩余车辆数:", self.Number) # 打印剩余车辆数，为执行后的车辆数列表
        print("车辆去向:", self.quantity_direction) # 打印车辆去向，为通过车辆数列表
        print("拥堵系数:", self.congestion_coefficient) # 打印拥堵系数，为拥堵系数列表
