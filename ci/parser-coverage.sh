#!/bin/bash
# Outputs parser coverage comment using scripts/checkfields/missing_fields.py

test -z "$1" && echo "usage: parser-coverage.sh filename.toml" && exit 1

set -eou pipefail

python3 scripts/checkfields/missing_fields.py "$1"
echo "\`\`\`"
grep 'False\|SUBJECT\|VISIT\|OBSERVATION' scripts/checkfields/check_fields.csv | column -t -s,
echo "\`\`\`"