#!/usr/bin/env bash
# ==============================================================================
# rad-mon / opi-mon Installation Script
# Installs rad-mon to /usr/local/bin/ with symlinks for global accessibility
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing rad-mon..."
sudo install -m 755 "${SCRIPT_DIR}/rad-mon.sh" /usr/local/bin/rad-mon
sudo ln -sf /usr/local/bin/rad-mon /usr/local/bin/opi-mon
sudo ln -sf /usr/local/bin/rad-mon /usr/bin/rad-mon
sudo ln -sf /usr/local/bin/rad-mon /usr/bin/opi-mon

echo "Installation complete!"
echo "You can now run 'rad-mon' or 'opi-mon' from any terminal."
