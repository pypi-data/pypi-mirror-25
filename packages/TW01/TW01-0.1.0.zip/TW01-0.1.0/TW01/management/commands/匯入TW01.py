from os import walk
from os.path import join, basename
from subprocess import PIPE
import subprocess


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.解析錯誤 import 解析錯誤
from 臺灣言語工具.音標系統.閩南語.通用拼音音標 import 通用拼音音標
from TW01.management.commands._匯入指令 import 匯入指令
from 臺灣言語資料庫.資料模型 import 版權表


class Command(匯入指令):

    公家內容 = {
        '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0].編號(),
        '來源': 來源表.objects.get_or_create(名='TW01')[0].編號(),
        '版權': 版權表.objects.get_or_create(版權='毋知')[0].pk,
        '種類': '字詞',
        '語言腔口': '臺語',
        '著作所在地': '臺灣',
        '著作年': '2000',
    }

    def _全部資料(self, 語料目錄):
        for 所在, _資料夾陣列, 檔案陣列 in sorted(walk(語料目錄)):
            for 檔案 in 檔案陣列:
                路徑 = join(所在, 檔案)
                if 路徑.endswith('.tcp'):
                    proc = subprocess.Popen(
                        ['iconv', '-f', 'big5', '-t', 'utf8', 路徑], stdout=PIPE
                    )
                    outs, _errs = proc.communicate()
#                     print(路徑)
                    for 一逝 in outs.decode().split('\n'):
                        if 一逝.strip():
                            編號, 漢羅, 通用 = 一逝.split()
                            音檔路徑 = join(所在, 編號 + '.wav')
#                             資料[編號] = (漢字, 通用)
                            try:
                                正規化物件 = (
                                    拆文分析器
                                    .對齊組物件(漢羅, 通用.replace('_', ' '))
                                    .轉音(通用拼音音標)
                                )
                                yield (basename(所在), 音檔路徑, 正規化物件)
                            except 解析錯誤:
                                print(漢羅, 通用)
                                pass
