import pandas as pd
from pyecharts.charts import Pie 
from pyecharts import options as opts

data = pd.read_excel('data.xlsx')
data.sort_values(by='天数', ascending=False, inplace=True)
province = data['省区市'].values.tolist()
days = data['天数'].values.tolist()
color_series = ['#faeb23', '#e8e517', '#c9db33', '#9fcb3d', '#6bbe45','#37b64b', '#3db979', '#11adcf', '#1f9bca', '#1d8fc6',                '#2d6da4', '#26539e', '#2a3780', '#423787', '#69398d','#7d3a93', '#913986', '#cf208f', '#ea257e', '#eb2462',                '#ee3131', '#f1562f', '#f67932', '#f89230']

pie = Pie(init_opts=opts.InitOpts(width='1350px', height='900px'))
pie.set_colors(color_series)
pie.add('', [z for z in zip(province, days)], radius=['30%', '120%'], center=['50%', '66%'], rosetype='area')
pie.set_global_opts(title_opts=opts.TitleOpts(title='多个省区市\n确诊病例连续多日', subtitle='零新增',                                               title_textstyle_opts=opts.TextStyleOpts(font_size=32, color='#0c2a46', font_family='KaiTi', font_weight='bold'),                                 subtitle_textstyle_opts=opts.TextStyleOpts(font_size=66, color='#0c2a46', font_family='KaiTi', font_weight='bold'),                                               pos_right='center', pos_left='center', pos_top='58%', pos_bottom='center'),                     legend_opts=opts.LegendOpts(is_show=True),                     toolbox_opts=opts.ToolboxOpts(pos_top='5%'))

pie.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='inside', font_size=16, formatter='{b}\n{c}天', font_style='normal', font_weight='bold', font_family='SimHei'))
pie.render('南丁格尔玫瑰图.html')
print("结束")