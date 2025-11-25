#!/usr/bin/env python3
"""
Level 2 - Issue J のテストスクリプト
問題: 画像拡大モーダルでESCキーを押してもモーダルが閉じない
期待: ESCキーを押すとモーダルが閉じること
"""

import sys
import re
from pathlib import Path
from playwright.sync_api import sync_playwright


def check_source_code():
    """
    spot-detail.jsでESCキーのイベントリスナーが実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    spot_detail_js = project_root / "frontend" / "spot-detail.js"

    if not spot_detail_js.exists():
        print(f"❌ エラー: {spot_detail_js} が見つかりません")
        return False

    with open(spot_detail_js, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # コメントアウトされていないコードのみをチェック
    # 複数行コメント（/* */）とコメントアウトされた行（//）を除外
    active_code = []
    in_multiline_comment = False

    for line in lines:
        stripped = line.strip()

        # 複数行コメントの開始
        if '/*' in stripped:
            in_multiline_comment = True

        # 複数行コメントの終了
        if '*/' in stripped:
            in_multiline_comment = False
            continue

        # コメント内または単一行コメントの場合はスキップ
        if in_multiline_comment or stripped.startswith('//'):
            continue

        active_code.append(line)

    active_code_str = ''.join(active_code)

    # ESCキーのイベントリスナーが実装されているかをチェック
    has_escape_check = bool(re.search(r"['\"]Escape['\"]", active_code_str))
    has_keydown_listener = bool(re.search(r"addEventListener\(['\"]keydown['\"]", active_code_str))

    if has_escape_check and has_keydown_listener:
        print("✅ コードチェック合格: ESCキーのイベントリスナーが実装されています")
        return True
    else:
        print("❌ コードチェック不合格: ESCキーのイベントリスナーが実装されていません")
        if not has_keydown_listener:
            print("  - keydownイベントリスナーが見つかりません")
        if not has_escape_check:
            print("  - 'Escape'キーのチェックが見つかりません")
        return False


def test_esc_key_closes_modal():
    """
    画像拡大モーダルでESCキーを押すとモーダルが閉じるかをチェック
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            print("\n【ステップ1: 実際の動作をチェック】")

            # spot-detail.htmlにアクセス
            page.goto('http://localhost:3001/spot-detail.html?id=1', wait_until='networkidle')

            # レビューセクションまでスクロール
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000)

            # レビューに画像があるか確認
            # レビュー画像はonclick属性にshowImageModalを持つimg要素
            review_images = page.locator('.reviews-list img[onclick*="showImageModal"]')

            if review_images.count() == 0:
                print("⚠️  レビュー画像が見つかりませんでした")
                print("  （画像がないとモーダルのテストができないため、ソースコードをチェックします）\n")
                browser.close()
                print("【ステップ2: ソースコードをチェック】")
                return check_source_code()

            print(f"レビュー画像を {review_images.count()} 個見つけました")

            # 最初の画像をクリックしてモーダルを開く
            review_images.first.click()
            page.wait_for_timeout(500)

            # モーダルが表示されているか確認
            modal = page.locator('#imageModal')

            if not modal.is_visible():
                print("❌ エラー: 画像をクリックしてもモーダルが表示されません")
                browser.close()
                return False

            print("✅ モーダルが表示されました")

            # ESCキーを押す
            page.keyboard.press('Escape')
            page.wait_for_timeout(500)

            # モーダルが閉じたか確認
            if modal.is_visible():
                print("❌ 不合格: ESCキーを押してもモーダルが閉じませんでした")
                browser.close()
                return False
            else:
                print("✅ 合格: ESCキーでモーダルが正しく閉じました")
                browser.close()
                return True

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def main():
    print("=" * 60)
    print("Level 2 - Issue J: ESCキーでモーダルを閉じる機能チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)

    result = test_esc_key_closes_modal()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        print("ESCキーでモーダルを閉じる機能に問題があります。Issue Jの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
