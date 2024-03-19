import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from math import radians, cos, sin, asin, sqrt
import json
import seaborn as sns
import matplotlib.pyplot as plt
import os
from matplotlib import font_manager as fm
font_path = os.path.join(os.getcwd(), "customFonts", "NanumGothic-Bold.ttf")

# 한글 폰트 설정
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)
plt.rc('axes', unicode_minus=False)  # 마이너스 폰트 설정

# Seaborn 스타일 설정
sns.set(font=font_name))

subway_stations = pd.read_csv('./data/metro_station_final.csv')
pharmacies = pd.read_csv('./data/pharmacy.csv')
bus_stops = pd.read_csv('./data/seoul_bus_stop.csv')
market = pd.read_csv('./data/mart_and_market.csv')
department_store = pd.read_csv("./data/department_store.csv")
shopping_mall = pd.read_csv("./data/shopping_mall.csv")
center_point = pd.read_csv('./data/seoul_town_name_ceneter_point.csv')
park = pd.read_csv('./data/park.csv')
walking_path = pd.read_csv("./data/walking_path.csv")
population_ratio = pd.read_csv("./data/2030_population_ratio.csv")
df_combined = pd.read_csv("./data/total_rent_data.csv")
with open('./data/bjd_region_to_codinate.geojson', 'r') as f:
    geojson_data = json.load(f)
rent_df = pd.read_csv("./data/rent_price_전세.csv")
rent_df = rent_df[rent_df["건물용도"]=="단독다가구"][["town_name","평당평균보증금"]]
rent_df = rent_df.set_index(keys="town_name")
population_ratio = population_ratio.set_index(keys="법정구역")


col4, col5,= st.columns([3, 1])
with col4:
    st.title('🗺️동네 기반 시설 지도 서비스')
with col5:
    st.image("./images/image_logo.png")
st.write("👉**입력하신 동네에 대한 다양한 종합 정보를 확인할 수 있습니다.**")
town_name = st.text_input('동 이름을 입력하세요:')
col1, col2, col3 = st.columns(3)
with col1:
    show_subway = st.checkbox('지하철역')
    show_pharmacies = st.checkbox('약국')
    show_bus_stops = st.checkbox('버스정류장')
    show_market = st.checkbox('대형마트&슈퍼')

with col2:
    show_park = st.checkbox('공원')
    show_department_store = st.checkbox('백화점')
    show_shopping_mall = st.checkbox('쇼핑몰')
    show_walking_path = st.checkbox("산책로")
with col3:
    show_option =  st.selectbox('히트맵 선택',["선택안함","2030 1인가구 비율","2030(여성)_1인가구_비율"
                                                           ,"2030(남성)_1인가구_비율","평당 전세가(만원)"])
    selected_building_type = st.multiselect('건물용도별 전세가 동향:', df_combined['건물용도'].unique())



radius = st.slider('반경을 설정하세요 (km):', min_value=0.1, max_value=5.0, value=1.0, step=0.1)

def town_center_point(town_name, center_point):
    town_center = center_point[center_point['emd_nm'] == town_name]

    if not town_center.empty:
        center_long = town_center['center_long'].values[0]
        center_lat = town_center['center_lati'].values[0]
        return center_lat,center_long
    else:

        return 37.5665,126.9780
  
center_lat, center_long = town_center_point(town_name, center_point)
  

m = folium.Map(location=[center_lat, center_long], zoom_start=14)

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371 
    return c * r


def add_markers(dataframe, category_name, radius, color):
    for index, row in dataframe.iterrows():
        lat, long = row['y'], row['x']
        if haversine(center_long, center_lat, long, lat) <= radius:  # 지정된 반경 이내의 위치에 대해서만
            folium.Marker(
                [lat, long],
                popup=f"{row['name']} ({category_name})",
                icon=folium.Icon(color=color)  # 각 항목별로 다른 색상 지정
            ).add_to(m)
            
def plot_trends(df_combined, selected_dong, building_type_list):
    plt.figure(figsize=(12, 6))
    color_palette = sns.color_palette("hsv", len(building_type_list))

    filtered_data = df_combined[df_combined['전월세구분'] == '전세']
    
    for i, building_type in enumerate(building_type_list):
        specific_data = filtered_data[(filtered_data['건물용도'] == building_type) & (filtered_data['법정동'] == selected_dong)]
        if not specific_data.empty:
            sns.lineplot(data=specific_data, x='접수년도', y='평당평균보증금(만원)', label=f'{selected_dong} - {building_type}', marker='o', linewidth=3, color=color_palette[i])
            for x, y in zip(specific_data['접수년도'], specific_data['평당평균보증금(만원)']):
                plt.text(x, y, f'{y:.0f}', color=color_palette[i], ha='center', va='bottom')

        average_data = filtered_data[filtered_data['건물용도'] == building_type].groupby('접수년도')['평당평균보증금(만원)'].mean().reset_index()
        sns.lineplot(data=average_data, x='접수년도', y='평당평균보증금(만원)', label=f'서울시 평균 - {building_type}', linestyle='--', linewidth=2, color=color_palette[i])

    plt.title(f'{selected_dong} 연도별 평당평균보증금 변화')
    plt.xlabel('접수년도')
    plt.ylabel('평당평균보증금(만원)')
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)

if not town_name:
    st.warning('원하시는 동을 입력하세요!!')
else:
    if selected_building_type: 
        if town_name: 
            plot_trends(df_combined, town_name, selected_building_type)
    else:
        if show_subway:
            add_markers(subway_stations, '지하철역', radius, 'blue')
        if show_pharmacies:
            add_markers(pharmacies, '약국', radius, 'green')
        if show_bus_stops:
            add_markers(bus_stops, '버스정류장', radius, 'red')
        if show_market:
            add_markers(market, '대형마트&슈퍼', radius, 'purple')
        if show_park:
            add_markers(park, '공원', radius, 'darkgreen')
        if show_department_store:
            add_markers(department_store, '백화점', radius, 'orange')
        if show_shopping_mall:
            add_markers(shopping_mall, '쇼핑몰', radius, 'pink')
        if show_walking_path:
            add_markers(walking_path, '산책로', radius, 'darkblue')

        if show_option == "평당 전세가(만원)":
            folium.Choropleth(
                geo_data=geojson_data,
                data=rent_df["평당평균보증금"],
                columns=[rent_df.index, rent_df["평당평균보증금"]],
                fill_color='YlOrRd',
                fill_opacity=0.5,
                line_opacity=0.3,
                threshold_scale=[200, 600, 1000, 1500, 2000, 2500, 3000],
                key_on='feature.properties.EMD_NM'
            ).add_to(m)

        elif show_option == "2030 1인가구 비율":
            data_column = "2030_1인가구_비율"
            folium.Choropleth(
                geo_data=geojson_data,
                data=population_ratio[data_column],
                columns=[population_ratio.index, population_ratio[data_column]],
                fill_color='YlOrRd',
                fill_opacity=0.5,
                line_opacity=0.3,
                key_on='feature.properties.EMD_NM'
            ).add_to(m)

        elif show_option == "2030(여성)_1인가구_비율":
            data_column = "2030(여성)_1인가구_비율"
            folium.Choropleth(
                geo_data=geojson_data,
                data=population_ratio[data_column],
                columns=[population_ratio.index, population_ratio[data_column]],
                fill_color='YlOrRd',
                fill_opacity=0.5,
                line_opacity=0.3,
                key_on='feature.properties.EMD_NM'
            ).add_to(m)

        elif show_option == "2030(남성)_1인가구_비율":
            data_column = "2030(남성)_1인가구_비율"
            folium.Choropleth(
                geo_data=geojson_data,
                data=population_ratio[data_column],
                columns=[population_ratio.index, population_ratio[data_column]],
                fill_color='YlOrRd',
                fill_opacity=0.5,
                line_opacity=0.3,
                key_on='feature.properties.EMD_NM'
            ).add_to(m)

        folium_static(m,width=800, height=550)