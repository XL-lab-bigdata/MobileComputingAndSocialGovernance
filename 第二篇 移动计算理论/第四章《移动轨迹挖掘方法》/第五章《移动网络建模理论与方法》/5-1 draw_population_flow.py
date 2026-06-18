import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap
import random

# 设置随机种子以确保结果可重复
random.seed(42)
np.random.seed(42)

# 设置matplotlib参数以符合科学期刊风格
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial'],
    'font.size': 12,  # 增大基础字体
    'axes.linewidth': 0,
})

# 创建一个新的解决方案：使用两个子图层，一个用于线条，一个用于节点
fig = plt.figure(figsize=(14, 10), dpi=300, facecolor='white')  # 略微增大画布

# 创建两个重叠的轴，底层用于画线，上层用于画节点
ax_edges = plt.axes([0, 0, 1, 1])  # 底层 - 线条
ax_nodes = plt.axes([0, 0, 1, 1], frameon=False)  # 上层 - 节点
ax_edges.set_aspect('equal')
ax_nodes.set_aspect('equal')

# 内置美国各州坐标数据 (经度, 纬度)
state_coords = {
    'AK': (-150, 61), 'AL': (-86.8, 32.8), 'AR': (-92.3, 34.8), 'AZ': (-111.6, 34.3),
    'CA': (-119.4, 36.8), 'CO': (-105.5, 39), 'CT': (-72.7, 41.6), 'DC': (-77, 38.9),
    'DE': (-75.5, 39), 'FL': (-83.6, 28), 'GA': (-83.4, 32.7), 'HI': (-157, 20.7),
    'IA': (-93.5, 42.1), 'ID': (-114, 43.4), 'IL': (-89.3, 40), 'IN': (-86.3, 40),
    'KS': (-98.5, 39), 'KY': (-84.9, 37.7), 'LA': (-91.8, 31), 'MA': (-71.5, 42.3),
    'MD': (-76.7, 39), 'ME': (-69, 45.4), 'MI': (-84.5, 43.4), 'MN': (-95.4, 46),
    'MO': (-92.5, 38.4), 'MS': (-89.8, 32.8), 'MT': (-109.6, 47), 'NC': (-79.8, 35.6),
    'ND': (-100.5, 47.5), 'NE': (-99.8, 41.5), 'NH': (-71.5, 44), 'NJ': (-74.5, 40.2),
    'NM': (-106, 34.4), 'NV': (-117, 39.3), 'NY': (-75.5, 43), 'OH': (-82.8, 40.3),
    'OK': (-97.5, 35.6), 'OR': (-120.5, 43.9), 'PA': (-77.8, 41), 'RI': (-71.5, 41.7),
    'SC': (-81, 33.9), 'SD': (-100, 44.4), 'TN': (-86.5, 35.8), 'TX': (-99, 31),
    'UT': (-111.5, 39.3), 'VA': (-78.8, 37.5), 'VT': (-72.5, 44.2), 'WA': (-120.5, 47.4),
    'WI': (-89.6, 44.3), 'WV': (-80.7, 38.7), 'WY': (-107.3, 43)
}

# 为阿拉斯加和夏威夷调整位置，使其显示在地图上
state_coords['AK'] = (-130, 25)
state_coords['HI'] = (-120, 25)

# 内置各州人口数据（2021估计值，单位：百万）
state_populations = {
    'CA': 39.24, 'TX': 29.53, 'FL': 21.78, 'NY': 19.84, 'PA': 12.97, 'IL': 12.67,
    'OH': 11.71, 'GA': 10.80, 'NC': 10.55, 'MI': 10.03, 'NJ': 9.27, 'VA': 8.64,
    'WA': 7.74, 'AZ': 7.22, 'MA': 6.98, 'TN': 6.97, 'IN': 6.79, 'MO': 6.17,
    'MD': 6.17, 'WI': 5.87, 'CO': 5.81, 'MN': 5.71, 'SC': 5.19, 'AL': 5.04,
    'LA': 4.66, 'KY': 4.51, 'OR': 4.25, 'OK': 4.02, 'CT': 3.61, 'UT': 3.34,
    'IA': 3.19, 'NV': 3.14, 'AR': 3.01, 'MS': 2.96, 'KS': 2.94, 'NM': 2.12,
    'NE': 1.97, 'ID': 1.90, 'WV': 1.79, 'HI': 1.45, 'NH': 1.39, 'ME': 1.37,
    'MT': 1.10, 'RI': 1.09, 'DE': 1.01, 'SD': 0.89, 'ND': 0.77, 'AK': 0.73,
    'VT': 0.65, 'WY': 0.58, 'DC': 0.69
}

# 定义州的相邻关系，用于生成更多真实的迁移流数据
state_neighbors = {
    'AK': [], 'HI': [],
    'WA': ['OR', 'ID'],
    'OR': ['WA', 'ID', 'NV', 'CA'],
    'CA': ['OR', 'NV', 'AZ'],
    'ID': ['WA', 'OR', 'NV', 'UT', 'WY', 'MT'],
    'NV': ['OR', 'ID', 'UT', 'AZ', 'CA'],
    'AZ': ['CA', 'NV', 'UT', 'NM'],
    'UT': ['ID', 'WY', 'CO', 'NM', 'AZ', 'NV'],
    'MT': ['ID', 'WY', 'ND', 'SD'],
    'WY': ['MT', 'SD', 'NE', 'CO', 'UT', 'ID'],
    'CO': ['WY', 'NE', 'KS', 'OK', 'NM', 'UT'],
    'NM': ['AZ', 'UT', 'CO', 'OK', 'TX'],
    'ND': ['MT', 'SD', 'MN'],
    'SD': ['ND', 'MN', 'IA', 'NE', 'WY', 'MT'],
    'NE': ['SD', 'IA', 'MO', 'KS', 'CO', 'WY'],
    'KS': ['NE', 'MO', 'OK', 'CO'],
    'OK': ['KS', 'MO', 'AR', 'TX', 'NM', 'CO'],
    'TX': ['NM', 'OK', 'AR', 'LA'],
    'MN': ['ND', 'SD', 'IA', 'WI'],
    'IA': ['MN', 'WI', 'IL', 'MO', 'NE', 'SD'],
    'MO': ['IA', 'IL', 'KY', 'TN', 'AR', 'OK', 'KS', 'NE'],
    'AR': ['MO', 'TN', 'MS', 'LA', 'TX', 'OK'],
    'LA': ['AR', 'MS', 'TX'],
    'WI': ['MN', 'IA', 'IL', 'MI'],
    'IL': ['WI', 'IA', 'MO', 'KY', 'IN'],
    'IN': ['IL', 'KY', 'OH', 'MI'],
    'MI': ['WI', 'IN', 'OH'],
    'OH': ['MI', 'IN', 'KY', 'WV', 'PA'],
    'KY': ['OH', 'WV', 'VA', 'TN', 'MO', 'IL', 'IN'],
    'TN': ['KY', 'VA', 'NC', 'GA', 'AL', 'MS', 'AR', 'MO'],
    'MS': ['TN', 'AL', 'LA', 'AR'],
    'AL': ['TN', 'GA', 'FL', 'MS'],
    'GA': ['NC', 'SC', 'FL', 'AL', 'TN'],
    'FL': ['GA', 'AL'],
    'SC': ['NC', 'GA'],
    'NC': ['VA', 'SC', 'GA', 'TN'],
    'VA': ['WV', 'MD', 'DC', 'NC', 'TN', 'KY'],
    'WV': ['OH', 'PA', 'MD', 'VA', 'KY'],
    'MD': ['PA', 'DE', 'DC', 'VA', 'WV'],
    'DE': ['PA', 'NJ', 'MD'],
    'PA': ['NY', 'NJ', 'DE', 'MD', 'WV', 'OH'],
    'NJ': ['NY', 'PA', 'DE'],
    'NY': ['VT', 'MA', 'CT', 'NJ', 'PA'],
    'CT': ['NY', 'MA', 'RI'],
    'RI': ['CT', 'MA'],
    'MA': ['NH', 'VT', 'NY', 'CT', 'RI'],
    'VT': ['NH', 'NY', 'MA'],
    'NH': ['ME', 'MA', 'VT'],
    'ME': ['NH'],
    'DC': ['MD', 'VA']
}

# 内置更大规模的人口迁移流动数据（结合IRS迁移数据与合理的低流量迁移扩展）
migration_flows = [
    # 主要迁移流数据（保留原有的高流量路线）
    ('CA', 'TX', 82000), ('NY', 'FL', 63900), ('CA', 'AZ', 59700), ('CA', 'WA', 51000),
    ('CA', 'NV', 47400), ('CA', 'OR', 38100), ('IL', 'FL', 30400), ('NY', 'CA', 30300),
    ('NY', 'NJ', 29700), ('IL', 'TX', 28700), ('MA', 'NH', 26300), ('NJ', 'FL', 26200),
    ('FL', 'TX', 25800), ('TX', 'CA', 25500), ('PA', 'FL', 23900), ('TX', 'FL', 21800),
    ('MI', 'FL', 21300), ('OH', 'FL', 21100), ('PA', 'NJ', 18900), ('OH', 'TX', 18200),
    ('TX', 'CO', 17700), ('VA', 'FL', 17600), ('NY', 'NC', 17500), ('CA', 'TX', 17100),
    ('NY', 'PA', 16900), ('TX', 'OK', 16300), ('CA', 'CO', 16200), ('GA', 'FL', 16100),
    ('IL', 'WI', 15400), ('NJ', 'PA', 15300), ('TX', 'LA', 15200), ('WA', 'CA', 15100),
    ('NY', 'CT', 14700), ('GA', 'TX', 14400), ('MD', 'VA', 14300), ('VA', 'NC', 14300),
    ('NJ', 'NY', 14200), ('NC', 'FL', 14000), ('CO', 'TX', 13900), ('MI', 'TX', 13700),
    ('CA', 'UT', 13600), ('AZ', 'CA', 13500), ('IL', 'IN', 13000), ('OH', 'NC', 12900),
    ('NJ', 'TX', 12700), ('NV', 'CA', 12500), ('PA', 'NY', 12500), ('CO', 'CA', 12300),
    ('IL', 'AZ', 12100), ('CA', 'FL', 12000), ('IN', 'FL', 11900), ('OR', 'WA', 11800),
    ('MO', 'TX', 11600), ('CA', 'TN', 11400), ('WA', 'OR', 11300), ('UT', 'ID', 11100),
    ('WA', 'TX', 11000), ('AL', 'FL', 10800), ('NJ', 'DE', 10700), ('WI', 'FL', 10500),
    ('AR', 'TX', 10400), ('GA', 'NC', 10300), ('NY', 'MA', 10100), ('OK', 'TX', 10000),

    # 中等流量迁移数据
    ('AZ', 'TX', 9800), ('MN', 'FL', 9700), ('TN', 'FL', 9600), ('MO', 'FL', 9500),
    ('IA', 'FL', 9400), ('OH', 'MI', 9300), ('KY', 'TN', 9200), ('CO', 'FL', 9100),
    ('WA', 'ID', 8900), ('CO', 'WA', 8800), ('NY', 'TX', 8700), ('CT', 'NY', 8600),
    ('MA', 'FL', 8500), ('MI', 'OH', 8400), ('CA', 'ID', 8300), ('PA', 'OH', 8200),
    ('IN', 'IL', 8100), ('KY', 'OH', 8000), ('OR', 'CA', 7900), ('NC', 'SC', 7800),
    ('SC', 'NC', 7700), ('TX', 'AZ', 7600), ('NC', 'VA', 7500), ('AL', 'GA', 7400),
    ('GA', 'AL', 7300), ('TN', 'GA', 7200), ('PA', 'MD', 7100), ('CT', 'MA', 7000),
    ('VA', 'MD', 6900), ('NM', 'TX', 6800), ('UT', 'CA', 6700), ('CT', 'FL', 6600),
    ('CA', 'HI', 6500), ('HI', 'CA', 6400), ('NY', 'VA', 6300), ('IL', 'MO', 6200),
    ('MO', 'IL', 6100), ('WA', 'FL', 6000), ('MA', 'NY', 5900), ('CO', 'UT', 5800),
    ('UT', 'CO', 5700), ('NC', 'TX', 5600), ('OH', 'PA', 5500), ('ID', 'WA', 5400),
    ('WA', 'AZ', 5300), ('FL', 'GA', 5200), ('GA', 'TN', 5100), ('IN', 'OH', 5000),
    ('OH', 'IN', 4900), ('WI', 'MN', 4800), ('MN', 'WI', 4700), ('IL', 'MI', 4600),
    ('NY', 'CO', 4500), ('MD', 'FL', 4400), ('IL', 'CA', 4300), ('WI', 'IL', 4200),
    ('IA', 'MN', 4100), ('TX', 'GA', 4000), ('PA', 'NC', 3900), ('AZ', 'CO', 3800),
]

# 为相邻州添加迁移流（确保地理相邻的州之间有数据）
for state, neighbors in state_neighbors.items():
    for neighbor in neighbors:
        # 计算基于人口的合理迁移量 (人口较少地区的迁移数量较少)
        pop_src = state_populations.get(state, 1)
        pop_dst = state_populations.get(neighbor, 1)

        # 计算基本迁移量 - 基于源州和目标州的人口规模
        base_migration = int((pop_src * pop_dst) ** 0.5 * 20)

        # 添加随机变化 (±30%)
        variation = random.uniform(0.7, 1.3)
        migration_value = int(base_migration * variation)

        # 限制最小和最大值
        migration_value = max(300, min(migration_value, 3500))

        # 检查这条边是否已经存在，避免重复
        existing = False
        for src, dst, _ in migration_flows:
            if src == state and dst == neighbor:
                existing = True
                break

        if not existing:
            migration_flows.append((state, neighbor, migration_value))

        # 添加一些远距离低流量迁移，确保网络更加丰富
all_states = list(state_coords.keys())
for _ in range(250):  # 添加250条随机迁移线
    src = random.choice(all_states)
    dst = random.choice(all_states)

    # 避免自环和已有的边
    if src != dst:
        # 检查是否已存在
        existing = False
        for s, d, _ in migration_flows:
            if s == src and d == dst:
                existing = True
                break

        if not existing:
            # 远距离迁移应该更少
            pop_factor = (state_populations.get(src, 1) * state_populations.get(dst, 1)) ** 0.4
            migration_value = int(pop_factor * random.uniform(150, 2000) / 10)
            migration_value = max(100, min(migration_value, 2500))  # 限制值范围
            migration_flows.append((src, dst, migration_value))

        # 创建网络图
G = nx.DiGraph()

# 添加节点（各州）
for state, (lon, lat) in state_coords.items():
    # 减少随机性，使节点更接近真实地理位置
    jitter = np.random.normal(0, 0.2, 2)
    pos = (lon + jitter[0], lat + jitter[1])
    population = state_populations.get(state, 1)
    G.add_node(state, pos=pos, population=population)

# 添加边（州际迁移流）
for source, target, weight in migration_flows:
    if source != target:  # 避免自环
        G.add_edge(source, target, weight=weight)

    # 获取节点位置
pos = nx.get_node_attributes(G, 'pos')

# 更新配色方案 - 更美观的配色
region_colors = {
    'Northeast': '#4a6bab',  # 深蓝色
    'Midwest': '#8a56a9',  # 紫色
    'South': '#d95f4e',  # 红橙色
    'West': '#2b9b81'  # 青绿色
}

# 定义区域颜色
regions = {
    'Northeast': ['CT', 'ME', 'MA', 'NH', 'RI', 'VT', 'NJ', 'NY', 'PA'],
    'Midwest': ['IL', 'IN', 'MI', 'OH', 'WI', 'IA', 'KS', 'MN', 'MO', 'NE', 'ND', 'SD'],
    'South': ['DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA', 'DC', 'WV', 'AL', 'KY', 'MS', 'TN', 'AR', 'LA', 'OK', 'TX'],
    'West': ['AZ', 'CO', 'ID', 'MT', 'NV', 'NM', 'UT', 'WY', 'AK', 'CA', 'HI', 'OR', 'WA']
}

# 为节点分配颜色
node_colors = []
for node in G.nodes():
    color = '#d9d9d9'  # 默认浅灰色
    for region, states in regions.items():
        if node in states:
            color = region_colors[region]
            break
    node_colors.append(color)

# 计算边权重，用于线条粗细
weights = [G[u][v]['weight'] for u, v in G.edges()]
max_weight = max(weights)
min_weight = min(weights)


# 创建更好的权重到宽度的映射函数 - 修改为更大的差异
def width_mapping(weight):
    # 使用幂函数缩放增强差异
    # 调整系数使高权重线条更粗，低权重线条更细
    adjusted_min = max(0.05, min_weight)
    log_weight = np.log10(weight / adjusted_min)
    log_max = np.log10(max_weight / adjusted_min)

    # 增加指数系数，扩大差异
    return 3.5 * (0.08 + 0.92 * (log_weight / log_max) ** 1.3)  # 增加线宽范围和非线性度


# 更优雅的边颜色渐变 - 增强色彩对比
edge_cmap = LinearSegmentedColormap.from_list(
    'edge_colormap',
    [(1.0, 1.0, 1.0, 0.05),  # 极低权重几乎不可见
     (0.85, 0.85, 0.95, 0.2),  # 低权重淡蓝色
     (0.6, 0.6, 0.9, 0.5),  # 中等权重中蓝色
     (0.3, 0.3, 0.8, 0.85)]  # 高权重深蓝色，更高透明度
)

# 按权重升序排列边，小权重的在底层
sorted_edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])

# 设置更大的节点尺寸
node_sizes = []
for node in G.nodes():
    population = G.nodes[node]['population']
    # 增加基础大小以突出节点
    size = 2 * (160 + 80 * np.sqrt(population))  # 大幅增加节点大小
    node_sizes.append(size)

# ===== 关键修改：使用两个子图层分别绘制线条和节点 =====

# 1. 绘制底层图 - 迁移流量线条
for u, v, data in sorted_edges:
    weight = data['weight']
    width = width_mapping(weight)

    # 获取坐标
    x1, y1 = pos[u]
    x2, y2 = pos[v]

    # 距离越远，曲线越平缓
    dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    base_rad = 0.15
    rad = base_rad / (1 + dist / 40)  # 动态调整曲率

    # 为避免平行线重叠，添加轻微随机曲率变化
    rad *= random.uniform(0.7, 1.3)
    if random.random() > 0.5:
        rad = -rad

        # 计算贝塞尔曲线的控制点
    xc = (x1 + x2) / 2 - rad * (y2 - y1)
    yc = (y1 + y2) / 2 + rad * (x2 - x1)

    # 创建曲线路径
    t = np.linspace(0, 1, 100)
    x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * xc + t ** 2 * x2
    y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * yc + t ** 2 * y2

    # 根据权重选择颜色 - 使用对数归一化增强差异
    norm_weight = (np.log10(weight) - np.log10(min_weight)) / (np.log10(max_weight) - np.log10(min_weight))
    edge_color = edge_cmap(norm_weight)

    # 基于迁移量选择线型 (实线/虚线) - 关键修改：增强不同流量的视觉差异
    if weight < 1000:  # 最小流量使用细虚线
        ax_edges.plot(x, y, '--', lw=width, color=edge_color, solid_capstyle='round',
                      dashes=(1, 2), alpha=0.5)
    elif weight < 5000:  # 中等流量使用点划线
        ax_edges.plot(x, y, '-', lw=width, color=edge_color, solid_capstyle='round',
                      alpha=0.65)
    else:  # 高流量使用粗实线
        ax_edges.plot(x, y, '-', lw=width * 1.2, color=edge_color, solid_capstyle='round',
                      alpha=0.9)  # 增加高流量线条的宽度和不透明度

# 2. 切换到上层图 - 绘制节点
# 在上层轴上绘制节点，确保它们显示在线条之上
nx.draw_networkx_nodes(G, pos,
                       node_size=node_sizes,
                       node_color=node_colors,
                       edgecolors='white',
                       linewidths=1.2,  # 增加边框宽度
                       alpha=0.9,
                       ax=ax_nodes)  # 关键：在上层轴上绘制

# 在上层绘制州名标签 - 调整为只显示主要州和更大字体
major_states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI', 'VA', 'WA', 'AZ', 'MA', 'CO']
labels = {state: state for state in G.nodes() if state in major_states}
nx.draw_networkx_labels(G, pos, labels=labels,
                        font_size=12,  # 增大字体
                        font_weight='bold',
                        font_color='black',
                        ax=ax_nodes)  # 关键：在上层轴上绘制

# 去除两个轴的坐标轴和边框
for ax in [ax_edges, ax_nodes]:
    ax.set_axis_off()
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # 输出边的数量，确认数据量
print(f"Total migration flows: {len(G.edges())}")

# 保存高分辨率图像 - 包括SVG格式
plt.tight_layout(pad=0)
plt.savefig('us_migration_network.svg', format='svg', bbox_inches='tight', pad_inches=0)
print("Migration network visualization saved as SVG.")

# 显示图形
plt.show()  