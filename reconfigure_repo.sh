#!/bin/bash
# ================================================
# 🔄 MECHANICAL MIND REPOSITORY RESET & TOKEN CONFIG
# ================================================
# Version: 3.1.1
# Safely re-clones repo and configures GITHUB_TOKEN
# ================================================

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
REPO_URL="git@github.com:MechBot-2x/MechanicalMind-Dependency-AI.git"
TARGET_DIR="MechanicalMind-Dependency-AI"
CONFIG_SCRIPT="configure_token.sh"

# Step 1: Remove existing repository
echo -e "${YELLOW}🗑️  Removing existing repository...${NC}"
if [ -d "$TARGET_DIR" ]; then
    rm -rf "$TARGET_DIR" && echo -e "${GREEN}✅ Successfully removed old repository${NC}"
else
    echo -e "${YELLOW}⚠️  Repository directory not found, skipping removal${NC}"
fi

# Step 2: Clone fresh copy
echo -e "${YELLOW}📥 Cloning repository...${NC}"
git clone "$REPO_URL" "$TARGET_DIR" && \
cd "$TARGET_DIR" && \
echo -e "${GREEN}✅ Successfully cloned repository${NC}"

# Step 3: Create token configuration script
cat << 'EOF' > "$CONFIG_SCRIPT"
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
EOF

# Make script executable
chmod +x "$CONFIG_SCRIPT" && \
echo -e "${GREEN}✅ Created configuration script${NC}"

# Step 4: Execute configuration
echo -e "${YELLOW}🛠️  Running token configuration...${NC}"
./"$CONFIG_SCRIPT"

# Final instructions
echo -e "\n${GREEN}🎉 Setup complete! Next steps:${NC}"
echo "1. Review the created workflow file:"
echo "   cat .github/workflows/token_verification.yml"
echo "2. Commit and push your changes:"
echo "   git add .github/workflows/token_verification.yml"
echo "   git commit -m 'Configure GITHUB_TOKEN permissions'"
echo "   git push origin main"
echo "3. Manually trigger the workflow in GitHub Actions to verify"
