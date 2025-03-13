# Acessible protein-ligand-Metal-Mg2+-Dummy (WORKING - 2025)

This google colab has been adjusted to perform a simple molecular dynamics (MD) of the OpenMM - Simple-Simulate-Complex developed by Tim Dudgeon and John Chodera (https://github.com/tdudgeon/simple-simulate-complex) with Mg2+-dependent metalloproteins. In this case, some parameters have been adjusted so that an Mg2+ dummy is recognized that is capable of performing octahedral coordination during the MD and maintaining an orientation that is closer to what is expected biologically (https://doi.org/10.1021/acs.jcim.5b00286).

The entire execution process is hosted on Google Colab [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1JWrIuQTpksdFexwtlSpfdo1y5ZQazJIL). and is automated so that all you have to do is enter the protein and the desired ligand. The preparation of the protein and the ligand, adjusting the charges and replacing the Mg2+ atom with the Mg2+-dummy takes place automatically. Simulation with only the protein or only the ligand in water is also being implemented.

<p align="center">
  <img src="/9mvn71.gif" alt="Descrição da Imagem" />
</p>
