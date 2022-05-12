# ******************************************************************
#       /\ /|       @file       run.py
#       \ V/        @brief      
#       | "")       @author     Shadowrabbit, yingtu0401@gmail.com
#       /  |                    
#      /  \\        @Modified   2022/5/12
#    *(__\_\        @Copyright  Copyright (c) 2022, Shadowrabbit
# ******************************************************************
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
import random

# 数据文件
import stat

PATH = "./data.txt"


def run():
    # 数据文件检查
    file_check()
    mode = get_mode()
    # 确定范围
    range_left, range_right = get_range()
    calc_time = get_calc_count()
    for i in range(calc_time):
        log(os.linesep)
        # 生成组
        if mode == 1:
            group1, group2 = generate_group1(range_left, range_right)
        else:
            group1, group2 = generate_group2(range_left, range_right)
        # 前2个最大值组成的数组 1组 2组
        max_group1, max_group2 = top_k(group1, 2), top_k(group2, 2)
        print_result(max_group1, max_group2)
    os.system("pause")


# brief 获取随机数分布模式
# private
def get_mode():
    log("请输入模式")
    log("模式1 纯随机16个数")
    log("模式2 平均分布16个数")
    mode = int(input())
    return mode


# brief 获取范围
# private
def get_range():
    log("请输入范围区间 左")
    range_left = int(input())
    log("请输入范围区间 右")
    range_right = int(input())
    if not isinstance(range_left, int) or not isinstance(range_right, int) or range_left < 0 or range_right < 0:
        log(f"区间范围只接受正整数 [{range_left},{range_right}]")
        return
    if range_left > range_right:
        log(f"左区间不可以大于右区间")
        return
    log(f"当前输入的随机数范围[{range_left},{range_right}]")
    return range_left, range_right


# brief 获取计算次数
# private
def get_calc_count():
    log("请输入计算次数")
    calc_time = int(input())
    if not isinstance(calc_time, int) or calc_time < 0:
        log(f"计算次数必须为正整数 当前{calc_time}")
        return
    log(f"计算次数:{calc_time}")
    return calc_time


# brief 生成组
# private
def generate_group1(range_left, range_right):
    group1 = []
    str_group1 = []
    for i in range(8):
        random_value = get_random_num(range_left, range_right)
        group1.append(random_value)
        str_group1.append(str(random_value))
    group2 = []
    str_group2 = []
    for i in range(8):
        random_value = get_random_num(range_left, range_right)
        group2.append(random_value)
        str_group2.append(str(random_value))
    log(f"group1成员:{str.join(',', str_group1)}")
    log(f"group2成员:{str.join(',', str_group2)}")
    return group1, group2


# brief 生成组 方案2
# private
def generate_group2(range_left, range_right):
    group1 = []
    str_group1 = []
    group2 = []
    str_group2 = []
    for i in range(16):
        random_value = get_random_num(range_left, range_right)
        # 组1满了
        if len(group1) >= 8:
            group2.append(random_value)
            str_group2.append(str(random_value))
            continue
        # 组2满了
        if len(group2) >= 8:
            group1.append(random_value)
            str_group1.append(str(random_value))
            continue
        aver1 = len(group1) != 0 and sum(group1) / len(group1) or 0  # 1组平均值
        aver2 = len(group2) != 0 and sum(group2) / len(group2) or 0
        # 都没满 平均数相同的情况 随机插入
        if aver1 == aver2:
            random.random()
            r = random.randint(0, 1)
            if r == 0:
                group1.append(random_value)
                str_group1.append(str(random_value))
            else:
                group2.append(random_value)
                str_group2.append(str(random_value))
            continue
        # 1组平均数少的情况
        if aver1 < aver2:
            group1.append(random_value)
            str_group1.append(str(random_value))
            continue
        # 2组平均数少的情况
        if aver1 > aver2:
            group2.append(random_value)
            str_group2.append(str(random_value))
    log(f"group1成员:{str.join(',', str_group1)}")
    log(f"group2成员:{str.join(',', str_group2)}")
    return group1, group2


# brief 获取一个范围随机数
# private
def get_random_num(range_left, range_right) -> int:
    random.random()
    r = random.randint(range_left, range_right)
    return r


# brief 获取前N个最大值
# private
def top_k(num_list, n):
    if not num_list:
        log("参数不合法: num_list")
        return
    if n > len(num_list):
        log(f"获取的最大值数量超过数组 获取数量:{n} 数组长度{len(num_list)}")
        return
    pad = min(num_list) - 1  # 最小值填充
    result = []
    for i in range(n):
        result.append(max(num_list))
        max_idx = num_list.index(max(num_list))  # 找最大值索引
        num_list[max_idx] = pad  # 最大值填充
    return result


# brief 获取分数和
# private
def get_total_score(num_list):
    if not num_list:
        return 0
    result = 0
    for i in range(len(num_list)):
        log(f"分数最大值{i + 1}: {num_list[i]}")
        result += num_list[i]
    return result


# brief 打印结果
# private
def print_result(max_group1, max_group2):
    total_score1 = get_total_score(max_group1)
    total_score2 = get_total_score(max_group2)
    log(f"group1 前两个最大分数和total_score1:{total_score1}")
    log(f"group2 前两个最大分数和total_score2:{total_score2}")
    log(f"total_score1-total_score2={total_score1 - total_score2}\ngroup1/group2={(total_score1 / total_score2):.2f}")


# brief 数据文件检测
# private
def file_check():
    # 数据文件存在 清档
    if os.path.exists(PATH):
        os.chmod(PATH, stat.S_IRWXU)
        os.remove(PATH)


# brief 记录日志
# private
def log(value: str):
    print(value)
    data_file = codecs.open(PATH, "a", "utf-8")
    data_file.write(os.linesep)
    data_file.write(value)
    data_file.close()


if __name__ == '__main__':
    run()
