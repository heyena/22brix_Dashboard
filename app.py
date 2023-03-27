import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import cv2
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import plotly.graph_objects as go
import io 


st.set_page_config(page_title="22Brix Dashboard")

with st.sidebar:
    choose = option_menu("22Brix Dashboard", ["광고비/광고 매출 추이", "Funnel별 성과", "광고 상품별 성과", "파워링크 성과", "파워링크 키워드 Top"],
                         icons=['coin','funnel','clipboard-data','bar-chart', 'list-ol'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#282b30"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#424549"},
    }
    )

hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
      
hide_table_row_index = """
               <style>
               thead tr th:first-child {display:none}
               tbody th {display:none}
               </style>
               """
# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
st.markdown(hide_table_row_index, unsafe_allow_html=True)


# 데이터셋 Read 
df_sheet0 = pd.read_excel("Dataset.xlsx", sheet_name=0)
df_sheet1 = pd.read_excel("Dataset.xlsx", sheet_name=1)
df_sheet2 = pd.read_excel("Dataset.xlsx", sheet_name=2)
df_sheet3 = pd.read_excel("Dataset.xlsx", sheet_name=3)
df_Revenue_keyword = pd.read_excel("Dataset.xlsx", sheet_name="매출상위_키워드")
df_Impression_keyword = pd.read_excel("Dataset.xlsx", sheet_name="노출상위_키워드")
df_Cost_keyword = pd.read_excel("Dataset.xlsx", sheet_name="고비용_키워드")
df_Trend = pd.read_excel("Dataset.xlsx", sheet_name="Trend")

if choose == "광고비/광고 매출 추이":
   st.write("### ※ 비용 & 매출 & ROAS")

   col1, col2, col3 = st.columns(3)
   col1.metric("총비용(VAT포함, 원)", "2,557,610원", "1,081,685원")
   col2.metric("매출액(원)", "8,156,900원", "2,793,300원")
   col3.metric("ROAS(%)", "310.82%", "-8.11%")

   st.write("---")

   st.write("### ※ 광고비와 광고 매출 추이")
   # Cost	Impressions	Click	Conversion	Revenue	Ratio
   options = st.multiselect(
      '지표 선택해주세요',
      ['Cost', 'Revenue','Impressions', 'Click', 'Conversion', 'Ratio'],
      ['Conversion'])

   st.line_chart(df_Trend, x='yyyymmdd', y = options, width=0, height=0, use_container_width=True)

   st.write("---")

elif choose == "Funnel별 성과":
   st.write("### ※  Funnel별 성과")
   data = dict(
      number=[323002, 6863, 635],
      Funnel=["노출수", "클릭수", "전환수"])
   fig = px.funnel(data, x='number', y='Funnel')

   st.plotly_chart(fig, theme="streamlit")    

   st.table(df_sheet0)      
   st.table(df_sheet1["Performance Summary"])

elif choose == "광고 상품별 성과":
   st.write("### ※  광고 상품별 성과")

   x = [
         ["총비용(원, VAT포함) ", "노출수", "클릭수", "전환수"],
         ["","", "", ""]
       ]
   fig = go.Figure()
   fig.add_bar(x=x,y=[df_sheet2["총비용 비율"].loc[0], df_sheet2["노출수 비율"].loc[0], df_sheet2["클릭수 비율"].loc[0], df_sheet2["전환수 비율"].loc[0]],name="파워링크")
   fig.add_bar(x=x,y=[df_sheet2["총비용 비율"].loc[1], df_sheet2["노출수 비율"].loc[1], df_sheet2["클릭수 비율"].loc[1], df_sheet2["전환수 비율"].loc[1]],name="쇼핑검색")
   fig.add_bar(x=x,y=[df_sheet2["총비용 비율"].loc[2], df_sheet2["노출수 비율"].loc[2], df_sheet2["클릭수 비율"].loc[2], df_sheet2["전환수 비율"].loc[2]],name="브랜드검색/신제품검색")
   fig.update_layout(barmode="relative")
   
   st.plotly_chart(fig, theme="streamlit")

   st.dataframe(df_sheet2)
   st.table(df_sheet1["광고상품별 Comment"])


elif choose == "파워링크 성과":
   st.write("### ※ 파워링크 Brand vs. Non-Brand 성과")

   st.dataframe(df_sheet3, use_container_width=False)
   # st.table(df_sheet3)

   c_type = [df_sheet3["캠페인 유형"].loc[0], df_sheet3["캠페인 유형"].loc[1]]

   fig1 = go.Figure(data=[
        go.Bar(name='총비용(원)', x=c_type, y=[df_sheet3["총비용(원)의 SUM"].loc[0],df_sheet3["총비용(원)의 SUM"].loc[1]]),
        go.Bar(name='전환매출액(원)', x=c_type, y=[df_sheet3["전환매출액(원)의 SUM"].loc[0],df_sheet3["전환매출액(원)의 SUM"].loc[1]])
    ])
   
   fig2 = go.Figure(data=[
        go.Bar(name='광고수익율(%)', x=c_type, y=[df_sheet3["광고수익율(%)의 SUM"].loc[0],df_sheet3["광고수익율(%)의 SUM"].loc[1]])
    ])
   # Change the bar mode
   fig1.update_layout(barmode='group')

   tab1, tab2 = st.tabs(["총비용 vs 전환매출액 비교", "광고수익율(%) 비교"])
   with tab1:
        st.plotly_chart(fig1, theme="streamlit")
   with tab2:
        st.plotly_chart(fig2, theme="streamlit")

   st.write("---")

elif choose == "파워링크 키워드 Top":
   st.write("### ※ 파워링크 키워드 리스트")
   tab1, tab2, tab3 = st.tabs(["매출 상위", "노출 상위", "고비용"])

   with tab1:
      st.write("#### 매출 상위 키워드")
      st.dataframe(df_Revenue_keyword)

   with tab2:
      st.write("#### 노출 상위 키워드")
      st.dataframe(df_Impression_keyword)

   with tab3:
      st.write("#### 고비용 키워드")
      st.dataframe(df_Cost_keyword) 


