#!/usr/bin/env python3
"""
Level 3 - Issue I のテストスクリプト
問題: イベントコントローラーでエラーハンドリングが不十分（例外発生時にスタックトレースが露出）
期待: try-exceptでエラーをキャッチして適切なエラーレスポンスを返すこと
"""

import sys
import re
from pathlib import Path


def check_error_handling():
    """
    event_controller.pyのget_eventsメソッドでエラーハンドリングが実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    event_controller = project_root / "app" / "controllers" / "event_controller.py"

    if not event_controller.exists():
        print(f"❌ エラー: {event_controller} が見つかりません")
        return False

    with open(event_controller, 'r', encoding='utf-8') as f:
        content = f.read()

    print("エラーハンドリングの実装確認を開始します\n")

    # コメントを除外したコードを取得
    lines = content.split('\n')
    in_multiline_comment = False
    in_get_events = False
    method_code = []

    for line in lines:
        stripped = line.strip()

        if '/*' in stripped or "'''" in stripped or '"""' in stripped:
            in_multiline_comment = not in_multiline_comment

        if in_multiline_comment:
            continue

        # get_eventsメソッドの範囲を特定
        if 'def get_events' in line:
            in_get_events = True

        if in_get_events:
            # コメント行でない場合のみ追加
            if not stripped.startswith('#'):
                method_code.append(line)
            # 次のメソッドやルートの定義が来たら終了
            if (line.strip().startswith('def ') or line.strip().startswith('@')) and 'def get_events' not in line and '@event_bp.route' not in line:
                in_get_events = False

    method_code_str = '\n'.join(method_code)

    # エラーハンドリングのパターン
    has_try = bool(re.search(r'\btry\s*:', method_code_str))
    has_except = bool(re.search(r'\bexcept\s+', method_code_str))
    has_error_response = bool(re.search(r"jsonify\s*\(\s*\{.*['\"]error['\"]", method_code_str))
    has_status_code = bool(re.search(r'\),\s*\d{3}\s*$', method_code_str, re.MULTILINE))

    print("チェック結果:")
    print(f"  try文の使用: {'✅ あり' if has_try else '❌ なし'}")
    print(f"  except文の使用: {'✅ あり' if has_except else '❌ なし'}")
    print(f"  エラーレスポンス: {'✅ あり' if has_error_response else '❌ なし'}")
    print(f"  HTTPステータスコード: {'✅ あり' if has_status_code else '❌ なし'}")
    print()

    if has_try and has_except:
        print("✅ 合格: エラーハンドリングが実装されています")
        return True
    else:
        print("❌ 不合格: エラーハンドリングが実装されていません。Issue Iの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 3 - Issue I: イベントコントローラーのエラーハンドリングチェック")
    print("=" * 60)

    result = check_error_handling()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
