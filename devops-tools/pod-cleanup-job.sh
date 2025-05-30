#!/bin/bash

# Kubernetes Deployment Cleanup Script
# Cleans up deployments older than 45 minutes where pod names start with "Challenge"
# Also removes associated services and other related resources

set -e

# Configuration
THRESHOLD_MINUTES=1
THRESHOLD_SECONDS=$((THRESHOLD_MINUTES * 60))
NAMESPACE="${NAMESPACE:-default}"
DRY_RUN="${DRY_RUN:-false}"

echo "=================================="
echo "K8s Deployment Cleanup Script"
echo "=================================="
echo "Namespace: $NAMESPACE"
echo "Threshold: $THRESHOLD_MINUTES minutes ($THRESHOLD_SECONDS seconds)"
echo "Dry Run: $DRY_RUN"
echo "=================================="

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed or not in PATH"
    exit 1
fi

# Check if we can connect to the cluster
if ! kubectl cluster-info &> /dev/null; then
    echo "Error: Cannot connect to Kubernetes cluster"
    exit 1
fi

echo "Starting cleanup process..."

# Get current timestamp
CURRENT_TIME=$(date +%s)

# Debug: Show all deployments for troubleshooting
echo ""
echo "All deployments in namespace '$NAMESPACE':"
kubectl get deployments -n "$NAMESPACE" --no-headers -o custom-columns=NAME:.metadata.name,AGE:.metadata.creationTimestamp 2>/dev/null || {
    echo "No deployments found in namespace '$NAMESPACE' or namespace doesn't exist"
    exit 0
}

echo ""

# Get all deployment names and filter for Challenge
echo "Looking for deployments with names starting with 'Challenge'..."
ALL_DEPLOYMENTS=$(kubectl get deployments -n "$NAMESPACE" --no-headers -o custom-columns=NAME:.metadata.name 2>/dev/null || echo "")

if [ -z "$ALL_DEPLOYMENTS" ]; then
    echo "No deployments found in namespace '$NAMESPACE'"
    exit 0
fi

CHALLENGE_DEPLOYMENTS=""
for dep in $ALL_DEPLOYMENTS; do
    if [[ "$dep" == Challenge* ]]; then
        CHALLENGE_DEPLOYMENTS="$CHALLENGE_DEPLOYMENTS $dep"
    fi
done

# Trim whitespace
CHALLENGE_DEPLOYMENTS=$(echo $CHALLENGE_DEPLOYMENTS | xargs)

if [ -z "$CHALLENGE_DEPLOYMENTS" ]; then
    echo "No deployments found starting with 'Challenge'"

    # Fallback: case-insensitive search
    echo "Checking for deployments containing 'challenge' (case-insensitive)..."
    FALLBACK_DEPLOYMENTS=""
    for dep in $ALL_DEPLOYMENTS; do
        if [[ "${dep,,}" == *challenge* ]]; then
            FALLBACK_DEPLOYMENTS="$FALLBACK_DEPLOYMENTS $dep"
        fi
    done

    FALLBACK_DEPLOYMENTS=$(echo $FALLBACK_DEPLOYMENTS | xargs)

    if [ -z "$FALLBACK_DEPLOYMENTS" ]; then
        echo "No deployments found containing 'challenge'"
        echo "Available deployments: $ALL_DEPLOYMENTS"
        exit 0
    else
        echo "Found deployments containing 'challenge': $FALLBACK_DEPLOYMENTS"
        CHALLENGE_DEPLOYMENTS="$FALLBACK_DEPLOYMENTS"
    fi
fi

echo "Found Challenge deployments: $CHALLENGE_DEPLOYMENTS"
echo ""

# Function to find and delete associated services
delete_associated_services() {
    local deployment_name=$1
    local services_deleted=0
    
    echo "  Looking for services associated with deployment: $deployment_name"
    
    # Method 1: Check for service with same name as deployment
    if kubectl get service "$deployment_name" -n "$NAMESPACE" >/dev/null 2>&1; then
        if [ "$DRY_RUN" = "true" ]; then
            echo "  [DRY RUN] Would delete service with same name: $deployment_name"
        else
            echo "  Deleting service with same name: $deployment_name"
            if kubectl delete service "$deployment_name" -n "$NAMESPACE"; then
                echo "  ✓ Successfully deleted service: $deployment_name"
                services_deleted=$((services_deleted + 1))
            else
                echo "  ✗ Failed to delete service: $deployment_name"
            fi
        fi
    fi
    
    # Method 2: Find services by selector labels that match the deployment
    echo "  Searching for services with selectors matching deployment labels..."
    
    # Get deployment labels
    DEPLOYMENT_LABELS=$(kubectl get deployment "$deployment_name" -n "$NAMESPACE" -o jsonpath='{.spec.selector.matchLabels}' 2>/dev/null)
    
    if [ -n "$DEPLOYMENT_LABELS" ] && [ "$DEPLOYMENT_LABELS" != "{}" ]; then
        # Convert JSON labels to label selector format
        LABEL_SELECTOR=$(echo "$DEPLOYMENT_LABELS" | sed 's/[{}"]//g' | sed 's/:/=/g' | sed 's/,/,/g')
        
        if [ -n "$LABEL_SELECTOR" ]; then
            echo "  Using label selector: $LABEL_SELECTOR"
            
            # Find services that might be selecting pods from this deployment
            RELATED_SERVICES=$(kubectl get services -n "$NAMESPACE" -o name 2>/dev/null | while read service_name; do
                service_name=${service_name#service/}
                # Skip if it's the same-name service we already handled
                if [ "$service_name" != "$deployment_name" ]; then
                    # Check if service selector matches deployment labels
                    SERVICE_SELECTOR=$(kubectl get service "$service_name" -n "$NAMESPACE" -o jsonpath='{.spec.selector}' 2>/dev/null)
                    if [ -n "$SERVICE_SELECTOR" ] && [ "$SERVICE_SELECTOR" != "{}" ]; then
                        # Simple check - if service selector contains deployment labels
                        if echo "$DEPLOYMENT_LABELS" | grep -q "$(echo "$SERVICE_SELECTOR" | sed 's/[{}"]//g')" 2>/dev/null; then
                            echo "$service_name"
                        fi
                    fi
                fi
            done)
            
            for related_service in $RELATED_SERVICES; do
                if [ -n "$related_service" ]; then
                    if [ "$DRY_RUN" = "true" ]; then
                        echo "  [DRY RUN] Would delete related service: $related_service"
                    else
                        echo "  Deleting related service: $related_service"
                        if kubectl delete service "$related_service" -n "$NAMESPACE"; then
                            echo "  ✓ Successfully deleted related service: $related_service"
                            services_deleted=$((services_deleted + 1))
                        else
                            echo "  ✗ Failed to delete related service: $related_service"
                        fi
                    fi
                fi
            done
        fi
    fi
    
    # Method 3: Check for services with labels indicating they belong to this deployment
    echo "  Searching for services with metadata labels referencing this deployment..."
    LABELED_SERVICES=$(kubectl get services -n "$NAMESPACE" -o json 2>/dev/null | \
        jq -r --arg dep "$deployment_name" '.items[] | select(.metadata.labels // {} | to_entries[] | .value == $dep or (.key | test("app|component|deployment") and .value == $dep)) | .metadata.name' 2>/dev/null || echo "")
    
    for labeled_service in $LABELED_SERVICES; do
        if [ -n "$labeled_service" ] && [ "$labeled_service" != "$deployment_name" ]; then
            if [ "$DRY_RUN" = "true" ]; then
                echo "  [DRY RUN] Would delete labeled service: $labeled_service"
            else
                echo "  Deleting labeled service: $labeled_service"
                if kubectl delete service "$labeled_service" -n "$NAMESPACE"; then
                    echo "  ✓ Successfully deleted labeled service: $labeled_service"
                    services_deleted=$((services_deleted + 1))
                else
                    echo "  ✗ Failed to delete labeled service: $labeled_service"
                fi
            fi
        fi
    done
    
    if [ $services_deleted -eq 0 ]; then
        echo "  No associated services found for deployment: $deployment_name"
    else
        echo "  ✓ Deleted $services_deleted associated service(s) for deployment: $deployment_name"
    fi
    
    return $services_deleted
}

# Process each deployment
DELETED_COUNT=0
KEPT_COUNT=0
TOTAL_SERVICES_DELETED=0

for DEPLOYMENT in $CHALLENGE_DEPLOYMENTS; do
    echo "Checking deployment: $DEPLOYMENT"

    # Get deployment creation time
    CREATION_TIME=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" -o jsonpath='{.metadata.creationTimestamp}' 2>/dev/null)

    if [ -z "$CREATION_TIME" ]; then
        echo "Warning: Could not get creation time for deployment $DEPLOYMENT"
        continue
    fi

    # Convert to timestamp (handle different date command versions)
    if date --version >/dev/null 2>&1; then
        # GNU date (Linux)
        CREATION_TIMESTAMP=$(date -d "$CREATION_TIME" +%s 2>/dev/null)
    else
        # BSD date (macOS)
        CREATION_TIMESTAMP=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$CREATION_TIME" +%s 2>/dev/null)
    fi

    if [ -z "$CREATION_TIMESTAMP" ]; then
        echo "Warning: Could not parse creation time for deployment $DEPLOYMENT: $CREATION_TIME"
        continue
    fi

    # Calculate age in seconds
    AGE_SECONDS=$((CURRENT_TIME - CREATION_TIMESTAMP))
    AGE_MINUTES=$((AGE_SECONDS / 60))

    echo "  Creation time: $CREATION_TIME"
    echo "  Age: $AGE_MINUTES minutes ($AGE_SECONDS seconds)"
    echo "  Threshold: $THRESHOLD_MINUTES minutes ($THRESHOLD_SECONDS seconds)"

    if [ $AGE_SECONDS -gt $THRESHOLD_SECONDS ]; then
        echo "  ✓ Deployment $DEPLOYMENT is older than threshold"

        if [ "$DRY_RUN" = "true" ]; then
            echo "  [DRY RUN] Would delete deployment: $DEPLOYMENT"
            delete_associated_services "$DEPLOYMENT"
        else
            echo "  Deleting deployment: $DEPLOYMENT"
            if kubectl delete deployment "$DEPLOYMENT" -n "$NAMESPACE"; then
                echo "  ✓ Successfully deleted deployment: $DEPLOYMENT"
                
                # Delete associated services
                delete_associated_services "$DEPLOYMENT"
                TOTAL_SERVICES_DELETED=$((TOTAL_SERVICES_DELETED + $?))
            else
                echo "  ✗ Failed to delete deployment: $DEPLOYMENT"
                continue
            fi
        fi

        DELETED_COUNT=$((DELETED_COUNT + 1))
    else
        echo "  - Deployment $DEPLOYMENT is within threshold, keeping it"
        KEPT_COUNT=$((KEPT_COUNT + 1))
    fi

    echo ""
done

echo "=================================="
echo "Cleanup Summary:"
echo "  Deployments processed: $((DELETED_COUNT + KEPT_COUNT))"
echo "  Deployments deleted: $DELETED_COUNT"
echo "  Services deleted: $TOTAL_SERVICES_DELETED"
echo "  Deployments kept: $KEPT_COUNT"
if [ "$DRY_RUN" = "true" ]; then
    echo "  Mode: DRY RUN (no actual deletions performed)"
fi
echo "=================================="
echo "Cleanup process completed"
