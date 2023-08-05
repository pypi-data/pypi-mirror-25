#! /usr/bin/env python3
#
# (c) Sven Sager, License: LGPLv3
#
# -*- coding: utf-8 -*-
"""Setupscript fuer python3-revpimodio."""
from distutils.core import setup

setup(
    author="Sven Sager",
    author_email="akira@narux.de",
    url="https://revpimodio.org",
    maintainer="Sven Sager",
    maintainer_email="akira@revpimodio.org",

    license="LGPLv3",
    name="revpimodio",
    version="1.0.2",

    py_modules=["revpimodio"],

    description="Python3 Programmierung für Kunbus RevolutionPi",
    long_description=""
    "Das Modul stellt alle Devices und IOs aus der piCtory Konfiguration \n"
    "in Python3 zur Verfügung. Es ermöglicht den direkten Zugriff auf die \n"
    "Werte über deren vergebenen Namen. Lese- und Schreibaktionen mit dem \n"
    "Prozessabbild werden von dem Modul selbst verwaltet, ohne dass sich \n"
    "der Programmierer um Offsets und Adressen kümmern muss. Für die \n"
    "Gatewaymodule wie ModbusTCP oder Profinet sind eigene 'Inputs' und \n"
    "'Outputs' über einen bestimmten Adressbereich definierbar. Auf \n"
    "diese IOs kann mit Python3 über den Namen direkt auf die Werte \n"
    "zugegriffen werden.",

    classifiers=[
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
