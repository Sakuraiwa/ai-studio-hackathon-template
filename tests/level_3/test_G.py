#!/usr/bin/env python3
"""
Level 3 - Issue G のテストスクリプト
問題: 平均評価がNULLの場合のチェックがなく、round()実行時にエラーが発生する
期待: NULLチェックを行い、NULLの場合は0または適切なデフォルト値を設定すること
"""

import sys
import re
from pathlib import Path


def check_null_handling():
    """
    stats_service.pyのget_summaryメソッドでNULLハンドリングが実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    stats_service = project_root / "app" / "services" / "stats_service.py"

    if not stats_service.exists():
        print(f"❌ エラー: {stats_service} が見つかりません")
        return False

    with open(stats_service, 'r', encoding='utf-8') as f:
        content = f.read()

    print("NULLハンドリングの実装確認を開始します\n")

    # コメントを除外したコードを取得
    lines = content.split('\n')
    in_multiline_comment = False
    in_get_summary = False
    method_code = []

    for line in lines:
        stripped = line.strip()

        # get_summaryメソッドの範囲を特定
        if 'def get_summary' in line and 'get_summary_stats' not in line:
            in_get_summary = True

        if in_get_summary:
            # コメント行でない場合のみ追加
            if not stripped.startswith('#'):
                method_code.append(line)
            # 次のメソッドの定義が来たら終了
            if line.strip().startswith('def ') and 'def get_summary' not in line:
                in_get_summary = False

    method_code_str = '\n'.join(method_code)

    # NULLチェックのパターン
    # パターン1: if文でNoneチェック
    has_none_check = bool(re.search(r"if.*avg_rating_overall.*is None|if.*avg_rating_overall.*== None", method_code_str))
    has_not_none_check = bool(re.search(r"if.*avg_rating_overall.*is not None|if.*avg_rating_overall.*!= None", method_code_str))

    # パターン2: or演算子でデフォルト値を設定
    has_or_default = bool(re.search(r"avg_rating_overall\s+or\s+0", method_code_str))

    # パターン3: 三項演算子でチェック
    has_ternary = bool(re.search(r"0\s+if.*avg_rating_overall.*is None", method_code_str))

    # パターン4: round()の前にチェック
    # avg_rating_overallを含むif文の中でround()が呼ばれているかをチェック
    has_check_before_round = bool(re.search(r"if\s+.*avg_rating_overall.*:\s*\n\s*.*round\s*\(\s*.*avg_rating", method_code_str, re.DOTALL))

    print("チェック結果:")
    print(f"  None/NULLチェック（if is None）: {'✅ あり' if has_none_check else '❌ なし'}")
    print(f"  None/NULLチェック（if is not None）: {'✅ あり' if has_not_none_check else '❌ なし'}")
    print(f"  デフォルト値設定（or演算子）: {'✅ あり' if has_or_default else '❌ なし'}")
    print(f"  三項演算子でのチェック: {'✅ あり' if has_ternary else '❌ なし'}")
    print(f"  round()前のチェック: {'✅ あり' if has_check_before_round else '❌ なし'}")
    print()

    # いずれかのNULLハンドリングパターンが実装されていればOK
    if has_none_check or has_not_none_check or has_or_default or has_ternary or has_check_before_round:
        print("✅ 合格: NULLハンドリングが実装されています")
        return True
    else:
        print("❌ 不合格: NULLハンドリングが実装されていません。Issue Gの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 3 - Issue G: 平均評価のNULLハンドリングチェック")
    print("=" * 60)

    result = check_null_handling()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
