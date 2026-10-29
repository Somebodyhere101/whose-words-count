#!/bin/bash
# Self-stop for run 29 (PREREG_W), one pod: bash ss29.sh A|B|C. Uses its own markers and folder, /workspace/agpw<x>, on the shared volume.
# After CLOUD29_DONE in run29<x>.log: pack, then wait for /workspace/FETCHED29<X> (written by the laptop watcher) or 6 min.
# It also stops after 15 min with no python or pip running, or at a 4-hour cap.
X=$1; x=$(echo $X | tr A-Z a-z)
stop_pod() {
  echo "$(date) selfstop29$X: $1" >> /workspace/selfstop29$X.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop29$X.log 2>&1
}
pack() { tar czf /workspace/results29$X.tgz -C /workspace/agpw$x out_w 2>/dev/null; md5sum /workspace/results29$X.tgz > /workspace/results29$X.md5; touch /workspace/PACKED29$X; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD29_DONE /workspace/run29$X.log 2>/dev/null; then
    pack
    for w in $(seq 1 6); do [ -f /workspace/FETCHED29$X ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 14400 ]; then pack; stop_pod cap4h; exit; fi
  if pgrep -f "python|pip" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
