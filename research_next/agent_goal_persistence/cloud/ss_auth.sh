#!/bin/bash
# Self-stop for AUTHPILOT (ss_mp1.sh with auth labels). After CLOUD_AUTH_DONE in run_auth.log: pack, then wait for
# /workspace/FETCHED_AUTH (laptop watcher) or 6 min. Also stops after 15 idle min or at a 2.5-hour cap.
stop_pod() {
  echo "$(date) selfstop_auth: $1" >> /workspace/selfstop_auth.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop_auth.log 2>&1
}
pack() { tar czf /workspace/results_auth.tgz -C /workspace/agpauth out_auth 2>/dev/null; md5sum /workspace/results_auth.tgz > /workspace/results_auth.md5; touch /workspace/PACKED_AUTH; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD_AUTH_DONE /workspace/run_auth.log 2>/dev/null; then
    pack
    for w in $(seq 1 6); do [ -f /workspace/FETCHED_AUTH ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 6000 ]; then pack; stop_pod cap100min; exit; fi
  if pgrep -f "python|pip|git" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
