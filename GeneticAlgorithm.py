import random  # 导入随机数模块
import adjust  # 导入调整模块，用于处理交叉路口数据
import crossing  # 导入交叉路口类
import update_data  # 导入更新数据模块，用于更新交叉路口数据
from typing import List  # 导入 List 类型别名，用于类型注解
import concurrent.futures  # 导入线程池模块

class GeneticAlgorithm:
    def __init__(self, population_size, crossover_rate, mutation_rate, gene_type, crossing_list: List[crossing.Crossing]):
        """
        初始化遗传算法对象。

        参数:
        - population_size: 种群大小，表示每一代中个体的数量
        - crossover_rate: 交叉概率，表示进行交叉操作的概率
        - mutation_rate: 变异概率，表示进行变异操作的概率
        - gene_type: 基因类型，表示每个基因的取值范围（例如二进制基因可取值为[0, 1]）
        - crossing_list: 交叉路口对象列表，表示遗传算法需要调整的路口
        """
        self.population_size = population_size  # 设置种群大小
        self.crossover_rate = crossover_rate  # 设置交叉概率
        self.mutation_rate = mutation_rate  # 设置变异概率
        self.gene_type = gene_type  # 设置基因类型
        self.crossing_list = crossing_list  # 设置交叉路口对象列表
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=64)  # 创建线程池执行器

    def initialize_population(self):
        """
        初始化种群，生成随机个体。

        返回:
        - population: 初始种群，包含多个个体的列表
        """
        population = []  # 初始化种群列表
        for _ in range(self.population_size):  # 循环生成指定数量的个体
            individual = self.generate_individual()  # 生成随机个体
            population.append(individual)  # 将个体加入种群列表
        return population  # 返回初始化的种群

    def generate_individual(self):
        """
        生成随机个体。

        返回:
        - individual: 生成的随机个体，即基因序列
        """
        individual = []  # 初始化个体列表
        for _ in range(16 * 4):  # 循环生成基因序列
            temp = random.randint(1, self.gene_type)  # 生成基因值
            individual.append([temp, self.gene_type - temp])  # 将基因值加入个体列表，确保和为 gene_type
        return individual  # 返回生成的个体

    def crossover(self, parent1, parent2):
        """
        交叉操作，生成子代。

        参数:
        - parent1: 父代1，一个个体（基因序列）
        - parent2: 父代2，一个个体（基因序列）

        返回:
        - child1: 子代1，由父代1和父代2交叉得到的新个体
        - child2: 子代2，由父代1和父代2交叉得到的新个体
        """
        num_points = random.randint(1, min(len(parent1), len(parent2)) - 1)  # 随机选择交叉点数量
        crossover_points = sorted(random.sample(range(min(len(parent1), len(parent2))), num_points))  # 随机选择交叉点位置

        child1 = parent1[:]  # 复制父代1作为子代1的初始基因序列
        child2 = parent2[:]  # 复制父代2作为子代2的初始基因序列
        for i in range(0, len(crossover_points), 2):  # 遍历交叉点位置
            start_point = crossover_points[i]  # 获取交叉起始点位置
            end_point = crossover_points[i + 1] if i + 1 < len(crossover_points) else len(parent1)  # 获取交叉终止点位置

            # 交换父代1和父代2之间的基因片段，生成子代1和子代2
            child1[start_point:end_point], child2[start_point:end_point] = child2[start_point:end_point], child1[start_point:end_point]

        self.fix_dna(child1)  # 修复子代1的基因序列
        self.fix_dna(child2)  # 修复子代2的基因序列
        return child1, child2  # 返回生成的子代
    
    def fix_dna(self, dna):
        """
        修复 DNA，确保每个 DNA 和为 gene_type。
        """
        for i in range(len(dna)):  # 遍历基因序列
            dna[i][1] = self.gene_type - dna[i][0]  # 确保每个基因的和为 gene_type

    def mutate(self, individual):
        """
        变异操作，对个体进行基因突变。

        参数:
        - individual: 待变异的个体（基因序列）

        返回:
        - mutated_individual: 变异后的个体（基因序列）
        """
        mutation_point = random.randint(0, len(individual) - 1)  # 随机选择变异点位置
        mutated_individual = individual[:]  # 复制个体作为变异后的个体
        mutated_gene = random.randint(1, self.gene_type)  # 随机生成新的基因值
        mutated_individual[mutation_point] = [mutated_gene, self.gene_type - mutated_gene]  # 在变异点更新基因值
        return mutated_individual  # 返回变异后的个体

    def select_parents(self, population):
        """
        选择父代，根据适应度函数评估选择较优秀的个体作为父代。

        参数:
        - population: 当前种群，包含多个个体的列表

        返回:
        - parents: 选择出的父代，包含多个个体的列表
        """
        fitness_scores = self.evaluate_fitness(population)  # 计算种群中每个个体的适应度评分
        
        # 如果总适应度为零，则平均分配概率，以避免除以零错误
        if sum(fitness_scores) == 0:
            probabilities = [1 / len(population)] * len(population)
        else:
            probabilities = [fitness / sum(fitness_scores) for fitness in fitness_scores]  # 计算每个个体被选择的概率
        
        parents = random.choices(population, weights=probabilities, k=2)  # 根据适应度选择父代
        return parents

    def evaluate_fitness(self, population):
        """
        评估种群中个体的适应度。

        参数:
        - population: 当前种群，包含多个个体的列表

        返回:
        - fitness_scores: 个体适应度评分，一个列表，每个元素对应一个个体的适应度评分
        """
        fitness_scores = [self.fitness_function(individual) for individual in population]  # 计算种群中每个个体的适应度评分
        return fitness_scores  # 返回适应度评分列表

    def evolve(self, population):
        """
        进化过程，包括选择、交叉、变异等操作。

        参数:
        - population: 当前种群，包含多个个体的列表

        返回:
        - new_population: 进化后的新种群，包含多个个体的列表
        """
        new_population = []  # 初始化新种群列表
        while len(new_population) < len(population):  # 循环直到新种群数量达到原种群数量
            parent1, parent2 = self.select_parents(population)  # 选择父代
            if random.random() < self.crossover_rate:  # 根据交叉率决定是否进行交叉操作
                child1, child2 = self.crossover(parent1, parent2)  # 进行交叉操作
            else:
                child1, child2 = parent1[:], parent2[:]  # 若不进行交叉，则子代与父代相同
            if random.random() < self.mutation_rate:  # 根据变异率决定是否进行变异操作
                child1 = self.mutate(child1)  # 进行变异操作
            if random.random() < self.mutation_rate:  # 根据变异率决定是否进行变异操作
                child2 = self.mutate(child2)  # 进行变异操作
            new_population.append(child1)  # 将子代加入新种群
            new_population.append(child2)  # 将子代加入新种群
        return new_population  # 返回进化后的新种群

    def run(self, generations):
        """
        运行遗传算法，进行指定代数的迭代。

        参数:
        - generations: 迭代代数，表示遗传算法将进行的代数

        返回:
        - final_population: 最终种群，经过指定代数的进化后的种群
        """
        
        population = self.initialize_population()  # 初始化种群
        for _ in range(generations):  # 循环进行指定代数的迭代
            population = self.evolve(population)  # 进化种群
        
        return population  # 返回最终种群
    
    def fitness_function(self, individual):
        """
        计算个体的适应度，评估个体在当前情况下的性能。

        参数:
        - individual: 待评估的个体（基因序列）

        返回:
        - fitness_score: 个体的适应度评分
        """
        # 定义评估单个个体的函数
        def evaluate_individual(individual, crossing_list):
            crossing_fitness_function :List[crossing.Crossing] = []  # 初始化交叉路口适应度函数列表
            for i in range(64):  # 遍历交叉路口
                crossing_fitness_function.append(crossing.Crossing(self.crossing_list[i].Number, individual[i]))  # 生成新的路口对象列表
            for _ in range(3):  # 执行交叉路口的模拟
                for j in range(64):
                    crossing_fitness_function[j].crossing_green()  # 更新绿灯状态
                    crossing_fitness_function[j].congestion_coefficient_fun()  # 计算拥堵系数
                update_data.update_data(crossing_fitness_function)  # 更新交叉路口数据
                
            total_congestion = sum(sum(crossing.congestion_coefficient) for crossing in crossing_fitness_function)  # 计算总拥堵指数
            quantity_direction_sum = sum(crossing.Crossing.quantity_direction_copy)  # 计算总流量
            return (quantity_direction_sum - total_congestion) /64  # 计算个体适应度评分，总拥堵指数除以路口数和每个路口的绿灯变化次数

        # 使用多线程并行计算适应度评分
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_individual = {executor.submit(evaluate_individual, individual, self.crossing_list): individual}
            for future in concurrent.futures.as_completed(future_to_individual):
                individual = future_to_individual[future]
                try:
                    fitness_score = future.result()  # 获取个体的适应度评分
                    return fitness_score  # 返回个体的适应度评分
                except Exception as exc:
                    print(f'Individual {individual} generated an exception: {exc}')  # 打印异常信息
