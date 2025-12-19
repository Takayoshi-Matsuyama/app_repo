# Copyright 2025 Takayoshi Matsuyama
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

# ユーティリティモジュールのバージョン情報
# (utility module version information)
module_version = "0.3.0"


class ConfigVersionIncompatibleError(Exception):
    """設定バージョンが互換性のない場合に発生する例外
    (Exception raised for incompatible configuration version)"""

    pass


class Utility:
    """ユーティリティクラス (Utility class)"""

    @staticmethod
    def get_module_version() -> str:
        """ユーティリティモジュールのバージョン (Utility module version)"""
        return module_version

    @staticmethod
    def is_config_compatible(module_version: str, config_version: str) -> bool:
        """モジュールバージョンと設定バージョンの互換性をチェックする
        (Checks compatibility between module version and configuration version)

        Args:
            module_version (str): モジュールのバージョン文字列 (Module version string)
            config_version (str): 設定のバージョン文字列 (Configuration version string)

        Returns:
            bool: 互換性がある場合はTrue、ない場合はFalse (True if compatible, False otherwise)

        Raises:
            ValueError: バージョン文字列の形式が不正な場合 (If the version string format is invalid)
        """
        try:
            module_major, module_minor, module_patch = [
                int(x) for x in module_version.split(".")
            ]
            config_major, config_minor, config_patch = [
                int(x) for x in config_version.split(".")
            ]
            # メジャーバージョン番号が異なる場合、互換性がない
            # (if major version numbers differ, not compatible)
            return module_major == config_major
        except Exception as e:
            message = (
                f"Invalid version format: module_version={module_version}"
                f", config_version={config_version}"
            )
            raise ValueError(message) from e
