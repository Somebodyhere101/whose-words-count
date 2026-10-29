#!/bin/bash
# Self-stop for MPILOT (copied from ss34.sh with mp1 labels). After CLOUD_MP1_DONE in run_mp1.log: pack, then wait for
# /workspace/FETCHED_MP1 (written by the laptop watcher) or 6 min. Also stops after 15 idle min or at a 3-hour cap.
stop_pod() {
  echo "$(date) selfstop_mp1: $1" >> /workspace/selfstop_mp1.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop_mp1.log 2>&1
}
pack() { tar czf /workspace/results_mp1.tgz -C /workspace/agpmp1 out_mp 2>/dev/null; md5sum /workspace/results_mp1.tgz > /workspace/results_mp1.md5; touch /workspace/PACKED_MP1; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD_MP1_DONE /workspace/run_mp1.log 2>/dev/null; then
    pack
    for w in $(seq 1 6); do [ -f /workspace/FETCHED_MP1 ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 10800 ]; then pack; stop_pod cap3h; exit; fi
  if pgrep -f "python|pip|git" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
