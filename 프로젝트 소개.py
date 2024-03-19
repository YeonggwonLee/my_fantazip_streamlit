import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")

st.image("./fantazip_logo.png")

st.markdown("## 나의 판타집이 알려줄게! ➡︎ 서울에서 살기 좋은 동네🏡")
st.markdown("#### 데이터 기반 2030 사회초년생 1인가구가 살기 좋은 동네 찾기")
st.divider()

st.subheader("❓WHAT IS '나의 판타집'?")
# 수정 필요
st.write("**'나의 판타집'** 팀은 멀티캠퍼스 데이터 분석 및 서비스 개발 교육의 파이널 프로젝트를 진행하기 위해 만들어진 팀입니다.")

st.write(" ")
st.write(" ")

st.subheader("❓WHY 살기좋은 동네를 추천?")
st.write("서울에서 자취방을 구할 때, 가장 먼저 내가 감당할 수 있는 금액대를 결정하고 그 후에 \
    지역이나 동네 선택해서 부동산을 찾아가거나 부동산 관련 어플리케이션을 사용하게 됩니다. \
    저희는 이 과정 중 하나는 지역/동네를 결정하는 단계가 정보의 산재로 인해서 굉장히 까다롭다는 생각을 했습니다 \
    그리하여 2030 사회초년생에게 살기 좋은 동네와 관련 데이터를 분석 및 검증하여 필요한 정보를 제공하고자 합니다. ")
st.write(" ")
st.subheader("❓WHY 2030 사회초년생 1인가구")
st.write("결과적으로, 2030 사용자 성향에 맞게 다양한 요인(교통, 문화여가, 치안, 생활편의)을 간단하게 \
    설정하기만 하면 나만의 커스텀 동네를 추천해주고자 하는 서비스를 만들고. \
    더불어, 데이터 분석으로 2030 여성 사회초년생을 위해 안전한 동네에 대한 정보도 추가적으로 제공하고자 합니다. ")


st.write(" ")
st.write(" ")

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 🕵️‍♀️데이터 분석 team🕵️‍♀️")
    data= ({
                        '구성원': ['오유정', '민정윤'],
                        '특징01': ['광주 피플','세종 피플'],
                        '특징02': ['INTP','INFP'],
                        '특징03': ['서울 취뽀 희망','서울 취뽀 희망']
                        })
    df = pd.DataFrame(data)
    st.dataframe(df)
    st.write(f"**< 데이터 분석 목적 >**")
    st.info("✔️ 2030 사회초년생 여성을 위한 안전한 동네 추출하기")
    with st.expander(label=f"**분석 목적 선정 배경**"): 
        st.image("./data/001.png")
        st.image("./data/002.png")
    

with col2:
    st.markdown("#### 🧑‍💻서비스 개발 team🧑‍💻")
    data2= ({
                    '구성원': ['이영권', '김주호'],
                    '특징01': ['수원 피플','서울 피플'],
                    '특징02': ['ISTP','ENTJ'],
                    '특징03': ['서울 취뽀 희망','서울 취뽀 희망']})
    df2 = pd.DataFrame(data2)
    st.dataframe(df2)
    st.write(f"**< 서비스 개발 목적 >**")
    st.info("✔️ 사용자 선호도에 따른 맞춤형 AI 동네 추천 서비스 개발")
    with st.expander(label="**개발 목적 선정 배경**"):
        st.write("주거지를 정할 때 여러 요인을 함께 고려하게 되는데 주변환경을 모두 고려해주는 서비스가 없어서 답답함을 느꼈습니다. 그렇다면 우리가 만들어보면 좋지 않을까? 하는 생각에서 사용자 선호도에 따른 맞춤형 AI 동네 추천 서비스를 개발하게 되었습니다.")
