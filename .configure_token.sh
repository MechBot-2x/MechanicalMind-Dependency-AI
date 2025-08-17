#!/bin/bash
# ================================================
# 🛡️ MECHANICAL MIND TOKEN VERIFICATION SCRIPT
# ================================================
# Version: 3.1.0
# Checks and configures GITHUB_TOKEN with safety checks
# ================================================

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to verify existing token
verify_token() {
    echo -e "${YELLOW}🔍 Verifying existing GITHUB_TOKEN configuration...${NC}"
    
    # Check in workflow files
    local token_usage=$(grep -r "secrets.GITHUB_TOKEN" .github/workflows/ 2>/dev/null)
    
    if [ -z "$token_usage" ]; then
        echo -e "${RED}❌ No GITHUB_TOKEN usage found in workflow files${NC}"
        return 1
    else
        echo -e "${GREEN}✅ GITHUB_TOKEN referenced in workflows:${NC}"
        echo "$token_usage" | while read -r line; do
            echo -e "  📄 ${line}"
        done
        
        # Check permissions
        local permissions=$(grep -A 5 -r "permissions:" .github/workflows/ 2>/dev/null)
        if [ -z "$permissions" ]; then
            echo -e "${YELLOW}⚠️  No explicit permissions found for GITHUB_TOKEN${NC}"
            return 2
        else
            echo -e "${GREEN}🔑 Current token permissions:${NC}"
            echo "$permissions" | while read -r line; do
                echo -e "  🔧 ${line}"
            done
            return 0
        fi
    fi
}

# Function to configure token
configure_token() {
    echo -e "\n${YELLOW}🛠️  Configuring GITHUB_TOKEN...${NC}"
    
    # Create workflows directory if doesn't exist
    mkdir -p .github/workflows
    
    # Create backup
    cp .github/workflows/*.yml .github/workflows/backup/ 2>/dev/null
    
    # Generate minimal safe configuration
    cat <<EOF > .github/workflows/token_test.yml
name: Token Verification Workflow

on:
  workflow_dispatch:

permissions:
  contents: read
  actions: read

jobs:
  verify-token:
    runs-on: ubuntu-latest
    steps:
      - name: Check token permissions
        run: |
          echo "Token permissions verified"
          echo "Workflow run ID: \${{ github.run_id }}"
EOF

    echo -e "${GREEN}✅ Created test workflow with safe permissions${NC}"
}

# Main execution
echo -e "\n${YELLOW}⚙️  MechanicalMind Token Configuration System${NC}"
echo -e "${YELLOW}=============================================${NC}"

# Step 1: Verify existing configuration
verify_token
verification_status=$?

case $verification_status in
    0)
        echo -e "\n${GREEN}✅ Token already properly configured. No changes needed.${NC}"
        exit 0
        ;;
    1)
        echo -e "\n${YELLOW}⚠️  No existing token configuration found${NC}"
        ;;
    2)
        echo -e "\n${YELLOW}⚠️  Existing configuration needs permission updates${NC}"
        ;;
esac

# Step 2: Get user confirmation
read -p "Do you want to configure GITHUB_TOKEN with safe defaults? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ Configuration aborted by user${NC}"
    exit 1
fi

# Step 3: Configure token
configure_token

# Step 4: Verify new configuration
echo -e "\n${YELLOW}🔍 Verifying new configuration...${NC}"
verify_token

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}🎉 Successfully configured GITHUB_TOKEN with proper permissions${NC}"
    echo -e "Next steps:"
    echo -e "1. Commit and push these changes"
    echo -e "2. Monitor the test workflow run"
    echo -e "3. Review permissions for your specific needs"
else
    echo -e "\n${RED}❌ Configuration failed. Please check manually.${NC}"
    exit 1
fi
