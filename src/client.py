import streamlit as st
import grpc
import tutorial_pb2
import tutorial_pb2_grpc
import os
import pandas as pd
import base64

favicon_path = os.path.join(os.getcwd(), "static/favicon.ico")

st.set_page_config(
    page_title="gRPC Tutorial",
    page_icon=favicon_path,
    layout="centered",
    initial_sidebar_state="expanded",
        menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 画像をbase64エンコード
image_base64 = get_image_base64("static/icon.png")

# HTMLにbase64エンコードした画像を埋め込む
st.markdown(
    f"""
    <style>
        .custom-image {{
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 200px;
            height: 200px;
            border-radius: 25px;
            box-shadow: 0px 4px 20px rgba(125, 0, 64, 1.0);
        }}
    </style>
    """,
    unsafe_allow_html=True
)
# カスタムテーマの適用
st.markdown("""
    <style>
        :root {
            --primary-color: #004a55;
            --background-color: #00171f;
            --text-color: #222;
        }
        .stApp {
            background-color: var(--background-color);
            color: var(--text-color);
        }
    </style>
""", unsafe_allow_html=True)
# Custom CSS
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    .Widget>label {
        color: #31333F;
        font-weight: bold;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #4CAF50;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
# HTMLにbase64エンコードした画像を埋め込む
st.sidebar.markdown(
    f"""
    <img src="data:image/png;base64,{image_base64}" class="custom-image">
    """,
    unsafe_allow_html=True
)
st.sidebar.title("📊 Data Visualizer")
st.sidebar.markdown("---")
# Data input method
input_method = st.sidebar.radio("Choose input method:", ("Upload CSV", "Enter Data Manually"))

if input_method == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    else:
        data = None
else:
    data_input = st.sidebar.text_area("Enter your data (comma-separated numbers):", "1.2, 2.3, 3.4, 4.5, 5.6")
    data = pd.DataFrame({'value': [float(x.strip()) for x in data_input.split(",")]})

# Main content
st.title("📈 Data Visualization Dashboard")
# st.title("gRPC Tutorial")

def create_client():
    # インセキュアな接続を使用（テスト用）
    # channel = grpc.insecure_channel('grpc-fastapi-app.fly.dev:50051')
    server_url = st.secrets.get("GRPC_SERVER_URL", "localhost:50051")
    channel = grpc.insecure_channel(server_url)
    st.write(f"Connecting to: {server_url}")

    return channel, tutorial_pb2_grpc.DataServiceStub(channel)

try:
    channel, stub = create_client()
    st.success("gRPCサーバーに接続しました")
except Exception as e:
    st.error(f"接続エラー: {str(e)}")
    st.stop()

query = st.text_input("Enter a query")

if st.button("Submit"):
    try:
        request = tutorial_pb2.DataRequest(query=query)
        response = stub.GetData(request)
        st.write(f"サーバーからのレスポンス: {response.message}")
    except grpc.RpcError as e:
        st.error(f"gRPCエラー: {str(e)}")
        st.error(f"詳細: {e.details() if hasattr(e, 'details') else 'No details'}")
        st.error(f"コード: {e.code() if hasattr(e, 'code') else 'No code'}")