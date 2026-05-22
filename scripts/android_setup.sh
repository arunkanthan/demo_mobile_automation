#!/usr/bin/env bash
set -euo pipefail

# Minimal Android SDK / emulator setup helper
# Assumes you have Android command line tools (sdkmanager, avdmanager) available

SDK_ROOT=${ANDROID_SDK_ROOT:-"$HOME/Library/Android/sdk"}
export ANDROID_SDK_ROOT="$SDK_ROOT"
export PATH="$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools:$ANDROID_SDK_ROOT/emulator:$PATH"

echo "Using ANDROID_SDK_ROOT=$ANDROID_SDK_ROOT"

# Check Java runtime
if ! command -v java >/dev/null 2>&1; then
  cat <<'WARN'
ERROR: Java runtime not found.
Install OpenJDK (recommended) before running this script. On macOS you can:

  brew install openjdk
  sudo mkdir -p /Library/Java/JavaVirtualMachines
  sudo ln -sfn "$(brew --prefix)/opt/openjdk/libexec/openjdk.jdk" /Library/Java/JavaVirtualMachines/openjdk.jdk
  echo 'export PATH="$(brew --prefix)/opt/openjdk/bin:$PATH"' >> ~/.zshrc
  echo 'export JAVA_HOME="$(/usr/libexec/java_home)"' >> ~/.zshrc
  source ~/.zshrc

After installing Java, re-run this script.
WARN
  exit 1
fi

command -v sdkmanager >/dev/null 2>&1 || { echo >&2 "sdkmanager not found. Install Android command-line tools or Android Studio."; exit 1; }

echo "Accepting Android licenses..."
yes | sdkmanager --licenses >/dev/null 2>&1 || true

echo "Installing command-line tools, platform-tools, and emulator (if missing)..."
sdkmanager --sdk_root="$ANDROID_SDK_ROOT" "cmdline-tools;latest" "platform-tools" "emulator" "platforms;android-33" || true

# Ensure SDK command-line tool binaries are first in PATH
export PATH="$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools:$ANDROID_SDK_ROOT/emulator:$PATH"

if ! command -v avdmanager >/dev/null 2>&1; then
  echo >&2 "avdmanager not found after installing command-line tools. Check that cmdline-tools are installed under $ANDROID_SDK_ROOT/cmdline-tools/latest/bin."
  exit 1
fi

# System image selection: allow user to pass a system image as second arg
# Example image id: system-images;android-33;google_apis;x86_64
REQUESTED_IMAGE=${2:-}

HOST_ARCH=$(uname -m)
echo "Detected host architecture: $HOST_ARCH"

case "$HOST_ARCH" in
  arm64|aarch64)
    DEFAULT_IMAGES=(
      "system-images;android-33;google_apis_playstore;arm64-v8a"
      "system-images;android-33;google_apis;arm64-v8a"
      "system-images;android-33;default;arm64-v8a"
      "system-images;android-31;google_apis;arm64-v8a"
    )
    ;;
  *)
    DEFAULT_IMAGES=(
      "system-images;android-33;google_apis;x86_64"
      "system-images;android-33;default;x86_64"
      "system-images;android-31;google_apis;x86_64"
      "system-images;android-30;default;x86"
    )
    ;;
esac

if [ -n "$REQUESTED_IMAGE" ]; then
  CANDIDATES=("$REQUESTED_IMAGE" "${DEFAULT_IMAGES[@]}")
else
  CANDIDATES=("${DEFAULT_IMAGES[@]}")
fi

SELECTED_IMAGE=""
for img in "${CANDIDATES[@]}"; do
  if [ -z "$img" ]; then
    continue
  fi
  echo "Trying system image: $img"
  if sdkmanager --sdk_root="$ANDROID_SDK_ROOT" --list_installed | grep -Fq "$img"; then
    echo "Image already installed: $img"
    SELECTED_IMAGE="$img"
    break
  fi
  echo "Attempting to install $img (may fail if not available)"
  if yes | sdkmanager --sdk_root="$ANDROID_SDK_ROOT" --install "$img"; then
    SELECTED_IMAGE="$img"
    break
  else
    echo "Failed to install $img, trying next candidate..."
  fi
done

if [ -z "$SELECTED_IMAGE" ]; then
  echo "ERROR: Could not find or install any suitable system image."
  echo "Available system images (partial list):"
  sdkmanager --sdk_root="$ANDROID_SDK_ROOT" --list | grep "system-images;" || true
  exit 1
fi

AVD_NAME=${1:-test_avd}

echo "Creating AVD named $AVD_NAME (if not exists)..."
if avdmanager list avd | grep -q "^$AVD_NAME"; then
  echo "AVD $AVD_NAME already exists"
else
  echo "Creating AVD $AVD_NAME with system image $SELECTED_IMAGE"
  echo no | avdmanager create avd -n "$AVD_NAME" -k "$SELECTED_IMAGE" --force
fi

echo "To start the emulator run:" 
echo "  $ANDROID_SDK_ROOT/emulator/emulator -avd $AVD_NAME &"
echo "Then verify with: adb devices"

echo "Done."
