#!/bin/bash

# Set age threshold in seconds (50 minutes = 3000 seconds)
AGE_THRESHOLD=3000

# Get current time in seconds
now=$(date +%s)

# Get list of services with their creation timestamps
kubectl get svc -n default -o json | jq -r '.items[] | "\(.metadata.namespace) \(.metadata.name) \(.metadata.creationTimestamp)"' | while read ns name timestamp; do
    # Convert creation timestamp to seconds
    if [ "$name" == "kubernetes" ]; then
        continue
    fi
    created=$(date -d "$timestamp" +%s)
    age=$((now - created))

    # If age is greater than threshold, delete the service
    if [ "$age" -gt "$AGE_THRESHOLD" ]; then
        echo "Deleting service $ns/$name (age: $((age / 60)) min)"
        kubectl delete svc "$name" -n "$ns"
    fi
done

