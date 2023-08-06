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
    version='54',
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
    long_description='''"
"After 17 to 27 months of treatment, both haloperidol- and olanzapine-treated monkeys had an equivalent and highly significant 8% to 11% decrease in fresh brain weight and volume when compared with the sham group."

Geachte Minister-President,

Ik ben Bart Thate, een 49 jarige schizofrenie patient. 

Op 20 Oktober 2012 heb ik na correspondentie met de :ref:`Koningin <beuker>` een :ref:`klacht <greffe>` tegen de Nederland ingedient (Thate tegen Nederland 69389/12). 
De klacht betrof het falen van de :ref:`(F)ACT <fact>` methodiek, de methode die GGZ Nederland gebruikt om vorm te geven aan de wetten die gedwongen behandeling in Nederland mogelijk maken.
De :ref:`Uitspraak <uitspraak>` is niet-ontvankelijk.
Omdat de :ref:`Koningin <beuker>` gemeld heeft dat ze vanwege ministeriele verantwoordelijkheden geen tussenkomst kan bieden, wend ik mij tot u.

De zorg die de GGZ met de :ref:`(F)ACT <fact>` methodiek levert omvat niet het toedienen van medicatie maar het toedienen van gif.

Er is bewijs dat antipsychotica gif zijn:

1) haloperiodol (haldol) - https://echa.europa.eu/substance-information/-/substanceinfo/100.000.142
2) clozapine (leponex) - https://echa.europa.eu/substance-information/-/substanceinfo/100.024.831
3) olanzapine (zyprexa) - https://echa.europa.eu/substance-information/-/substanceinfo/100.125.320
4) aripriprazole (abilify) https://echa.europa.eu/substance-information/-/substanceinfo/100.112.532

Er is bewijs dat antipsychotica hersenweefselverlies veroorzaken:

* http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3476840/ 

Ik constateer dat de arts niet een geneesmiddel toedient maar een gif.
Dit maakt strafrechterlijke vervolging mogelijk, echter het is voor mij niet mogelijk gebleken om :ref:`aangifte <aangifte>` te doen van mishandeling als de psychiater zijn patient met gif mishandelt:

* De IGZ treft geen structurele :ref:`onzorgvuldigheid <igz>` in de afhandeling van klachten bij GGZ-NHN aan.
* De :ref:`Hoge Raad <hogeraad>` concludeert dat het geen verantwoordelijkheid heeft en verwijst naar het Openbaar Ministerie, dat niet reageert.
* Daarna heb ik het Europeese Hof voor de Rechten van de Mens aangeschreven om een :ref:`klacht <greffe>` tegen Nederland in te dienen. 
* Pas na een gang langs het EVRM reageert Het :ref:`Openbaar Ministerie <om>` wel en verwijst naar de IGZ, die de klacht melding al heeft afgesloten. 

Ik concludeer dat het in Nederland voor de GGZ patient niet mogelijk is om aangifte te doen voor een strafbaar feit als een arts met gif mishandelt.
Ik concludeer dat er daardoor voor de GGZ patient niet een daadwerkelijk remedie aanwezig is om een einde te kunnen maken aan mishandeling die een arts pleegt als hij gif toedient.

Daarom eis ik van u:

1) direct antipsychotica van de markt te halen.
2) de politie meteen bloed metingen van medicijnspiegels laten uitvoeren om mishandeling gepleegd door toediening van voor het leven of de gezondheid vast te stellen.
3) het OM instrueren dat waar men gif toedient waar men zegt medicijnen toe te dienen direct voor de strafrechter te halen.
4) rechtsbijstand voor GGZ patienten die zelf geen aangifte kunnen doen verplichten.
5) direct een Wet laten aannemen die elke toediening van anitpsychotica expliciet verbied, ook toedieningen niet strafbaar door het Wetboek van Strafrecht geboden strafuitsluitingsgronden.


Er vanuit gaande dat u mijn eisen zult inwilligen,



Bart Thate 


| email: bthate@dds.nl
| url: http://evrm2.readthedocs.io

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
