# Finite Element Method

Originally this work was done as part of a group assignment in the practice lecture ``Numerical Simulation for Digital Engineering`` in the summer term 2024.  
Outlined below are the requirements of the original project, the planned additional work and the original group participants.  
Requirements were all fullfilled accordingly. Ultimately the CI-CD Pipeline was also set up but never finished to check the functionality of the Code. A second additional part of the assignment, which is not mentioned below, was to try and optimize the code to run as quickly as possible. For this there was unfortunately no time left before the deadline.

Because of these unfullfilled goals of the project and the desire to improve the functionality and accessibility of the code, the decision was made to continue the project.  
Idealy this tool can ultimately be used to accept various combinations of inputs and then calculate and show the numerical simulation as a picture which can be downloaded throught the artifacts of a pipeline.  

#### Features in work:
- Improved Input System 
- Neumann Boundary Conditions unequal to zero
- Creating picture out of the result-valules
- Creating Functional CI-CD Pipeline to check atleast simple some testcases
- Optimization of the Code

------
## Original Project

### Aim of the Project: 
- Implementation of the Finite-Element-Method using Python

### Requirements:
- Rectangular geometry (length & width can be defined as required)
- QUAD mesh generation
- First-order approach functions (classical node approach functions), numerical integration of any order for element matrices 
- Specification of Dirichlet and Neumann Boundary Conditions on the four edges of the domain
- Specification of values along an arbitrary line within the domain
- Anisotropic material (material tensor)
- Input checks and error messages

### Additional work: 
- Implementation of a CI/CD - Pipeline

### Group Participants:
- Pöhl Luis
- Tschurtschenthaler Max
- Unterthiner Alexander
- Unterthurner Benedikt
