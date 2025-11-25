#!/usr/bin/env python3
"""
Level 3 - Issue F のテストスクリプト
問題: レビュー内容の文字数制限チェックがない（10万文字でも投稿可能）
期待: レビュー内容の文字数を制限し（例: 1000文字）、超えた場合はエラーを返すこと
"""

import sys
import re
from pathlib import Path


def check_character_limit():
    """
    review_service.pyのcreate_reviewメソッドで文字数制限が実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    review_service = project_root / "app" / "services" / "review_service.py"

    if not review_service.exists():
        print(f"❌ エラー: {review_service} が見つかりません")
        return False

    with open(review_service, 'r', encoding='utf-8') as f:
        content = f.read()

    print("文字数制限の実装確認を開始します\n")

    # コメントを除外したコードを取得
    lines = content.split('\n')
    in_multiline_comment = False
    in_create_review = False
    method_code = []

    for line in lines:
        stripped = line.strip()

        # create_reviewメソッドの範囲を特定
        if 'def create_review' in line and 'create_review_with_photo' not in line:
            in_create_review = True

        if in_create_review:
            # コメント行でない場合のみ追加
            if not stripped.startswith('#'):
                method_code.append(line)
            # 次のメソッドの定義が来たら終了
            if line.strip().startswith('def ') and 'def create_review' not in line:
                in_create_review = False

    method_code_str = '\n'.join(method_code)

    # 文字数チェックのパターン
    # パターン1: len()を使った長さチェック
    has_len_check = bool(re.search(r"len\s*\(\s*review_data\['review_content'\]\s*\)\s*>", method_code_str))
    has_len_check_alt = bool(re.search(r"len\s*\(\s*review_content\s*\)\s*>", method_code_str))

    # パターン2: エラーメッセージ
    has_length_error = bool(re.search(r'文字.*制限|長すぎ|文字数|超え', method_code_str))

    print("チェック結果:")
    print(f"  len()による長さチェック: {'✅ あり' if (has_len_check or has_len_check_alt) else '❌ なし'}")
    print(f"  文字数エラーメッセージ: {'✅ あり' if has_length_error else '❌ なし'}")
    print()

    if (has_len_check or has_len_check_alt) and has_length_error:
        print("✅ 合格: レビュー内容の文字数制限が実装されています")
        return True
    elif (has_len_check or has_len_check_alt):
        print("⚠️  文字数チェックはありますが、エラーメッセージが確認できません")
        return True
    else:
        print("❌ 不合格: レビュー内容の文字数制限が実装されていません。Issue Fの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 3 - Issue F: レビュー内容の文字数制限チェック")
    print("=" * 60)

    result = check_character_limit()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
