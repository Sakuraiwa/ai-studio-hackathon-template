#!/usr/bin/env python3
"""
Level 2 - Issue D のテストスクリプト
問題: 観光地詳細ページの平均評価が小数点以下が長すぎる（例: 4.666666667）
期待: 平均評価は小数点第1位まで表示されること（例: 4.7）
"""

import sys
import re
from pathlib import Path
from playwright.sync_api import sync_playwright


def check_source_code():
    """
    spot-detail.jsで.toFixed(1)が使われているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    spot_detail_js = project_root / "frontend" / "spot-detail.js"

    if not spot_detail_js.exists():
        print(f"❌ エラー: {spot_detail_js} が見つかりません")
        return False

    with open(spot_detail_js, 'r', encoding='utf-8') as f:
        content = f.read()

    # avg_ratingに対してtoFixed(1)が使われているかをチェック
    # パターン: spot.avg_rating.toFixed(1) または avg_rating.toFixed(1)
    pattern = r'avg_rating\.toFixed\(1\)'

    if re.search(pattern, content):
        print("✅ コードチェック合格: .toFixed(1) が使用されています")
        return True
    else:
        print("❌ コードチェック不合格: .toFixed(1) が使用されていません")
        return False


def test_rating_decimal_format():
    """
    spot-detail.jsで.toFixed(1)が使われているかをチェック（メイン）
    実際の表示もチェック（補助的）
    """
    print("\n【ステップ1: ソースコードをチェック】")
    code_check_passed = check_source_code()

    if not code_check_passed:
        # ソースコードチェックで不合格なら、実際の表示も確認（補助的）
        print("\n【ステップ2: 実際の表示をチェック（補助的確認）】")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            try:
                print("複数の観光地で小数点以下が2桁以上表示されるか確認します...")

                found_long_decimal = False

                # spot_id 1〜20 をテスト
                for spot_id in range(1, 21):
                    page.goto(f'http://localhost:3001/spot-detail.html?id={spot_id}', wait_until='networkidle')

                    # 平均評価表示を取得
                    rating_element = page.locator('#spotRating')

                    if rating_element.count() == 0:
                        continue

                    rating_text = rating_element.text_content()

                    # 数値部分を抽出
                    match = re.search(r'[⭐★☆]\s*([\d.]+)', rating_text)

                    if not match:
                        continue

                    rating_value = match.group(1)

                    # 小数点以下がある場合のみチェック
                    if '.' in rating_value:
                        decimal_part = rating_value.split('.')[1]
                        decimal_length = len(decimal_part)

                        if decimal_length > 1:
                            found_long_decimal = True
                            print(f"\nspot_id={spot_id}: {rating_text}")
                            print(f"  評価数値: {rating_value}")
                            print(f"  小数点以下の桁数: {decimal_length}桁")
                            print(f"  ❌ 小数点以下が{decimal_length}桁です（期待: 1桁）")
                            break

                browser.close()

                if found_long_decimal:
                    print("\n❌ 実際の表示でも問題が確認されました")
                else:
                    print("\n⚠️  実際の表示では問題が見つかりませんでしたが、ソースコードに問題があります")
                    print("   （データによっては小数点が長く表示される可能性があります）")

                return False

            except Exception as e:
                print(f"❌ エラー: テスト実行中にエラーが発生しました: {e}")
                browser.close()
                return False

    return True


def main():
    print("=" * 60)
    print("Level 2 - Issue D: 平均評価の小数点表示チェック")
    print("=" * 60)
    print("※ このテストを実行する前に、ポート3001でアプリケーションが起動している必要があります")
    print("=" * 60)

    result = test_rating_decimal_format()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        print("平均評価の小数点表示に問題があります。Issue Dの「どうあるべきか」を確認してください。")
        sys.exit(1)


if __name__ == "__main__":
    main()
