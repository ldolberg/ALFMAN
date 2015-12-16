ALFAMAN
=======

Authors : Lautaro Dolberg , Jérôme François , Shihabur Rahman Chowdhury , Reaz Ahmed, Raouf Boutaba  and Thomas Engel
Date : 16/12/2015
All rights reserved
GPL version 2.0 to be found at: http://www.gnu.org/licenses/gpl-2.0.txt
2015 University of Luxembourg - Interdisciplinary Centre for Security Reliability and Trust (SnT)

## Description

ALFMAN is a framework for enabling application-level flow management in
SDN-enabled network 

The framework is composed of two components: the augmented controller (AC) and the system probe (SP)

The SP is instantiated at all hosts hosting users and applications to be referred to when defining policies. It keeps track of application-level information about traffic flows at these hosts.

This information is stored in the database of the AC. Then the
AC takes as input application-level policies composed of rules.
These rules are very similar to OpenFlow rules with additional
fields to match application-level information. The rule engine
of the AC translates these rules to OpenFlow and forwards it
to the OpenFlow controller and then to the switches.

The framework is implemented in Python

## Installation

copy the folder src/awareness_deamon to your workspace

## Usage