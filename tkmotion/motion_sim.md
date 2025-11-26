```
Copyright 2025 Takayoshi Matsuyama

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

# モーションシミュレーション

# 目的
離散時間におけるモーション制御システムの動作のシミュレーション

# クラス

| クラス | 分類 | 説明 |
| -- | -- | -- |
| PhycicalObject / 物体 | 実体に基づく | 物理的な物体 |
| Motor / モータ | 実体に基づく | 電流をトルク/推力に変換する |
| Encodder / エンコーダ | 実体に基づく | 物体の位置を数値化する |
| ServoAmp / サーボアンプ | 実体に基づく | 指令トルク/推力を電流に変換し、増幅する |
| ServoController / サーボ制御器 | ソフトウェア | 指令トルク/推力を計算する |
| DiscreteTime / 離散時間 | ソフトウェア | 離散時間の時系列 |
