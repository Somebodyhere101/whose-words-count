#!/bin/bash
# Self-stop for run 34 (PREREG_Y part B). /workspace is the network volume or the pod's volume disk; both survive a stop.
# After CLOUD34_DONE in run34.log: pack, then wait for /workspace/FETCHED34 (written by the laptop watcher) or 6 min.
# It also stops after 15 min with no python, pip or git running, or at a 4-hour cap.
stop_pod() {
  echo "$(date) selfstop34: $1" >> /workspace/selfstop34.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop34.log 2>&1
}
pack() { tar czf /workspace/results34.tgz -C /workspace/agpyb out_y 2>/dev/null; md5sum /workspace/results34.tgz > /workspace/results34.md5; touch /workspace/PACKED34; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD34_DONE /workspace/run34.log 2>/dev/null; then
    pack
    for w in $(seq 1 6); do [ -f /workspace/FETCHED34 ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 14400 ]; then pack; stop_pod cap4h; exit; fi
  if pgrep -f "python|pip|git" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
