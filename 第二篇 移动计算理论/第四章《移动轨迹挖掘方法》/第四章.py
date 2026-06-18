import pandas as pd
from skmob import TrajDataFrame
from skmob.preprocessing import detection
from skmob.measures.individual import distance_straight_line, maximum_distance, radius_of_gyration
from skmob.measures.individual import random_entropy, real_entropy, uncorrelated_entropy
from skmob.measures.collective import visits_per_time_unit

# 读取Geolife样例数据
data = pd.read_csv('Geolife Trajectories 1.3/Data/000/Trajectory/20081023025304.plt', skiprows=6, names=['Latitude', 'Longitude', 'Zeros', 'Altitude', 'Date-time', 'Date', 'Time'])
# 转换为TrajDataFrame
tdf = TrajDataFrame(data,timestamp=True, latitude='Latitude',longitude='Longitude', datetime='Date-time', user_id='user_000')
print(tdf)

# 轨迹直线距离和路径距离计算
start_point = tdf.iloc[0][['lat', 'lng']]
end_point = tdf.iloc[-1][['lat', 'lng']]
straight_line_dist = distance_straight_line(tdf)
print(f"直线距离: {straight_line_dist} km")
route_dist = maximum_distance(tdf)
print(f"路径距离: {straight_line_dist} km")

# （相对于质心的）活动半径计算
rog = radius_of_gyration(tdf)
print(f"活动半径: {rog} km")


# 随机熵、真实熵、时间无关熵计算
rand_ent = random_entropy(tdf)
real_ent = real_entropy(tdf)
uncorr_ent = uncorrelated_entropy(tdf)
print(f"随机熵: {rand_ent}")
print(f"真实熵: {real_ent}")
print(f"时间无关熵: {uncorr_ent}")