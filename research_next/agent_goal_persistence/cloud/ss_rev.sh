#!/bin/bash
# Self-stop for REVPILOT (ss_auth.sh with rev labels; cap 75 min). After CLOUD_REV_DONE in run_rev.log: pack, then wait for
# /workspace/FETCHED_REV (laptop watcher) or 6 min. Also stops after 15 idle min or at a 75-min cap.
stop_pod() {
  echo "$(date) selfstop_rev: $1" >> /workspace/selfstop_rev.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop_rev.log 2>&1
}
pack() { tar czf /workspace/results_rev.tgz -C /workspace/agprev out_rev 2>/dev/null; md5sum /workspace/results_rev.tgz > /workspace/results_rev.md5; touch /workspace/PACKED_REV; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD_REV_DONE /workspace/run_rev.log 2>/dev/null; then
    pack
    for w in $(seq 1 6); do [ -f /workspace/FETCHED_REV ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 4500 ]; then pack; stop_pod cap75min; exit; fi
  if pgrep -f "python|pip|git" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
