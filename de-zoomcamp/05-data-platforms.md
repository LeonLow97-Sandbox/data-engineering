# Data Platforms

## Setup Bruin

```sh
# 1. Install Bruin
curl -LsSf https://getbruin.com/install/cli | sh
source ~/.zshrc
bruin version

# 2. Install Bruin Extension on VSCode

# 3. Initialize Bruin
cd /data-engineering/de-zoomcamp/codes/05-bruin
bruin init
# Please select a template below:
#  [ ] athena
#  [ ] bronze-silver-postgres
#  [ ] chess
#  [ ] clickhouse
#  [ ] databricks
#  [x] default

# 4. Install Bruin's own Python runtime
cd bruin-pipeline
bruin run \
  --start-date 2026-02-21T00:00:00.000Z \
  --end-date 2026-02-21T23:59:59.999999999Z \
  --environment default \
  "/Users/leonlow/Desktop/GitHub/learning/data-engineering/de-zoomcamp/codes/05-bruin/bruin-pipeline/assets/my_python_asset.py"
```

## Bruin Zoomcamp

```sh
bruin init zoomcamp
```
