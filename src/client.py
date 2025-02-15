import streamlit as st
import grpc
import tutorial_pb2
import tutorial_pb2_grpc

st.title("gRPC Tutorial")

def create_client():
    # インセキュアな接続を使用（テスト用）
    channel = grpc.insecure_channel('grpc-fastapi-app.fly.dev:50051')
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