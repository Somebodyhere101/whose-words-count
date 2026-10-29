#!/bin/bash
# Self-stop: after CLOUD23_DONE, wait for /workspace/FETCHED23 (written by the laptop watcher) or 6 min (run 23, shared network volume: own markers and folder);
# also on 15 min with no python/pip, or a 4-hour cap. Results are packed to /workspace/results23.tgz first.
stop_pod() {
  echo "$(date) selfstop23: $1" >> /workspace/selfstop23.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop23.log 2>&1
}
pack() { tar czf /workspace/results23.tgz -C /workspace/agpm $(cd /workspace/agpm && ls -d out_*) 2>/dev/null; md5sum /workspace/results23.tgz > /workspace/results23.md5; touch /workspace/PACKED23; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD23_DONE /workspace/run23.log 2>/dev/null; then
    pack
    for w in $(seq 1 6); do [ -f /workspace/FETCHED23 ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 14400 ]; then pack; stop_pod cap4h; exit; fi
  if pgrep -f "python|pip" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
