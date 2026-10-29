#!/bin/bash
# Self-stop: after CLOUD16_DONE, wait for /workspace/FETCHED (written by the laptop watcher) or 20 min;
# also on 15 min with no python/pip, or a 3-hour cap. Results are packed to /workspace/results16.tgz first.
stop_pod() {
  echo "$(date) selfstop16: $1" >> /workspace/selfstop.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop.log 2>&1
}
pack() { tar czf /workspace/results16.tgz -C /workspace/agp $(cd /workspace/agp && ls -d out_*) 2>/dev/null; md5sum /workspace/results16.tgz > /workspace/results16.md5; touch /workspace/PACKED; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD16_DONE /workspace/run16.log 2>/dev/null; then
    pack
    for w in $(seq 1 20); do [ -f /workspace/FETCHED ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 10800 ]; then pack; stop_pod cap3h; exit; fi
  if pgrep -f "python|pip" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
