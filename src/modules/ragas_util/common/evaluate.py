import os
from dotenv import load_dotenv
from ragas.metrics import (
    context_precision,
    answer_relevancy,
    faithfulness,
    context_recall,
    context_relevancy,
    context_entity_recall,
    answer_similarity,
    answer_correctness,
)
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from datasets import Dataset
from ragas import evaluate as rags_evaluate
import datetime
import pandas as pd


def evaluate(dataset: Dataset):
    # モデル定義
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
    OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "")
    OPENAI_EMBBEDING_MODEL = os.getenv("OPENAI_EMBBEDING_MODEL", "")
    chat_llm = ChatOpenAI(
        model=OPENAI_CHAT_MODEL,
        temperature=0,
    )
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBBEDING_MODEL)

    # 使用するメトリクス
    metrics = [
        context_precision,
        answer_relevancy,
        faithfulness,
        context_recall,
        context_relevancy,
        context_entity_recall,
        answer_similarity,
        answer_correctness,
    ]

    # 評価を実行
    print(f"\033[92mStart Evaluation by RAGAS\033[0m")
    eval_res = rags_evaluate(
        dataset=dataset, metrics=metrics, llm=chat_llm, embeddings=embeddings
    )
    eval_results_df = eval_res.to_pandas()
    print(eval_results_df)

    # csvとして結果を保存
    if type(eval_results_df) != pd.DataFrame:
        raise TypeError("result.to_pandas() が DataFrame を返していません。")
    parent_dir = "tmp"
    today = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=9))
    ).strftime("%Y%m%dT%H%M%SJST")
    path = os.path.abspath(os.path.join(os.getcwd(), f"{parent_dir}/ragas_{today}.csv"))
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    eval_results_df.to_csv(path, index=True)
    print(f"\033[92m結果を {path} に保存しました。\033[0m")
