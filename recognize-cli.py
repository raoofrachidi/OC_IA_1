"""Language Recognize CLI
This file defines the `detector-cli.py` command line.
usage: detector-cli.py --text "TEXT"
"""
import argparse
import requests
import uuid
import environs


class Recognize:
    def __init__(self):
        env = environs.Env()
        env.read_env()

        self.subscription_key = env.str("SUBSCRIPTION_KEY")
        self.endpoint = env.str("ENDPOINT") + '/detect'
        self.location = env.str("LOCATION")

    def detect_language(self, text: str) -> str:
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Ocp-Apim-Subscription-Region": self.location,
            "Content-type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4()),
        }
        params = {
            'api-version': '3.0'
        }
        body = [{"text": text}]
        request = requests.post(self.endpoint, params=params, headers=headers, json=body)
        response = request.json()

        return response[0]["language"]


def process_text(recognize: Recognize, text: str) -> None:
    print(f'Detected language : { recognize.detect_language(text) }')


def main(recognize: Recognize) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--text')
    args = parser.parse_args()
    if args.text:
        process_text(recognize, args.text)


if __name__ == '__main__':
    main(Recognize())


# Text to be tested
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# French : "L'alimentation industrielle convient parfaitement à la croissance du chiot et à l'adulte."
# Russian : "Занимает пятое место в диптихе автокефальных поместных церквей мира."
# English : "He was a economics graduate from Elphinstone College, Mumbai. He was an industrialist in plastics business."
# Spanish : "Barilla est un'impresa murtinassionale italiana de su setore alimentàriu, lìdera mundiale in su mercadu de sos macarrones sicos, de sos sutzos prontos in Europa."
# Indonesian : "Kemunculan pertamanya adalah ketika mencium kakak kelasnya, Kyoko. Sejak Yuuki meminta agar Sakura merahasiakan hal tersebutlah keduanya menjadi akrab."
# Chinese : "胡赛尼本人和小说的主人公阿米尔一样，都是出生在阿富汗首都喀布尔，少年时代便离开了这个国家。胡赛尼直到2003年小说出版之后才首次回到已经离开27年的祖国。他在苏联入侵时离开了阿富汗"
# Arabic : "قبل عام بالضبط وبتاريخ 21/7/2012 أعلن البغدادي خطة هدم الأسوار وبتاريخ 21/7/2013"
