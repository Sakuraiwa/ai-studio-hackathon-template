#!/usr/bin/env python3
"""
Level 3 - Issue D のテストスクリプト
問題: レビュー投稿フォームで、JavaScriptによる星評価のバリデーションが実装されていない
期待: 星評価が0の場合、JavaScriptでエラーメッセージを表示して投稿を防ぐこと
"""

import sys
import re
from pathlib import Path
from playwright.sync_api import sync_playwright


def check_source_code():
    """
    spot-detail.jsで星評価0のバリデーションが実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    spot_detail_js = project_root / "frontend" / "spot-detail.js"

    if not spot_detail_js.exists():
        print(f"❌ エラー: {spot_detail_js} が見つかりません")
        return False

    with open(spot_detail_js, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # コメントアウトされていないコードのみをチェック
    active_code = []
    in_multiline_comment = False

    for line in lines:
        stripped = line.strip()

        if '/*' in stripped:
            in_multiline_comment = True

        if '*/' in stripped:
            in_multiline_comment = False
            continue

        if in_multiline_comment or stripped.startswith('//'):
            continue

        active_code.append(line)

    active_code_str = ''.join(active_code)

    # 星評価0のチェックが実装されているかを確認
    # パターン: rating === '0' または rating == '0' または rating === 0
    has_rating_check = bool(re.search(r"rating\s*===?\s*['\"]?0['\"]?", active_code_str))

    if has_rating_check:
        print("✅ コードチェック合格: 星評価0のバリデーションが実装されています")
        return True
    else:
        print("❌ コードチェック不合格: 星評価0のバリデーションが実装されていません")
        return False


def test_rating_validation():
    """
    レビュー投稿フォームで星評価0の場合にバリデーションが動作するかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            print("\n【ステップ1: 実際の動作をチェック】")

            # spot-detail.htmlにアクセス
            page.goto('http://localhost:3001/spot-detail.html?id=1', wait_until='networkidle')

            # ログイン状態かチェック（ログインしていないとレビューフォームが表示されない）
            review_form = page.locator('#reviewForm')

            if review_form.count() == 0:
                print("⚠️  レビューフォームが見つかりませんでした")
                print("  （ログインが必要な可能性があります。ソースコードをチェックします）\n")
                browser.close()
                print("【ステップ2: ソースコードをチェック】")
                return check_source_code()

            print("レビューフォームを見つけました")

            # レビューテキストを入力前にフォームが表示されているか確認
            review_text = page.locator('#reviewText')

            # フォームが表示されていない場合はソースコードチェックにフォールバック
            if not review_text.is_visible():
                print("⚠️  レビューフォームが表示されていません")
                print("  （ログイン状態が必要です。ソースコードをチェックします）\n")
                browser.close()
                print("【ステップ2: ソースコードをチェック】")
                return check_source_code()

            # レビューセクションまでスクロール
            page.evaluate("document.querySelector('#reviewForm').scrollIntoView()")
            page.wait_for_timeout(500)

            # レビューテキストを入力（星評価は0のまま）
            review_text.fill('テスト用のレビューです')

            # 星評価が0のまま投稿ボタンをクリック
            # HTMLのrequired属性を一時的に削除してJavaScriptバリデーションのみをテスト
            page.evaluate("""
                const ratingInput = document.getElementById('ratingValue');
                if (ratingInput) {
                    ratingInput.removeAttribute('required');
                }
            """)

            # ダイアログ（alert）をキャプチャ
            dialog_message = None

            def handle_dialog(dialog):
                nonlocal dialog_message
                dialog_message = dialog.message
                dialog.accept()

            page.on('dialog', handle_dialog)

            # 投稿ボタンをクリック
            submit_button = page.locator('#reviewForm button[type="submit"]')
            submit_button.click()
            page.wait_for_timeout(1000)

            browser.close()

            # アラートが表示されたかチェック
            if dialog_message:
                print(f"✅ アラートが表示されました: 「{dialog_message}」")
                # 星評価に関するメッセージかチェック
                if '星' in dialog_message or '評価' in dialog_message or 'rating' in dialog_message.lower():
                    print("✅ 合格: 星評価0のバリデーションが正しく動作しています")
                    return True
                else:
                    print("⚠️  アラートは表示されましたが、星評価に関するメッセージではありませんでした")
                    return False
            else:
                print("❌ 不合格: 星評価0でもアラートが表示されませんでした")
                print("  （JavaScriptバリデーションが実装されていない可能性があります）")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 3 - Issue D: 星評価バリデーションチェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)

    result = test_rating_validation()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        print("星評価バリデーションに問題があります。Issue Dの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
