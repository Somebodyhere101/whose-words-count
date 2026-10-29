#!/bin/bash
# Self-stop for run 30 (PREREG_V; shared network volume, own markers and folder /workspace/agpv).
# After CLOUD30_DONE: pack, then wait for /workspace/FETCHED30 (written by the laptop watcher) or 6 min.
# It also stops after 15 min with no python or pip running, or at a 3-hour cap.
stop_pod() {
  echo "$(date) selfstop30: $1" >> /workspace/selfstop30.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop30.log 2>&1
}
pack() { tar czf /workspace/results30.tgz -C /workspace/agpv out_v 2>/dev/null; md5sum /workspace/results30.tgz > /workspace/results30.md5; touch /workspace/PACKED30; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD30_DONE /workspace/run30.log 2>/dev/null; then
    pack
    for w in $(seq 1 6); do [ -f /workspace/FETCHED30 ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 10800 ]; then pack; stop_pod cap3h; exit; fi
  if pgrep -f "python|pip" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
