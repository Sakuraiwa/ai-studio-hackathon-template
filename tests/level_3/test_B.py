#!/usr/bin/env python3
"""
Level 3 - Issue B のテストスクリプト
問題: 月パラメータのバリデーションがない（13月、0月なども受け付ける）
期待: 月は1〜12の範囲でバリデーションを行い、範囲外の場合はエラーを返すこと
"""

import sys
import re
from pathlib import Path


def check_month_validation():
    """
    event_repository.pyのfind_by_monthメソッドで月のバリデーションが実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    event_repo = project_root / "app" / "repositories" / "event_repository.py"

    if not event_repo.exists():
        print(f"❌ エラー: {event_repo} が見つかりません")
        return False

    with open(event_repo, 'r', encoding='utf-8') as f:
        content = f.read()

    print("月のバリデーション実装確認を開始します\n")

    # コメントを除外したコードを取得
    lines = content.split('\n')
    in_multiline_comment = False
    in_find_by_month = False
    method_code = []

    for line in lines:
        stripped = line.strip()

        # find_by_monthメソッドの範囲を特定
        if 'def find_by_month' in line:
            in_find_by_month = True

        if in_find_by_month:
            # コメント行でない場合のみ追加
            if not stripped.startswith('#'):
                method_code.append(line)
            # 次のメソッドの定義が来たら終了
            if line.strip().startswith('def ') and 'def find_by_month' not in line:
                in_find_by_month = False

    method_code_str = '\n'.join(method_code)

    # バリデーションのパターン
    # パターン1: if文での範囲チェック（month < 1 or month > 12など）
    has_range_check_lt = bool(re.search(r'(month|int\(month\))\s*<\s*1', method_code_str))
    has_range_check_gt = bool(re.search(r'(month|int\(month\))\s*>\s*12', method_code_str))
    has_range_check_combined = bool(re.search(r'1\s*<=.*month.*<=\s*12', method_code_str))
    has_range_check_not_in = bool(re.search(r'not\s+in\s+range\(1,\s*13\)', method_code_str))

    # パターン2: エラーを返す処理
    has_error_return = bool(re.search(r'return\s+\[\]|return\s+None', method_code_str))
    has_exception = bool(re.search(r'raise|ValueError|Exception', method_code_str))

    print("チェック結果:")
    print(f"  月の範囲チェック（< 1）: {'✅ あり' if has_range_check_lt else '❌ なし'}")
    print(f"  月の範囲チェック（> 12）: {'✅ あり' if has_range_check_gt else '❌ なし'}")
    print(f"  月の範囲チェック（1-12）: {'✅ あり' if has_range_check_combined else '❌ なし'}")
    print(f"  月の範囲チェック（not in range）: {'✅ あり' if has_range_check_not_in else '❌ なし'}")
    print(f"  エラー処理: {'✅ あり' if (has_error_return or has_exception) else '❌ なし'}")
    print()

    # いずれかのバリデーションパターンが実装されていればOK
    has_validation = (has_range_check_lt and has_range_check_gt) or has_range_check_combined or has_range_check_not_in

    if has_validation:
        print("✅ 合格: 月のバリデーションが実装されています")
        return True
    else:
        print("❌ 不合格: 月のバリデーションが実装されていません。Issue Bの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 3 - Issue B: 月パラメータのバリデーションチェック")
    print("=" * 60)

    result = check_month_validation()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
