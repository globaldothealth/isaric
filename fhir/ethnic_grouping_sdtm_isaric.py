ethnic_sdtm_isaric = [
    (
        "Arab",
        [
            r"arab(?:ique|ic|e)?",
            r"alg[e,é]ri(?:an|en|enne)",
            r"comor[o,e]s",
            "egyptian",
            r"iraqi?",
            r"leban(?:ese|on)",
            r"palestin(?:a|e|ian)",
            r"jordan(?:ia|ian)?",
            r"maurit(?:ian|us)",
            r"maro[c,cc,kk][o,a]?n?",
            r"morr?occ?(?:o|an)",
            r"middle\s?east(ern)?",
            r"saudi\s?arabian",
            r"sudan(ese)?",
            r"syrian?",
            r"tunisian?",
            r"y[e,a]mani?",
        ],
    ),
    (
        "Black",
        [
            "black",
            r"african?",
            r"afro(-)?american",
            r"afro(-)?caribe[e,a]n",
            r"cape\s?verd(?:e|ean|ian)",
            r"chan?d",
            "creole",
            r"east\s?african",
            "ethiopian",
            r"eritrean?",
            "gambian",
            "guinean",
            "ivoirien",  # cote d'ivoire
            "kami",  # tanzania
            "kaapverdian",  # cape verde
            "liberia",
            "madagascar",
            "malagache",  # madagascar
            "mauritius",
            "negro",
            r"nigerian?",
            "noir",
            "pari",  # sudan
            r"senegal(?:ise|ese)?",
            r"sierra leonn?e",
            r"somalian?",
        ],
    ),
    (
        "Central_Asian",
        [
            "kazakhstan",
            r"kyrgyz?(stan)?",
        ],
    ),
    (
        "East_Asian",
        [
            r"east[\s,_]?asian?"
            r"amarel[a,o]",  # "yellow", term in brazil for ethnic east asian
            r"chin(?:a|ese)",
            r"japan(ese)?",
            "taiwanese",
            "korean",
            r"tibet(ian)?",
        ],
    ),
    (
        "South_Asian",
        [
            r"south[\s,_]?asian?",
            r"afghan(istan)?",
            r"banga?la?deshi?",
            r"indian?",
            r"nepa(?:l|ll)?(?:i|ese)?",
            "maldivian",
            r"pakistani?",
            r"sri lankan?",
            "agrawal",
            "bish?w[o,a]karma",  # nepali
            "chauhan",
            "chaurasia",
            "chepang",  # indian caste
            "dalit",
            "damai",  # nepali caste
            "dangi",
            "danuwar",
            "devi",
            "gurung",  # nepalese
            "sinha",
            "jain",  # west india
            "kathariya",  # nepal
            "kumal",  # nepal
            "kunwar",  # nepalese/indian
            "lama",  # nepal
            "lamgade",  # nepal
            "lepcha",  # india
            "magar",  # nepal
            "majhi",  # nepal
            "malik",  # pakistani
            "oriisa",  # india
            "parashar",
            "pariyar",
            "rana",  # nepal, subgroup of tharu
            "saru",
            "sunar",
            "thami",
        ],
    ),
    (
        "South_East_Asian",
        [
            r"sou?t?h[\s,_]?eas[t,e][\s,_]?asian?",
            r"indon?es[i,e]an?",
            r"malay(sian)?",
            r"cambodian?",
            r"brunei(an)?",
            r"thai(land)?",
            r"phill?ip[p,h]?in[e,o]s?",
            r"fill?ipin[o,es]",
            r"vietnam(ese)?",
            r"mya[n,m]mar",
            r"rohin?g?n?yan?",
            r"bur(na)?m(?:a|ese)?",
            "bajau",
            "bidayuh",
            "bugis",
            r"cambodian?",
            "dusun",  # borneo
            "iban",  # malaysia
            "kadazan",  # malaysia
            "kedayan",  # brunei
            "kemboja",
            "melanau",  # malaysia
            "murut",  # borneo
            r"singapore(an)?",
            "siamese",  # thai
            "laos",
            "sarawak",
            "suluk",
        ],
    ),
    (
        "West_Asian",
        [
            r"west(ern)?[\s,_]?asian?",
            r"armenian?",
            r"tur(?:c|key|que)",
            r"turkis[h,k]",
            r"tyrkia",
            r"iran(?ese|ian)?",
            r"azerbaijani?",
            r"kurde?",
        ],
    ),
    (
        "Latin_American",
        [
            r"latino?[\s,_]?america(?:n|os)?",
            "latine",
            "antillean",
            "barbados",
            "caribbean" r"cura[ç,c]ao(an)?",
            "chile",
            r"columbian?",
            "cuba",
            "dominican",
            "ecuador",
            r"el\s?salvador",
            "guyana",
            r"ha[i,ï]ti(?:an|enne)?",
            "martiniquaise",
            r"pard[a,o]",  # Brazilian for 'mixed origin' historically
            r"peru(vian)?",
            r"suri?nam(?:e|es|ese|esian)?",
            "trinidad",
            r"west\s?indies",
        ],
    ),
    (
        "White",
        [
            "white",
            "caucasi[a,e]n",
            "eur(?:opean|asian)",
            r"alban(?:ise|ia|ian)",
            r"american?",
            "amerique",
            r"austrian?",
            r"bosnian?",
            r"bulgar(?ian|ia|y)",
            "british",
            "canadian",
            "cigano",  # portuguese romani
            r"croat(ian)?",
            r"czech\s?republic",
            "dutch",
            r"finn(ish)?",
            r"french",
            r"german(ic)?",
            r"georgian?",
            "greek",
            r"hungar(?:y|ian)",
            "irish",
            r"israeli",
            r"ital(?:y|ian|iano)",
            "jewish",
            "mediterranean",
            "macedonian",
            "maltese",
            "moldova",
            "muldave",
            "polish",
            r"portug[u,e]?ese?",
            r"rou?ma?(?:ni|nia|ian|nian)?",
            r"russian?",
            r"serbian?",
            r"slovakian?",
            "slovenia",
            "spanish",
            "ukrainian",
            "juegoslavie",
            r"yug[o,u]slav(?:ia|ian)?",
        ],
    ),
    (
        "Oceania",
        [
            r"cook islands?",
            r"australian?",
            r"new\s?zealand",
            r"f[i,u]ji(an)?",
            "guinee",
            "micronesian",
            "pacifica",
            "samoan",
            "niuean",  # polynesian
            "tongan",
            "melanesian",
        ],
    )(
        "Aboriginal_First_Nations_Indigenous",
        [
            "aboriginal",
            r"first[\s,_]?nations?",
            "indigenous",
            "maori",
            "bajau",
            "indigena",
            "metis",
        ],
    ),
]
