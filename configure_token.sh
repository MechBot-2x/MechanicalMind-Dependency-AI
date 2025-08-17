#!/bin/bash
# GITHUB_TOKEN Configuration Script

verify_token() {
    echo "🔍 Checking existing token configuration..."
    grep -r "secrets.GITHUB_TOKEN" .github/workflows/ 2>/dev/null || \
    echo "ℹ️ No existing token configuration found"
}

configure_workflow() {
    local PERMISSIONS="$1"
    local WORKFLOW_FILE=".github/workflows/token_verification.yml"
    
    mkdir -p .github/workflows
    cat << EOWF > "$WORKFLOW_FILE"
name: Token Permissions Verification
on: [workflow_dispatch]
permissions: $PERMISSIONS
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Token permissions verified"
EOWF

    echo "✅ Created verification workflow with permissions:"
    yq eval '.permissions' "$WORKFLOW_FILE"
}

# Main execution
PS3="Select permission profile: "
options=(
    "Basic CI/CD (read-only)"
    "Deployment (write access)"
    "Runner Management (admin access)"
    "Custom"
    "Exit"
)

select opt in "${options[@]}"
do
    case $opt in
        "Basic CI/CD (read-only)")
            configure_workflow "{ contents: read, actions: read, packages: read }"
            break
            ;;
        "Deployment (write access)")
            configure_workflow "{ contents: write, deployments: write }"
            break
            ;;
        "Runner Management (admin access)")
            configure_workflow "{ actions: write, runners: write }"
            break
            ;;
        "Custom")
            read -p "Enter custom permissions (YAML format): " custom_perms
            configure_workflow "$custom_perms"
            break
            ;;
        "Exit")
            echo "Configuration cancelled"
            exit 0
            ;;
        *) echo "Invalid option";;
    esac
done

verify_token
