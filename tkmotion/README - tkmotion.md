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

update: 2025/11/30

# モーションシミュレータ

# 1. 動機
モーション制御に関する組み込みシステムの開発に携わっています。<br>
「制御理論から実機械への応用まで」を、きちんと実践できるようにしたい。<br>
そのための学習として、このモーションシミュレータを作成しました。

# 2. コンセプト
  組み込み制御システムのフローに基づく、離散時系列の制御シミュレータ。<br>
  （指令計算 ⇒ 操作量計算 ⇒ 物体の運動変化 ⇒ フィードバック）

## 2.1 特徴
1. 「MotionFlow（モーション制御フロー）」 クラスを中心に概念整理した、現実に即した分かりやすいオブジェクト指向設計
2. カスタマイズ可能（JSONファイルでパラメータ設定）
3. 拡張可能（系統的に設計したPythonパッケージ構成とバージョン管理）

## 2.2 用途
1. 組み込み制御システムの検証
2. 制御工学の学習

# 3. 使用例
Jupyter Notebookで実行する例を示す。

## 3.1 シミュレーション実行

```
import pandas as pd         # パッケージのインポート (pandas 表形式データ処理)
import tkmotion as tkm      # パッケージのインポート (モーションシミュレータ)

flow = tkm.MotionFlow()     # モーション制御フローのインスタンスを作成
flow.load_discrete_time()   # 離散時系列の設定をロード (デフォルト Δt=100[μs]、継続時間=6[s])
flow.load_motion_profile()  # モーションプロファイルの設定をロード (デフォルト 台形速度)
flow.load_controller()      # コントローラの設定をロード (デフォルト PIDコントローラ)
flow.load_plant()           # プラントの設定をロード (デフォルト 質量を持つ物体)
df = flow.execute()         # 制御フローを実行。結果をpandas.DataFrame形式で得る
```

## 3.2 実行結果をグラフで確認

### 3.2.1 物体の速度変化
DataFrameから「経過時間 "time_s"」と「物体速度 "obj_velocity_m_s"」を取り出し、<br>
グラフ描画パッケージ plotly.express でlineプロットを作成する。
```
import plotly.express as px
fig = px.line(df, x="time_s", y=["obj_velocity_m_s"], title="PhysicalObj Velocity")
fig.update_layout(
    xaxis=dict(title="time [s]"),
    yaxis=dict(title="velocity [m/s]"),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.7))
fig.show()
```
![速度 line plot](./img/tkmotion-PhysicalObj-vel-251130-01.png)

### 3.2.2 物体の位置変化
DataFrameから「経過時間 "time_s"」と「物体位置 "obj_position_m"」を取り出し、<br>
グラフ描画パッケージ plotly.express でlineプロットを作成する。
```
import plotly.express as px
fig = px.line(df, x="time_s", y=["obj_position_m"], title="PhysicalObj Position")
fig.update_layout(
    xaxis=dict(title="time [s]"),
    yaxis=dict(title="position [m]"),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
fig.show()
```
![位置 line plot](./img/tkmotion-PhysicalObj-pos-251130-01.png)

# 4. 設計

## 4.1 Pythonパッケージ（ディレクトリ）とモジュール（.pyファイル）の構成
```
tkmotion/
	__init__.py  # ディレクトリをPythonパッケージとして扱わせるためのスクリプトファイル
	flow/  # motion flow / モーション制御フロー
		__init__.py
		motion_flow.py
	time/  # time series / 時系列
		__init__.py
		discrete_time.py
		default_discrete_time.json  # 離散時系列 デフォルト設定
	prof/  # motion profile / モーションプロファイル
		__init__.py
		motion_profile.py
		default_motion_prof.json  # モーションプロファイル デフォルト設定
	ctrl/  # motion control / モーション制御
		__init__.py
		controller.py
		default_controller.json  # コントローラ デフォルト設定
	plant/  # plant (control target) / プラント (制御対象)
		__init__.py
		plant.py
		physical_object.py
		default_plant.json  # プラント デフォルト設定
	util/  # utility / ユーティリティ
		__init__.py
		utility.py
```

## 4.2 モジュールとクラス

### 4.2.1 パッケージ: tkmotion.flow
motion flow / モーションフロー

| モジュール | ver | クラス | 責務 | 主要特性 |
| -- | -- | -- | -- | -- |
| motion_flow.py | 0.1.0 | MotionFlow<br>(モーション制御フロー) | モーション指令の流れを司り、<br>シミュレーションを実行 | load_discrete_time()<br>load_motion_profile()<br>load_controller()<br>load_plant()<br>execute() |

### 4.2.2 パッケージ: tkmotion.time
time series / 時系列

| モジュール | ver | クラス | 責務 | 主要特性 |
| -- | -- | -- | -- | -- |
| discrete_time.py | 0.1.0 | DiscreteTime<br>(離散時間) | 間隔Δtの離散時系列を表現 | get_time_step_generator() |
| ↑ | ↑ | DiscreteTimeLoader<br>(離散時間ローダ) | 設定 (jsonファイル) を読み込み、<br>DiscreteTimeクラスのインスタンスを生成 | load() |

### 4.2.3 パッケージ: tkmotion.prof
motion profile / モーションプロファイル

| モジュール | ver | クラス | 責務 | 主要特性 |
| -- | -- | -- | -- | -- |
| motion_profile.py | 0.1.0 | MotionProfile<br>(モーションプロファイル) | モーションプロファイルのベースクラス。<br>モーションプロファイルの共通特性を定義 | calculate_cmd_vel_pos() |
| ↑ | ↑ | TrapezoidalMotionProfile<br>(台形モーションプロファイル) | 台形状に変化する速度（加速・定速・減速）から<br>指令速度・指令位置を計算する | ↑ |
| ↑ | ↑ | MotionProfileLoader<br>(モーションプロファイルローダ) | 設定 (jsonファイル) を読み込み、<br>MotionProfileクラスのインスタンスを生成 | load() |
| ↑ | ↑ | VelocityZeroOrMinusError<br>(速度ゼロ・マイナスエラー)  | 設定速度がゼロ、またはマイナスの例外を表す | - |
| ↑ | ↑ | AccelerationZeroOrMinusError<br>(加速度ゼロ・マイナスエラー) | 設定加速度がゼロ、またはマイナスの例外を表す | - |
| ↑ | ↑ | MovingLengthZeroError<br>(移動距離ゼロエラー) | 設定移動量がゼロの例外を表す | - |

### 4.2.4 パッケージ: tkmotion.ctrl
motion control / モーション制御

| モジュール | ver | クラス | 責務 | 主要特性 |
| -- | -- | -- | -- | -- |
| controller.py | 0.1.0 | Controller<br>(コントローラ) | コントローラのベースクラス。<br>コントローラの共通特性を定義 | reset()<br>calculate_force() |
| ↑ | ↑ | PIDController<br>(PIDコントローラ) | PID計算を実行するコントローラ<br>・Proportional 比例<br>・Integral 積分<br>・Derivative 微分 | kvp, kvi, kvd<br>kpp, kpi, kpd<br>reset()<br>calculate_force() |
| ↑ | ↑ | ControllerLoader<br>(コントローラローダ) | 設定 (jsonファイル) を読み込み、<br>Controllerクラスのインスタンスを生成 | load() |

### 4.2.5 パッケージ: tkmotion.plant
plant (control target)  / プラント (制御対象)

| モジュール | ver | クラス | 責務 | 主要特性 |
| -- | -- | -- | -- | -- |
| plant.py | 0.1.0 | Plant<br>(プラント) | 制御対象を表現する | physical_obj |
| ↑ | ↑ | PlantLoader<br>(プラントローダ) | プラントの設定 (jsonファイル) を読み込み、<br>Plantクラスと、Plantに属する各クラスのインスタンスを生成 | load() |
| ↑ | ↑ | PhysicalObject<br>(物理オブジェクト) | 現実の物体を表現する | mass<br>acc, vel, pos<br>reset()<br>apply_force() |

### 4.2.6 パッケージ: tkmotion.util
utility / ユーティリティ

| モジュール | ver | クラス | 責務 | 主要特性 |
| -- | -- | -- | -- | -- |
| utility.py | 0.1.0 | Utility<br>(ユーティリティ) | 共通の補助機能を定義する | is_config_compatible() |
| ↑ | ↑ | ConfigVersionIncompatibleError<br>(設定バージョン非互換エラー) | 設定バージョンに互換性がない例外を表す | - |

## 4.3 クラス図 (概要)

![クラス図 (概要)](./img/tkmotion-class-diagram-summary-251130-01.png)

# 5. バージョン管理

Python Packaging User Guide バージョニング (https://packaging.python.org/ja/latest/discussions/versioning/) の「セマンティックバージョニング」を採用する。

バージョン番号変更の規則（上記 Python Packaging User Guide より）
* APIの変更で互換性を失う時には major 番号、
* 後方互換性を保ったままで新機能を追加する場合には minor を、そして
* 後方互換性を維持したままのバグ修正の場合には patch を増加させる。

# 6. 開発環境

# 6.1 Pythonバージョン

```
> python --version

Python 3.13.1
```

# 6.2 Pythonパッケージ
```
> pip freeze

affine==2.4.0
anyio==4.9.0
argon2-cffi==23.1.0
argon2-cffi-bindings==21.2.0
arrow==1.3.0
asttokens==3.0.0
async-lru==2.0.5
attrs==25.3.0
babel==2.17.0
beautifulsoup4==4.13.4
black==25.1.0
bleach==6.2.0
branca==0.8.1
certifi==2025.4.26
cffi==1.17.1
charset-normalizer==3.4.1
click==8.1.8
click-plugins==1.1.1.2
cligj==0.7.2
colorama==0.4.6
comm==0.2.2
contourpy==1.3.2
cycler==0.12.1
debugpy==1.8.14
decorator==5.2.1
defusedxml==0.7.1
et_xmlfile==2.0.0
executing==2.2.0
fastjsonschema==2.21.1
feedparser==6.0.12
flake8==7.2.0
folium==0.20.0
fonttools==4.57.0
fqdn==1.5.1
geographiclib==2.0
geopandas==1.1.1
geopy==2.4.1
h11==0.16.0
html5lib==1.1
httpcore==1.0.9
httpx==0.28.1
idna==3.10
ipykernel==6.29.5
ipython==9.2.0
ipython_pygments_lexers==1.1.1
isoduration==20.11.0
jedi==0.19.2
Jinja2==3.1.6
joblib==1.4.2
json5==0.12.0
jsonpickle==4.1.1
jsonpointer==3.0.0
jsonschema==4.23.0
jsonschema-specifications==2025.4.1
jupyter-events==0.12.0
jupyter-lsp==2.2.5
jupyter_client==8.6.3
jupyter_core==5.7.2
jupyter_server==2.15.0
jupyter_server_terminals==0.5.3
jupyterlab==4.4.1
jupyterlab_pygments==0.3.0
jupyterlab_server==2.27.3
kiwisolver==1.4.8
lxml==6.0.0
MarkupSafe==3.0.2
matplotlib==3.10.1
matplotlib-inline==0.1.7
mccabe==0.7.0
mistune==3.1.3
mypy==1.15.0
mypy_extensions==1.1.0
narwhals==2.0.0
nbclient==0.10.2
nbconvert==7.16.6
nbformat==5.10.4
nest-asyncio==1.6.0
networkx==3.5
notebook_shim==0.2.4
numpy==2.2.5
opencv-python==4.12.0.88
openpyxl==3.1.5
overrides==7.7.0
packaging==25.0
pandas==2.2.3
pandocfilters==1.5.1
parso==0.8.4
pathspec==0.12.1
pillow==11.2.1
platformdirs==4.3.7
plotly==6.2.0
prometheus_client==0.21.1
prompt_toolkit==3.0.51
psutil==7.0.0
pure_eval==0.2.3
pyarrow==21.0.0
pycodestyle==2.13.0
pycparser==2.22
pyflakes==3.3.2
Pygments==2.19.1
pyogrio==0.11.0
pyparsing==3.2.3
pyproj==3.7.1
python-dateutil==2.9.0.post0
python-json-logger==3.3.0
pytz==2025.2
pyvis==0.3.2
pywin32==310
pywinpty==2.0.15
PyYAML==6.0.2
pyzmq==26.4.0
rasterio==1.4.3
referencing==0.36.2
requests==2.32.3
retrying==1.3.4
rfc3339-validator==0.1.4
rfc3986-validator==0.1.1
rpds-py==0.24.0
scikit-learn==1.6.1
scipy==1.15.2
Send2Trash==1.8.3
setuptools==80.1.0
sgmllib3k==1.0.0
shapely==2.1.1
six==1.17.0
sniffio==1.3.1
soupsieve==2.7
stack-data==0.6.3
terminado==0.18.1
threadpoolctl==3.6.0
tinycss2==1.4.0
tornado==6.4.2
traitlets==5.14.3
types-python-dateutil==2.9.0.20241206
typing_extensions==4.13.2
tzdata==2025.2
uri-template==1.3.0
urllib3==2.4.0
wcwidth==0.2.13
webcolors==24.11.1
webencodings==0.5.1
websocket-client==1.8.0
xyzservices==2025.4.0
```
