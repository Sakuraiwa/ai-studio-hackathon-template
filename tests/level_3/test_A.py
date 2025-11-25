#!/usr/bin/env python3
"""
Level 3 - Issue A のテストスクリプト
問題: YouTube動画が埋め込まれていない（静的な画像プレースホルダーのみ）
期待: 3つの観光地（草津温泉、富岡製糸場、尾瀬国立公園）にYouTube動画が埋め込まれていること
"""

import sys
import re
from pathlib import Path


def check_youtube_embeds():
    """
    index.htmlに3つのYouTube動画が埋め込まれているかをチェック
    """
    project_root = Path(__file__).parent.parent.parent
    index_html = project_root / "frontend" / "index.html"

    if not index_html.exists():
        print(f"❌ エラー: {index_html} が見つかりません")
        return False

    with open(index_html, 'r', encoding='utf-8') as f:
        content = f.read()

    print("YouTube動画埋め込み確認を開始します\n")

    # 期待される動画ID
    expected_videos = {
        'GrEEoEmmrKs': '草津温泉',
        'OFg0mXRNDpI': '富岡製糸場',
        'o7zDfKZrlJ8': '尾瀬国立公園'
    }

    # iframeタグのパターン
    iframe_pattern = r'<iframe[^>]*src=["\']https?://www\.youtube\.com/embed/([^"\']+)["\'][^>]*>'

    found_videos = re.findall(iframe_pattern, content, re.IGNORECASE)

    print("チェック結果:")
    results = {}

    for video_id, name in expected_videos.items():
        if video_id in found_videos:
            print(f"  {name}: ✅ 埋め込みあり")
            results[name] = True
        else:
            print(f"  {name}: ❌ 埋め込みなし")
            results[name] = False

    print()

    # すべての動画が埋め込まれていればOK
    all_embedded = all(results.values())

    if all_embedded:
        print("✅ 合格: すべての観光地にYouTube動画が埋め込まれています")
        return True
    else:
        print("❌ 不合格: YouTube動画の埋め込みが不足しています。Issue Aの「どうあるべきか」を確認してください。")
        print("   ヒント: <iframe> タグを使用し、src属性に https://www.youtube.com/embed/VIDEO_ID を指定してください")
        return False


def main():
    print("=" * 60)
    print("Level 3 - Issue A: YouTube動画埋め込みチェック")
    print("=" * 60)

    result = check_youtube_embeds()

    print("=" * 60)
    if result:
        print("🎉 テスト合格！")
        sys.exit(0)
    else:
        print("💔 テスト不合格")
        sys.exit(1)


if __name__ == "__main__":
    main()
