import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st
from sklearn import datasets

#ダッシュボードの生成
def main():
    st.set_page_config(layout="wide")

    #データの読み込み
    file = st.sidebar.file_uploader("Upload csv file", type="csv")
    #csvファイルが読み込まれた後，実行
    if file != None:
        #読み込んだデータをデータフレーム化
        df = pd.read_csv(file, encoding="utf_8")
        print(df)

        #特徴量名のリストを作成する
        X = df.iloc[:,:-1]
        print(X)
        y = df.iloc[:,[-1]]
        print(y)
        feature_list = [feature for feature in X.columns]
        print(feature_list)
        target_name = y.columns.values
        print(target_name)

        #サイドバーの生成
        st.sidebar.markdown("## Settings")
        feature_selected = st.sidebar.selectbox("Feature Values", feature_list)

        #データフレームの表示
        st.markdown("Data Frame")
        st.dataframe(df.head())

        #要約統計量の表示
        st.markdown("Summary Statistics")
        st.dataframe(df[feature_selected].describe())

        #欠損値の数を表示
        st.markdown("Missing Value")
        st.text(df[feature_selected].isnull().sum())

        #コンテンツのグラフの作成
        df_feature = df.groupby(target_name[0])[feature_selected].count().reset_index()
        #st.markdown(df_feature)


if __name__ == "__main__":
    #main関数の呼び出し
    main()