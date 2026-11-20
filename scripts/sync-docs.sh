#!/usr/bin/env bash
# 把 book/ 主本同步到 docs/（Pages 只发布 docs/）
set -euo pipefail
cd "$(dirname "$0")/.."
cp "book/润泽说-道可道之数字学（整理稿）.md" docs/
echo "synced -> docs/"
