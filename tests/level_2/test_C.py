#!/usr/bin/env python3
"""
Level 2 - Issue C のテストスクリプト
問題: formatDistance関数でreturn文が抜けているため、undefinedを返してしまう
期待: 各分岐でreturn文を追加し、正しく距離文字列を返すこと
"""

import sys
import re
from pathlib import Path


def check_source_code():
    """
    api-client.jsのformatDistance関数でreturn文が追加されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    api_client_js = project_root / "frontend" / "api-client.js"

    if not api_client_js.exists():
        print(f"❌ エラー: {api_client_js} が見つかりません")
        return False

    with open(api_client_js, 'r', encoding='utf-8') as f:
        content = f.read()

    print("formatDistance関数のreturn文チェックを開始します\n")

    # formatDistance関数を抽出
    function_match = re.search(
        r'function\s+formatDistance\s*\([^)]*\)\s*\{([^}]+)\}',
        content,
        re.DOTALL
    )

    if not function_match:
        print("❌ 不合格: formatDistance関数が見つかりません")
        return False

    function_body = function_match.group(1)

    # コメント行を除外
    lines = function_body.split('\n')
    active_lines = []
    for line in lines:
        stripped = line.strip()
        # コメント行やコメントアウトされた行を除外
        if not stripped.startswith('//') and not stripped.startswith('*'):
            active_lines.append(line)

    active_code = '\n'.join(active_lines)

    # return文の存在チェック（最低2つ必要: if分岐とelse分岐）
    return_count = len(re.findall(r'\breturn\b', active_code))

    if return_count < 2:
        print(f"❌ 不合格: return文が不足しています（見つかった数: {return_count}個、必要: 2個以上）")
        print("\nformatDistance関数には少なくとも2つのreturn文が必要です：")
        print("  1. meters >= 1000 の場合のreturn")
        print("  2. else の場合のreturn")
        print("\n現在のコード:")
        print(function_body[:200] + "...")
        return False

    # より詳細なチェック: return文が適切な位置にあるか
    # パターン1: return (meters / 1000).toFixed(1) + 'km'
    km_return = re.search(r'return\s+\([^)]*meters[^)]*\/[^)]*1000[^)]*\)\.toFixed\(1\)\s*\+\s*[\'"]km[\'"]', active_code)
    # パターン2: return meters + 'm'
    m_return = re.search(r'return\s+meters\s*\+\s*[\'"]m[\'"]', active_code)

    if not km_return:
        print("❌ 不合格: km表示のreturn文が正しく実装されていません")
        print("期待される形式: return (meters / 1000).toFixed(1) + 'km';")
        return False

    if not m_return:
        print("❌ 不合格: m表示のreturn文が正しく実装されていません")
        print("期待される形式: return meters + 'm';")
        return False

    print("✅ 合格: formatDistance関数にreturn文が正しく実装されています")
    print(f"  - km表示のreturn文: 実装済み")
    print(f"  - m表示のreturn文: 実装済み")
    return True


def main():
    print("=" * 60)
    print("Level 2 - Issue C: formatDistance関数のreturn文チェック")
    print("=" * 60)
    print()

    success = check_source_code()

    print()
    print("=" * 60)
    if success:
        print("✅ テスト合格")
        print()
        print("formatDistance関数が正しく修正されています。")
        print("距離が適切にフォーマットされて表示されます。")
        sys.exit(0)
    else:
        print("❌ テスト不合格")
        print()
        print("formatDistance関数のreturn文が不足しています。")
        print("Issue Cの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
