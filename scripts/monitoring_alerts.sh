aws cloudwatch put-metric-alarm \
  --alarm-name "HighRunnerCPU" \
  --metric-name "CPUUtilization" \
  --namespace "GitHubRunners" \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
