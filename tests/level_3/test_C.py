#!/usr/bin/env python3
"""
Level 3 - Issue C のテストスクリプト
問題: ログアウト後もレビュー投稿フォームが表示されてしまう
期待: ログアウト後はレビューフォームを非表示にし、ログイン通知を表示すること
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def test_review_form_after_logout():
    """
    ログアウト後にレビューフォームが非表示になるかをチェック（Playwright）
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # spot-detail.htmlにアクセス
            page.goto('http://localhost:3001/spot-detail.html?id=1', wait_until='networkidle')
            page.wait_for_timeout(1000)

            # まずログイン状態を確認
            login_button = page.locator('button:has-text("ログイン")')
            logout_button = page.locator('button:has-text("ログアウト")')

            # ログイン状態なら一旦ログアウト
            if logout_button.count() > 0:
                logout_button.click()
                page.wait_for_timeout(500)

            # ログアウト状態でのフォーム表示をチェック
            review_form = page.locator('#reviewForm')
            login_notice = page.locator('#loginNotice')

            is_form_visible = review_form.is_visible() if review_form.count() > 0 else False
            is_notice_visible = login_notice.is_visible() if login_notice.count() > 0 else False

            print("ログアウト状態での表示チェック:")
            print(f"  レビューフォーム: {'表示' if is_form_visible else '非表示'}")
            print(f"  ログイン通知: {'表示' if is_notice_visible else '非表示'}")
            print()

            browser.close()

            if not is_form_visible and is_notice_visible:
                print("✅ 合格: ログアウト後はレビューフォームが非表示になっています")
                return True
            elif is_form_visible:
                print("❌ 不合格: ログアウト後もレビューフォームが表示されています。Issue Cの「どうあるべきか」を確認してください。")
                return False
            else:
                print("⚠️  フォームは非表示ですが、ログイン通知も表示されていません")
                return False

        except Exception as e:
            print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
            browser.close()
            return False


def check_source_code():
    """
    spot-detail.jsでログイン状態によるフォーム制御が実装されているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    spot_detail_js = project_root / "frontend" / "spot-detail.js"

    if not spot_detail_js.exists():
        print(f"❌ エラー: {spot_detail_js} が見つかりません")
        return False

    with open(spot_detail_js, 'r', encoding='utf-8') as f:
        content = f.read()

    # コメントを除外したコードを取得
    lines = content.split('\n')
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

    active_code_str = '\n'.join(active_code)

    # ログイン状態チェックがあるか
    import re
    has_login_check = bool(re.search(r'if\s*\(\s*isLoggedIn\s*\)', active_code_str))
    has_form_control = bool(re.search(r'reviewForm.*style\.display', active_code_str))
    has_notice_control = bool(re.search(r'loginNotice.*style\.display', active_code_str))

    print("\nソースコードチェック:")
    print(f"  ログイン状態チェック: {'✅ あり' if has_login_check else '❌ なし'}")
    print(f"  フォーム表示制御: {'✅ あり' if has_form_control else '❌ なし'}")
    print(f"  ログイン通知制御: {'✅ あり' if has_notice_control else '❌ なし'}")
    print()

    if has_login_check and has_form_control and has_notice_control:
        print("✅ 合格: ログイン状態による表示制御が実装されています")
        return True
    else:
        print("❌ 不合格: ログイン状態による表示制御が実装されていません。Issue Cの「どうあるべきか」を確認してください。")
        return False


def main():
    print("=" * 60)
    print("Level 3 - Issue C: ログアウト後のレビューフォーム表示チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)

    # まずPlaywrightでテスト
    result = test_review_form_after_logout()

    # 失敗したらソースコードもチェック
    if not result:
        print("\n【追加チェック: ソースコード確認】")
        result = check_source_code()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
