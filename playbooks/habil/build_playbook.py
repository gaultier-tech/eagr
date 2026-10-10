#!/usr/bin/env python3
"""Génère le playbook Eagr V2 de Habil (R1, R2 / closing, Suivi).

Sources : Notion Habil « 03 · Du rendez-vous à la signature » et
« Objections, réponses et suites » (O-01 à O-14).
Usage : python3 build_playbook.py  ->  habil_playbook_v2.json
"""
import json
from pathlib import Path

CLIENT_ID = "ced0e378-3fc2-45bb-9db6-aaf52f1b3e27"


def fr(s):
    return {"fr": s}


def adv(title, content, example):
    return {"title": fr(title), "content": fr(content), "example": fr(example)}


def tech(name, l1, l2, l3, l4, advice, cond=None):
    t = {
        "nameI18n": fr(name),
        "level1I18n": fr(l1),
        "level2I18n": fr(l2),
        "level3I18n": fr(l3),
        "level4I18n": fr(l4),
        "adviceContent": advice,
        "subTechniques": [],
    }
    if cond:
        t["conditionDefinition"] = {"evaluateWhen": cond}
    return t


def skill(name, techniques, cond=None):
    s = {"nameI18n": fr(name), "techniques": techniques}
    for i, t in enumerate(techniques):
        t["sortOrder"] = i
    if cond:
        s["conditionDefinition"] = {"evaluateWhen": cond}
    return s


def fact(id_, type_, prompt, pivot=None):
    f = {"id": id_, "type": type_, "promptI18n": fr(prompt)}
    if pivot:
        f["pivotId"] = pivot
    return f


def direct(id_, fact_id=None):
    return {"id": id_, "rule": {"type": "direct", "factId": fact_id or id_}}


def det(signal):
    return {"is": "detected", "signal": signal}


def not_det(signal):
    return {"is": "not_detected", "signal": signal}


QUALIF = (
    "Si un sujet est évoqué sans détail suffisant pour trancher, répondre 'unasked'. "
    "Répondre 'denied' ou 'not_detected' uniquement si le transcript contient une preuve "
    "du contraire. Une information donnée spontanément par le prospect compte comme recueillie, "
    "même sans question du commercial."
)

# ---------------------------------------------------------------------------
# SEGMENT 1 · R1 DÉCOUVRIR ET DÉMONTRER
# ---------------------------------------------------------------------------

r1_ouverture = skill("Ouverture du rendez-vous", [
    tech(
        "Reprendre le motif et sa priorité",
        "Le commercial ouvre directement sur la présentation d'Habil sans mentionner la raison pour laquelle le rendez-vous a été pris.",
        "Le commercial évoque le motif du rendez-vous en termes génériques (« vous vouliez voir le logiciel ») sans reprendre l'irritant exprimé lors du premier appel ni vérifier qu'il est encore d'actualité.",
        "Le commercial reprend l'irritant précis noté lors du premier échange, dans les mots du prospect, et pose une question pour vérifier qu'il reste prioritaire.",
        "Le commercial reprend l'irritant précis noté lors du premier échange, pose une question pour vérifier qu'il reste prioritaire, et annonce le sujet par lequel il démarre en fonction de la réponse (« si c'est surtout la reprise après la visite qui vous pèse, on part de là »).",
        [
            adv("Repars des mots du premier appel",
                "Le rendez-vous a été pris sur un irritant précis, noté dans HubSpot par Jean-Charles ou Pierre. Relis la note avant et ouvre avec cet irritant, dans les mots du prospect : il reconnaît sa situation et tu évites de repartir de zéro.",
                "« Lors de notre premier échange, vous m'aviez dit que le plus pénible, c'était de reprendre les infos de la visite pour faire le devis. C'est toujours le sujet numéro un pour vous ? »"),
            adv("Vérifie que la priorité tient",
                "Entre la prise de rendez-vous et le rendez-vous, la situation a pu changer. Une question de vérification évite de démontrer pendant une heure un sujet devenu secondaire. Si la priorité a bougé, adapte le programme plutôt que de dérouler ce qui était prévu.",
                "Prospect : « Oui, enfin, là en ce moment c'est surtout les relances de devis qui m'embêtent. » Commercial : « D'accord, alors on commence par les relances et on regarde la reprise après la visite ensuite. »"),
        ],
    ),
    tech(
        "Cadrer le déroulé du rendez-vous",
        "Le commercial n'annonce aucun déroulé et commence la démonstration sans dire ce qui va être vu.",
        "Le commercial annonce un déroulé générique (« je vais vous montrer l'outil ») sans mentionner l'étape de découverte sur un dossier du prospect ni demander son accord.",
        "Le commercial annonce un déroulé en deux temps nommés, d'abord un dossier récent du prospect puis la démonstration ciblée, et demande l'accord du prospect sur ce déroulé.",
        "Le commercial annonce le déroulé (dossier récent du prospect, démonstration ciblée, point sur la suite), précise que la fin du rendez-vous servira à décider ensemble de la suite, y compris s'il n'y a pas d'intérêt, et demande l'accord du prospect.",
        [
            adv("Annonce le dossier avant la démo",
                "Le prospect s'attend à voir le logiciel. Dis-lui que tu commences par un de ses dossiers récents : c'est ce qui rendra la démonstration utile pour lui, et ça légitime les questions que tu vas poser.",
                "« Je vous propose qu'on parte d'abord d'un de vos dossiers récents, pour voir comment ça se passe chez vous, et ensuite je vous montre uniquement ce qui correspond. Ça vous va ? »"),
            adv("Donne-toi le droit de conclure",
                "Annoncer dès le début que la fin servira à décider de la suite, y compris de s'arrêter, rend la conclusion naturelle et évite le « je vais réfléchir » de politesse. Un prospect qui sait qu'il peut dire non parle plus franchement.",
                "« Et à la fin, on regarde ensemble s'il y a un intérêt à aller plus loin. S'il n'y en a pas, vous me le dites, ça me va très bien aussi. »"),
        ],
    ),
])

r1_decouverte = skill("Découverte sur un dossier réel", [
    tech(
        "Parcourir un dossier récent",
        "Le commercial ne demande aucun dossier ou exemple concret et reste sur des questions générales sur l'activité.",
        "Le commercial pose une question générale sur le fonctionnement (« comment vous fonctionnez ? ») sans l'ancrer sur un dossier précis du prospect.",
        "Le commercial demande au prospect de dérouler un dossier récent précis, de la demande du client jusqu'au devis, et relance sur au moins une étape de ce dossier.",
        "Le commercial demande de dérouler un dossier récent précis étape par étape, de la demande du client à la visite puis au devis, relance sur les étapes où l'information est recherchée ou ressaisie, et reformule le parcours du dossier en synthèse avant de passer à la suite.",
        [
            adv("Demande le dernier dossier traité",
                "Un dossier réel donne des faits, une question générale donne une opinion. Demande le dernier dossier traité, pas « un dossier type » : le prospect s'en souvient et tu entends les vraies étapes, avec leurs détours.",
                "« Prenons le dernier devis que vous avez fait. La demande est arrivée comment ? » Prospect : « Par téléphone, ma femme l'a notée sur le cahier. » « Et ensuite, la visite, elle s'est calée comment ? »"),
            adv("Suis la demande jusqu'au devis",
                "La valeur d'Habil se joue entre la demande du client, la visite et le devis. Suis le dossier sur tout ce chemin sans sauter d'étape : c'est souvent dans les passages entre deux étapes que l'information se perd ou se ressaisit.",
                "« Après la visite, vos notes, vous les retrouvez où au moment de faire le devis ? » Prospect : « Dans mon carnet, je retape tout le soir. »"),
        ],
    ),
    tech(
        "Cartographier outils et personnes",
        "Le commercial ne pose aucune question sur les outils utilisés ni sur les personnes qui interviennent dans le traitement des demandes.",
        "Le commercial demande quel logiciel est utilisé sans identifier qui intervient à quelle étape (secrétariat, technicien, dirigeant).",
        "Le commercial identifie par des questions les outils utilisés et la personne qui intervient sur au moins deux étapes du dossier (prise de demande, visite, devis).",
        "Le commercial identifie pour les trois étapes (prise de demande, visite, devis) l'outil utilisé et la personne qui intervient, et pose une question sur la façon dont l'information passe d'une étape à l'autre.",
        [
            adv("Associe une personne à une étape",
                "Savoir qu'ils utilisent un tableur ou un ERP ne suffit pas. Ce qui compte, c'est qui fait quoi : c'est ce qui te dira qui utilisera Habil et qui doit être convaincu.",
                "« Quand la demande arrive, c'est qui qui la prend ? » Prospect : « Le secrétariat. » « Et le devis, c'est vous ou le technicien qui a fait la visite ? »"),
            adv("Cherche les passages de relais",
                "Les ressaisies naissent quand l'information change de main ou d'outil. Une question sur le passage entre deux étapes fait apparaître ce que le prospect ne voit plus parce qu'il le fait depuis des années.",
                "« Ce que le technicien note pendant la visite, ça arrive comment jusqu'à la personne qui fait le devis ? »"),
        ],
    ),
    tech(
        "Préciser l'irritant et son impact",
        "Le commercial ne questionne pas l'irritant et passe à la démonstration sur la base du motif initial.",
        "Le commercial note l'irritant tel qu'il est formulé (« c'est la paperasse ») sans demander sur quelle tâche précise il porte ni ce qu'il entraîne.",
        "Le commercial pose une question qui ramène l'irritant à une tâche précise (recherche, ressaisie, relance) et une question sur sa conséquence pour l'entreprise.",
        "Le commercial ramène l'irritant à une tâche précise, demande sa conséquence (temps du dirigeant, délai de réponse au client, dossier oublié) et demande quelle priorité le prospect lui donne par rapport à ses autres sujets.",
        [
            adv("Transforme « la paperasse » en tâche",
                "« La paperasse » ou « l'administratif » ne se démontrent pas. Une tâche précise, si : rechercher une info, la retaper, relancer un client. Ramène l'irritant à ce niveau avant de montrer quoi que ce soit.",
                "Prospect : « C'est l'administratif qui me prend la tête. » Commercial : « Dans l'administratif, c'est quoi la tâche que vous aimeriez le plus ne plus faire ? »"),
            adv("Demande ce que ça coûte vraiment",
                "Un irritant sans conséquence reste un confort. Demande ce qu'il entraîne pour l'entreprise : des soirées, des devis envoyés tard, des clients qui partent ailleurs. C'est cette conséquence qui justifiera la décision, pas la fonctionnalité.",
                "« Et quand le devis part avec quelques jours de retard, qu'est-ce que ça change pour vous ? » Prospect : « Il y en a qui signent ailleurs entre-temps. »"),
        ],
    ),
    tech(
        "Chiffrer le temps ou le volume",
        "Le commercial ne pose aucune question chiffrée sur le volume de demandes ou le temps passé.",
        "Le commercial avance lui-même un chiffre ou un gain (« vous devez perdre des heures ») sans poser de question chiffrée au prospect.",
        "Le commercial pose au moins une question chiffrée sur le volume de dossiers ou le temps passé sur la tâche identifiée.",
        "Le commercial pose une question chiffrée sur le volume de dossiers et une sur le temps passé sur la tâche identifiée, et sépare dans sa reformulation la part de temps que l'outil peut réduire de celle qu'il ne touche pas (déplacement, visite elle-même).",
        [
            adv("Laisse le chiffre venir de lui",
                "Un chiffre avancé par le commercial est contesté, un chiffre donné par le prospect lui appartient. Pose la question et note la réponse telle quelle dans HubSpot, même si elle est approximative. S'il ne sait pas, note « non chiffré » : ça reste une information.",
                "« Des devis comme celui-là, vous en faites combien par semaine, à peu près ? » Prospect : « Une dizaine. » « Et pour chacun, le temps de remise au propre, c'est combien ? »"),
            adv("Ne vends pas un gain imaginaire",
                "Une visite de 45 minutes n'est pas du temps supprimable. Distingue ce qu'Habil peut réduire (recherche, ressaisie) de ce qu'il ne touche pas. Un chiffre honnête tient en closing, un chiffre gonflé se retourne contre toi.",
                "« Donc sur l'heure que vous me décrivez, la visite reste la visite. Ce qu'on peut regarder, ce sont les dix minutes où vous retapez vos notes. »"),
        ],
    ),
    tech(
        "Identifier ce qu'il veut conserver",
        "Le commercial ne demande pas ce que le prospect veut garder dans son fonctionnement actuel.",
        "Le commercial demande si le fonctionnement actuel convient par une question fermée (« ça vous va comme ça ? ») sans demander ce qui doit être conservé.",
        "Le commercial pose une question ouverte sur ce que le prospect tient à garder dans son fonctionnement actuel et reformule au moins un élément nommé.",
        "Le commercial pose une question ouverte sur ce que le prospect veut conserver, reformule les éléments nommés, et annonce comment la démonstration ou la proposition en tiendra compte.",
        [
            adv("Demande ce qui marche bien",
                "Un artisan bien organisé ne veut pas tout changer. Lui demander ce qu'il veut garder montre que tu ne viens pas tout casser, et te donne les limites à respecter dans la démonstration et la proposition.",
                "« Dans votre façon de faire actuelle, qu'est-ce que vous tenez absolument à garder ? » Prospect : « Le carnet en visite, je ne lâcherai pas. »"),
            adv("Montre que tu en tiens compte",
                "Reformuler ce qu'il veut garder, puis l'utiliser dans la suite, transforme une réticence en critère. Il voit que la solution s'adapte à lui et pas l'inverse.",
                "« Très bien, on garde le carnet en visite. Je vais vous montrer uniquement ce qui se passe après, quand vous rentrez au bureau. »"),
        ],
    ),
])

r1_demo = skill("Démonstration ciblée", [
    tech(
        "Démontrer une action liée au besoin",
        "Le commercial ne fait aucune démonstration, ou parcourt les menus du logiciel dans l'ordre sans citer le besoin du prospect.",
        "Le commercial démontre une action annoncée comme liée au besoin, mais sur un exemple fictif générique, sans reprendre le dossier ou la tâche décrits par le prospect.",
        "Le commercial annonce le lien avec l'irritant du prospect avant de démontrer et réalise la démonstration sur la tâche précise que le prospect a décrite (« vous m'avez parlé de la ressaisie après la visite, voilà ce que ça donne »).",
        "Le commercial démontre l'action sur le dossier ou le type de dossier décrit par le prospect, en reprenant ses mots et ses étapes, et limite la démonstration aux actions liées au besoin en proposant de garder le reste pour plus tard.",
        [
            adv("Démontre son dossier, pas le tien",
                "La démonstration la plus convaincante rejoue le dossier que le prospect vient de te décrire. Reprends ses étapes, ses mots, son type de chantier. Un exemple fictif lui demande un effort de transposition qu'il ne fera pas.",
                "« Vous m'avez parlé du dépannage de chaudière de la semaine dernière. Je reprends ce cas : la demande arrive, je la saisis là, et après la visite, voilà où se retrouvent vos notes pour le devis. »"),
            adv("Montre peu, montre juste",
                "Tout montrer noie le besoin. Limite-toi aux actions qui répondent à l'irritant identifié et propose de garder le reste pour plus tard. Une démonstration courte et ciblée laisse le temps de parler de la suite.",
                "« Il y a d'autres choses dans l'outil, mais je ne vais pas vous les montrer aujourd'hui, ça ne correspond pas à ce que vous m'avez décrit. On pourra y revenir si besoin. »"),
        ],
    ),
    tech(
        "Comparer les manipulations",
        "Le commercial ne compare pas la démonstration au fonctionnement actuel du prospect.",
        "Le commercial affirme un gain global (« vous allez gagner un temps fou ») sans nommer de manipulation supprimée.",
        "Le commercial nomme au moins une manipulation supprimée par rapport au fonctionnement actuel décrit par le prospect.",
        "Le commercial nomme les manipulations supprimées et les manipulations ajoutées par Habil (saisie initiale, prise en main), et fait le solde avec le prospect sur la tâche démontrée.",
        [
            adv("Nomme ce qui disparaît",
                "« Gagner du temps » ne veut rien dire pour un artisan. Nomme la manipulation qui disparaît, en la reliant à ce qu'il t'a décrit : retaper les notes, chercher l'adresse, rappeler pour une info oubliée.",
                "« Ce que vous faisiez le soir, retaper les notes de visite dans le devis, là vous ne le faites plus : c'est déjà dedans. »"),
            adv("Assume ce qui s'ajoute",
                "Un nouvel outil ajoute aussi des manipulations : saisir la demande, prendre l'outil en main. Les annoncer toi-même te rend crédible et évite que l'objection tombe plus tard. Fais ensuite le solde avec lui.",
                "« En échange, il faut saisir la demande dans l'outil quand elle arrive, au lieu du cahier. Sur un dossier comme celui-là, vous diriez que le compte est bon ou pas ? »"),
        ],
    ),
    tech(
        "Demander l'impact concret",
        "Le commercial enchaîne d'une action démontrée à la suivante sans poser de question au prospect sur ce qu'il vient de voir.",
        "Le commercial pose une question fermée de validation (« c'est bien, non ? », « ça vous plaît ? »).",
        "Le commercial pose une question ouverte sur ce que l'action démontrée change concrètement dans le quotidien du prospect (« Qu'est-ce que cela change concrètement pour vous ? »).",
        "Le commercial pose une question ouverte sur ce que l'action démontrée change concrètement, puis une question sur ce qui manque ou ne convient pas, et reformule les deux réponses.",
        [
            adv("Pose la question du changement",
                "« Ça vous plaît ? » appelle un oui de politesse. « Qu'est-ce que cela change concrètement pour vous ? » oblige le prospect à se projeter avec ses propres mots, et ce sont ces mots que tu reprendras au moment de la proposition.",
                "« Qu'est-ce que cela change concrètement pour vous ? » Prospect : « Bah je ne retape plus le soir, déjà. »"),
            adv("Cherche aussi ce qui manque",
                "Demander ce qui manque ou ne convient pas fait sortir les réserves pendant que tu peux encore y répondre. Une réserve découverte au closing coûte un rendez-vous de plus.",
                "« Et à l'inverse, qu'est-ce qui vous manque, ou qui ne collerait pas à votre façon de faire ? »"),
        ],
    ),
])

r1_objections = skill("Traitement des objections", [
    tech(
        "Accueillir l'objection",
        "Le commercial contredit l'objection dès qu'elle est exprimée (« non mais justement ») ou l'ignore et poursuit la démonstration.",
        "Le commercial accuse réception par une formule standard (« je comprends, mais ») immédiatement suivie d'un contre-argument.",
        "Le commercial accuse réception de l'objection en reprenant au moins un mot du prospect, sans contre-argument dans la même réplique.",
        "Le commercial accuse réception en reprenant les mots du prospect, légitime le point de vue (« c'est une vraie question quand on vient de changer de logiciel ») et annonce qu'il va poser une question avant de répondre.",
        [
            adv("Accuse réception, puis tais-toi",
                "Accueillir, c'est montrer que tu as entendu, rien de plus. Pas de « mais », pas d'argument dans la même phrase. Reprends un mot du prospect pour qu'il sache que tu l'as écouté.",
                "Prospect : « On vient juste de changer de logiciel. » Commercial : « Ah, vous venez de changer. D'accord. »"),
            adv("Légitime avant de répondre",
                "Dire que l'objection est légitime désamorce la confrontation. Le prospect n'a plus besoin de la défendre et peut t'expliquer ce qu'il y a derrière.",
                "« C'est normal, après une migration, on n'a pas envie d'en relancer une. Je peux vous poser une question avant de vous répondre ? »"),
        ],
    ),
    tech(
        "Creuser la vraie nature",
        "Le commercial répond à l'objection sans poser aucune question dessus.",
        "Le commercial pose une question fermée qui suppose la nature de l'objection (« c'est le prix qui vous bloque ? »).",
        "Le commercial pose une question ouverte sur ce qui motive l'objection avant d'y répondre.",
        "Le commercial pose une question ouverte sur ce qui motive l'objection, relance sur la réponse, et vérifie qu'il s'agit du seul frein (« à part ça, y a-t-il autre chose qui vous retient ? »).",
        [
            adv("Ouvre au lieu de deviner",
                "Derrière « on a déjà un ERP » il peut y avoir une migration récente, un manque non couvert ou un vrai refus. Une question ouverte te dit lequel. Une question fermée t'enferme dans ta propre hypothèse.",
                "« Qu'est-ce qui vous fait dire ça ? » Prospect : « L'ERP fait déjà les devis. » « Et entre l'appel du client et le devis, il fait quoi ? »"),
            adv("Vérifie qu'il n'y a rien d'autre",
                "Traiter un frein pour en découvrir un deuxième juste après use la confiance. Avant de répondre, vérifie que c'est le seul : tu sauras si ta réponse peut suffire.",
                "« D'accord. Et à part ça, il y a autre chose qui vous ferait hésiter ? »"),
        ],
    ),
    tech(
        "Reformuler l'objection",
        "Le commercial ne reformule pas l'objection avant d'y répondre.",
        "Le commercial répète l'objection mot pour mot (« vous avez déjà un ERP ») sans y intégrer ce que la question de creusage a révélé.",
        "Le commercial reformule l'objection en intégrant l'élément révélé par le creusage et demande au prospect si c'est bien ça.",
        "Le commercial reformule l'objection en distinguant ce qui relève du principe et ce qui relève du moment ou des conditions, et demande au prospect si c'est bien ça avant de répondre.",
        [
            adv("Reformule avec ce que tu as appris",
                "Une reformulation utile n'est pas un écho. Elle intègre ce que le creusage a fait apparaître, et c'est à cette version-là que tu vas répondre, pas à la phrase de départ.",
                "« Si je comprends bien, l'ERP vous convient pour les devis, et ce qui reste à la main, c'est la prise de demande et le suivi des visites. C'est ça ? »"),
            adv("Sépare le principe du moment",
                "« Pas maintenant » et « pas pour nous » n'appellent pas la même réponse. Dire lequel des deux tu as entendu évite de pousser un prospect qui a juste besoin d'un autre moment.",
                "« Donc ce n'est pas l'idée qui vous gêne, c'est de lancer ça en pleine saison de chantiers. J'ai bien compris ? »"),
        ],
    ),
    tech(
        "Répondre sur l'outil déjà en place",
        "Le commercial dénigre l'outil en place ou affirme qu'Habil le remplace avantageusement sans rien demander sur ce qu'il couvre.",
        "Le commercial demande quel outil est utilisé puis enchaîne sur les points forts d'Habil sans identifier ce que l'outil couvre déjà.",
        "Le commercial demande ce que l'outil en place couvre déjà entre la demande du client, la visite et le devis, et positionne Habil uniquement sur une étape désignée comme non couverte, ou acte qu'il n'y a pas de manque si aucune n'est désignée.",
        "Le commercial demande ce que l'outil en place couvre étape par étape, demande s'il reste une recherche ou une ressaisie en dehors de cet outil, puis soit positionne Habil sur ce manque en posant la question de la compatibilité avec l'outil en place, soit acte l'absence de manque et propose d'en rester là.",
        [
            adv("Demande ce que l'outil couvre déjà",
                "Face à Extrabat ou à un ERP, ne compare pas les logiciels. Demande ce qu'il couvre entre la demande du client, la visite et le devis. Habil n'a de place que là où il reste un manque reconnu.",
                "« Très bien. Qu'est-ce qu'il couvre déjà entre la demande du client, la visite et le devis ? » Prospect : « Les devis et la facturation. » « Et la prise de demande et la visite, elles passent où ? »"),
            adv("Accepte qu'il n'y ait pas de manque",
                "Si l'outil en place couvre tout, dis-le et arrête-toi. Une démo de curiosité n'est pas une opportunité, et un prospect qu'on n'a pas forcé reste joignable plus tard. Pas d'urgence artificielle après une migration récente.",
                "« Si votre outil couvre déjà tout ça, je ne vais pas vous proposer un changement sans intérêt. Il ne reste pas une recherche ou une ressaisie en dehors ? » Prospect : « Non, franchement. » « Alors on en reste là, merci de votre franchise. »"),
        ],
        cond=det("objection_outil_en_place"),
    ),
    tech(
        "Traiter le gain jugé faible",
        "Le commercial conteste le chiffre du prospect (« non, ça vous prend forcément plus ») ou répète le gain de temps global d'Habil.",
        "Le commercial accepte le chiffre du prospect puis reparle du gain de temps global d'Habil sans isoler de tâche précise.",
        "Le commercial accepte le chiffre du prospect et pose une question pour isoler un type de dossier ou une tâche où l'information est réellement recherchée ou ressaisie.",
        "Le commercial accepte le chiffre, sépare explicitement le temps non compressible (visite, attente du choix du client) du temps de reprise d'information, et cadre l'échange sur cette seule tâche ou acte l'absence de gain si aucune n'existe.",
        [
            adv("Donne-lui raison sur le chiffre",
                "« Un devis me prend cinq minutes » est souvent vrai pour un dépannage. Contester le chiffre te met en face de lui. Accepte-le, puis cherche s'il existe un type de dossier plus lourd.",
                "« D'accord. Sur ces devis-là, il y a sans doute peu à gagner. Ce sont surtout des dépannages, ou vous avez aussi des projets avec étude ? »"),
            adv("Isole la seule tâche qui compte",
                "Le délai dépend souvent du choix du client, et la visite reste la visite. Sépare ce temps-là de la tâche que l'outil peut réduire, et cadre l'échange sur elle. S'il n'y en a pas, ne vends pas un gain imaginaire.",
                "« L'attente vient du choix du client, pas forcément du chiffrage. Et de votre côté, quel temps de travail reste nécessaire une fois ces choix faits ? »"),
        ],
        cond=det("objection_gain_faible"),
    ),
    tech(
        "Conclure et tester l'adhésion",
        "Le commercial reprend la démonstration après sa réponse sans revenir sur l'objection.",
        "Le commercial termine sa réponse par une question fermée générique (« ça vous va ? ») sans nommer l'objection traitée.",
        "Le commercial demande au prospect si sa réponse lève le point soulevé, en nommant l'objection.",
        "Le commercial nomme l'objection, demande si sa réponse la lève, et annonce la suite concrète selon la réponse (reprise de la démonstration sur ce point, vérification produit à faire, ou arrêt).",
        [
            adv("Nomme l'objection en refermant",
                "Un « je comprends » du prospect ne veut pas dire que l'objection est levée. Repose-la nommément et écoute la réponse : c'est la seule façon de savoir si tu peux avancer.",
                "« Sur la question de l'ERP que vous avez déjà, est-ce que ce que je vous ai dit répond à votre question ? »"),
            adv("Enchaîne sur une suite concrète",
                "Une objection levée doit déboucher sur un pas en avant, une objection non levée sur une décision claire. Annonce ce qui se passe ensuite plutôt que de reprendre là où tu t'étais arrêté.",
                "Prospect : « Oui, si ça se branche avec l'ERP, ça m'intéresse. » Commercial : « Alors je vérifie ce point précis avec notre équipe produit et je vous montre ensuite le suivi des visites. »"),
        ],
    ),
], cond=det("objection_r1"))

r1_qualif = skill("Qualification de la décision", [
    tech(
        "Définir périmètre et utilisateurs",
        "Le commercial ne pose aucune question sur les personnes qui utiliseraient Habil ni sur le périmètre concerné.",
        "Le commercial demande combien de personnes utiliseraient l'outil sans préciser lesquelles ni pour quelles étapes.",
        "Le commercial identifie par nom ou par rôle les utilisateurs et les étapes du dossier qu'ils traiteraient dans Habil.",
        "Le commercial identifie par rôle les utilisateurs et les étapes concernées, et distingue ce qui entrerait dans Habil dès le démarrage de ce qui reste hors périmètre.",
        [
            adv("Parle de rôles, pas d'un nombre",
                "« Combien d'utilisateurs ? » donne un prix, pas une adoption. Demande qui ferait quoi dans l'outil : c'est ce qui conditionne la mise en route et la réussite après la signature.",
                "« Concrètement, qui l'utiliserait au quotidien ? » Prospect : « Le secrétariat, surtout. » « Et les techniciens, pour la visite, ils s'en serviraient aussi ? »"),
            adv("Délimite ce qui démarre",
                "Tout mettre dans l'outil dès le premier jour fait peur. Proposer un périmètre de départ, et dire ce qui reste en dehors, rend la décision plus simple et la proposition plus juste.",
                "« Je vous propose qu'on démarre sur la prise de demande et les visites. La facturation, vous la gardez dans votre outil actuel pour l'instant. »"),
        ],
    ),
    tech(
        "Identifier décideur et conditions",
        "Le commercial ne demande pas qui décide ni comment la décision sera prise.",
        "Le commercial pose une question fermée sur la décision (« c'est vous qui décidez ? ») et s'arrête à la réponse.",
        "Le commercial demande qui participe à la décision et au moins une condition à réunir pour décider (budget, avis d'un associé, essai, période).",
        "Le commercial identifie le décideur et les personnes consultées, les conditions à réunir pour décider, et propose d'inviter la personne utile au prochain échange si elle n'est pas présente.",
        [
            adv("Demande comment la décision se prend",
                "Dans une entreprise du bâtiment, le dirigeant décide souvent avec son associé, son conjoint ou son comptable. Demande qui participe, sans présumer : une personne oubliée au premier rendez-vous bloque le closing.",
                "« Pour une décision comme celle-là, vous en parlez avec quelqu'un d'autre avant de vous lancer ? »"),
            adv("Fais nommer les conditions",
                "Les conditions de décision sont ta feuille de route vers la signature : un budget, une période, l'accord d'un associé. Demande-les maintenant plutôt que de les découvrir en fin de cycle.",
                "« Qu'est-ce qu'il faudrait réunir pour que vous puissiez dire oui ? » Prospect : « Que mon associé voie aussi l'outil. » « Alors on l'invite au prochain échange ? »"),
        ],
    ),
    tech(
        "Situer la date de démarrage",
        "Le commercial n'aborde pas le moment où le prospect pourrait démarrer.",
        "Le commercial demande « c'est pour quand ? » et accepte la réponse sans relancer sur une période ni sur ce qui la conditionne.",
        "Le commercial demande une période de démarrage envisagée et ce qui la conditionne (saison de chantiers, fin d'un contrat, disponibilité de l'équipe).",
        "Le commercial demande une période de démarrage et ce qui la conditionne, et vérifie qu'elle est réaliste compte tenu des étapes de mise en route (prise en main, reprise des données).",
        [
            adv("Cherche ce qui fixe le moment",
                "La période de démarrage dépend rarement de l'envie : elle dépend de la saison, d'un contrat en cours, de l'équipe. Demande ce qui la conditionne pour savoir si la date est solide.",
                "« Vous vous verriez démarrer quand ? » Prospect : « Pas avant la fin des gros chantiers. » « Ça tombe vers quand, à peu près ? »"),
            adv("Confronte la date à la mise en route",
                "Une date irréaliste promet un démarrage raté. Rappelle ce que demande la mise en route et vérifie que la période choisie le permet.",
                "« Pour démarrer en octobre, il faudrait qu'on fasse la prise en main avec le secrétariat fin septembre. C'est jouable de votre côté ? »"),
        ],
    ),
])

r1_suite = skill("Choix de la suite", [
    tech(
        "Choisir la sortie adaptée",
        "Le commercial termine le rendez-vous sans proposer de suite, ou propose un second rendez-vous par défaut sans raison exprimée.",
        "Le commercial propose une suite (« je vous envoie une proposition », « on refait un point ») sans la justifier par ce qui a été établi pendant le rendez-vous.",
        "Le commercial propose une seule suite et la justifie par un élément établi pendant le rendez-vous : proposition si l'usage et les conditions sont clairs, second échange pour une réserve nommée, arrêt si aucune valeur n'est apparue.",
        "Le commercial résume en une phrase ce qui a été établi (besoin, usage, conditions), en déduit une seule suite parmi proposition, second échange sur une réserve nommée ou arrêt, et demande l'accord du prospect sur ce choix.",
        [
            adv("Un seul rendez-vous peut suffire",
                "Si l'usage est compris et les conditions qualifiées, propose directement la proposition. Un second échange ne se justifie que pour une réserve précise. Imposer deux rendez-vous quand un seul suffit allonge le cycle pour rien.",
                "« Vous m'avez dit que le besoin, c'est la reprise après la visite, que ce serait le secrétariat et vous deux, et que vous décidez seul. Je vous envoie la proposition, ça vous va ? »"),
            adv("Sache proposer l'arrêt",
                "Si aucune valeur n'est apparue, dis-le et arrête. Un R1 qui finit proprement sur un non vaut mieux qu'une relance qui ne mènera nulle part, et il protège la qualité de ton pipeline.",
                "« Honnêtement, avec votre organisation actuelle, je ne vois pas ce qu'on vous apporterait. Je préfère vous le dire. Si ça change, vous savez où me trouver. »"),
        ],
    ),
    tech(
        "Verrouiller la prochaine étape",
        "Le commercial clôt le rendez-vous sans fixer de prochaine étape.",
        "Le commercial convient d'une suite sans date précise (« on se rappelle la semaine prochaine »).",
        "Le commercial fixe une date et une heure pour la prochaine étape et nomme son objet.",
        "Le commercial fixe date, heure et objet de la prochaine étape, nomme les participants utiles et ce que chacun doit préparer d'ici là, et confirme l'envoi de l'invitation.",
        [
            adv("Date, heure et objet",
                "« Plus tard » ne qualifie pas une opportunité. Une suite n'existe que si elle a une date, une heure et un objet. Propose deux créneaux pour faciliter le choix.",
                "« Je vous propose qu'on se reparle de la proposition mardi à 18 h ou jeudi à 8 h. Qu'est-ce qui vous arrange ? »"),
            adv("Prépare le prochain échange",
                "Le prochain échange se gagne maintenant : qui doit être là, qui prépare quoi. Confirme l'invitation avec le lien pour éviter le rendez-vous non tenu.",
                "« Jeudi 8 h, avec votre associé. De mon côté je vous envoie la proposition avant, vous de votre côté vous regardez le point sur la facturation. Je vous envoie l'invitation tout de suite. »"),
        ],
        cond=not_det("arret_motive"),
    ),
])

r1 = {
    "nameI18n": fr("R1 découvrir et démontrer"),
    "classificationTriggers": {
        "required": [
            "The call is a scheduled sales meeting between a Habil team member and a construction trade business (plumbing, heating, electrical or similar) that is evaluating the Habil software",
            "The Habil team member explores how the prospect currently handles customer requests, site visits or quotes, or demonstrates the software",
        ],
        "disqualifying": [
            "The call is a first cold call with no appointment previously agreed",
            "A demonstration of Habil was already given to this prospect in a previous meeting and the call focuses on the commercial offer, pricing, contract terms or signature",
            "The external participant is an existing Habil customer using the software",
            "The call is internal, a recruitment interview, or unrelated to selling Habil",
        ],
        "weak_positive": [
            "The prospect mentions an existing tool such as Extrabat, an ERP, a spreadsheet or a paper notebook",
            "The prospect raises an objection about time, current organisation or an existing tool",
        ],
        "strong_positive": [
            "The Habil team member refers to the reason the meeting was booked during a previous phone call",
            "The prospect walks through a recent customer file from request to visit to quote",
            "The Habil team member demonstrates a feature of the software live",
        ],
    },
    "factsDefinition": [
        fact("motif_repris", "behavioral",
             "Le commercial a-t-il rappelé l'irritant ou le motif précis pour lequel le rendez-vous a été pris ? 'detected' si un irritant ou un motif concret est cité, 'not_detected' sinon. (Fact analytique.)"),
        fact("dossier_reel_parcouru", "behavioral",
             "Un dossier récent et réel du prospect a-t-il été parcouru étape par étape (demande, visite, devis) ? 'detected' si au moins deux étapes d'un même dossier réel sont décrites, 'not_detected' sinon. (Fact analytique.)"),
        fact("outils_actuels_nommes", "behavioral",
             "Les outils actuels du prospect (logiciel, ERP, Extrabat, tableur, papier) ont-ils été nommés pendant l'appel ? 'detected' si au moins un outil est nommé, 'not_detected' sinon. (Fact analytique.)"),
        fact("temps_ou_volume_chiffre", "behavioral",
             "Un chiffre sur le volume de dossiers ou le temps passé sur une tâche figure-t-il dans le transcript, donné par le prospect ? 'detected' si oui, 'not_detected' sinon. Un chiffre avancé seul par le commercial ne compte pas. (Fact analytique.)"),
        fact("demo_liee_besoin", "behavioral",
             "Le commercial a-t-il démontré une action du logiciel en la reliant explicitement à un besoin ou un irritant exprimé par le prospect ? 'detected' si oui, 'not_detected' si aucune démonstration ou une démonstration générale sans lien. (Fact analytique.)"),
        fact("decideur_identifie", "qualification",
             "La personne qui décide de l'achat d'Habil côté prospect a-t-elle été identifiée ? 'confirmed' si le décideur est nommé ou désigné par son rôle, 'denied' si le sujet est abordé sans réponse claire, 'unasked' si non abordé. (Fact analytique.)"),
        fact("objection_r1", "behavioral",
             "Le prospect a-t-il exprimé une objection ou une résistance active pendant l'appel (manque de temps, déjà équipé, déjà bien organisé, gain jugé faible, prix, changement récent de logiciel) ? 'detected' uniquement en cas de résistance exprimée, pas pour une simple question d'information. Sinon 'not_detected'."),
        fact("objection_outil_en_place", "behavioral",
             "Le prospect a-t-il opposé l'outil qu'il utilise déjà (Extrabat, ERP, autre logiciel, changement récent de logiciel) comme raison de ne pas avoir besoin d'Habil ? 'detected' si oui, 'not_detected' si l'outil est seulement mentionné sans résistance."),
        fact("objection_gain_faible", "behavioral",
             "Le prospect a-t-il affirmé que le gain possible est faible parce que la tâche lui prend peu de temps ou dépend d'autres facteurs (« un devis me prend cinq minutes », « le délai dépend du client », « la visite prend l'essentiel du temps ») ? 'detected' si oui, 'not_detected' sinon."),
        fact("proposition_decidee", "behavioral",
             "Pendant l'appel, le commercial et le prospect ont-ils convenu de l'envoi ou de la présentation d'une proposition commerciale (offre, devis) comme suite ? 'detected' si oui, 'not_detected' sinon."),
        fact("second_echange_reserve_datee", "behavioral",
             "Pendant l'appel, un second échange a-t-il été fixé avec une date précise pour traiter une réserve nommée (question produit, avis d'un associé, point de compatibilité) ? 'detected' si une date et l'objet de la réserve sont présents, 'not_detected' sinon."),
        fact("arret_motive", "behavioral",
             "Le commercial ou le prospect a-t-il conclu explicitement qu'il n'y a pas d'intérêt à aller plus loin (pas de besoin, besoin non couvert, outil en place suffisant) ? 'detected' si l'arrêt est acté pendant l'appel, 'not_detected' sinon. (Fact analytique, sert aussi de condition.)"),
    ],
    "signalsDefinition": [
        direct("objection_r1"),
        direct("objection_outil_en_place"),
        direct("objection_gain_faible"),
        direct("arret_motive"),
        direct("proposition_decidee"),
        direct("second_echange_reserve_datee"),
    ],
    "qualificationInstruction": QUALIF,
    "outcomeDefinition": {
        "version": "1",
        "successWhen": {"any": [
            {"signal": "proposition_decidee", "is": "detected"},
            {"signal": "second_echange_reserve_datee", "is": "detected"},
        ]},
    },
    "skills": [r1_ouverture, r1_decouverte, r1_demo, r1_objections, r1_qualif, r1_suite],
}

# ---------------------------------------------------------------------------
# SEGMENT 2 · R2 / CLOSING
# ---------------------------------------------------------------------------

r2_reprise = skill("Reprise de l'engagement", [
    tech(
        "Reprendre l'engagement antérieur",
        "Le commercial démarre par une nouvelle démonstration ou par l'offre sans évoquer ce qui avait été convenu au précédent échange.",
        "Le commercial mentionne le précédent échange en termes génériques (« suite à notre dernier rendez-vous ») sans rappeler ce qui avait été convenu.",
        "Le commercial rappelle explicitement ce qui avait été convenu au précédent échange (point à vérifier, personne à inviter, élément à préparer) et demande où en est le prospect sur ce point.",
        "Le commercial rappelle ce qui avait été convenu, demande où en est le prospect sur ce point, et annonce le programme de l'échange en fonction de la réponse, sans refaire une démonstration déjà vue.",
        [
            adv("Ouvre sur ce qui avait été convenu",
                "Le second échange existe pour une raison précise. Rappelle-la d'entrée : la question à vérifier, l'associé à inviter, le point à préparer. Ça remet le prospect dans sa propre décision au lieu de tout recommencer.",
                "« La dernière fois, on s'était dit que je vérifiais la compatibilité avec votre outil de facturation, et que vous en parliez à votre associé. Vous avez pu en parler ? »"),
            adv("Ne refais pas la démonstration",
                "Refaire la démonstration renvoie l'échange en phase de découverte. Pars de l'engagement pris et ne remontre que ce qui répond au point resté ouvert.",
                "« Je ne vais pas vous remontrer tout l'outil. Je vous montre juste ce qui répondait à la question de votre associé, et ensuite on regarde la proposition. »"),
        ],
    ),
    tech(
        "Rappeler besoin et preuve montrée",
        "Le commercial ne rappelle ni le besoin retenu ni ce qui a été démontré.",
        "Le commercial rappelle les fonctionnalités vues (« vous avez vu le planning, les devis ») sans les relier au besoin du prospect.",
        "Le commercial rappelle le besoin retenu dans les mots du prospect et l'action démontrée qui y répond.",
        "Le commercial rappelle le besoin retenu dans les mots du prospect et l'action démontrée qui y répond, puis demande si ce besoin reste le bon point de départ pour décider.",
        [
            adv("Rappelle le besoin avant l'outil",
                "Ce qui fait signer, c'est le besoin, pas la liste des fonctionnalités vues. Rappelle-le dans ses mots, puis l'action qui y répond : le prospect retrouve sa raison d'acheter.",
                "« Vous m'aviez dit que le plus lourd, c'était de retaper les notes de visite le soir. Et on avait vu que, dans l'outil, elles arrivent directement dans le devis. »"),
            adv("Vérifie que le besoin tient",
                "Entre deux échanges, le besoin a pu évoluer. Une question de vérification évite de construire le closing sur une base qui a bougé.",
                "« C'est toujours ce point-là qui compte le plus pour vous, ou il y a eu du nouveau depuis ? »"),
        ],
    ),
])

r2_reserve = skill("Faire émerger la réserve finale", [
    tech(
        "Demander le point restant",
        "Le commercial ne pose aucune question sur ce qui reste à valider pour décider.",
        "Le commercial pose une question fermée générique (« vous avez des questions ? », « c'est bon pour vous ? ») sans la relier à la décision.",
        "Le commercial pose une question ouverte reliée à la décision (« Quel point reste à valider pour que vous puissiez décider ? »).",
        "Le commercial pose une question ouverte reliée à la décision, puis reformule le point nommé avec les mots du prospect avant d'y répondre.",
        [
            adv("Relie la question à la décision",
                "« Vous avez des questions ? » appelle un « non, ça va » qui ne t'apprend rien. La question qui fait avancer est reliée à la décision : elle fait sortir le vrai point bloquant.",
                "« Quel point reste à valider pour que vous puissiez décider ? » Prospect : « Le prix, et savoir combien de temps on est engagé. »"),
            adv("Reformule le point avant d'y répondre",
                "Reformuler le point restant avec ses mots te garantit que tu réponds à la bonne question, et montre au prospect que tu l'as entendu.",
                "« Donc ce qui vous retient, c'est la durée d'engagement, plus que le montant lui-même. C'est ça ? »"),
        ],
    ),
    tech(
        "Isoler la dernière réserve",
        "Le commercial traite le premier point soulevé sans vérifier s'il en existe d'autres.",
        "Le commercial demande s'il y a autre chose seulement après avoir répondu au premier point (« et sinon, c'est tout ? »).",
        "Le commercial demande, avant de traiter la réserve, si elle est la seule à lever pour décider.",
        "Le commercial demande, avant de traiter la réserve, si elle est la seule, et pose la condition explicitement (« si on règle ce point, est-ce que vous êtes en mesure de décider ? »).",
        [
            adv("Vérifie avant de répondre",
                "Répondre à une réserve pour en découvrir une autre ensuite fait tourner l'échange en rond. Demande d'abord si c'est la seule : tu sais alors ce qu'il faut régler pour conclure.",
                "« D'accord, la durée d'engagement. Avant que je vous réponde, est-ce qu'il y a autre chose qui vous ferait hésiter ? »"),
            adv("Pose la condition clairement",
                "« Si on règle ce point, vous êtes en mesure de décider ? » transforme la réserve en dernière marche. Si la réponse est non, tu viens de découvrir le vrai frein.",
                "« Si on trouve une solution sur la durée d'engagement, est-ce que vous êtes en mesure de décider aujourd'hui ? »"),
        ],
    ),
])

r2_offre = skill("Présentation de l'offre", [
    tech(
        "Annoncer l'offre et son total",
        "Le commercial n'annonce pas de prix total, ou renvoie le chiffrage à un envoi ultérieur sans rien présenter.",
        "Le commercial annonce un prix unitaire ou mensuel (« c'est tant par utilisateur ») sans total ni lien avec le périmètre défini.",
        "Le commercial annonce le périmètre retenu, le nombre d'utilisateurs, les options et le total chiffré.",
        "Le commercial annonce le périmètre, les utilisateurs, les options et le total, relie le périmètre au besoin retenu, et termine son annonce par une question au prospect sans ajouter d'argument après le chiffre.",
        [
            adv("Annonce un total, pas un tarif",
                "Un prix par utilisateur oblige le prospect à faire le calcul, et il le fera au pire moment. Annonce le périmètre, les utilisateurs, les options et le total : c'est ce qu'il paiera.",
                "« Sur ce qu'on a défini, la prise de demande et les visites, pour vous, le secrétariat et vos deux techniciens, avec l'option planning, ça fait un total de [montant] par mois. »"),
            adv("Après le chiffre, une question",
                "Enchaîner les arguments après le prix donne l'impression de s'excuser. Annonce le chiffre, puis pose une question et écoute la réponse.",
                "« Voilà le total. Comment vous le situez par rapport à ce que vous aviez en tête ? »"),
        ],
    ),
    tech(
        "Expliciter engagement et conditions",
        "Le commercial n'aborde ni la durée d'engagement, ni l'accompagnement, ni les frais éventuels.",
        "Le commercial évoque les conditions en termes généraux (« il y a un petit engagement ») sans préciser la durée, les frais ni l'accompagnement.",
        "Le commercial précise la durée d'engagement, l'accompagnement prévu et les frais éventuels.",
        "Le commercial précise la durée d'engagement, l'accompagnement et les frais éventuels, indique que ces conditions figureront par écrit sur le devis, et demande si l'une d'elles pose question.",
        [
            adv("Dis tout avant la signature",
                "Une condition découverte après la signature casse la confiance et l'activation. Annonce la durée d'engagement, l'accompagnement et les frais éventuels avant que le prospect ne signe.",
                "« L'engagement est de [durée]. La mise en route comprend une prise en main avec votre secrétariat. Il n'y a pas d'autres frais que ceux du devis. »"),
            adv("Renvoie aux conditions écrites",
                "Un accord oral ne vaut pas signature. Dis que tout ce que tu viens d'annoncer figurera par écrit sur le devis : le prospect sait exactement ce qu'il signe.",
                "« Tout ce que je vous dis là sera écrit noir sur blanc dans le devis. Est-ce qu'il y a un de ces points qui vous pose question ? »"),
        ],
    ),
])

r2_objections = skill("Objections de closing", [
    tech(
        "Accueillir l'objection",
        "Le commercial contredit l'objection dès qu'elle est exprimée (« non, ce n'est pas cher ») ou l'ignore et poursuit vers la signature.",
        "Le commercial accuse réception par une formule standard (« je comprends, mais ») immédiatement suivie d'un contre-argument.",
        "Le commercial accuse réception de l'objection en reprenant au moins un mot du prospect, sans contre-argument dans la même réplique.",
        "Le commercial accuse réception en reprenant les mots du prospect, légitime le point de vue (« c'est normal de regarder l'engagement de près ») et annonce qu'il va poser une question avant de répondre.",
        [
            adv("Reçois l'objection sans la combattre",
                "Au closing, la tentation est de défendre l'offre tout de suite. Commence par montrer que tu as entendu, avec un mot du prospect, et rien d'autre dans la même phrase.",
                "Prospect : « C'est plus cher que ce que je pensais. » Commercial : « Plus cher que prévu. D'accord. »"),
            adv("Rends l'objection légitime",
                "Dire qu'une objection est normale au moment de signer enlève la tension. Le prospect peut alors t'expliquer ce qu'il y a vraiment derrière.",
                "« C'est normal de regarder ça de près avant de s'engager. Je peux vous poser une question ? »"),
        ],
    ),
    tech(
        "Creuser la vraie nature",
        "Le commercial répond à l'objection sans poser aucune question dessus.",
        "Le commercial pose une question fermée qui suppose la nature de l'objection (« c'est le budget qui coince ? »).",
        "Le commercial pose une question ouverte sur ce qui motive l'objection avant d'y répondre.",
        "Le commercial pose une question ouverte sur ce qui motive l'objection, relance sur la réponse, et distingue s'il s'agit du montant, du moment ou de l'engagement.",
        [
            adv("Cherche ce qu'il y a derrière",
                "« C'est cher » peut vouloir dire trop par rapport au budget, trop par rapport à l'usage, ou pas le bon moment. Une question ouverte te dit lequel, et c'est à celui-là que tu répondras.",
                "« Quand vous dites plus cher que prévu, vous le comparez à quoi ? »"),
            adv("Distingue montant, moment et engagement",
                "Les trois appellent des réponses différentes : ajuster le périmètre, décaler la date, expliquer les conditions. Relance jusqu'à savoir lequel est en jeu.",
                "Prospect : « C'est surtout de m'engager maintenant, avec la saison. » Commercial : « Donc ce n'est pas tant le montant que le moment de démarrer ? »"),
        ],
    ),
    tech(
        "Reformuler l'objection",
        "Le commercial ne reformule pas l'objection avant d'y répondre.",
        "Le commercial répète l'objection mot pour mot (« c'est trop cher ») sans y intégrer ce que la question de creusage a révélé.",
        "Le commercial reformule l'objection en intégrant l'élément révélé par le creusage et demande au prospect si c'est bien ça.",
        "Le commercial reformule l'objection en distinguant ce qui relève du principe et ce qui relève du moment ou des conditions, et demande au prospect si c'est bien ça avant de répondre.",
        [
            adv("Reformule la version creusée",
                "Ta reformulation doit contenir ce que tu as appris en creusant. C'est la preuve que tu as compris, et c'est la question précise à laquelle tu vas répondre.",
                "« Si je résume, le montant vous va, mais vous ne voulez pas payer en pleine saison alors que l'équipe n'aura pas le temps de s'y mettre. C'est ça ? »"),
            adv("Fais valider avant de répondre",
                "Une reformulation sans validation reste une hypothèse. Attends son accord avant de répondre : si tu t'es trompé, il te corrige maintenant plutôt qu'après ta réponse.",
                "« J'ai bien compris, ou il y a autre chose ? » Prospect : « Non, c'est exactement ça. »"),
        ],
    ),
    tech(
        "Traiter l'objection prix",
        "Le commercial propose une remise dès l'objection, ou maintient le prix sans justification (« c'est le tarif »).",
        "Le commercial justifie le prix par les fonctionnalités d'Habil sans le rapporter au besoin ou au temps évoqués par le prospect.",
        "Le commercial rapporte le prix à un élément précis du besoin retenu ou à une manipulation supprimée identifiée pendant le cycle.",
        "Le commercial rapporte le prix au besoin retenu, détaille ce que comprend le total, et propose un ajustement de périmètre ou d'options avant toute remise.",
        [
            adv("Rapporte le prix à son besoin",
                "Le prix se défend contre le besoin du prospect, pas contre la liste des fonctionnalités. Reprends ce qu'il t'a dit en découverte : la tâche du soir, les devis qui partent tard.",
                "« Ce montant, c'est pour ne plus retaper vos notes de visite le soir. Vous m'aviez parlé d'une dizaine de devis par semaine. »"),
            adv("Ajuste le périmètre, pas le prix",
                "Une remise immédiate dit que le prix n'était pas le vrai. Si le budget coince, propose plutôt de démarrer sur un périmètre plus restreint ou sans une option.",
                "« Si on démarre sans l'option planning, sur la prise de demande et les visites seulement, on passe à [montant]. Ça vous parlerait davantage ? »"),
        ],
        cond=det("objection_prix"),
    ),
    tech(
        "Traiter l'objection engagement",
        "Le commercial minimise l'engagement (« ce n'est rien ») ou introduit une urgence artificielle (« l'offre s'arrête ce soir »).",
        "Le commercial rappelle la durée d'engagement sans répondre au motif de la crainte exprimée.",
        "Le commercial nomme le motif de la crainte (durée, reprise des données, prise en main) et y répond par un élément précis de l'accompagnement ou des conditions écrites.",
        "Le commercial nomme le motif de la crainte, y répond par un élément précis de l'accompagnement ou des conditions écrites, et propose une modalité de démarrage qui le réduit (périmètre de départ restreint, date de démarrage adaptée).",
        [
            adv("Réponds au motif de la crainte",
                "La peur de l'engagement porte rarement sur la durée elle-même : c'est la peur que l'équipe ne s'y mette pas, ou que la reprise soit lourde. Nomme ce motif et réponds-y avec l'accompagnement prévu.",
                "« Ce qui vous inquiète, c'est que l'équipe ne l'utilise pas et que vous payiez pour rien. La mise en route prévoit justement une prise en main avec chacun d'eux. »"),
            adv("Pas d'urgence artificielle",
                "Une fausse échéance détruit la confiance au moment où tu en as le plus besoin. Propose plutôt un démarrage qui réduit le risque : un périmètre plus petit, une date qui évite la saison.",
                "« On peut démarrer après vos gros chantiers, sur la prise de demande seulement. Vous verrez si l'équipe s'y met avant d'étendre. »"),
        ],
        cond=det("objection_engagement"),
    ),
    tech(
        "Conclure et tester l'adhésion",
        "Le commercial passe à la signature après sa réponse sans revenir sur l'objection.",
        "Le commercial termine sa réponse par une question fermée générique (« ça vous va ? ») sans nommer l'objection traitée.",
        "Le commercial demande au prospect si sa réponse lève le point soulevé, en nommant l'objection.",
        "Le commercial nomme l'objection, demande si sa réponse la lève, et selon la réponse revient à la demande de signature ou convient d'une action précise datée sur le point restant.",
        [
            adv("Teste la levée nommément",
                "Un « je comprends » ne dit pas que l'objection est levée. Demande-le en nommant l'objection, et écoute la réponse avant de passer à la signature.",
                "« Sur la question de l'engagement, est-ce que ce que je vous propose vous convient ? »"),
            adv("Reviens à la décision",
                "Une objection levée doit te ramener à la décision. Si elle ne l'est pas, convient d'une action datée précise plutôt que d'un « je réfléchis ».",
                "Prospect : « Oui, comme ça, ça me va. » Commercial : « Alors je vous envoie le devis avec ce démarrage, vous pouvez le signer aujourd'hui ? »"),
        ],
    ),
], cond=det("objection_r2"))

r2_engagement = skill("Engagement et signature", [
    tech(
        "Nommer signataire et responsable",
        "Le commercial ne demande pas qui signera ni qui sera responsable de l'usage d'Habil.",
        "Le commercial demande qui signe sans identifier la personne responsable de l'usage au quotidien.",
        "Le commercial identifie le signataire et la personne responsable de l'usage au quotidien.",
        "Le commercial identifie le signataire et le responsable de l'usage, demande si le signataire a les éléments pour signer, et convient de qui prend en charge la mise en route côté prospect.",
        [
            adv("Distingue qui signe et qui utilise",
                "Le dirigeant signe, mais c'est souvent le secrétariat qui fera vivre l'outil. Identifie les deux : sans responsable de l'usage, un compte créé ne devient pas un compte activé.",
                "« C'est vous qui signerez le devis ? » Prospect : « Oui, c'est moi. » « Et au quotidien, qui sera la personne de référence sur l'outil ? »"),
            adv("Prépare la mise en route",
                "Convenir dès maintenant de qui pilote la mise en route côté prospect évite le flottement après la signature, là où beaucoup de démarrages s'enlisent.",
                "« Pour la prise en main, je vois ça avec votre secrétaire directement, ou vous préférez être là ? »"),
        ],
    ),
    tech(
        "Fixer une date de démarrage",
        "Le commercial n'aborde pas la date de démarrage.",
        "Le commercial évoque un démarrage sans date (« dès que possible », « à la rentrée »).",
        "Le commercial convient d'une date de démarrage précise.",
        "Le commercial convient d'une date de démarrage précise, la confronte aux contraintes du prospect (saison de chantiers, disponibilité de l'équipe), et distingue la création du compte du début de l'utilisation.",
        [
            adv("Une vraie date, pas « à la rentrée »",
                "Une date de démarrage précise rend l'achat concret et sert de repère pour la mise en route. « Dès que possible » se transforme en jamais.",
                "« On fixe le démarrage au lundi 5 octobre ? »"),
            adv("Compte créé n'est pas outil utilisé",
                "Créer le compte ne vaut pas activation. Parle de la date où l'équipe commence réellement à s'en servir, et vérifie qu'elle tient avec la saison et les disponibilités.",
                "« Le compte peut être ouvert dès la signature. Mais pour que vos techniciens s'en servent vraiment, mieux vaut viser après le chantier de la mi-octobre. On part sur le 19 ? »"),
        ],
    ),
    tech(
        "Demander la signature du devis",
        "Le commercial termine l'échange sans demander la signature ni convenir d'une action datée.",
        "Le commercial pose une question d'intention (« alors, ça vous tente ? ») ou se contente d'un accord oral sans parler de la signature du devis.",
        "Le commercial demande explicitement la signature du devis.",
        "Le commercial demande explicitement la signature du devis, précise les modalités concrètes (envoi du devis pendant l'échange, moment de la signature), et convient d'une action précise datée avec la preuve attendue si la signature n'a pas lieu pendant l'échange.",
        [
            adv("Demande la signature, clairement",
                "« Ça vous tente ? » ne demande rien. Un accord oral ne vaut pas signature. Demande explicitement la signature du devis : c'est la seule sortie qui fait avancer le dossier.",
                "« Est-ce que vous êtes d'accord pour qu'on y aille ? Je vous envoie le devis maintenant et vous pouvez le signer pendant qu'on est ensemble. »"),
            adv("Sinon, une action datée et précise",
                "Si la signature ne se fait pas pendant l'échange, n'accepte pas « je vous redis ». Convenez d'une action précise, datée, avec ce que le prospect doit avoir vérifié d'ici là.",
                "« D'accord, vous voulez le montrer à votre comptable. On se rappelle jeudi à 18 h, une fois qu'il a vu le devis, pour la signature ? »"),
        ],
    ),
])

r2 = {
    "nameI18n": fr("R2 et closing"),
    "classificationTriggers": {
        "required": [
            "The call is a sales meeting between a Habil team member and a construction trade business that already had at least one previous meeting where Habil was presented or demonstrated",
            "The commercial offer, its price, scope, commitment terms, start date or signature are discussed during the call",
        ],
        "disqualifying": [
            "The call is the first meeting where the prospect's current process is discovered and the software is demonstrated for the first time",
            "The decision to buy was already made before the call, the prospect expresses no reservation, objection or hesitation, and no amount is discussed, defended or renegotiated: the call only executes administrative steps",
            "The external participant is an existing Habil customer using the software outside of a new purchase",
            "The call is internal, a recruitment interview, or unrelated to selling Habil",
        ],
        "weak_positive": [
            "The prospect raises an objection about price, commitment duration, timing or data migration",
            "A partner, associate or accountant of the prospect joins the call",
        ],
        "strong_positive": [
            "The Habil team member recalls what was agreed at the end of the previous meeting",
            "The Habil team member presents a total price, the number of users, options or the commitment duration",
            "Signature of the quote or a start date is explicitly discussed",
        ],
    },
    "factsDefinition": [
        fact("engagement_anterieur_repris", "behavioral",
             "Le commercial a-t-il rappelé explicitement ce qui avait été convenu au précédent échange (point à vérifier, personne à inviter, élément à préparer) ? 'detected' si oui, 'not_detected' sinon. (Fact analytique.)"),
        fact("reserve_finale_nommee", "behavioral",
             "Un point précis restant à valider pour décider a-t-il été nommé pendant l'appel ? 'detected' si un point précis est formulé, 'not_detected' sinon. (Fact analytique.)"),
        fact("total_annonce", "behavioral",
             "Un prix total chiffré de l'offre a-t-il été annoncé pendant l'appel ? 'detected' si un total est donné, 'not_detected' si seul un prix unitaire ou aucun prix n'est donné. (Fact analytique.)"),
        fact("conditions_annoncees", "behavioral",
             "La durée d'engagement, l'accompagnement ou les frais ont-ils été précisés pendant l'appel ? 'detected' si au moins la durée d'engagement est précisée, 'not_detected' sinon. (Fact analytique.)"),
        fact("signataire_identifie", "qualification",
             "La personne qui signera le devis côté prospect a-t-elle été identifiée ? 'confirmed' si oui, 'denied' si le sujet est abordé sans réponse claire, 'unasked' si non abordé. (Fact analytique.)"),
        fact("date_demarrage_fixee", "behavioral",
             "Une date de démarrage précise (jour, ou semaine identifiée) a-t-elle été convenue ? 'detected' si oui, 'not_detected' si le démarrage reste sans date (« dès que possible », « à la rentrée »). (Fact analytique.)"),
        fact("objection_r2", "behavioral",
             "Le prospect a-t-il exprimé une objection ou une résistance active pendant l'appel (prix, engagement, timing, reprise des données, besoin de consulter un tiers) ? 'detected' uniquement en cas de résistance exprimée, pas pour une simple question d'information. Sinon 'not_detected'."),
        fact("objection_prix", "behavioral",
             "Le prospect a-t-il exprimé une résistance active sur le prix (« c'est cher », « plus que prévu », « pas dans le budget ») ? 'detected' si oui, 'not_detected' pour une simple demande d'information tarifaire."),
        fact("objection_engagement", "behavioral",
             "Le prospect a-t-il exprimé une résistance sur la durée d'engagement, la reprise des données ou la crainte que l'équipe n'utilise pas l'outil ? 'detected' si oui, 'not_detected' sinon."),
        fact("signature_engagee", "behavioral",
             "Pendant l'appel, le devis a-t-il été signé, ou le prospect a-t-il donné son accord explicite pour signer avec une date de signature précise ? 'detected' si oui. Un accord oral sans date de signature, ou une création de compte seule, ne comptent pas : 'not_detected'."),
    ],
    "signalsDefinition": [
        direct("objection_r2"),
        direct("objection_prix"),
        direct("objection_engagement"),
        direct("signature_engagee"),
    ],
    "qualificationInstruction": QUALIF,
    "outcomeDefinition": {
        "version": "1",
        "successWhen": {"all": [
            {"signal": "signature_engagee", "is": "detected"},
        ]},
    },
    "skills": [r2_reprise, r2_reserve, r2_offre, r2_objections, r2_engagement],
}

# ---------------------------------------------------------------------------
# SEGMENT 3 · SUIVI (très léger)
# ---------------------------------------------------------------------------

suivi_relance = skill("Relance ciblée", [
    tech(
        "Rappeler l'objet de la relance",
        "Le commercial n'indique pas l'objet de son appel ou le présente comme une simple prise de nouvelles.",
        "Le commercial cite l'objet de la relance (« c'est pour le devis ») sans rappeler le point resté ouvert lors du dernier échange.",
        "Le commercial rappelle l'objet de la relance et le point précis resté ouvert lors du dernier échange.",
        "Le commercial rappelle l'objet de la relance, le point resté ouvert, et l'engagement pris de part et d'autre lors du dernier échange (date, document, personne à consulter).",
        [
            adv("Rappelle le point resté ouvert",
                "« Je voulais savoir où vous en étiez » laisse le prospect chercher de quoi tu parles. Rappelle le point précis resté ouvert : la relance devient la suite logique du dernier échange.",
                "« Je vous appelle pour le devis envoyé mardi. Vous deviez le montrer à votre associé. »"),
            adv("Rappelle l'engagement des deux côtés",
                "Rappeler ce que chacun devait faire remet la relance sur un accord commun, pas sur une insistance commerciale.",
                "« De mon côté, j'ai vérifié la compatibilité avec votre outil de facturation, c'est bon. Et de votre côté, votre associé a pu regarder ? »"),
        ],
    ),
    tech(
        "Demander l'état de la décision",
        "Le commercial ne pose aucune question sur l'avancement de la décision.",
        "Le commercial pose une question fermée (« vous avez pu regarder ? ») et s'arrête à la réponse.",
        "Le commercial pose une question ouverte sur l'avancement de la décision et sur ce qui a été fait concernant le point resté ouvert.",
        "Le commercial pose une question ouverte sur l'avancement de la décision, puis demande ce qui reste à valider pour décider et reformule la réponse.",
        [
            adv("Demande où en est la décision",
                "« Vous avez pu regarder ? » appelle un oui ou un non. Une question ouverte te dit où en est vraiment la décision et ce qui s'est passé depuis.",
                "« Où vous en êtes dans votre réflexion depuis notre échange ? »"),
            adv("Cherche ce qui reste à valider",
                "Une relance utile fait apparaître le dernier point bloquant. Demande-le directement, puis reformule pour être sûr de traiter le bon.",
                "« Qu'est-ce qui reste à valider pour que vous puissiez décider ? » Prospect : « Mon associé trouve que c'est le mauvais moment. » « Donc c'est le moment de démarrer qui pose question, pas l'outil ? »"),
        ],
    ),
])

suivi_suite = skill("Engagement sur la suite", [
    tech(
        "Lever le point bloquant",
        "Le commercial ignore le point bloquant exprimé et redemande une décision.",
        "Le commercial répond au point bloquant par un argument général sur Habil sans poser de question sur ce point.",
        "Le commercial pose une question sur le point bloquant puis y répond par un élément précis (conditions écrites, accompagnement, vérification produit, date de démarrage).",
        "Le commercial pose une question sur le point bloquant, le reformule, y répond par un élément précis, et demande si sa réponse lève ce point.",
        [
            adv("Questionne avant de répondre",
                "Le point bloquant d'une relance est souvent différent de l'objection du rendez-vous. Pose une question avant de répondre, sinon tu traites l'ancien sujet.",
                "Prospect : « On hésite encore. » Commercial : « Qu'est-ce qui vous fait hésiter, aujourd'hui ? »"),
            adv("Réponds avec un élément précis",
                "Une relance n'est pas le moment de refaire l'argumentaire. Réponds au point par un élément précis : une condition écrite, une date de démarrage, une vérification. Sollicite l'équipe produit seulement si une question produit précise conditionne la vente.",
                "« Si c'est la saison qui vous bloque, on peut dater le démarrage après vos gros chantiers. Ça règle la question pour vous ? »"),
        ],
        cond=det("point_bloquant_exprime"),
    ),
    tech(
        "Fixer une action datée",
        "Le commercial termine l'appel sans suite convenue.",
        "Le commercial convient d'une suite sans date (« je vous rappelle plus tard », « tenez-moi au courant »).",
        "Le commercial convient d'une action précise avec une date (signature, rappel, échange avec le décideur) et nomme son objet.",
        "Le commercial convient d'une action précise datée, nomme qui fait quoi d'ici là et ce qui sera vérifié à cette date, ou acte une clôture motivée si le prospect renonce.",
        [
            adv("« Plus tard » n'est pas une suite",
                "Une relance qui finit sur « tenez-moi au courant » remet le dossier dans le flou. Convenez d'une action précise et datée, notée dans HubSpot.",
                "« On se rappelle vendredi à 17 h, une fois que vous avez vu votre associé. Si c'est bon pour lui, on signe à ce moment-là. »"),
            adv("Sache clore proprement",
                "Si le prospect renonce, acte-le et note le motif. Un dossier clos proprement vaut mieux qu'une relance qui revient tous les quinze jours sans rien changer.",
                "« Je comprends, ce n'est pas le moment. Je note que vous ne donnez pas suite pour l'instant. Merci de m'avoir répondu franchement. »"),
        ],
    ),
])

suivi = {
    "nameI18n": fr("Suivi après proposition"),
    "classificationTriggers": {
        "required": [
            "The call is a short follow-up between a Habil team member and a construction trade business that already received or discussed a Habil proposal or quote in a previous exchange",
            "The call is about the status of the prospect's decision, without a full presentation of the offer or a demonstration of the software",
        ],
        "disqualifying": [
            "The Habil software is demonstrated during the call",
            "The offer, its price, options and commitment terms are presented in detail during the call",
            "The decision to buy was already made before the call, the prospect expresses no reservation, objection or hesitation, and no amount is discussed: the call only executes administrative steps",
            "The call is a first cold call with no previous exchange about a proposal",
        ],
        "weak_positive": [
            "The prospect says they have not yet had time to look at the proposal",
        ],
        "strong_positive": [
            "The Habil team member refers to a quote or proposal sent earlier",
            "The Habil team member asks where the prospect stands on the decision",
        ],
    },
    "factsDefinition": [
        fact("point_bloquant_exprime", "behavioral",
             "Le prospect a-t-il exprimé un point qui l'empêche de décider (prix, moment, avis d'un tiers, question produit) ? 'detected' si oui, 'not_detected' sinon. Une démarche administrative non encore faite, dont personne ne conteste le principe, n'est pas un point bloquant."),
        fact("action_datee_convenue", "behavioral",
             "Une action précise avec une date (jour, ou jour et heure) a-t-elle été convenue pour la suite ? 'detected' si oui, 'not_detected' si la suite reste sans date (« je vous rappelle », « tenez-moi au courant »)."),
        fact("signature_engagee_suivi", "behavioral",
             "Pendant l'appel, le devis a-t-il été signé, ou le prospect a-t-il donné son accord explicite pour signer avec une date de signature précise ? 'detected' si oui, 'not_detected' sinon. Un accord oral sans date ne compte pas."),
        fact("cloture_motivee", "behavioral",
             "Le prospect a-t-il renoncé explicitement, avec un motif acté pendant l'appel ? 'detected' si oui, 'not_detected' sinon. (Fact analytique.)"),
    ],
    "signalsDefinition": [
        direct("point_bloquant_exprime"),
        direct("action_datee_convenue"),
        direct("signature_engagee_suivi"),
    ],
    "qualificationInstruction": QUALIF,
    "outcomeDefinition": {
        "version": "1",
        "successWhen": {"any": [
            {"signal": "signature_engagee_suivi", "is": "detected"},
            {"signal": "action_datee_convenue", "is": "detected"},
        ]},
    },
    "skills": [suivi_relance, suivi_suite],
}

segments = [r1, r2, suivi]
for i, seg in enumerate(segments):
    seg["sortOrder"] = i
    for j, sk in enumerate(seg["skills"]):
        sk["sortOrder"] = j

ordered = []
for seg in segments:
    ordered.append({
        "nameI18n": seg["nameI18n"],
        "sortOrder": seg["sortOrder"],
        "classificationTriggers": seg["classificationTriggers"],
        "factsDefinition": seg["factsDefinition"],
        "signalsDefinition": seg["signalsDefinition"],
        "qualificationInstruction": seg["qualificationInstruction"],
        "outcomeDefinition": seg["outcomeDefinition"],
        "skills": seg["skills"],
    })

playbook = {
    "$schema": "playbook-v1",
    "clientId": CLIENT_ID,
    "clientName": "Habil",
    "segments": ordered,
}

out = Path(__file__).with_name("habil_playbook_v2.json")
out.write_text(json.dumps(playbook, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Écrit : {out}")
