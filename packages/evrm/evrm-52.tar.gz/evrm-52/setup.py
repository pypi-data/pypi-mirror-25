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
    version='52',
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
"After 17 to 27 months of treatment, both haloperidol- and olanzapine-treated monkeys had an equivalent and highly significant 8% to 11% decrease in fresh brain weight and volume when compared with the sham grou

Geachte Minister-President,

Op 20 Oktober 2012 heb ik na correspondentie met de :ref:`Koningin <beuker>` een :ref:`klacht <greffe>` tegen de Nederland ingedient (Thate tegen Nederland 69389/12). 
De klacht betrof het falen van de :ref:`(F)ACT <fact>` methodiek, de methode die GGZ Nederland gebruikt om vorm te geven aan de wetten die gedwongen behandeling in Nederland mogelijk maken.
De :ref:`Uitspraak <uitspraak>` is niet-ontvankelijk.
Omdat de :ref:`Koningin <beuker>` gemeld heeft dat ze vanwege ministeriele verantwoordelijkheden geen tussenkomst kan bieden, wend ik mij tot u.
U bent verantwoordelijk voor de zorg die de Staat der Nederlanden de GGZ patient levert, wel of niet onder dwang. U dient te zorgen dat deze zorg niet het plegen van strafbare feiten omvat.

Het is voor mij niet mogelijk gebleken om :ref:`aangifte <aangifte>` te doen van mishandeling als de psychiater zijn patient met gif mishandelt:

1) De IGZ treft geen structurele :ref:`onzorgvuldigheid <igz>` in de afhandeling van klachten bij GGZ-NHN aan.
2) De :ref:`Hoge Raad <hogeraad>` concludeert dat het geen verantwoordelijkheid heeft en verwijst naar het Openbaar Ministerie, dat niet reageert.
3) Daarna heb ik het Europeese Hof voor de Rechten van de Mens aangeschreven om een :ref:`klacht <greffe>` tegen Nederland in te dienen. 
4) De :ref:`Koningin <beuker>` kan hier geen verder tussenkomst verlenen.
5) :ref:`Uitspraak <uitspraak>` is niet-ontvankelijk.
6) Pas na een gang langs het EVRM reageert Het :ref:`Openbaar Ministerie <om>` wel en verwijst naar de IGZ, die de klacht melding al heeft afgesloten. 

Ik constateer dat er voor de GGZ patient geen toegang tot de strafrechter is.
Ik constateer ook dat het hier om het plegen van strafbare feiten gaat.

Er is bewijs dat antipsychotica gif zijn:

1) haloperiodol (haldol) - https://echa.europa.eu/substance-information/-/substanceinfo/100.000.142
2) clozapine (leponex) - https://echa.europa.eu/substance-information/-/substanceinfo/100.024.831
3) olanzapine (zyprexa) - https://echa.europa.eu/substance-information/-/substanceinfo/100.125.320
4) aripriprazole (abilify) https://echa.europa.eu/substance-information/-/substanceinfo/100.112.532

Er is ook bewijs gevonden dat antipsychotica hersenweefsel verlies veroorzaken:

* http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3476840/ 

Ik eis van u dat u vervolging van artsen die patienten in een toestand van
vergiftiging brengen ook te laten vervolgen voor mishandeling gepleegd door
toediening van voor het leven of de gezondheid schadelijke stoffen.

Omdat men geen behandelingen aan het doen is met medicatie die geen schade kunnen, maar mishandeling pleegt door gif toe te dienen.

Er vanuit gaande dat u het met mij eens bent en mijn eis zult inwilligen,


Bart Thate 

email: bthate@dds.nl
url: https://pypi.python.org/pypi/evrm


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
