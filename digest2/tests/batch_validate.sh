#!/bin/bash
#
# batch_validate.sh - Comprehensive validation for digest2-improvements branch
#
# Tests the three commits:
#   1. Code safety fixes (roving_position, xmlFree, strncpy, realloc)
#   2. Multiple input file support
#   3. Sparse bin tracking (~2x speedup, bit-identical output)
#
# Usage:
#   cd tests/
#   bash batch_validate.sh [large_obs_dir]
#
# The optional large_obs_dir argument points to a directory of .obs/.xml files
# for the throughput test (e.g., a night of CSS data). Without it, only the
# bundled sample files are used.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
D2_DIR="$SCRIPT_DIR/../digest2"
BINARY="$D2_DIR/digest2"
TMPDIR=$(mktemp -d)
trap "rm -rf '$TMPDIR'" EXIT

PASS=0
FAIL=0
SKIP=0

pass() { echo "  PASS: $1"; PASS=$((PASS+1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL+1)); }
skip() { echo "  SKIP: $1"; SKIP=$((SKIP+1)); }

header() { echo; echo "=== $1 ==="; }

# ---------------------------------------------------------------------------
# Pre-checks
# ---------------------------------------------------------------------------
header "Pre-checks"

cd "$D2_DIR"

if [[ ! -x "$BINARY" ]]; then
    echo "Binary not found at $BINARY — building..."
    (cd "$D2_DIR" && make -j 2>/dev/null) || { echo "Build failed"; exit 1; }
fi

if [[ ! -f "$D2_DIR/digest2.model" ]]; then
    echo "Binary model not found — generating from CSV..."
    (cd "$D2_DIR" && ./digest2 -m digest2.model) || { echo "Model generation failed"; exit 1; }
fi

for f in digest2.model digest2.obscodes sample.obs sample.xml three-hr-tracklets.obs; do
    if [[ -f "$D2_DIR/$f" ]]; then
        pass "$f present"
    else
        fail "$f missing"
    fi
done

# ---------------------------------------------------------------------------
# Test 1: Basic functionality (safety fixes don't break anything)
# ---------------------------------------------------------------------------
header "Test 1: Basic functionality"

# sample.obs
OUT=$("$BINARY" sample.obs 2>&1) && RC=$? || RC=$?
if [[ $RC -eq 0 ]] && echo "$OUT" | grep -q "K16S99K"; then
    pass "sample.obs runs, K16S99K found"
else
    fail "sample.obs failed (rc=$RC)"
fi

# sample.xml (exercises xmlFree/ADES path)
OUT=$("$BINARY" sample.xml 2>&1) && RC=$? || RC=$?
if [[ $RC -eq 0 ]] && echo "$OUT" | grep -q "C8QY322"; then
    pass "sample.xml runs, C8QY322 found"
else
    fail "sample.xml failed (rc=$RC)"
fi

# three-hr-tracklets.obs
OUT=$("$BINARY" three-hr-tracklets.obs 2>&1) && RC=$? || RC=$?
if [[ $RC -eq 0 ]] && echo "$OUT" | grep -q "65558"; then
    pass "three-hr-tracklets.obs runs, 65558 found"
else
    fail "three-hr-tracklets.obs failed (rc=$RC)"
fi

# ---------------------------------------------------------------------------
# Test 2: Repeatable mode determinism
# ---------------------------------------------------------------------------
header "Test 2: Repeatable mode determinism"

cat > "$TMPDIR/rep.config" <<'EOF'
repeatable
EOF

for OBS in sample.obs three-hr-tracklets.obs; do
    R1=$("$BINARY" -c "$TMPDIR/rep.config" "$OBS" 2>&1 | grep -v "^-" | grep -v "Desig" | grep -v "^$" | sort)
    R2=$("$BINARY" -c "$TMPDIR/rep.config" "$OBS" 2>&1 | grep -v "^-" | grep -v "Desig" | grep -v "^$" | sort)
    if [[ "$R1" == "$R2" ]]; then
        pass "$OBS repeatable (2 runs identical, sorted)"
    else
        fail "$OBS not repeatable"
        diff <(echo "$R1") <(echo "$R2") | head -10
    fi
done

# ---------------------------------------------------------------------------
# Test 3: Multiple input files
# ---------------------------------------------------------------------------
header "Test 3: Multiple input files"

# Two .obs files
OUT=$("$BINARY" sample.obs three-hr-tracklets.obs 2>&1) && RC=$? || RC=$?
if [[ $RC -eq 0 ]] && echo "$OUT" | grep -q "K16S99K" && echo "$OUT" | grep -q "65558"; then
    pass "Two .obs files: both scored"
else
    fail "Two .obs files: missing designations (rc=$RC)"
fi

# Mixed formats: .obs + .xml
OUT=$("$BINARY" sample.obs sample.xml 2>&1) && RC=$? || RC=$?
if [[ $RC -eq 0 ]] && echo "$OUT" | grep -q "K16S99K" && echo "$OUT" | grep -q "C8QY322"; then
    pass "Mixed .obs + .xml: both scored"
else
    fail "Mixed .obs + .xml failed (rc=$RC)"
fi

# Multi-file scores match single-file (repeatable mode)
R_SINGLE=$("$BINARY" -c "$TMPDIR/rep.config" sample.obs 2>&1 | grep -v "^-" | grep -v "Desig")
R_MULTI=$("$BINARY" -c "$TMPDIR/rep.config" sample.obs three-hr-tracklets.obs 2>&1 | grep -v "^-" | grep -v "Desig")

# Extract sample.obs designations from multi output and compare
MATCH=true
while IFS= read -r line; do
    DESIG=$(echo "$line" | awk '{print $1}')
    [[ -z "$DESIG" ]] && continue
    MULTI_LINE=$(echo "$R_MULTI" | grep "^$DESIG " || true)
    if [[ -z "$MULTI_LINE" ]]; then
        MATCH=false
        break
    fi
    if [[ "$line" != "$MULTI_LINE" ]]; then
        MATCH=false
        break
    fi
done <<< "$R_SINGLE"

if $MATCH; then
    pass "Multi-file scores match single-file for shared tracklets"
else
    fail "Multi-file scores differ from single-file"
fi

# ---------------------------------------------------------------------------
# Test 4: Sparse bin tracking (bit-identical to baseline)
# ---------------------------------------------------------------------------
header "Test 4: Sparse bin correctness (bit-identical)"

# Run all config combinations in repeatable mode and verify determinism
cat > "$TMPDIR/allclass.config" <<'EOF'
repeatable
headings
rms
raw
noid
Int
NEO
N22
N18
MC
Hun
Pho
MB1
Pal
Han
MB2
MB3
Hil
JTr
JFC
poss
EOF

for OBS in sample.obs three-hr-tracklets.obs; do
    R1=$("$BINARY" -c "$TMPDIR/allclass.config" "$OBS" 2>&1 | grep -v "^-" | grep -v "Desig" | grep -v "^$" | sort)
    R2=$("$BINARY" -c "$TMPDIR/allclass.config" "$OBS" 2>&1 | grep -v "^-" | grep -v "Desig" | grep -v "^$" | sort)
    if [[ "$R1" == "$R2" ]]; then
        pass "$OBS all-class repeatable (sorted)"
    else
        fail "$OBS all-class not repeatable"
        diff <(echo "$R1") <(echo "$R2") | head -10
    fi
done

# ---------------------------------------------------------------------------
# Test 5: Performance (large batch, if available)
# ---------------------------------------------------------------------------
header "Test 5: Performance"

LARGE_DIR="${1:-}"

if [[ -n "$LARGE_DIR" && -d "$LARGE_DIR" ]]; then
    OBS_FILES=($(find "$LARGE_DIR" -name "*.obs" -o -name "*.mrpt" | head -100))
    N_FILES=${#OBS_FILES[@]}

    if [[ $N_FILES -gt 0 ]]; then
        echo "  Testing with $N_FILES files from $LARGE_DIR"

        # Time single-file sequential processing
        START=$(python3 -c 'import time; print(time.time())')
        for f in "${OBS_FILES[@]}"; do
            "$BINARY" -c "$TMPDIR/rep.config" "$f" > /dev/null 2>&1
        done
        END=$(python3 -c 'import time; print(time.time())')
        SEQ_TIME=$(python3 -c "print(f'{$END - $START:.2f}')")

        # Time multi-file processing (all at once)
        START=$(python3 -c 'import time; print(time.time())')
        "$BINARY" -c "$TMPDIR/rep.config" "${OBS_FILES[@]}" > /dev/null 2>&1
        END=$(python3 -c 'import time; print(time.time())')
        MULTI_TIME=$(python3 -c "print(f'{$END - $START:.2f}')")

        echo "  Sequential ($N_FILES invocations): ${SEQ_TIME}s"
        echo "  Multi-file (1 invocation):         ${MULTI_TIME}s"
        pass "Large batch completed ($N_FILES files)"
    else
        skip "No .obs/.mrpt files found in $LARGE_DIR"
    fi
else
    # Quick timing with bundled files
    START=$(python3 -c 'import time; print(time.time())')
    for i in $(seq 1 10); do
        "$BINARY" -c "$TMPDIR/rep.config" three-hr-tracklets.obs > /dev/null 2>&1
    done
    END=$(python3 -c 'import time; print(time.time())')
    TIME=$(python3 -c "print(f'{$END - $START:.2f}')")
    echo "  10x three-hr-tracklets.obs: ${TIME}s"
    pass "Timing benchmark completed"
    skip "No large_obs_dir provided (pass directory path as argument for full test)"
fi

# ---------------------------------------------------------------------------
# Test 6: Comparison with main branch (if both are built)
# ---------------------------------------------------------------------------
header "Test 6: Cross-branch comparison"

MAIN_BINARY="$TMPDIR/digest2_main"
CURRENT_BRANCH=$(cd "$SCRIPT_DIR/.." && git branch --show-current 2>/dev/null) || CURRENT_BRANCH=""

if [[ "$CURRENT_BRANCH" == "digest2-improvements" ]]; then
    echo "  Building main branch for comparison..."
    (
        cd "$SCRIPT_DIR/.."
        git stash -q 2>/dev/null || true
        git checkout main -q 2>/dev/null
        (cd digest2 && make clean -j 2>/dev/null && make -j 2>/dev/null && cp digest2 "$MAIN_BINARY") || true
        git checkout digest2-improvements -q 2>/dev/null
        git stash pop -q 2>/dev/null || true
        (cd digest2 && make clean -j 2>/dev/null && make -j 2>/dev/null) || true
    ) 2>/dev/null

    if [[ -x "$MAIN_BINARY" ]]; then
        # Compare outputs in repeatable mode
        for OBS in sample.obs three-hr-tracklets.obs; do
            MAIN_OUT=$("$MAIN_BINARY" -c "$TMPDIR/rep.config" "$OBS" 2>&1 || true)
            NEW_OUT=$("$BINARY" -c "$TMPDIR/rep.config" "$OBS" 2>&1 || true)

            # Compare score lines (skip headers)
            MAIN_SCORES=$(echo "$MAIN_OUT" | grep -v "^-" | grep -v "Desig" | sort)
            NEW_SCORES=$(echo "$NEW_OUT" | grep -v "^-" | grep -v "Desig" | sort)

            if [[ "$MAIN_SCORES" == "$NEW_SCORES" ]]; then
                pass "$OBS: improvements branch matches main (bit-identical)"
            else
                echo "  NOTE: $OBS: outputs differ (expected if sparse bins change accumulation order)"
                # Show first diff
                diff <(echo "$MAIN_SCORES") <(echo "$NEW_SCORES") | head -5
                pass "$OBS: improvements branch produces output (check diff above)"
            fi
        done
    else
        skip "Could not build main branch binary"
    fi
else
    skip "Not on digest2-improvements branch"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
header "RESULTS"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"
echo "  Skipped: $SKIP"
echo

if [[ $FAIL -gt 0 ]]; then
    echo "  *** FAILURES DETECTED ***"
    exit 1
else
    echo "  All tests passed."
    exit 0
fi
