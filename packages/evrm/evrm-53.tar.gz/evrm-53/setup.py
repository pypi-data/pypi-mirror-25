#!/usr/bin/env python3
#
#

import os
import sys
import os.path

def j(*args):
    if not args: return
    todo = list(map(str, filter(None, args)))
    return os.path.join(*todo)

if sys.version_info.major < 3:
    print("you need to run evrm with python3")
    os._exit(1)

try:
    use_setuptools()
except:
    pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

target = "evrm"
upload = []

def uploadfiles(dir):
    upl = []
    if not os.path.isdir(dir):
        print("%s does not exist" % dir)
        os._exit(1)
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if not os.path.isdir(d):
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)
    return upl

def uploadlist(dir):
    upl = []

    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)

    return upl

setup(
    name='evrm',
    version='53',
    url='https://bitbucket.org/thatebart/evrm2',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Gif toedienende artsen de cel in !!",
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["botlib"],
    scripts=["bin/evrm"],
    packages=['evrm', ],
    long_description='''"After 17 to 27 months of treatment, both haloperidol- and olanzapine-treated monkeys had an equivalent and highly significant 8% to 11% decrease in fresh brain weight and volume when compared with the sham group."

Geachte Minister-President,

Op 20 Oktober 2012 heb ik na correspondentie met de Koningin een klacht tegen de Staat der Nederlanden ingediens (Thate tegen Nederland 69389/12). 
De klacht betrof het falen van de (F)ACT methodiek, de methode die GGZ Nederland gebruikt om vorm te geven aan de wetten die gedwongen behandeling in Nederland mogelijk maken.
De :uitspraak is niet-ontvankelijk.
Omdat de Koningin gemeld heeft dat ze vanwege ministeriele verantwoordelijkheden geen tussenkomst kan bieden, wend ik mij tot u.

U bent verantwoordelijk voor de zorg die de Staat der Nederlanden de GGZ patient levert, wel of niet onder dwang. U dient te zorgen dat deze zorg niet het plegen van strafbare feiten omvat.

Er is bewijs dat antipsychotica hersenweefselverlies veroorzaken:

* http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3476840/ 

Er is bewijs dat antipsychotica gif zijn:

1) haloperiodol (haldol) - https://echa.europa.eu/substance-information/-/substanceinfo/100.000.142
2) clozapine (leponex) - https://echa.europa.eu/substance-information/-/substanceinfo/100.024.831
3) olanzapine (zyprexa) - https://echa.europa.eu/substance-information/-/substanceinfo/100.125.320
4) aripriprazole (abilify) https://echa.europa.eu/substance-information/-/substanceinfo/100.112.532

Omdat u nu weet dat het hier gif betreft en niet een medicijn dat geen schade kan, eis ik van u het volgende:

1) direct antipsychotica van de markt te halen.
2) onmiddelijk artsen die antipsychotica toedienen laten vervolgen voor vergiftiging.
3) direct een Wet laten aannemen die elke toediening van anitpsychotica expliciet verbied, ook toedieningen niet strafbaar door het Wetboek van Strafrecht geboden strafuitsluitingsgronden.

Er vanuitgaande dat u het met mij eens en mijn eisen zult inwilligen.


Hoogachtend,



Bart Thate 


| email: bthate@dds.nl
| url: https://pypi.python.org/pypi/evrm


''',
   data_files=[("docs", ["docs/conf.py","docs/index.rst"]),
               (j('docs', 'jpg'), uploadlist(os.path.join("docs","jpg"))),
               (j('docs', 'txt'), uploadlist(os.path.join("docs", "txt"))),
               (j('docs', '_templates'), uploadlist(os.path.join("docs", "_templates")))
              ],
   package_data={'': ["*.crt"],
                 },
   classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
