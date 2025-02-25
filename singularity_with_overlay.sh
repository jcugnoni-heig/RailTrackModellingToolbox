#!/bin/bash

# Check if a command is installed
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "Error: $1 is not installed. Please install it before continuing."
        exit 1
    fi
}

# Check for required tools
check_command git
check_command curl

# Define default branch
branch_name=${1:-"main"}

# Display the branch being used
echo "Branch selected: $branch_name"

repo_url="https://github.com/jcugnoni-heig/RailTrackModellingToolbox.git"
repo_destination="github_repository"
sif_url="https://www.caelinux.com/downloads/stable/railtracktoolbox/singularity/RailTrackModellingToolbox.sif"

# Create the overlay image
dd if=/dev/zero of=overlay.img bs=1M count=512
mkfs.ext3 overlay.img
if [ $? -ne 0 ]; then
    echo "Error: Failed to create the overlay.img file."
    exit 1
fi
echo "Overlay image, overlay.img, created."

# Mount the overlay
sudo mount -o loop overlay.img /mnt/overlay
if [ $? -ne 0 ]; then
    echo "Error: Failed to mount the overlay."
    exit 1
fi
echo "Overlay mounted at path `/mnt/overlay`."

# Create necessary directories
sudo mkdir -p /mnt/overlay/upper
sudo mkdir -p /mnt/overlay/work
sudo mkdir -p /mnt/overlay/upper/opt/RailTrackModellingToolbox/src/MultiSleeperModel
sudo mkdir -p github_repository
echo "Necessary folders, upper and work, created."

# Clone the specific branch via Git
git clone -b "$branch_name" --single-branch "$repo_url" "$repo_destination"
if [ $? -ne 0 ]; then
    echo "Error: Failed to clone via Git."
    sudo umount /mnt/overlay
    exit 1
fi
echo "MultiSleeperModel extracted from GitHub."

# Copy the contents of the src/MultiSleeperModel folder to /mnt/overlay/upper/opt/RailTrackModellingToolbox/src/MultiSleeperModel
sudo cp -r "$repo_destination/src/MultiSleeperModel/." "/mnt/overlay/upper/opt/RailTrackModellingToolbox/src/MultiSleeperModel/"
if [ $? -ne 0 ]; then
    echo "Error: Failed to copy the contents."
    sudo umount /mnt/overlay
    exit 1
fi
echo "Contents of the MultiSleeperModel folder copied successfully."

# Run setup0.sh
if [ -f "$repo_destination/setup0.sh" ]; then
    echo "Running setup0.sh..."
    sudo bash $repo_destination/setup0.sh
    if [ $? -ne 0 ]; then
        echo "Error: setup0.sh failed."
        sudo umount /mnt/overlay
        exit 1
    fi
    echo "setup0.sh completed successfully."
else
    echo "Error: setup0.sh not found."
    sudo umount /mnt/overlay
    exit 1
fi

# Run setup.sh
if [ -f "$repo_destination/setup.sh" ]; then
    echo "Running setup.sh..."
    sudo bash $repo_destination/setup.sh
    if [ $? -ne 0 ]; then
        echo "Error: setup.sh failed."
        sudo umount /mnt/overlay
        exit 1
    fi
    echo "setup.sh completed successfully."
else
    echo "Error: setup.sh not found."
    sudo umount /mnt/overlay
    exit 1
fi

# Unmount the overlay
sudo umount /mnt/overlay
if [ $? -ne 0 ]; then
    echo "Error: Failed to unmount the overlay."
    exit 1
fi
echo "Overlay unmounted."

# Download the Singularity image via curl with progress bar
echo "Starting to download the Singularity image."
sudo curl -O --progress-bar "$sif_url"
if [ $? -ne 0 ]; then
    echo "Error: Failed to download the Singularity image."
    exit 1
fi
echo "Singularity image downloaded successfully."

echo "Script completed. You will find the Singularity image (RailTrackModellingToolbox.sif) and the overlay image (overlay.img) in the current folder."
echo "To run it, use the following command: >> singularity run --overlay overlay.img RailTrackModellingToolbox.sif"
