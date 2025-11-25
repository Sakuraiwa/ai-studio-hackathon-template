#!/usr/bin/env python3
"""
Level 3 - Issue J のテストスクリプト
問題: レビュー削除時に画像ファイルの削除処理が抜けている（ディスク容量を圧迫）
期待: レビュー削除時に関連する画像ファイルも削除すること
"""

import sys
import re
from pathlib import Path


def check_file_deletion():
    """
    review_service.pyのdelete_reviewメソッドで画像ファイル削除が実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    review_service = project_root / "app" / "services" / "review_service.py"

    if not review_service.exists():
        print(f"❌ エラー: {review_service} が見つかりません")
        return False

    with open(review_service, 'r', encoding='utf-8') as f:
        content = f.read()

    print("画像ファイル削除処理の実装確認を開始します\n")

    # コメントを除外したコードを取得
    lines = content.split('\n')
    in_multiline_comment = False
    in_delete_review = False
    method_code = []

    for line in lines:
        stripped = line.strip()

        # delete_reviewメソッドの範囲を特定
        if 'def delete_review' in line:
            in_delete_review = True

        if in_delete_review:
            # コメント行でない場合のみ追加
            if not stripped.startswith('#'):
                method_code.append(line)
            # 次のメソッドの定義が来たら終了
            if line.strip().startswith('def ') and 'def delete_review' not in line:
                in_delete_review = False

    method_code_str = '\n'.join(method_code)

    # 画像ファイル削除のパターン
    # パターン1: photo_filenameのチェック
    has_photo_check = bool(re.search(r"if.*photo_filename|if.*get\('photo_filename'\)", method_code_str))

    # パターン2: ファイル削除処理
    has_delete_photo = bool(re.search(r'delete_review_photo|delete.*photo|os\.remove|unlink', method_code_str))

    # パターン3: file_serviceの呼び出し
    has_file_service = bool(re.search(r'file_service|FileService', method_code_str))

    print("チェック結果:")
    print(f"  photo_filenameのチェック: {'✅ あり' if has_photo_check else '❌ なし'}")
    print(f"  ファイル削除処理: {'✅ あり' if has_delete_photo else '❌ なし'}")
    print(f"  file_serviceの使用: {'✅ あり' if has_file_service else '❌ なし'}")
    print()

    # photo_filenameのチェックとファイル削除処理が両方あればOK
    if has_photo_check and has_delete_photo:
        print("✅ 合格: 画像ファイル削除処理が実装されています")
        return True
    elif has_delete_photo:
        print("⚠️  ファイル削除処理はありますが、photo_filenameのチェックが確認できません")
        return True
    else:
        print("❌ 不合格: 画像ファイル削除処理が実装されていません。Issue Jの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 3 - Issue J: レビュー削除時の画像ファイル削除チェック")
    print("=" * 60)

    result = check_file_deletion()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
