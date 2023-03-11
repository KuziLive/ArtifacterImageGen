from io import BytesIO
import io
from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageFilter
import codecs
import json
import os
import itertools
from collections import Counter
import base64

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def culculate_op(data: dict):

    cwd = os.path.dirname(os.path.abspath(__file__))
    with codecs.open(f'{cwd}/Assets/duplicate.json', 'r', encoding='utf-8') as f:
        dup = json.load(f)
    with codecs.open(f'{cwd}/Assets/subopM.json', 'r', encoding='utf-8') as f:
        mapping = json.load(f)

    res = [None, None, None, None]
    keymap = list(map(str, data.keys()))

    is_dup = []
    # 重複するものがあるか判定
    for ctg, state in data.items():
        dup_value = dup[ctg]['ov']
        if str(state) in dup_value:
            is_dup.append((ctg, state))

    # フラグの設定
    counter_flag = 0
    dup_ctg = [i[0] for i in is_dup]
    maxium_state_ct = 9

    # 重複が 0 の時の処理
    if not len(is_dup):
        for ctg, state in data.items():
            idx = keymap.index(ctg)
            res[idx] = mapping[ctg][str(state)]
        return res

    # 重複するものが一つの場合

    if len(is_dup) == 1:
        # 重複のないもの
        single_state = {c: s for c, s in data.items() if c not in dup_ctg}
        for ctg, state in single_state.items():
            idx = keymap.index(ctg)
            res[idx] = mapping[ctg][str(state)]
            counter_flag += len(mapping[ctg][str(state)])

        # 重複するもの
        dup_state = {c: s for c, s in data.items() if c in dup_ctg}
        long = maxium_state_ct - counter_flag
        possiblity = []

        for ctg, state in dup_state.items():
            possiblity = dup[ctg][str(state)]
            for p in possiblity:
                if len(p) == long or len(p) == long-1:
                    idx = keymap.index(ctg)
                    res[idx] = p
                    return res

    # 重複するものが複数の場合
    if len(is_dup) == 2:
        single_state = {c: s for c, s in data.items() if c not in dup_ctg}
        for ctg, state in single_state.items():
            idx = keymap.index(ctg)
            res[idx] = mapping[ctg][str(state)]
            counter_flag += len(mapping[ctg][str(state)])

        dup_state = {c: s for c, s in data.items() if c in dup_ctg}
        long = maxium_state_ct - counter_flag

        sample = [[ctg, state]for ctg, state in dup_state.items()]

        possiblity1 = dup[sample[0][0]][str(sample[0][1])]
        possiblity2 = dup[sample[1][0]][str(sample[1][1])]

        p1 = [len(p) for p in possiblity1]
        p2 = [len(p) for p in possiblity2]

        p = itertools.product(p1, p2)
        r = None
        for v in p:
            if sum(v) == long or sum(v) == long-1:
                r = v
                break

        idx1 = keymap.index(sample[0][0])
        idx2 = keymap.index(sample[1][0])

        res[idx1] = possiblity1[p1.index(v[0])]
        res[idx2] = possiblity2[p2.index(v[1])]
        return res

    if len(is_dup) == 3:
        single_state = {c: s for c, s in data.items() if c not in dup_ctg}
        for ctg, state in single_state.items():
            idx = keymap.index(ctg)
            res[idx] = mapping[ctg][str(state)]
            counter_flag += len(mapping[ctg][str(state)])

        dup_state = {c: s for c, s in data.items() if c in dup_ctg}
        long = maxium_state_ct - counter_flag

        sample = [[ctg, state]for ctg, state in dup_state.items()]

        possiblity1 = dup[sample[0][0]][str(sample[0][1])]
        possiblity2 = dup[sample[1][0]][str(sample[1][1])]
        possiblity3 = dup[sample[2][0]][str(sample[2][1])]

        p1 = [len(p) for p in possiblity1]
        p2 = [len(p) for p in possiblity2]
        p3 = [len(p) for p in possiblity3]

        p = itertools.product(p1, p2, p3)
        r = None
        for v in p:
            if sum(v) == long or sum(v) == long-1:
                r = v
                break

        idx1 = keymap.index(sample[0][0])
        idx2 = keymap.index(sample[1][0])
        idx3 = keymap.index(sample[2][0])

        res[idx1] = possiblity1[p1.index(v[0])]
        res[idx2] = possiblity2[p2.index(v[1])]
        res[idx3] = possiblity3[p3.index(v[2])]

        return res

    if len(is_dup) == 4:
        dup_state = {c: s for c, s in data.items() if c in dup_ctg}
        long = maxium_state_ct - counter_flag

        sample = [[ctg, state]for ctg, state in dup_state.items()]

        possiblity1 = dup[sample[0][0]][str(sample[0][1])]
        possiblity2 = dup[sample[1][0]][str(sample[1][1])]
        possiblity3 = dup[sample[2][0]][str(sample[2][1])]
        possiblity4 = dup[sample[3][0]][str(sample[3][1])]

        p1 = [len(p) for p in possiblity1]
        p2 = [len(p) for p in possiblity2]
        p3 = [len(p) for p in possiblity3]
        p4 = [len(p) for p in possiblity4]

        p = itertools.product(p1, p2, p3, p4)
        r = None
        for v in p:
            if sum(v) == long or sum(v) == long-1:
                r = v
                break

        idx1 = keymap.index(sample[0][0])
        idx2 = keymap.index(sample[1][0])
        idx3 = keymap.index(sample[2][0])
        idx4 = keymap.index(sample[3][0])

        res[idx1] = possiblity1[p1.index(v[0])]
        res[idx2] = possiblity2[p2.index(v[1])]
        res[idx3] = possiblity3[p3.index(v[2])]
        res[idx4] = possiblity4[p4.index(v[3])]

        return res
    return


def read_json(path):
    with codecs.open(path, encoding='utf-8') as f:
        data = json.load(f)
    return data


def generation(data):

    ArtifactsData: dict = data.get('Artifacts')

    cwd = os.path.abspath(os.path.dirname(__file__))

    def config_font(size): return ImageFont.truetype(
        f'{cwd}/Assets/ja-jp.ttf', size)

    Base = Image.open(f'{cwd}/Base/炎.png')

    D = ImageDraw.Draw(Base)

    disper = ['会心率', '会心ダメージ', '攻撃パーセンテージ', '防御パーセンテージ', 'HPパーセンテージ', '水元素ダメージ', '物理ダメージ', '風元素ダメージ',
              '岩元素ダメージ', '炎元素ダメージ', '与える治癒効果', '与える治療効果', '雷元素ダメージ', '氷元素ダメージ', '草元素ダメージ', '与える治癒効果', '元素チャージ効率']
    StateOP = ('HP', '攻撃力', "防御力", "元素熟知", "会心率", "会心ダメージ", "元素チャージ効率")

    optionmap = {
        "攻撃パーセンテージ": "攻撃%",
        "防御パーセンテージ": "防御%",
        "元素チャージ効率": "元チャ効率",
        "HPパーセンテージ": "HP%",
    }

    # 聖遺物
    atftype = list()
    for i, parts in enumerate(['flower', "wing", "clock", "cup", "crown"]):
        details = ArtifactsData.get(parts)

        if not details:
            continue
        atftype.append(details['type'])
        PreviewPaste = Image.new('RGBA', Base.size, (255, 255, 255, 0))
        Preview = Image.open(
            f'{cwd}/Artifact/{details["type"]}/{parts}.png').resize((256, 256))
        enhancer = ImageEnhance.Brightness(Preview)
        Preview = enhancer.enhance(0.6)
        Preview = Preview.resize(
            (int(Preview.width*1.3), int(Preview.height*1.3)))
        Pmask1 = Preview.copy()

        Pmask = Image.open(
            f'{cwd}/Assets/ArtifactMask.png').convert('L').resize(Preview.size)
        Preview.putalpha(Pmask)
        if parts in ['flower', 'crown']:
            PreviewPaste.paste(Preview, (-37+373*i, 570), mask=Pmask1)
        elif parts in ['wing', 'cup']:
            PreviewPaste.paste(Preview, (-36+373*i, 570), mask=Pmask1)
        else:
            PreviewPaste.paste(Preview, (-35+373*i, 570), mask=Pmask1)
        Base = Image.alpha_composite(Base, PreviewPaste)
        D = ImageDraw.Draw(Base)

        mainop = details['main']['option']

        mainoplen = D.textlength(optionmap.get(
            mainop) or mainop, font=config_font(29))
        D.text((375+i*373-int(mainoplen), 655),
               optionmap.get(mainop) or mainop, font=config_font(29))
        MainIcon = Image.open(
            f'{cwd}/emotes/{mainop}.png').convert("RGBA").resize((35, 35))
        MainMask = MainIcon.copy()
        Base.paste(MainIcon, (340+i*373-int(mainoplen), 655), mask=MainMask)

        mainv = details['main']['value']
        if mainop in disper:
            mainvsize = D.textlength(f'{float(mainv)}%', config_font(49))
            D.text((375+i*373-mainvsize, 690),
                   f'{float(mainv)}%', font=config_font(49))
        else:
            mainvsize = D.textlength(format(mainv, ","), config_font(49))
            D.text((375+i*373-mainvsize, 690),
                   format(mainv, ","), font=config_font(49))
        levlen = D.textlength(f'+{details["Level"]}', config_font(21))
        D.rounded_rectangle((373+i*373-int(levlen), 748,
                            375+i*373, 771), fill='black', radius=2)
        D.text((374+i*373-levlen, 749),
               f'+{details["Level"]}', font=config_font(21))

        if details['Level'] == 20 and details['rarelity'] == 5:
            c_data = {}
            for a in details["sub"]:
                if a['option'] in disper:
                    c_data[a['option']] = str(float(a["value"]))
                else:
                    c_data[a['option']] = str(a["value"])
            psb = culculate_op(c_data)

        if len(details['sub']) == 0:
            continue

        for a, sub in enumerate(details['sub']):
            SubOP = sub['option']
            SubVal = sub['value']
            if SubOP in ['HP', '攻撃力', '防御力']:
                D.text((79+373*i, 811+50*a), optionmap.get(SubOP) or SubOP,
                       font=config_font(25), fill=(255, 255, 255, 190))
            else:
                D.text((79+373*i, 811+50*a), optionmap.get(SubOP)
                       or SubOP, font=config_font(25))
            SubIcon = Image.open(f'{cwd}/emotes/{SubOP}.png').resize((30, 30))
            SubMask = SubIcon.copy()
            Base.paste(SubIcon, (44+373*i, 811+50*a), mask=SubMask)
            if SubOP in disper:
                SubSize = D.textlength(f'{float(SubVal)}%', config_font(25))
                D.text((375+i*373-SubSize, 811+50*a),
                       f'{float(SubVal)}%', font=config_font(25))
            else:
                SubSize = D.textlength(format(SubVal, ","), config_font(25))
                if SubOP in ['防御力', '攻撃力', 'HP']:
                    D.text((375+i*373-SubSize, 811+50*a), format(SubVal, ","),
                           font=config_font(25), fill=(255, 255, 255, 190))
                else:
                    D.text((375+i*373-SubSize, 811+50*a), format(SubVal,
                           ","), font=config_font(25), fill=(255, 255, 255))

            if details['Level'] == 20 and details['rarelity'] == 5:
                nobi = D.textlength(
                    "+".join(map(str, psb[a])), font=config_font(11))
                D.text((375+i*373-nobi, 840+50*a), "+".join(map(str,
                       psb[a])), fill=(255, 255, 255, 160), font=config_font(11))

        PointRefer = {
            "total": {
                "SS": 220,
                "S": 200,
                "A": 180
            },
            "flower": {
                "SS": 50,
                "S": 45,
                "A": 40
            },
            "wing": {
                "SS": 50,
                "S": 45,
                "A": 40
            },
            "clock": {
                "SS": 45,
                "S": 40,
                "A": 35
            },
            "cup": {
                "SS": 45,
                "S": 40,
                "A": 37
            },
            "crown": {
                "SS": 40,
                "S": 35,
                "A": 30
            }
        }

    SetBounus = Counter([x for x in atftype if atftype.count(x) >= 2])
    for i, (n, q) in enumerate(SetBounus.items()):
        if len(SetBounus) == 2:
            D.text((1536, 243+i*35), n, fill=(0, 255, 0), font=config_font(23))
            D.rounded_rectangle((1818, 243+i*35, 1862, 266+i*35), 1, 'black')
            D.text((1835, 243+i*35), str(q), font=config_font(19))
        if len(SetBounus) == 1:
            D.text((1536, 263), n, fill=(0, 255, 0), font=config_font(23))
            D.rounded_rectangle((1818, 263, 1862, 288), 1, 'black')
            D.text((1831, 265), str(q), font=config_font(19))

    Base.show()
    Base.save(f'{cwd}/Tests/Image.png')

    return pil_to_base64(Base, format='png')


def pil_to_base64(img, format="jpeg"):
    buffer = BytesIO()
    img.save(buffer, format)
    img_str = base64.b64encode(buffer.getvalue()).decode("ascii")

    return img_str


generation(read_json('output.json'))
