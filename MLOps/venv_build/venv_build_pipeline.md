# 🐍 Virtual Environment Build & Metadata Management Pipeline

## 🎯 Objective

To automate the creation, validation, versioning, and discoverability of Python virtual environments using Jenkins, S3, and Athena. This solution ensures reproducibility, dependency conflict detection, and package-level searchability across builds.

---

## 📦 Features Overview

- Automated creation of Python virtual environments via Jenkins
- Dependency installation from `requirements.txt`
- Validation using `pipdeptree` for conflict detection
- Packaging and versioning of the venv
- Uploading artifacts to S3
- Generation of searchable `metadata.json`
- Query support using AWS Athena
- Discoverability of environments by installed packages

---

## 🧱 Design Components

### 1. Inputs

- `requirements.txt`
- (Optional) Python version
- Jenkins parameters:
  - `ENV_NAME`
  - `PYTHON_VERSION`
  - `FAIL_ON_CONFLICTS`

---

### 2. Virtual Environment Creation

```bash
python -m venv venv/
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3. Dependency Validation

- Install `pipdeptree`
- Run:
  ```bash
  pip install pipdeptree
  pipdeptree --warn silence > pipdeptree.txt
  pipdeptree --warn silence --json > pipdeptree.json
  ```

- Capture `pip freeze` output:
  ```bash
  pip freeze > installed_packages.txt
  ```

- Convert installed packages to JSON:
  ```bash
  python -c 'import pkg_resources, json; print(json.dumps(sorted(["{}=={}".format(d.project_name, d.version) for d in pkg_resources.working_set])))' > installed_packages.json
  ```

---

### 4. Archive the Virtual Environment

```bash
tar -czf venv_<version>.tar.gz venv/
```

---

### 5. Metadata File (metadata.json)

Structure:
```json
{
  "venv_version": "venv_20250722_163000",
  "created_at": "2025-07-22T08:30:00Z",
  "python_version": "3.10",
  "requirements_file": "s3://your-bucket/venv-builds/venv_20250722_163000/requirements.txt",
  "pipdeptree_output": "s3://your-bucket/venv-builds/venv_20250722_163000/pipdeptree.json",
  "venv_archive": "s3://your-bucket/venv-builds/venv_20250722_163000/venv_20250722_163000.tar.gz",
  "is_conflict_free": true,
  "conflicts": [],
  "installed_packages": [
    "kedro==0.18.14",
    "pandas==1.5.3",
    "numpy==1.24.4"
  ]
}
```

---

### 6. S3 Artifact Structure

```
s3://<bucket>/venv-builds/venv_<version>/
├── venv_<version>.tar.gz
├── requirements.txt
├── pipdeptree.txt
├── pipdeptree.json
├── installed_packages.txt
├── installed_packages.json
├── metadata.json
```

---

### 7. Athena Table Definition

```sql
CREATE EXTERNAL TABLE venv_builds_metadata (
  venv_version string,
  created_at timestamp,
  python_version string,
  requirements_file string,
  pipdeptree_output string,
  venv_archive string,
  is_conflict_free boolean,
  conflicts array<string>,
  installed_packages array<string>
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://your-bucket/venv-builds/'
TBLPROPERTIES ('classification'='json');
```

---

## 🔍 Discoverability with Athena

### Find all venvs with Kedro:

```sql
SELECT venv_version, created_at
FROM venv_builds_metadata
WHERE EXISTS (
  SELECT * FROM UNNEST(installed_packages) AS pkg
  WHERE pkg LIKE 'kedro%'
);
```

### Count venvs with Kedro:

```sql
SELECT count(*) AS total_kedro_envs
FROM venv_builds_metadata
WHERE EXISTS (
  SELECT * FROM UNNEST(installed_packages) AS pkg
  WHERE pkg LIKE 'kedro%'
);
```

---

## ✅ Jenkins Pipeline Summary

1. Validate input files
2. Create venv and install packages
3. Run `pipdeptree` and detect conflicts
4. Package the venv
5. Generate `metadata.json`
6. Upload all files to S3
7. Athena queries enable traceability and discoverability

---

## 🔐 Best Practices

- Use ephemeral Jenkins agents or clean workspace
- Avoid `sudo pip install`
- Sanitize logs before archiving
- Parameterize bucket and venv name
- Enforce naming conventions for venv versions
- Use Glue crawler to refresh Athena partitions if needed

---

## 🧩 Optional Enhancements

- Integrate with Glue workflows for metadata sync
- Add a UI to explore builds by package/version
- Slack/email notifications for build failures
- Store `pipdeptree` visualizations (e.g., SVG/DOT)

---

✅ Why Use pipdeptree
	•	Detect conflicts early
	•	Visualize full dependency tree
	•	Automate quality gates in Jenkins pipelines
	•	Export structured output for auditing or alerting
	•	Enable package-level searchability and governance

---
✅ What Is a “Pinned” Dependency?

A pinned dependency uses a fixed version with ==:

```txt
✅ pandas==1.5.3
❌ pandas
❌ pandas>=1.2
❌ pandas~=1.4
```

To ensure all dependencies are pinned in requirements.txt (i.e., every package has a version specified like pandas==1.5.3), you can add a validation step in your Bash script to raise an error if any unpinned packages are found.

```bash
echo "🔍 Checking if all dependencies are pinned in requirements.txt..."
UNPINNED=$(grep -vE '^\s*#' requirements.txt | grep -vE '^\s*$' | grep -vE '==' || true)

if [[ -n "$UNPINNED" ]]; then
  echo "❌ Found unpinned dependencies in requirements.txt:"
  echo "$UNPINNED"
  echo "🛑 Please pin all dependencies using '==' to ensure reproducibility."
  exit 1
else
  echo "✅ All dependencies are pinned."
fi
```