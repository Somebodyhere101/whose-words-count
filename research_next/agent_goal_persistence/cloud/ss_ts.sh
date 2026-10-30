#!/bin/bash
# Self-stop for TAGSTYLE (ss_rev3.sh with ts labels; cap 60 min). After CLOUD_TS_DONE in run_ts.log: pack, then wait for
# /workspace/FETCHED_TS (laptop watcher) or 6 min. Also stops after 15 idle min or at a 60-min cap.
stop_pod() {
  echo "$(date) selfstop_ts: $1" >> /workspace/selfstop_ts.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop_ts.log 2>&1
}
pack() { tar czf /workspace/results_ts.tgz -C /workspace/agpts out_ts 2>/dev/null; md5sum /workspace/results_ts.tgz > /workspace/results_ts.md5; touch /workspace/PACKED_TS; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD_TS_DONE /workspace/run_ts.log 2>/dev/null; then
    pack
    for w in $(seq 1 6); do [ -f /workspace/FETCHED_TS ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 3600 ]; then pack; stop_pod cap60min; exit; fi
  if pgrep -f "python|pip|git" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
