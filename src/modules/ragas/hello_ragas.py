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
from ragas import evaluate
import datetime
import pandas as pd


def dataset():
    # 質問事項
    questions = [
        "白石 玲奈は何歳の時にデビューしましたか？",  # case 1
        "2枚目にリリースしたアルバムのタイトルは何ですか？",  # case 2
        "2019年に出演したフェスは何ですか？",  # case3
    ]

    # 正しい答え
    ground_truths = [
        "20歳",
        " 『流星の詩』 (Meteor Poem)",
        "フジロックフェスティバルとコーチェラ・フェスティバル ",
    ]

    # 根拠となった情報(VectorStoreから取得した情報)
    contexts = [
        # case 1(正しい関連内容を取得)
        [
            "名前: 白石 玲奈 (Shiraishi Rena) 年齢: 28歳 生年月日: 1996年3月15日 デビューした歳: 20歳 リリースしたアルバム 1 アルバム名: 『青い夢』 (Blue Dream) リリース日: 2016年5月20日 詳細: デビューアルバムであり、瑞々しい感性と透明感あふれるボーカルで話題を呼んだ。アルバムには、青春の儚さや未来への希望を描いた曲が多く収録されており、特に「君と見",
            "の下町で生まれ育つ。幼少期から音楽に親しみ、ピアノとギターを独学で学ぶ。中学生の時に初めて作曲を始め、高校生になると地元のライブハウスで演奏するようになる。高校卒業後、音楽専門学校に進学し、本格的に音楽理論やボーカルトレーニングを学ぶ。20歳の時に自主制作アルバムをリリースし、これがレコード会社の目に留まりプロデビューを果たす。彼女の音楽は、その透明感のある声と詩的な歌詞、そして心に響くメロディで多くのファンを魅了している。出演したフェス一覧:フジロックフェスティバル (2",
        ],
        # case 2(正しい関連内容を取得)
        [
            "リリースしたアルバム 2アルバム名: 『流星の詩』 (Meteor Poem)リリース日: 2018年9月12日 詳細: セカンドアルバムで、より成熟した音楽性と深みのある歌詞が特徴。人生の様々な局面や感情を詩的に表現した楽曲が揃っており、「夜空に咲く花」がシングルとしてリリースされ、大人のリスナーからも支持を得た。アルバム全体を通じて、一貫したテーマとして「変化」と「成長」が描かれている。",
            "の下町で生まれ育つ。幼少期から音楽に親しみ、ピアノとギターを独学で学ぶ。中学生の時に初めて作曲を始め、高校生になると地元のライブハウスで演奏するようになる。高校卒業後、音楽専門学校に進学し、本格的に音楽理論やボーカルトレーニングを学ぶ。20歳の時に自主制作アルバムをリリースし、これがレコード会社の目に留まりプロデビューを果たす。彼女の音楽は、その透明感のある声と詩的な歌詞、そして心に響くメロディで多くのファンを魅了している。出演したフェス一覧:フジロックフェスティバル (2",
        ],
        # case 3(誤った関連内容を取得)
        [
            "名前: 白石 玲奈 (Shiraishi Rena) 年齢: 28歳 生年月日: 1996年3月15日 デビューした歳: 20歳 リリースしたアルバム 1 アルバム名: 『青い夢』 (Blue Dream) リリース日: 2016年5月20日 詳細: デビューアルバムであり、瑞々しい感性と透明感あふれるボーカルで話題を呼んだ。アルバムには、青春の儚さや未来への希望を描いた曲が多く収録されており、特に「君と見",
            "の下町で生まれ育つ。幼少期から音楽に親しみ、ピアノとギターを独学で学ぶ。中学生の時に初めて作曲を始め、高校生になると地元のライブハウスで演奏するようになる。高校卒業後、音楽専門学校に進学し、本格的に音楽理論やボーカルトレーニングを学ぶ。20歳の時に自主制作アルバムをリリースし、これがレコード会社の目に留まりプロデビューを果たす。彼女の音楽は、その透明感のある声と詩的な歌詞、そして心に響くメロディで多くのファンを魅了している。出演したフェス一覧:フジロックフェスティバル (2",
        ],
    ]

    # RAGから得られた回答
    answers = [
        "白石 玲奈がデビューしたのは20歳の時です。",  # case 1(正解)
        "2枚目にリリースされたアルバムのタイトルは「永遠の一瞬」です。",  # case 2(不正解)
        "ロック・イン・ジャパン・フェスとコーチェラ・フェスティバルに出演しました。 ",  # case 3(不正解)
    ]

    ds = Dataset.from_dict(
        {
            "question": questions,
            "answer": answers,
            "contexts": contexts,
            "ground_truth": ground_truths,
        }
    )

    return ds


def evaluate_const_param():
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
    ]

    # データセットの準備
    ds = dataset()

    # 評価を実行
    print(f"\033[92mStart Evaluation by RAGAS\033[0m")
    eval_res = evaluate(ds, metrics=metrics, llm=chat_llm, embeddings=embeddings)
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
