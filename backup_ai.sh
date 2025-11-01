#!/bin/bash
# =====================================
# 🔒 AI системийн бүрэн нөөцлөх скрипт
# by Tumenjargal & GPT-5 (2025)
# =====================================

# === Тохиргоо ===
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_DIR="$HOME/ai_backups"
BACKUP_FILE="$BACKUP_DIR/hybrid-ai-backup-$DATE.tar.gz"

HYBRID_AI_DIR="$HOME/hybrid-ai"
OLLAMA_MODELS_DIR="/var/snap/ollama/common/models"

# === Нөөцлөх хавтас үүсгэх ===
mkdir -p "$BACKUP_DIR"

echo "📦 AI системийн нөөцлөлт эхэлж байна..."
echo "🕒 Огноо: $DATE"
sleep 1

# === Ollama model шалгах ===
if [ ! -d "$OLLAMA_MODELS_DIR" ]; then
  echo "⚠️ Ollama models хавтас олдсонгүй: $OLLAMA_MODELS_DIR"
  echo "⛔ Ollama model хэсгийг алгаслаа."
  tar -czvf "$BACKUP_FILE" "$HYBRID_AI_DIR"
else
  echo "💾 Ollama model хамт багтааж байна..."
  sudo tar -czvf "$BACKUP_FILE" "$HYBRID_AI_DIR" "$OLLAMA_MODELS_DIR"
fi

# === Нөөц амжилттай эсэхийг шалгах ===
if [ -f "$BACKUP_FILE" ]; then
  echo "✅ Нөөц амжилттай хийгдлээ!"
  echo "📍 Файл хадгалагдсан: $BACKUP_FILE"
  du -h "$BACKUP_FILE" | awk '{print "💾 Файлын хэмжээ:", $1}'
else
  echo "❌ Нөөц үүссэнгүй. Алдаа гарлаа."
fi
