import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from pandas.api.types import is_numeric_dtype


#ダッシュボードの生成
def main():
    st.set_page_config(layout="wide")
    #タイトルの表示
    st.title("DashBoard")

    #データの読み込み
    file = st.sidebar.file_uploader("Upload csv file", type="csv")
    #csvファイルが読み込まれた後，実行
    if file != None:
        #読み込んだデータをデータフレーム化
        df = pd.read_csv(file, encoding="utf_8")
        print(df)
        print(df.dtypes)
        #特徴量名のリストを作成する
        feature_list = [feature for feature in df.columns]
        print(feature_list)

        #サイドバーのレイアウト
        st.sidebar.markdown("## Settings")
        #ピックアップしたい特徴量の選択
        feature_selected = st.sidebar.selectbox("Feature Values", feature_list)
        #予測対象の特徴量の選択
        target = st.sidebar.selectbox("Target", feature_list, index=1)
        #予測対象のデータ個数のカウント
        target_count = df[target].value_counts().reset_index(name="count")
        print(target_count)
        fig_target = go.Figure(data=[go.Pie(labels=target_count["index"], values=target_count["count"], hole=.3)])
        fig_target.update_layout(showlegend=False, height=200, margin={'l': 20, 'r': 60, 't': 0, 'b': 0})
        fig_target.update_traces(textposition='inside', textinfo='label+percent')

        #予測対象のデータ個数をグラフ表示
        st.sidebar.markdown("## Target Percentage")
        st.sidebar.plotly_chart(fig_target, use_container_width=True)
        #print(target_count)

        #データフレームの表示
        st.markdown("Data Frame")
        st.dataframe(df.head())

        if is_numeric_dtype(df[feature_selected]):
            #要約統計量の表示
            st.markdown("Summary Statistics")
            st.dataframe(df[feature_selected].describe())

            #欠損値の数を表示
            st.markdown("Missing Value")
            st.text(df[feature_selected].isnull().sum())
        else:
            #カテゴリカル変数の表示
            fig_cat = go.Figure()
            for i in target_count["index"]:
                fig_cat.add_trace(go.Bar(name=str(i), x=df[feature_selected], y=df[df[target]==i]))
            #fig_cat = go.Figure(data=[go.Bar(x=df[feature_selected], y=df[target])])
            fig_cat.update_layout(height=300, width=500, margin={'l': 20, 'r': 20, 't': 0, 'b': 0}, legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99), barmode='stack')
            fig_cat.update_xaxes(title_text=None)
            fig_cat.update_yaxes(title_text='# of samples')
            st.plotly_chart(fig_cat, use_container_width=True)
            st.markdown("")

        #コンテンツのグラフの作成
        #df_feature = df.groupby(target_name[0])[feature_selected].count().reset_index()
        #st.markdown(df_feature)


if __name__ == "__main__":
    #main関数の呼び出し
    main()