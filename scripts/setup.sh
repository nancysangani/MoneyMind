echo "🚀 Setting up MoneyMind..."
echo ""

# Create folder structure
echo "📁 Creating folder structure..."
mkdir -p ~/Documents/Finances/{2024,2025}/{Banking,Credit_Cards,Investments,Utilities,Subscriptions,Receipts,Tax_Prep}
mkdir -p ~/Documents/Finances/Dashboard

echo "✅ Folder structure created"
echo ""

# Copy dashboard template
echo "📊 Installing dashboard template..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cp "$PROJECT_ROOT/templates/dashboard/index.html" ~/Documents/Finances/Dashboard/
echo "✅ Dashboard template installed"
echo ""

# Create workflow shortcuts
echo "⚙️  Creating workflow shortcuts..."
mkdir -p ~/Documents/Finances/MoneyMind_Workflows
cp "$PROJECT_ROOT/accomplish-workflows"/*.md ~/Documents/Finances/MoneyMind_Workflows/
echo "✅ Workflows installed"
echo ""

echo "🎉 MoneyMind setup complete!"
echo ""
echo "Next steps:"
echo "1. Download and install Accomplish from https://accomplish.ai"
echo "2. Open Accomplish and configure your AI provider"
echo "3. Grant Accomplish folder access to:"
echo "   - ~/Downloads"
echo "   - ~/Documents/Finances"
echo "4. Try your first command:"
echo "   'organize all financial documents in my Downloads folder'"
echo ""
echo "For detailed help, see: docs/SETUP.md"
echo ""
echo "Happy automating! 💎"