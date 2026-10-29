#!/bin/bash
# Self-stop for run 33 (PREREG_Y part A). /workspace is the pod's volume disk, which survives a stop (L10).
# After CLOUD33_DONE in run33.log: pack, then wait for /workspace/FETCHED33 (written by the laptop watcher) or 6 min.
# It also stops after 15 min with no python, pip or git running, or at a 7-hour cap.
stop_pod() {
  echo "$(date) selfstop33: $1" >> /workspace/selfstop33.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop33.log 2>&1
}
pack() { tar czf /workspace/results33.tgz -C /workspace/agpy out_y 2>/dev/null; md5sum /workspace/results33.tgz > /workspace/results33.md5; touch /workspace/PACKED33; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD33_DONE /workspace/run33.log 2>/dev/null; then
    pack
    for w in $(seq 1 6); do [ -f /workspace/FETCHED33 ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 25200 ]; then pack; stop_pod cap7h; exit; fi
  if pgrep -f "python|pip|git" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
