
# Rail Track Modelling Toolbox

## Container and Linux distribution / virtual machine images 

To simplify the use of the toolbox without having to install all prerequisites and setup, we provide here several options:

1. A Linux distribution image (ISO) based on CAELinux 2020 with the toolbox preinstalled. This ISO image can be used to either
    - create a USB boot disk using the Ventoy utility and install the distribution on a physical machine (best performance)
    - install a virtual machine in your currently running operating system (VMWare Player or Workstation is recommended).

2. A Singularity container that can be used to run the toolbox in any Linux environment (provided that Singularity is installed, also works on Windows via WSL).


## Download links

Coming soon...

## Installation instruction: Physical Machine

1. Download the ISO image
2. Install Ventoy from https://www.ventoy.net/
3. Insert a USB flash disk (save data first as it will be formatted)
4. Run Ventoy to install the bootloader on that USB drive
5. Copy the ISO image in the VENTOY disk partition of the USB drive
6. Reboot your PC (in Windows press CTRL-SHIFT to perform a full reboot) and enter the UEFI / BIOS menu
7. Select the USB drive as a boot drive
8. In the boot menu, select CAELinux 2020 and wait until the full desktop is loaded. 
   ( if you cannot get tot the boot menu, enter your UEFI/BIOS and Disable SecureBoot)   
9. Once on the desktop, double click the Install CAELinux 2020 icon to start the installer. 
10. Install the distribution as you would do for any Ubuntu system (read Ubuntu documentation for more info). You will need at least 50Gb (>70Gb recommended) of hard disk space for the system.

Note that you can use the toolbox in Live mode without installation for simple computations   

## Installation instruction: Virtual Machine

1. Download the ISO image
2. Install VMware player from https://www.vmware.com/products/workstation-player.html (other VM options work for computations, but have some issues with 3D rendering in Salomé)
3. Create a new Virtual Machine
4. Set the OS type as Ubuntu 64bit, Memory >8Gb (16Gb or more recommended), and create a virtual disk of at least 100Gb (dynamic size).
5. In the VM settings, enable 3D acceleration and set the virtual DVD drive to point to the ISO image of the Toolbox (downloaded in point 1)
4. Run the Virtual machine
5. In the boot menu, select CAELinux 2020 and wait until the full desktop is loaded. 
   ( if you cannot get tot the boot menu, enter your UEFI/BIOS and Disable SecureBoot)   
9. Once on the desktop, double click the Install CAELinux 2020 icon to start the installer. 
10. Install the distribution as you would do for any Ubuntu system (read Ubuntu documentation for more info). Choose the "use the whole disk" option

Note that you can also use the toolbox in Live mode in a VM (without installation) for simple computations   


## Installation instruction: Singularity container

First you will need an installed Linux distribution of your choice, including WSL2 on Windows. 

Please note that we have made Singularity .deb packages for Ubuntu 18.04 to 22.04 to simplify the installation on those system (see download section).

1. In your Linux system, you will first need to install Singularity version 3.5 or above. If running Ubuntu 18.04 or 22.04, you can simply download the pre-made .deb packages above and double click on it to install Singularity.
For other OS or versions, please look for packages in your software center or read Singularity documentation to install from source: https://docs.sylabs.io/guides/3.5/user-guide/quick_start.html
2. Once Singularity is installed and verified to run, download the Singularity image .sif above and put it in the final folder where you intend to execute it.
3. The toolbox need to be able to write "temporary" files to the container and thus some memory need to be allocated for those operations. Run the following command to set the max size of temporary files:

> sudo singularity config global --set "sessiondir max size" 2048

Note: if you get "read only file system" or "no space left on device" when running models, you can increase this size to 4096 for example.

4. Now to run the toolbox simply type:

> singularity run --writable-tmpfs RailTrackModellingToolbox.sif

Note: if you want to modify some files in the container or update some models, you can create a writable "sandbox" version of the container with:

> singularity build --sandbox RailTrackModellingToolbox RailTrackModellingToolbox.sif

then you can enter a "root" shell with :

> sudo singularity shell RailTrackModellingToolbox

that will allow you to modify all the installed files in the container.

You can also run a simulation from the sandbox (that is  writable and thus data are persistent as well) with 

> singularity run --writable RailTrackModellingToolbox

Finally, if you want to package a modified container image from the modified sandbox, simply run:

> singularity build newRailTrackToolbox.sif RailTrackModellingToolbox 



