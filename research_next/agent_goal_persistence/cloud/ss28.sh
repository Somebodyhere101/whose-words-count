#!/bin/bash
# Self-stop for run 28 (Phase 0 pilot; shared network volume, own markers and folder /workspace/agpv0).
# After CLOUD28_DONE: pack, then wait for /workspace/FETCHED28 (written by the laptop watcher) or 6 min.
# Also stops after 15 min with no python/pip, or at a 3-hour cap. Results are packed to /workspace/results28.tgz first.
stop_pod() {
  echo "$(date) selfstop28: $1" >> /workspace/selfstop28.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop28.log 2>&1
}
pack() { tar czf /workspace/results28.tgz -C /workspace/agpv0 out_v0 2>/dev/null; md5sum /workspace/results28.tgz > /workspace/results28.md5; touch /workspace/PACKED28; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD28_DONE /workspace/run28.log 2>/dev/null; then
    pack
    for w in $(seq 1 6); do [ -f /workspace/FETCHED28 ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 10800 ]; then pack; stop_pod cap3h; exit; fi
  if pgrep -f "python|pip" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
