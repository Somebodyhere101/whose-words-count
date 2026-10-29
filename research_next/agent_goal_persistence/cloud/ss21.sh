#!/bin/bash
# Self-stop: after CLOUD21_DONE, wait for /workspace/FETCHED21 (written by the laptop watcher) or 6 min (run 21, shared network volume: own markers and folder);
# also on 15 min with no python/pip, or a 4-hour cap. Results are packed to /workspace/results21.tgz first.
stop_pod() {
  echo "$(date) selfstop21: $1" >> /workspace/selfstop21.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop21.log 2>&1
}
pack() { tar czf /workspace/results21.tgz -C /workspace/agpk $(cd /workspace/agpk && ls -d out_*) 2>/dev/null; md5sum /workspace/results21.tgz > /workspace/results21.md5; touch /workspace/PACKED21; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD21_DONE /workspace/run21.log 2>/dev/null; then
    pack
    for w in $(seq 1 6); do [ -f /workspace/FETCHED21 ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 14400 ]; then pack; stop_pod cap4h; exit; fi
  if pgrep -f "python|pip" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
