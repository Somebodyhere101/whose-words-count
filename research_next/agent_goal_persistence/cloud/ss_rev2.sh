#!/bin/bash
# Self-stop for REVPILOT 2 (ss_rev.sh with rev2 labels; cap 60 min). After CLOUD_REV2_DONE in run_rev2.log: pack, then wait for
# /workspace/FETCHED_REV2 (laptop watcher) or 6 min. Also stops after 15 idle min or at a 60-min cap.
stop_pod() {
  echo "$(date) selfstop_rev2: $1" >> /workspace/selfstop_rev2.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop_rev2.log 2>&1
}
pack() { tar czf /workspace/results_rev2.tgz -C /workspace/agprev2 out_rev 2>/dev/null; md5sum /workspace/results_rev2.tgz > /workspace/results_rev2.md5; touch /workspace/PACKED_REV2; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD_REV2_DONE /workspace/run_rev2.log 2>/dev/null; then
    pack
    for w in $(seq 1 6); do [ -f /workspace/FETCHED_REV2 ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 3600 ]; then pack; stop_pod cap60min; exit; fi
  if pgrep -f "python|pip|git" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
