#!/bin/bash
set -euo pipefail

# CONFIGURATION
ENV_NAME=".venv"
VERSION_ID="venv_$(date +%Y%m%d_%H%M%S)"
BUCKET="your-s3-bucket-name"
S3_PREFIX="venv-builds/$VERSION_ID"
TMP_DIR="/tmp/$VERSION_ID"
mkdir -p "$TMP_DIR"

echo "🔥 Creating virtual environment..."
python3 -m venv "$ENV_NAME"
source "$ENV_NAME/bin/activate"

echo "⬆️ Upgrading pip..."
pip install --upgrade pip

echo "📦 Installing requirements..."
cp requirements.txt "$TMP_DIR/"
pip install -r requirements.txt

echo "🔍 Installing pipdeptree..."
pip install pipdeptree

echo "🧭 Checking dependency tree for conflicts..."
pipdeptree --warn silence > "$TMP_DIR/pipdeptree.txt"
pipdeptree --warn silence --json > "$TMP_DIR/pipdeptree.json"

CONFLICTS=$(pipdeptree --warn fail | grep "WARNING" || true)
IS_CONFLICT_FREE=true
CONFLICT_LIST=()

if [[ -n "$CONFLICTS" ]]; then
  echo "❌ Dependency conflict detected!"
  echo "$CONFLICTS"
  IS_CONFLICT_FREE=false
  while IFS= read -r line; do
    CONFLICT_LIST+=("$line")
  done <<< "$CONFLICTS"
fi

echo "📋 Freezing installed packages..."
pip freeze > "$TMP_DIR/installed_packages.txt"
python -c 'import pkg_resources, json; print(json.dumps(sorted(["{}=={}".format(d.project_name, d.version) for d in pkg_resources.working_set])))' > "$TMP_DIR/installed_packages.json"

echo "📦 Archiving virtual environment..."
tar -czf "$TMP_DIR/$VERSION_ID.tar.gz" "$ENV_NAME/"

echo "🧾 Generating metadata.json..."
cat > "$TMP_DIR/metadata.json" <<EOF
{
  "venv_version": "$VERSION_ID",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "python_version": "$(python --version | cut -d' ' -f2)",
  "requirements_file": "s3://$BUCKET/$S3_PREFIX/requirements.txt",
  "pipdeptree_output": "s3://$BUCKET/$S3_PREFIX/pipdeptree.json",
  "venv_archive": "s3://$BUCKET/$S3_PREFIX/$VERSION_ID.tar.gz",
  "is_conflict_free": $IS_CONFLICT_FREE,
  "conflicts": $(printf '%s\n' "${CONFLICT_LIST[@]}" | jq -R . | jq -s .),
  "installed_packages": $(cat "$TMP_DIR/installed_packages.json")
}
EOF

echo "☁️ Uploading artifacts to S3..."
aws s3 cp "$TMP_DIR/" "s3://$BUCKET/$S3_PREFIX/" --recursive

deactivate
echo "✅ Build and upload complete."

if [ "$IS_CONFLICT_FREE" = false ]; then
  echo "🚨 Build failed due to dependency conflicts. See metadata.json for details."
  exit 1
fi
