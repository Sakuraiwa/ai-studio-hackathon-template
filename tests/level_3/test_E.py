#!/usr/bin/env python3
"""
Level 3 - Issue E のテストスクリプト
問題: レビュー投稿フォームで、JavaScriptによるレビュー内容のバリデーションが実装されていない
期待: レビュー内容が空白または空白スペースのみの場合、エラーメッセージを表示すること
"""

import sys
import re
from pathlib import Path
from playwright.sync_api import sync_playwright


def check_source_code():
    """
    spot-detail.jsでレビュー内容の空チェックが実装されているかをチェック
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

    # text.trim() または レビュー内容の空チェックが実装されているかを確認
    has_trim_check = bool(re.search(r'text\.trim\(\)', active_code_str))
    has_empty_check = bool(re.search(r'!text\.trim\(\)', active_code_str))

    if has_trim_check or has_empty_check:
        print("✅ コードチェック合格: レビュー内容の空チェックが実装されています")
        return True
    else:
        print("❌ コードチェック不合格: レビュー内容の空チェックが実装されていません")
        return False


def test_review_text_validation():
    """
    レビュー投稿フォームでレビュー内容が空白の場合にバリデーションが動作するかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            print("\n【ステップ1: 実際の動作をチェック】")

            # spot-detail.htmlにアクセス
            page.goto('http://localhost:3001/spot-detail.html?id=1', wait_until='networkidle')

            # レビューフォームを確認
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

            # 星評価を選択
            star_buttons = page.locator('.star-button')
            if star_buttons.count() > 0:
                star_buttons.nth(4).click()  # 5つ星を選択
                page.wait_for_timeout(300)

            # レビューテキストに空白スペースのみを入力
            review_text.fill('   ')  # 空白スペースのみ

            # HTMLのrequired属性を一時的に削除してJavaScriptバリデーションのみをテスト
            page.evaluate("""
                const textArea = document.getElementById('reviewText');
                if (textArea) {
                    textArea.removeAttribute('required');
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
                # レビュー内容に関するメッセージかチェック
                if 'レビュー' in dialog_message or 'コメント' in dialog_message or 'text' in dialog_message.lower():
                    print("✅ 合格: レビュー内容の空チェックが正しく動作しています")
                    return True
                else:
                    print("⚠️  アラートは表示されましたが、レビュー内容に関するメッセージではありませんでした")
                    return False
            else:
                print("❌ 不合格: 空白スペースのみでもアラートが表示されませんでした")
                print("  （JavaScriptバリデーションが実装されていない可能性があります）")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 3 - Issue E: レビュー内容バリデーションチェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)

    result = test_review_text_validation()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        print("レビュー内容バリデーションに問題があります。Issue Eの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
