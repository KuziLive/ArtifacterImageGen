import codecs
import dataclasses
import glob
import json
from typing import List
import os
from PIL import Image
import pyocr
import pyocr.builders
import sys


@dataclasses.dataclass
class Option:
    option: str = "NA"
    value: int = 0

# レベル、レアリティはOCRで読み取れてないのでいったん20で決め打ち
@dataclasses.dataclass
class Artifact:
    type: str = "NA"
    Level: int = 20
    rarelity: int = 5
    main: Option = None
    sub: List[Option] = dataclasses.field(default_factory=list)

    def get_series(self, artifact_name):
        series_book = {}
        with open("artifact_list.txt", encoding="utf-8") as f:
            for line in f:
                series, items = line.split('：')
                series_book[series] = [i.replace('\n', '') for i in items.split('、')]
            for series, items in series_book.items():
                for item in items:
                    if artifact_name == item:
                        return series
            return "NA"

    def format_status(self, status):
        status = status.replace("%", "")
        status = status.replace(",", "")
        status = status.replace(".0", "")
        return status

    def make_artifact(self, image_path, output_path, tool):
        im = Image.open(image_path)
        width = im.width
        height = im.height
        # 廻聖できるかできないかで位置がかわる
        # とりあえずbottomに4行とも「・」からはじまるかどうかで判定
        name_crop = im.crop((width * 0.375, height * 0.14,
                        width * 0.625, height * 0.19))
        middle_crop = im.crop((width * 0.38, height * 0.27,
                        width * 0.47, height * 0.35))
        bottom_crop = im.crop((width * 0.375, height * 0.46,
                        width * 0.56, height * 0.61))
        name = tool.image_to_string(
            name_crop,
            lang="jpn",
            builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )
        name = [i for i in name.split('\n') if not(i=='')]
        middle = tool.image_to_string(
            middle_crop,
            lang="jpn",
            builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )
        middle = [i for i in middle.split('\n') if not(i=='')]
        bottom = tool.image_to_string(
            bottom_crop,
            lang="jpn",
            builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )
        bottom = [i for i in bottom.split('\n') if not(i=='')]
        for element in bottom:
            if element[0] != '・':
                gap = 0.035
                name_crop = im.crop((width * 0.375, height * (0.14 - gap),
                                width * 0.625, height * (0.19 - gap)))
                middle_crop = im.crop((width * 0.38, height * (0.27 - gap),
                                width * 0.47, height * (0.35 - gap)))
                bottom_crop = im.crop((width * 0.375, height * (0.46 - gap),
                                width * 0.56, height * (0.61 - gap)))
                option = Option("", 0.0)
                name = tool.image_to_string(
                    name_crop,
                    lang="jpn",
                    builder=pyocr.builders.TextBuilder(tesseract_layout=6)
                )
                name = [i for i in name.split('\n') if not(i=='')]
                middle = tool.image_to_string(
                    middle_crop,
                    lang="jpn",
                    builder=pyocr.builders.TextBuilder(tesseract_layout=6)
                )
                middle = [i for i in middle.split('\n') if not(i=='')]
                bottom = tool.image_to_string(
                    bottom_crop,
                    lang="jpn",
                    builder=pyocr.builders.TextBuilder(tesseract_layout=6)
                )
                bottom = [i for i in bottom.split('\n') if not(i=='')]
                break
        print(name, end='\n\n')
        print(middle, end='\n\n')
        print(bottom, end='\n\n')
        name_crop.save(os.path.join(output_path + 'name_crop.png'), quality=100)
        middle_crop.save(os.path.join(output_path + 'middle_crop.png'), quality=100)
        bottom_crop.save(os.path.join(output_path + 'bottom_crop.png'), quality=100)
        # 取得したデータをArtifactに格納してreturn
        self.type = self.get_series(name[0])
        # TODO: ステータスがちゃんと読み取れていない場合は0に設定する？
        # メインステ
        main_option = None
        # 花のHPは検出されないので補完
        if len(middle) == 1:
            main_option = Option("HP", self.format_status(middle[0]))
        elif len(middle) == 2:
            main_option = Option(middle[0], self.format_status(middle[1]))
        else:
            main_option = Option("NA", 0)
        self.main = main_option
        # サブステ
        for subst in bottom:
            subst = subst.replace('・', '')
            sub_name, sub_num = subst.split('+')
            if '%' in sub_num:
                if sub_name == '攻撃力':
                    sub_name = '攻撃パーセンテージ'
                if sub_name == '防御力':
                    sub_name = '防御パーセンテージ'
                if sub_name == 'HP':
                    sub_name = 'HPパーセンテージ'
            sub_num = self.format_status(sub_num)
            sub_option = Option(sub_name, sub_num)
            self.sub.append(sub_option)

def read_json(path):
    with codecs.open(path, encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_json(path, json_data):
    with codecs.open(path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False)

def main():
    ## スクリーンショットをWin+Prtscn+Altでビデオ/Capturesに保存(花、羽、時計、杯、冠の順に撮ることに注意)
    # Lv20で☆５限定(4OP状態であることも前提)
    
    ## OCR用意
    # 環境変数「PATH」にTesseract-OCRのパスを設定。
    # Windowsの環境変数に設定している場合は不要。
    path='C:\\Program Files\\Tesseract-OCR\\'
    # path = "/mnt/c/\'Program Files\'/Tesseract-OCR/"
    os.environ['PATH'] = os.environ['PATH'] + path
    # pyocrにTesseractを指定する。
    pyocr.tesseract.TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # pyocr.tesseract.TESSERACT_CMD = '/mnt/c/\'Program Files\'/Tesseract-OCR/tesseract.exe'
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]
    print("Will use tool '%s'" % (tool.get_name()))

    # スクリーンショットを必要な部分のみ切り取る
    files_path = glob.glob(r'C:\Users\mktba\Videos\Captures\*.png')
    kind_list = [r"flower\\", r"wing\\", r"clock\\", r"cup\\", r"crown\\"]
    data = read_json('template.json')
    for file_path, kind in zip(files_path, kind_list):
        output_path = os.path.join(r'C:\Users\mktba\Documents\YouTubeLive\screen2score_sheet\ArtifacterImageGen\scanned_data', kind)
        artifact = Artifact()
        artifact.make_artifact(file_path, output_path, tool)
        print(artifact)
        data["Artifacts"][kind.replace("\\", "")]["type"] = artifact.type
        data["Artifacts"][kind.replace("\\", "")]["Level"] = artifact.Level
        data["Artifacts"][kind.replace("\\", "")]["rarelity"] = artifact.rarelity
        data["Artifacts"][kind.replace("\\", "")]["main"]["option"] = artifact.main.option
        artifact.main.value = float(artifact.main.value)
        if artifact.main.value.is_integer():
            artifact.main.value = int(artifact.main.value)
        data["Artifacts"][kind.replace("\\", "")]["main"]["value"] = artifact.main.value
        for sub_e, artifact_sub in zip(data["Artifacts"][kind.replace("\\", "")]["sub"], artifact.sub):
            sub_e["option"] = artifact_sub.option
            artifact_sub.value = float(artifact_sub.value)
            if artifact_sub.value.is_integer():
                artifact_sub.value = int(artifact_sub.value)
            sub_e["value"] = artifact_sub.value

    # Artifactクラスの内容をもとにocr_data.jsonを生成
    # 読み取ったステータス(名前、数値)が合法か確認
    # サブオプで違法だった場合もメインステをNAにする。サブステをNAにするのが面倒なため暫定対応
    write_json('output.json', data)
    
    # ArtifacterImageGenを起動
    os.system("python3 my_Generater.py")

    # later:
    # スコア算出処理を追加


if __name__ == '__main__':
    main()
