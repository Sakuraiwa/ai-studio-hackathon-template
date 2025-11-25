#!/usr/bin/env python3
"""
Level 3 - Issue H のテストスクリプト
問題: 観光地検索でGLOB演算子を使用しているため大文字小文字が区別される（検索が機能しない）
期待: LIKE演算子を使用して大文字小文字を区別しない検索を実現すること
"""

import sys
import re
from pathlib import Path


def check_glob_like_usage():
    """
    spot_repository.pyのfind_by_keywordメソッドでLIKE演算子が使われているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    spot_repo = project_root / "app" / "repositories" / "spot_repository.py"

    if not spot_repo.exists():
        print(f"❌ エラー: {spot_repo} が見つかりません")
        return False

    with open(spot_repo, 'r', encoding='utf-8') as f:
        content = f.read()

    print("検索クエリの演算子チェックを開始します\n")

    # コメントを除外したコードを取得
    lines = content.split('\n')
    in_multiline_comment = False
    in_search_spots = False
    method_code = []

    for line in lines:
        stripped = line.strip()

        # find_by_keywordメソッドの範囲を特定
        if 'def find_by_keyword' in line:
            in_search_spots = True

        if in_search_spots:
            # コメント行でない場合のみ追加
            if not stripped.startswith('#'):
                method_code.append(line)
            # 次のメソッドの定義が来たら終了
            if line.strip().startswith('def ') and 'def find_by_keyword' not in line:
                in_search_spots = False

    method_code_str = '\n'.join(method_code)

    # 演算子のチェック
    has_glob = bool(re.search(r'\bGLOB\b', method_code_str, re.IGNORECASE))
    has_like = bool(re.search(r'\bLIKE\b', method_code_str, re.IGNORECASE))

    print("チェック結果:")
    print(f"  GLOB演算子の使用: {'❌ 検出（問題あり）' if has_glob else '✅ 未検出'}")
    print(f"  LIKE演算子の使用: {'✅ 検出' if has_like else '❌ 未検出'}")
    print()

    # GLOBが使われておらず、LIKEが使われていればOK
    if not has_glob and has_like:
        print("✅ 合格: LIKE演算子を使用した検索が実装されています")
        return True
    elif has_glob:
        print("❌ 不合格: GLOB演算子が使われています（大文字小文字を区別してしまいます）。Issue Hの「どうあるべきか」を確認してください。")
        return False
    else:
        print("⚠️  GLOB演算子は見つかりませんでしたが、LIKE演算子も確認できません")
        return False


def main():
    print("=" * 60)
    print("Level 3 - Issue H: 観光地検索のGLOB/LIKE演算子チェック")
    print("=" * 60)

    result = check_glob_like_usage()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
