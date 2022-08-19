
# Rail Track Toolbox

## Context of development

This toolbox have been developed during a project called:
*Novel Rail Pads for Improved Noise Reduction and Reduced Track Maintenance.*  
This project was founded by the [Swiss Federal Office for the ENvironment FOEN](https://www.bafu.admin.ch/bafu/en/home/office.html) and carried out by a consortium of scientific laboratories form Switzerland. This consortium was a collaboration between the following entities:

- [Swiss Institute of Technology of Lausanne](https://www.epfl.ch/en/) (EPFL),  
- [Swiss Federal Railways](https://www.sbb.ch/en/home.html) (SBB),  
- [School of Engineering and Management of Yverdon](https://heig-vd.ch/en) (HEIG-vd),  
- [Swiss Federal Laboratories for Materials Science and Technology](https://www.empa.ch/) (EMPA).  

For the last phase of the project, a company joins the consortium:

- [Semperit Group](https://www.semperitgroup.com/) from Austria

The project aims to reduce the noise emission of rail tracks and increase track maintenance intervals by the development of a new rail pad. The selected approach was the development of an experimental set-up combine with a digital tween (i.e. The Three Sleepers Model presented later). Other models have been developed and experimentally validated to achieve our goals.

## What is this toolbox for ?

As said previously, the toolbox have been develops to design new rail pads, and thus can be used in the same way.  
Furthermore, models has been created using open source tools and can be easily modified and/or incremented with new functionalities.  
Therefore this toolbox is the first step in the creation of a open source and collaborative platform for the rail way experts.  
Anyone interested and working in this field can use and/or developed the existing models or add new ones.

## What does it contain ?

This toolbox is composed of four finites elements models and one semi-analytical model:

1. The *PadStiffness* Model
2. The *Semi-Analytical* Model
3. The *Three Sleepers* Model
4. The *Impulse* Model
5. The *Multi-Sleepers* Model

Each model can be found separately in the *src* directory. Alternatively the full toolbox can be downloaded as a Virtual Machine container and run on any Linux distribution.

A overview of each model is presented in the following paragraphs, please refer to the specific chapter in the documentation for more information on the models.

### The PadStiffness model

The Pad Stiffness Model aim to estimate the static and dynamic stiffness of the input pad design. It is a digital twin of an experimental compression system.
After validation in static and low dynamic (10 and 20 Hz) compression with the experimental results, the model have been extended to provide the stiffness in various directions and with an extended frequency range.  

### The Semi-Analytical model

### The Three Sleepers model

### The Impulse model

The Impulse model is a variation of the three sleepers model, operating in the time and not the frequency domain.  
It aims to reproduce a pass-by of a bogie on a sleeper. Therefore a *M* shaped impulse is imposed to both rails above the middle sleeper.

### The Multi-Sleepers model

## Download

## Libraries and dependencies

1. Code_Aster 2019
2. Salome (2019 ?)
3. Python 3? 2?  

   - Which specific libraries ?
   -

4. Bash
5. PyQT5
6. Others ?

## Getting Started

This repository contain three folders: *Documentation*, *src* and *Toolbox-VM*. The first folder contain the documentation of the toolbox: description of the models, how to use the interface and so on. The second folder, *src*, contain the individual models. The last folder, *Toolbox-VM*, contain a virtual machine container with the whole toolbox ready to be used on any Linux distribution.
The easiest way to start using the toolbox is to download and use the *Toolbox-VM* virtual machine container.
Once installed, the best way to start using the model is to use the GUI provided for each model. Part of the documentation describes the steps to follow in order to run a simulation with the selected model.

## Contributing

### Learning Code_Aster

If you want to learn more about *Code_Aster* you can visit their [official web site](https://www.code-aster.org/)

### Learning Salome

If you want to learn more about *Salome*, a multi-platform open source scientific computing environment, you can visit their [official web site](https://www.salome-platform.org/)

## License
