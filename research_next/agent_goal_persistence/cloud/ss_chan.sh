#!/bin/bash
# Self-stop for CHANNEL (ss_ts.sh with ch labels; cap 200 min). After CLOUD_CHAN_DONE in run_ch.log: pack, then wait for
# /workspace/FETCHED_CH (laptop watcher) or 6 min. Also stops after 15 idle min or at a 200-min cap.
stop_pod() {
  echo "$(date) selfstop_ch: $1" >> /workspace/selfstop_ch.log
  curl -s -X POST https://api.runpod.io/graphql -H "Content-Type: application/json" -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -d "{\"query\":\"mutation { podStop(input: {podId: \\\"$RUNPOD_POD_ID\\\"}) { id desiredStatus } }\"}" >> /workspace/selfstop_ch.log 2>&1
}
pack() { tar czf /workspace/results_ch.tgz -C /workspace/agpch out_chan out_chan_pilot 2>/dev/null; md5sum /workspace/results_ch.tgz > /workspace/results_ch.md5; touch /workspace/PACKED_CH; }
start=$(date +%s); idle=0
while true; do
  sleep 60
  if grep -q CLOUD_CHAN_DONE /workspace/run_ch.log 2>/dev/null; then
    pack
    for w in $(seq 1 6); do [ -f /workspace/FETCHED_CH ] && break; sleep 60; done
    stop_pod done; exit
  fi
  if [ $(( $(date +%s) - start )) -gt 12000 ]; then pack; stop_pod cap200min; exit; fi
  if pgrep -f "python|pip|git" > /dev/null; then idle=0; else idle=$((idle+1)); fi
  if [ $idle -ge 15 ]; then pack; stop_pod idle15min; exit; fi
done
