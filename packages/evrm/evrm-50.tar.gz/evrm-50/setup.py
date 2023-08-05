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
    version='50',
    url='https://bitbucket.org/thatebart/evrm2',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="De gif toedieningen zijn de foltering !!",
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["botlib"],
    scripts=["bin/evrm"],
    packages=['evrm', ],
    long_description='''
"After 17 to 27 months of treatment, both haloperidol- and olanzapine-treated monkeys had an equivalent and highly significant 8% to 11% decrease in fresh brain weight and volume when compared with the sham group."

Geachte Minister-President,

Het is voor mij niet mogelijk gebleken om :ref:`aangifte <aangifte>` te doen van mishandeling als de psychiater zijn patient met gif mishandelt:

1) De IGZ treft geen structurele :ref:`onzorgvuldigheid <igz>` in de afhandeling van klachten bij GGZ-NHN aan.
2) De :ref:`Hoge Raad <hogeraad>` concludeert dat het geen verantwoordelijkheid heeft en verwijst naar het Openbaar Ministerie, dat niet reageert.
3) Daarna heb ik het Europeese Hof voor de Rechten van de Mens aangeschreven om een :ref:`klacht <greffe>` tegen Nederland in te dienen. 
4) De :ref:`Koningin <beuker>` kan hier geen verder tussenkomst verlenen.
5) :ref:`Uitspraak <uitspraak>` is niet-ontvankelijk.
6) Pas na een gang langs het EVRM reageert Het :ref:`Openbaar Ministerie <om>` wel en verwijst naar de IGZ, die de klacht melding al heeft afgesloten. 

Ik constateer dat er voor de GGZ patient geen toegang tot de strafrechter is.
Ik constateer ook dat het hier om het plegen van strafbare feiten gaat.

| Er is bewijs dat antipsychotica gif zijn:

1) haloperiodol (haldol) - https://echa.europa.eu/substance-information/-/substanceinfo/100.000.142
2) clozapine (leponex) - https://echa.europa.eu/substance-information/-/substanceinfo/100.024.831
3) olanzapine (zyprexa) - https://echa.europa.eu/substance-information/-/substanceinfo/100.125.320
4) aripriprazole (abilify) https://echa.europa.eu/substance-information/-/substanceinfo/100.112.532

| Er is bewijs dat antipsychotica hersenweefsel verlies veroorzaken:

* http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3476840/ 

Een arts die met deze medcijnen mishandelt weet dat hij gif aan het toedienen is, de :ref:`(F)ACT <fact>` methode is ook een methode die het toedienen van gifstoffen op een verantwoorde manier zegt te doen. 
Men handelt in de GGZ vanuit het bewustzijn dat deze medicijnen gif zijn, tot aan het meten van bloedspiegels aan toe.
Vanuit zekerheidbewustzijn als opzet kan men, na een bloedspiegelmeting, de opzettelijke benadeling van de gezondheid bewijzen.

Omdat het hier mishandeling betreft EN de GGZ patient geen aangifte hiervan kan doen, eis ik van u dat u direct de toegang tot de strafrechter voor de GGZ patient realiseert.
Nalaten de GGZ patient toegang tot de strafrechter te verschaffen zou maken dat er aan mishandeling met gif geen einde word gezet.

Ik ga ervan uit dat u het met mij eens bent en mijn eis daarom ook in zult inwilligen.

Hoogachtend,

Bart Thate - :ref:`teksten <teksten>`

| botfather @ irc.freenode.net #dunkbots
| bthate@dds.nl


''',
   data_files=[("docs", ["docs/conf.py","docs/index.rst"]),
               (j('docs', 'jpg'), uploadlist(j("docs","jpg"))),
               (j('docs', 'txt'), uploadlist(j("docs", "txt"))),
               (j('docs', '_templates'), uploadlist(j("docs", "_templates")))
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
