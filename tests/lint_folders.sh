#!/bin/bash

TEST_DIRS=$*

if [ "$TEST_DIRS" = "" ]; then
        echo "Missing argument!"
        exit 1;
fi

TOTAL=0
FAILURES=0
for f in $(find $TEST_DIRS -name \*.py|grep -v venv); do
        echo -n "Linting / syntax checking $f... "
        let TOTAL=TOTAL+1
        flake8 $f
        RET=$?
        if [ "$RET" -eq "0" ]; then
                echo "OK"
        else
                let FAILURES=FAILURES+1
                echo "FAIL"
        fi
done

let SUCCESS=TOTAL-FAILURES
echo -n "$TOTAL tests, $SUCCESS passed, $FAILURES failed... "
if [ "$FAILURES" = "0" ]; then
        echo "OK";
        exit 0;
else
        echo "ERROR";
        exit 1;
fi
