# 加载必要的包  
library(ggplot2)  
library(dplyr)  
library(giscoR)  
library(maps)  

# 获取意大利边界数据  
Italy <- gisco_get_countries(country = "Italy", resolution = 1)  

# 获取并处理城市数据  
data <- world.cities %>%   
  filter(country.etc == "Italy") %>%  
  arrange(pop) %>%  
  mutate(  
    name = factor(name, unique(name)),  
    pop = pop / 1000000  
  )  

# 设置人口分级  
mybreaks <- c(0.05, 0.1, 0.25, 0.5, 1, 2, 5)  

# 创建主要城市间的连接数据  
# 选择人口超过50万的城市  
major_cities <- data %>% filter(pop >= 0.2)  

# 创建城市间连接的数据框  
connections <- expand.grid(  
  city1 = 1:nrow(major_cities),  
  city2 = 1:nrow(major_cities)  
) %>%  
  filter(city1 < city2) %>%  # 避免重复连接  
  mutate(  
    x = major_cities$long[city1],  
    y = major_cities$lat[city1],  
    xend = major_cities$long[city2],  
    yend = major_cities$lat[city2],  
    # 计算连接线权重（基于两端城市的人口乘积）  
    weight = major_cities$pop[city1] * major_cities$pop[city2]  
  )  

# 创建地图  
p <- ggplot() +  
  # 底图层  
  geom_sf(data = Italy, fill = "grey", alpha = 0.3) +  
  
  # 添加城市间连接  
  geom_curve(  
    data = connections,  
    aes(  
      x = x, y = y,  
      xend = xend, yend = yend,  
      alpha = weight,  
      size = weight  
    ),  
    curvature = 0.2,  
    color = "#4B0082",  # 深紫色  
    show.legend = FALSE  
  ) +  
  
  # 城市点图层  
  geom_point(  
    data = data,  
    aes(x = long, y = lat, size = pop, color = pop),  
    shape = 20,  
    alpha = 0.8  
  ) +  
  
  # 设置点大小  
  scale_size_continuous(  
    name = "Population (in Million)",  
    trans = "log",  
    range = c(0.5, 5),  
    breaks = mybreaks  
  ) +  
  
  # 设置连接线透明度和粗细  
  scale_alpha_continuous(  
    range = c(0.1, 0.3)  
  ) +  
  
  # 设置颜色  
  scale_color_viridis_c(  
    option = "plasma",  
    trans = "log",  
    breaks = mybreaks,  
    name = "Population (in Million)"  
  ) +  
  
  # 设置主题  
  theme_void() +  
  
  # 设置图例  
  guides(  
    colour = guide_legend(  
      keyheight = unit(0.8, 'cm'),  
      keywidth = unit(0.8, 'cm'),  
      title.hjust = 0.5,  
      label.theme = element_text(size = 5)  
    )  
  ) +  
  
  # 设置标题  
  ggtitle("The Largest Cities in Italy by Population") +  
  
  # 自定义主题  
  theme(  
    legend.position = c(0.93, 0.77),  
    text = element_text(color = "#22211d"),  
    plot.margin = margin(r = 0.8, l = 0.8, unit = "cm"),   
    plot.background = element_rect(fill = "#f7f7f5", color = NA),  
    panel.background = element_rect(fill = "#f7f7f5", color = NA),  
    plot.title = element_text(size = 16, hjust = 0.5, color = "#4e4d47"),  
    legend.title = element_text(size = 8),  
    legend.text = element_text(size = 7)  
  )  

# 显示地图  
print(p)  

# 保存地图  
ggsave("italy_cities_network.pdf", p, width = 10, height = 12, device = "pdf", bg = "white")