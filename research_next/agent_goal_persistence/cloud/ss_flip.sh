#!/bin/bash
# Self-stop for FLIP (ss_ts.sh with fl labels; cap 90 min). After CLOUD_FLIP_DONE in run_fl.log: pack, then wait for
# /workspace/FETCHED_FL (laptop watcher) or 6 min. Also stops after 15 idle min or at a 90-min cap.
stop_pod() {
  echo "$(date) selfstop_fl: $1" >> /workspace/selfstop_fl.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop_fl.log 2>&1
}
pack() { tar czf /workspace/results_fl.tgz -C /workspace/agpfl out_flip 2>/dev/null; md5sum /workspace/results_fl.tgz > /workspace/results_fl.md5; touch /workspace/PACKED_FL; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD_FLIP_DONE /workspace/run_fl.log 2>/dev/null; then
    pack
    for w in $(seq 1 6); do [ -f /workspace/FETCHED_FL ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 5400 ]; then pack; stop_pod cap90min; exit; fi
  if pgrep -f "python|pip|git" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
