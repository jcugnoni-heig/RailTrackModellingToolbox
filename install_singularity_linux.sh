#!/bin/bash

# ----- functions definitions -------------------------------------------------------

dependeciesInstallation(){

  echo "Installation of system dependecies"

  sudo apt-get update && sudo apt-get install -y \
      build-essential \
      libssl-dev \
      uuid-dev \
      libgpgme11-dev \
      squashfs-tools \
      libseccomp-dev \
      wget \
      pkg-config \
      git \
      cryptsetup
}

goInstallation(){

  echo "Installation of Go"

  export VERSION=1.16.4 OS=linux ARCH=amd64 && \  # Replace the values as needed
    wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz && \ # Downloads the required Go package
    sudo tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz && \ # Extracts the archive
    rm go$VERSION.$OS-$ARCH.tar.gz    # Deletes the ``tar`` file

  echo 'export PATH=/usr/local/go/bin:$PATH' >> ~/.bashrc && \
    source ~/.bashrc
}

singularityDownload(){

  echo "Download SingularityCE version 3.8.1 from a release"

  export VERSION=3.8.1 && # adjust this as necessary \
      wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-ce-${VERSION}.tar.gz && \
      tar -xzf singularity-ce-${VERSION}.tar.gz && \
      cd singularity-ce-${VERSION}
}

singularityCompilation(){
  
  echo "Compilation of the SingularityCE source code"

  export PATH=/usr/local/go/bin:$PATH

  ./mconfig && \
      make -C builddir && \
      sudo make -C builddir install
}

# ----- end functions definitions ---------------------------------------------------

# ----- script steps ----------------------------------------------------------------

echo "Installation of singularity started."

dependeciesInstallation

while [[ true ]] 
do
    read -p "Do you need to install Go (programmation laguange) ?[y/n]" go
    
    if [ "$go" == "yes" -o "$go" == "y" ];
        then
            break
    elif [ "$go" == "no"  -o "$go" == "n" ];
        then
            break
    else
        echo "I didn't get your answer, please re-try..."
    fi
done

if [ "$go" == "yes" -o "$go" == "y" ];
  then
    goInstallation
fi

singularityDownload

singularityCompilation

echo "Installation of singularity completed"

# ----- end script steps ------------------------------------------------------------
