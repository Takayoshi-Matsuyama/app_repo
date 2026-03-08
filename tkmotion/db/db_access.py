# Copyright 2026 Takayoshi Matsuyama
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import psycopg
from psycopg import OperationalError

# データベースモジュールのバージョン情報
# (Database module version information)
module_version = "0.3.1"


class DBAccessor:
    """データベースアクセサークラスの基底クラス
    (Base class for database accessor classes)
    """

    # クラス変数 Dockerコンテナ内のPostgreSQLサーバに接続するためのパラメータ
    connection_params = {
        "host": "127.0.0.1",
        "port": "5432",
        "user": "postgres",
        "password": "secret",
        "dbname": "postgres",  # デフォルトのデータベース名
    }

    def connect(self) -> None:
        """データベースに接続するメソッド
        (Method to connect to the database)

        予め、DockerのPostgreSQL用コンテナを起動しておく必要があります。
        (You need to have a PostgreSQL Docker container running beforehand.)
        """
        print("Connecting to the database...")
        try:
            # connect() で接続を確立します
            # autocommit=True にしておくと、後で手動commitが不要になりテスト時に便利です
            with psycopg.connect(**self.connection_params, autocommit=True) as conn:

                # 接続情報の確認
                print("接続成功！")
                print(f"Backend PID: {conn.info.backend_pid}")

                # 念のため、簡単なSQLを実行して応答を確認します
                with conn.cursor() as cur:
                    cur.execute("SELECT version();")
                    db_version = cur.fetchone()
                    print(f"Database Version: {db_version[0]}")

        except OperationalError as e:
            print(f"接続失敗...: {e}")

    def show_table_schema(self, table_name: str):
        """指定したテーブルのスキーマを表示するメソッド
        (Method to display the schema of a specified table)

        Args:
            table_name (str): スキーマを表示したいテーブルの名前 (Name of the table whose schema you want to display)
        """
        print(f"Showing schema for table: {table_name}")
        # information_schema.columns から列の定義情報を取得するSQL

        sql = """
        SELECT 
            column_name, 
            data_type, 
            column_default, 
            is_nullable
        FROM 
            information_schema.columns
        WHERE 
            table_name = %s
        ORDER BY 
            ordinal_position;
        """

        try:
            with psycopg.connect(**self.connection_params) as conn:
                with conn.cursor() as cur:
                    # プレースホルダを使ってテーブル名を渡します
                    cur.execute(sql, (table_name,))
                    columns = cur.fetchall()

                    if not columns:
                        print(f"テーブル '{table_name}' が見つかりません。")
                        return

                    # 結果を見やすく整形して出力
                    print(f"=== テーブル '{table_name}' のスキーマ定義 ===")
                    print(
                        "{'列名 (Column Name)':<25} | {'データ型 (Data Type)':<20} | "
                        "{'デフォルト値 (Default)':<30} | {'NULL許可'}"
                    )
                    print("-" * 100)

                    for col in columns:
                        col_name = col[0]
                        data_type = col[1]
                        # デフォルト値が設定されていない場合は 'None' と表示
                        col_default = str(col[2]) if col[2] is not None else "None"
                        is_nullable = col[3]

                        print(
                            f"{col_name:<25} | {data_type:<20} | {col_default:<30} | {is_nullable}"
                        )

        except Exception as e:
            print(f"スキーマ取得エラー: {e}")

    def fetch_plant_params(self, plant_id: int) -> dict | None:
        select_sql = """
        SELECT mass_kg, damper_Ns_m, spring_N_m, spring_balance_pos_m, 
            static_friction_coeff, dynamic_friction_coeff
        FROM mds_plant
        WHERE id = %s;
        """

        try:
            with psycopg.connect(**self.connection_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(select_sql, (plant_id,))
                    record = cur.fetchone()

                    if record:
                        # 取得したタプルデータを辞書型に変換
                        return {
                            "mass_kg": record[0],
                            "damper_Ns_m": record[1],
                            "spring_N_m": record[2],
                            "spring_balance_pos_m": record[3],
                            "static_friction_coeff": record[4],
                            "dynamic_friction_coeff": record[5],
                        }
                    else:
                        print("指定されたIDのデータが見つかりません。")
                        return None

        except Exception as e:
            print(f"データ読み込みエラー: {e}")
            return None
