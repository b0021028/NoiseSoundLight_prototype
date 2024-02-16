# 音光
## 概要
- RaspberryPi4・USBマイク・赤外線LED を使って 音を検出し赤外線機器を操作することができます。
## 環境
### ハードウェア
- RaspberryPi4
- USBマイク
- 赤外線LED(940nm) および LED用の抵抗
### ソフトウェア
- Ubuntu 23.x.x 64bit
- Python 3.11.x

## クイックスタート
1. RaspberryPi4 に ubuntuをインストール
2. NoiseSoundLight_prototype/ へ cd
3. `source setup.sh` を実行 (sudo 要求あり)
4. USBマイク接続
5. gpio20 に 赤外線LEDと抵抗をつける
6. `source activate.sh` を実行
7. 大きく拍手すると 画面上に 1と表示され `nec_on True` と表示されます (nec RE0206のCH2 全灯 を出力しています)

## 赤外線登録
- 赤外線登録には別途機器と irrp.py というプログラムが必要です
- ir_signals/ に jsonファイルを追加することで赤外線の登録ができます
- 音との結び付けは functions/function.json で行ってください