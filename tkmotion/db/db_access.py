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

# データベースモジュールのバージョン情報
# (Database module version information)
module_version = "0.3.1"


class DBAccessor:
    """データベースアクセサークラスの基底クラス
    (Base class for database accessor classes)
    """

    def connect(self) -> None:
        """データベースに接続するメソッド
        (Method to connect to the database)
        """
        raise NotImplementedError("Subclasses must implement this method")

    def disconnect(self) -> None:
        """データベースから切断するメソッド
        (Method to disconnect from the database)
        """
        raise NotImplementedError("Subclasses must implement this method")
