from django.core.management import call_command
from django.core.management.base import BaseCommand


from 臺灣言語資料庫.資料模型 import 影音表


class 匯入指令(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '語料目錄',
            type=str,
        )
        parser.add_argument(
            '--匯入幾筆',
            type=int,
            default=100000,
            help='試驗用，免一擺全匯'
        )

    def handle(self, *args, **參數):
        call_command('顯示資料數量')

        匯入數量 = 0
        for 語者, 音檔路徑, 正規化物件 in self._全部資料(參數['語料目錄']):
            影音內容 = {
                '影音所在': 音檔路徑,
                '屬性': {'語者': 語者},
            }
            影音內容.update(self.公家內容)
            影音 = 影音表.加資料(影音內容)
            文本內容 = {
                '文本資料': 正規化物件.看型(),
                '音標資料': 正規化物件.看音(),
            }
            文本內容.update(self.公家內容)
            影音.寫文本(文本內容)
            聽拍內容 = {'聽拍資料': [{
                '開始時間': 0,
                '結束時間': 影音.聲音檔().時間長度(),
                '內容': 正規化物件.看分詞(),
                '語者': 語者,
            }]}
            聽拍內容.update(self.公家內容)
            影音.寫聽拍(聽拍內容)

            匯入數量 += 1
            if 匯入數量 % 100 == 0:
                print('匯入 {} 筆'.format(匯入數量))
            if 匯入數量 == 參數['匯入幾筆']:
                break

        call_command('顯示資料數量')
