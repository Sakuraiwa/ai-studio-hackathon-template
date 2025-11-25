#!/usr/bin/env python3
"""
Level 2 - Issue F のテストスクリプト
問題: チェックイン機能で未来の日付を選択できてしまう
期待: 未来の日付を選択した場合、エラーメッセージを表示してチェックインを拒否すること
"""

import sys
import re
from pathlib import Path


def check_source_code():
    """
    index.htmlのcheckIn関数で日付バリデーションが実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    index_html = project_root / "frontend" / "index.html"

    if not index_html.exists():
        print(f"❌ エラー: {index_html} が見つかりません")
        return False

    with open(index_html, 'r', encoding='utf-8') as f:
        content = f.read()

    print("checkIn関数の日付バリデーションチェックを開始します\n")

    # checkIn関数を抽出
    function_match = re.search(
        r'function\s+checkIn\s*\([^)]*\)\s*\{(.*?)\n\s*\}',
        content,
        re.DOTALL
    )

    if not function_match:
        print("❌ 不合格: checkIn関数が見つかりません")
        return False

    function_body = function_match.group(1)

    # コメントアウトされていないコードを抽出
    lines = function_body.split('\n')
    active_lines = []
    for line in lines:
        stripped = line.strip()
        # コメント行を除外
        if not stripped.startswith('//') and '/*' not in stripped:
            active_lines.append(line)

    active_code = '\n'.join(active_lines)

    # 必要な要素のチェック
    checks_passed = []
    checks_failed = []

    # 1. new Date()で選択された日付をDate型に変換しているか
    date_conversion = re.search(r'new\s+Date\s*\(\s*selectedDate\s*\)', active_code) or \
                     re.search(r'new\s+Date\s*\(\s*[\'"]?\$\{selectedDate\}[\'"]?\s*\)', active_code)

    if date_conversion:
        checks_passed.append("選択された日付のDate型への変換")
    else:
        checks_failed.append("選択された日付のDate型への変換（new Date(selectedDate)）")

    # 2. 今日の日付を取得しているか
    today_date = re.search(r'(const|let|var)\s+today\s*=\s*new\s+Date\s*\(\s*\)', active_code)

    if today_date:
        checks_passed.append("今日の日付の取得")
    else:
        checks_failed.append("今日の日付の取得（const today = new Date()）")

    # 3. 日付の比較を行っているか
    date_comparison = re.search(r'(selected|selectedDate)\s*>\s*(today|todayDate)', active_code) or \
                     re.search(r'(selected|selectedDate)\.getTime\(\)\s*>\s*(today|todayDate)\.getTime\(\)', active_code)

    if date_comparison:
        checks_passed.append("日付の比較処理")
    else:
        checks_failed.append("日付の比較処理（selected > today）")

    # 4. 「未来の日付は選択できません」のエラーメッセージ
    error_message = re.search(r'[\'"]未来の日付は選択できません[\'"]', active_code)

    if error_message:
        checks_passed.append("エラーメッセージの表示")
    else:
        checks_failed.append("エラーメッセージ「未来の日付は選択できません」")

    # 結果の表示
    print("チェック結果:")
    print()

    for check in checks_passed:
        print(f"  ✅ {check}")

    for check in checks_failed:
        print(f"  ❌ {check}")

    print()

    if checks_failed:
        print("❌ 不合格: 日付バリデーションが不完全です")
        print()
        print("不足している実装:")
        for check in checks_failed:
            print(f"  - {check}")
        print()
        print("ヒント:")
        print("  1. new Date(selectedDate) で選択された日付をDate型に変換")
        print("  2. const today = new Date() で今日の日付を取得")
        print("  3. selected > today で未来かどうかを比較")
        print("  4. 未来の場合は alert('未来の日付は選択できません') を表示")
        return False

    print("✅ 合格: 日付バリデーションが正しく実装されています")
    return True


def main():
    print("=" * 60)
    print("Level 2 - Issue F: チェックイン機能の日付バリデーション")
    print("=" * 60)
    print()

    success = check_source_code()

    print()
    print("=" * 60)
    if success:
        print("✅ テスト合格")
        print()
        print("チェックイン機能の日付バリデーションが正しく実装されています。")
        print("未来の日付を選択した場合、エラーメッセージが表示されます。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("日付バリデーションが不足しています。")
        print("Issue Fの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
