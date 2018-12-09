# Modeling and Simulation of Social Systems Fall 2018 – Research Plan

> * Group Name:  PlaneBoarding
> * Group participants names: Nils Blach, Anton Schäfer 
> * Project Title: Airplane Boarding
> * Programming language: Python

## General Introduction
(States your motivation clearly: why is it important / interesting to solve this problem?)
(Add real-world examples, if any)
(Put the problem into a historical context, from what does it originate? Are there already some proposed solutions?)

## The Model

The model is agent-based an fcouses on passengers' behavious in the aisle. In each discrete time step of 0.1 s, all actors in the aisle can act. The actors behaviour can be described with a finite state machine.


## Fundamental Questions

How does our model compare to the one from Van Landeghem and Beuselinck?
How do the Steffen method and other boarding methods compare to each other, when applied for different planes?
How does luggage load influence boarding time?


## Expected Results

We expect our model to yield similar results as the one given by Van Landeghem and Beuselinck. The Steffen method is supposed to be the most effective boarding method, so we expect it to perform best. We expect that the boarding time drastically increases with increasing luggage load.


## References 

(Add the bibliographic references you intend to use)
(Explain possible extension to the above models)
(Code / Projects Reports of the previous year)


## Research Methods

We use an agent-based model.


## Other

We do not use any datasets. The data

# Reproducibility

Before reproducing our work, make sure you have pyhton3, numpy, and matplotlib installed. 
To run the light test, just run the python script light_test.py. It will simulate boarding of an Airbus A320-200 with 100 % load and 180 passengers, using the random seat assignment and the Steffen method. It will print the boarding times to the console. To run the full test, first run the python script full_test.py to generate the data.


