import requests
import json
import os
from dotenv import load_dotenv
from datasets import Dataset


def qa(query: str) -> dict:
    load_dotenv()
    DIFY_API_KEY = os.getenv("DIFY_API_KEY", "")
    DIFY_BASE_URL = os.getenv("DIFY_BASE_URL", "")
    user = "user-123"

    # APIエンドポイントとヘッダーの設定
    url = f"{DIFY_BASE_URL}/v1/chat-messages"
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",  # 生成したAPIシークレットキーを設定
        "Content-Type": "application/json",
    }

    # 初回リクエストのデータ
    data = {
        "inputs": {},
        "query": query,  # 初回のチャットクエリ
        "response_mode": "blocking",
        "conversation_id": "",  # 初回は空の会話ID
        "user": user,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()
    return response_data


def dataset(query: str, ground_truth: str) -> Dataset:
    response_data = qa(query)

    # 取得した会話IDを表示
    conversation_id = response_data.get("conversation_id")
    answer = response_data.get("answer")
    retriever_resources = response_data.get("metadata", {}).get("retriever_resources")
    retriever_resource_contents = [
        retriever_resource["content"] for retriever_resource in retriever_resources
    ]
    print("会話ID:", conversation_id)
    print("回答:", answer)
    print("参考にしたナレッジ:", retriever_resources)

    ds = Dataset.from_dict(
        {
            "question": [query],
            "answer": [answer],
            "contexts": [retriever_resource_contents],
            "ground_truth": [ground_truth],
        }
    )

    return ds
