from datasets import Dataset
from modules.ragas_util.common.evaluate import evaluate
from modules.ragas_util.dify.qa import dataset


def evaluate_dify():
    # データセットの準備
    ds = dataset(
        "バックエンドAPIでcsv形式のナレッジを定期的に登録するには？短く教えて",
        "DifyのバックエンドAPIを使用して、定期的にCSV形式のナレッジを登録するには、以下の手順を行います",
    )
    evaluate(ds)
