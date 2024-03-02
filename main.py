# 导入所需模块和类
import adjust  # 导入调整模块，用于处理交叉路口数据
import time  # 导入时间模块，用于计时
import crossing  # 导入交叉路口类
import update_data  # 导入更新数据模块，用于更新交叉路口数据
from GeneticAlgorithm import GeneticAlgorithm  # 从遗传算法模块中导入遗传算法类
from typing import List  # 导入 List 类型别名，用于类型注解

def updata_main(crossing_list: List[crossing.Crossing], crossingtime_list):
    """
    更新交叉路口对象列表中的交叉时间。

    参数:
    - crossing_list: 交叉路口对象列表，表示需要更新交叉时间的路口
    - crossingtime_list: 包含64个元素的列表，表示交叉时间的列表
    """
    for i in range(64):
        crossing_list[i].crossingtime = crossingtime_list[i]

# 定义遗传算法参数
population_size = 5  # 种群大小
crossover_rate = 0.9  # 交叉概率
mutation_rate = 0.1  # 变异概率
gene_type = 20  # 基因类型
h = 5  # 变异增量
generations = 10  # 进化代数

# 初始化交叉路口对象列表
crossing_list: List[crossing.Crossing] = []

# 打开文件today.txt，读取首次车辆数据
file = open("today.txt", "r")  # 打开文件
main_list_temp = list(file.read().split("\n"))  # 将文件内容按换行符分割，转换为列表
crossing_data_list = adjust.adjust_Crossing(main_list_temp[0])  # 调用adjust_Crossing函数，对第一行数据进行处理，返回一个列表
file.close()  # 关闭文件

# 创建交叉路口对象列表
for i in range(64):
    # 根据交叉路口数据列表中的每一项，创建一个交叉路口对象，并传入初始的绿灯时间，然后将对象添加到交叉路口列表中
    crossing_list.append(crossing.Crossing(crossing_data_list[i], [gene_type - h, h]))

# 初始化计数器和累计器
TF = 1  # 循环计数器
sun = 0  # 拥堵系数累计器
sun_congestion_coefficient = 0  # 拥堵系数累计器
sun_quantity_direction_copy = 0  # 流量累计器
Time = time.time()  # 记录开始时间

# 主循环
while TF < 50:
    # 模拟运行
    for i in range(64):
        crossing_list[i].crossing_green()  # 更新交叉路口的绿灯状态
        crossing_list[i].congestion_coefficient_fun()  # 计算交叉路口的拥堵系数
        sun_congestion_coefficient += sum(crossing_list[i].congestion_coefficient)  # 计算拥堵系数的累加和

    '''关闭/开启优化'''
    # 创建遗传算法对象
    genetic_algorithm = GeneticAlgorithm(population_size, crossover_rate, mutation_rate, gene_type, crossing_list)

    # 运行遗传算法
    final_population = genetic_algorithm.run(generations)

    # 输出最终种群中适应度最高的个体
    best_individual = max(final_population, key=genetic_algorithm.fitness_function)
    crossing.Crossing.quantity_direction = crossing.Crossing.quantity_direction_copy[:]
        
    updata_main(crossing_list, best_individual)  # 更新交叉路口数时间部分
    '''关闭/开启优化'''

    update_data.update_data_main(crossing_list)  # 更新交叉路口数据车辆数据部分
    
    # 更新累计器和计数器
    sun_quantity_direction_copy += sum(crossing.Crossing.quantity_direction_copy)  # 更新流量累计器
    TF += 1  # 计数器自增

# 打印平均拥堵系数和总运行时间
print("平均拥堵系数: ", sun_congestion_coefficient / 50)  # 计算并打印平均拥堵系数
print("time : ", time.time() - Time)  # 打印程序运行的总时间
