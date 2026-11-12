"""Board Exam packs (CBSE, UP, Bihar, Maharashtra, Others) → packs/board-*.v1.json + index.json course 'board'.
'v' = from the owner's doc (verified). 'r' = added from research (please verify against the board's 2026-27 syllabus)."""
import json, copy
from pathlib import Path
V, R = 'verified', 'verify'
SCI10 = [('Chemical Reactions and Equations',V),('Acids, Bases and Salts',V),('Metals and Non-metals',V),('Carbon and its Compounds',V),('Life Processes',V),('Control and Coordination',V),('How do Organisms Reproduce?',V),('Heredity and Evolution',V),('Light: Reflection and Refraction',V),('Human Eye and Colourful World',V),('Electricity',V),('Magnetic Effects of Electric Current',V),('Our Environment',R)]
MATH10 = [(c,V) for c in ['Real Numbers','Polynomials','Pair of Linear Equations','Quadratic Equations','Arithmetic Progressions','Triangles','Coordinate Geometry','Introduction to Trigonometry','Some Applications of Trigonometry','Circles','Areas Related to Circles','Surface Areas and Volumes','Statistics','Probability']]
SST10 = [(c,R) for c in ['History: Rise of Nationalism in Europe','History: Nationalism in India','History: The Making of a Global World','History: The Age of Industrialisation','History: Print Culture and the Modern World','Geography: Resources and Development','Geography: Forest and Wildlife Resources','Geography: Water Resources','Geography: Agriculture','Geography: Minerals and Energy Resources','Geography: Manufacturing Industries','Geography: Lifelines of National Economy','Civics: Power Sharing','Civics: Federalism','Civics: Gender, Religion and Caste','Civics: Political Parties','Civics: Outcomes of Democracy','Economics: Development','Economics: Sectors of the Indian Economy','Economics: Money and Credit','Economics: Globalisation and the Indian Economy','Economics: Consumer Rights']]
PHY12 = [('Electric Charges and Fields',V),('Electrostatic Potential and Capacitance',V),('Current Electricity',V),('Moving Charges and Magnetism',V),('Magnetism and Matter',V),('Electromagnetic Induction',V),('Alternating Current',V),('Electromagnetic Waves',R),('Ray Optics and Optical Instruments',V),('Wave Optics',V),('Dual Nature of Radiation and Matter',V),('Atoms',V),('Nuclei',V),('Semiconductor Electronics',V)]
CHEM12 = [(c,V) for c in ['Solutions','Electrochemistry','Chemical Kinetics','d and f Block Elements','Coordination Compounds','Haloalkanes and Haloarenes','Alcohols, Phenols and Ethers','Aldehydes, Ketones and Carboxylic Acids','Amines','Biomolecules']]
MATH12 = [(c,R) for c in ['Relations and Functions','Inverse Trigonometric Functions','Matrices','Determinants','Continuity and Differentiability','Application of Derivatives','Integrals','Application of Integrals','Differential Equations','Vector Algebra','Three Dimensional Geometry','Linear Programming','Probability']]
BIO12 = [(c,R) for c in ['Sexual Reproduction in Flowering Plants','Human Reproduction','Reproductive Health','Principles of Inheritance and Variation','Molecular Basis of Inheritance','Evolution','Human Health and Disease','Microbes in Human Welfare','Biotechnology: Principles and Processes','Biotechnology and its Applications','Organisms and Populations','Ecosystem','Biodiversity and Conservation']]
ACC12 = [(c,V) for c in ['Accounting for Partnership: Basic Concepts','Reconstitution of Partnership (Admission/Retirement/Death)','Dissolution of Partnership Firm','Accounting for Share Capital','Issue and Redemption of Debentures','Analysis of Financial Statements','Accounting Ratios','Cash Flow Statement']]
BST12 = [(c,V) for c in ['Nature and Significance of Management','Principles of Management','Business Environment','Planning & Organizing','Staffing, Directing & Controlling','Financial Management','Financial Markets','Marketing Management','Consumer Protection']]
ECO12 = [(c,R) for c in ['Macro: National Income Accounting','Macro: Money and Banking','Macro: Determination of Income and Employment','Macro: Government Budget and the Economy','Macro: Balance of Payments','Indian Economy: Development Experience (1947–90) and Reforms since 1991','Indian Economy: Current Challenges','Indian Economy: Comparison with Neighbours']]
HIS12 = [('Bricks, Beads and Bones (Harappan)',V),('Kings, Farmers and Towns',V),('Kinship, Caste and Class',V),('Thinkers, Beliefs and Buildings',R),('Through the Eyes of Travellers',V),('Bhakti-Sufi Traditions',V),('An Imperial Capital: Vijayanagara',V),('Peasants, Zamindars and the State',R),('Colonialism and the Countryside',V),('Rebels and the Raj',V),('Mahatma Gandhi and the Nationalist Movement',V),('Framing the Constitution',R)]
POL12 = [(c,V) for c in ['The End of Bipolarity','New Centres of Power','Contemporary South Asia','International Organisations','Environment and Natural Resources','Challenges of Nation Building','Planned Development',"India's External Relations",'Democratic Resurgence','Regional Aspirations']]
GEO12 = [(c,R) for c in ['Human Geography: Nature and Scope','The World Population','Human Development','Primary Activities','Secondary Activities','Tertiary and Quaternary Activities','Transport and Communication (World)','International Trade (World)','India: Population','India: Human Settlements','India: Land Resources and Agriculture','India: Water Resources','India: Mineral and Energy Resources','India: Planning and Sustainable Development','India: Transport and Communication','India: International Trade','Geographical Perspective on Selected Issues']]

UP_HIN10 = [(c,V) for c in ['Gadya: Mitrata (Ramchandra Shukla)','Gadya: Mamta (Jaishankar Prasad)','Gadya: Bhartiya Sanskriti (Rajendra Prasad)','Kavya: Surdas - Pad','Kavya: Tulsidas - Dhanush Bhang','Kavya: Raskhan - Savaiye','Sanskrit: Varanasi','Sanskrit: Deshbhakt Chandrashekhar','Sanskrit: Jeevan Sutrani']]
UP_SST10 = [(c,V) for c in ['Itihas: Europe me Rashtravad ka Uday','Itihas: Bharat me Rashtravad','Itihas: Bhumandalikrit Vishwa ka Banna','Bhugol: Sansadhan evam Vikas','Bhugol: Van aur Vanya Jeev','Bhugol: Jal Sansadhan','Bhugol: Krishi','Nagrik Shastra: Satta ki Sajhedari','Nagrik Shastra: Sanghvad','Arthashastra: Vikas','Arthashastra: Bharatiya Arthvyavastha ke Kshetrak']]
UP_BIO12 = [(c,V) for c in ['Pushpi Padapon mein Laingik Janan','Manav Janan','Janan Swasthya','Vanshagati tatha Vividhta ke Siddhant','Vanshagati ke Aanvik Aadhar','Vikas (Evolution)','Manav Swasthya tatha Rog','Jaiv Praudyogiki (Biotech)','Jaiv Vividhata evam Sanrakshan']] + [(c,R) for c in ['Manav Kalyan mein Sukshmjeev','Jeev aur Samashti','Paritantra']]
UP_ACC12 = [(c,V) for c in ['Sajhedari ka Pravesh','Avkash Grahan tatha Mrityu','Sajhedari ka Vighatan','Ansho ka Nirgaman evam Haran','Rinpatro ka Nirgaman','Company ke Antim Khaate']]
UP_GEO12 = [(c,V) for c in ['Manav Bhugol - Prakriti evam Vishay Kshetra','Vishwa Jansankhya','Manav Vikas','Prathmik & Ditiyak Kriyayein','Jansankhya Vitran','Pravas','Manav Basti','Bhu-Sansadhan tatha Krishi']]
BR_SCI10 = [(c,V) for c in ['Prakash ka Paravartan tatha Apavartan','Manav Netra tatha Rangbiranga Sansar','Vidyut','Vidyut Dhara ke Chumbakiya Prabhav','Rasayanik Abhikriyayein','Amla, Bhasma aur Lavan','Dhatu aur Adhatu','Carbon aur uske Yaugik','Jaiv Prakram','Niyantran aur Samanvay','Jeev Janan kaise karte hai','Anuvanshiktva']] + [('Hamara Paryavaran',R)]
BR_MATH10 = [(c,V) for c in ['Bahupad','Do char wale Raikhik Samikaran','Dwigat Samikaran','Samantar Shreni','Tribhuj','Vrit','Rachnayein','Nirdeshank Jyamiti']] + [(c,R) for c in ['Vastavik Sankhyayein','Trikonmiti ka Parichay','Trikonmiti ke Anuprayog','Vrit se Sambandhit Kshetrafal','Prishthiya Kshetrafal aur Aayatan','Sankhyiki','Prayikta']]
BR_PHY12 = [(c,V) for c in ['Vaidyut Avesh tatha Kshetra','Sthir Vaidyut Vibhav','Vidyut Dhara','Gatiman Avesh aur Chumbakatva','Kiran Prakashiki','Tarang Prakashiki','Vikiran tatha Dravya ki Dwait Prakriti','Nabhik','Ardhchalak']] + [(c,R) for c in ['Chumbakatva evam Dravya','Vaidyut Chumbakiya Prerna','Pratyavarti Dhara','Vaidyut Chumbakiya Tarange','Parmanu']]
BR_EPS12 = [(c,V) for c in ['Sensing and Identification of Entrepreneurial Opportunities','Environment Scanning','Market Assessment','Formulation of Project Report','Resource Assessment','Financial Planning','Marketing Mix']]
BR_HIS12 = [(c,V) for c in ['Eente, Manke tatha Asthiyan','Raja, Kisan aur Nagar','Vicharak, Vishwas aur Imaratein','Bhakti Sufi Paramparayein','Upniveshvad aur Dehat','Vidrohi aur Raj','Mahatma Gandhi aur Rashtriya Andolan','Samvidhan ka Nirman']]
MH_SCI1 = [(c,V) for c in ['Gravitation','Periodic Classification of Elements','Chemical Reactions and Equations','Effects of Electric Current','Heat','Refraction of Light','Space Missions']] + [(c,R) for c in ['Lenses','Metallurgy','Carbon Compounds']]
MH_SCI2 = [(c,V) for c in ['Heredity and Evolution','Life Processes in Living Organisms','Environmental Management','Towards Green Energy','Animal Classification','Disaster Management']] + [(c,R) for c in ['Introduction to Microbiology','Cell Biology and Biotechnology','Social Health']]
MH_M1 = [(c,V) for c in ['Linear Equations in Two Variables','Quadratic Equations','Arithmetic Progression','Financial Planning','Probability','Statistics']]
MH_M2 = [(c,V) for c in ['Similarity','Pythagoras Theorem','Circle','Geometric Constructions','Coordinate Geometry','Trigonometry','Mensuration']]
MH_PHY12 = [(c,V) for c in ['Rotational Dynamics','Mechanical Properties of Fluids','Kinetic Theory of Gases and Radiation','Thermodynamics','Oscillations','Superposition of Waves','Wave Optics','Electrostatics','Current Electricity','Magnetic Fields due to Electric Current','Dual Nature of Radiation','Structure of Atoms']] + [(c,R) for c in ['Magnetic Materials','Electromagnetic Induction','AC Circuits','Semiconductor Devices']]
MH_CHEM12 = [(c,R) for c in ['Solid State','Solutions','Ionic Equilibria','Chemical Thermodynamics','Electrochemistry','Chemical Kinetics','Elements of Groups 16, 17 and 18','Transition and Inner Transition Elements','Coordination Compounds','Halogen Derivatives','Alcohols, Phenols and Ethers','Aldehydes, Ketones and Carboxylic Acids','Amines','Biomolecules','Introduction to Polymer Chemistry','Green Chemistry and Nanochemistry']]
MH_MATH12 = [(c,R) for c in ['Mathematical Logic','Matrices','Trigonometric Functions','Pair of Straight Lines','Vectors','Line and Plane','Linear Programming','Differentiation','Applications of Derivatives','Indefinite Integration','Definite Integration','Application of Definite Integration','Differential Equations','Probability Distributions','Binomial Distribution']]
MH_BIO12 = [(c,R) for c in ['Reproduction in Lower and Higher Plants','Reproduction in Lower and Higher Animals','Inheritance and Variation','Molecular Basis of Inheritance','Origin and Evolution of Life','Plant Water Relation','Plant Growth and Mineral Nutrition','Respiration and Circulation','Control and Co-ordination','Human Health and Diseases','Enhancement of Food Production','Biotechnology','Organisms and Populations','Ecosystems and Energy Flow','Biodiversity, Conservation and Environmental Issues']]
MH_OCM12 = [(c,V) for c in ['Principles of Management','Functions of Management','Entrepreneurship Development','Business Services','Emerging Modes of Business','Social Responsibilities of Business','Consumer Protection','Marketing']]
MH_SP12 = [(c,V) for c in ['Introduction to Corporate Finance','Sources of Corporate Finance','Issue of Shares','Issue of Debentures','Deposits','Correspondence with Members','Correspondence with Debentureholders','Depository System','Payment of Dividend and Interest']]
MH_BK12 = [(c,R) for c in ['Introduction to Partnership and Final Accounts','Reconstitution of Partnership (Admission)','Reconstitution of Partnership (Retirement/Death)','Dissolution of Partnership Firm','Accounts of Not-for-Profit Concerns','Bills of Exchange','Analysis of Financial Statements','Computer in Accounting']]
MH_ECO12 = [(c,V) for c in ['Introduction to Micro Economics','Utility Analysis','Demand Analysis','Elasticity of Demand','Supply Analysis','Forms of Market','Index Numbers','National Income','Public Finance in India','Money Market and Capital Market in India','Foreign Trade of India']]

CBSE = {'10': {'': {'Science': SCI10, 'Mathematics': MATH10, 'Social Science': SST10}},
        '12': {'science': {'Physics': PHY12, 'Chemistry': CHEM12, 'Mathematics': MATH12, 'Biology': BIO12},
               'commerce': {'Accountancy': ACC12, 'Business Studies': BST12, 'Economics': ECO12, 'Mathematics': MATH12},
               'arts': {'History': HIS12, 'Political Science': POL12, 'Geography': GEO12, 'Economics': ECO12}}}
BOARDS = {
 'cbse': ('CBSE', '🏫', CBSE),
 'up': ('UP Board', '🟠', {'10': {'': {'Hindi': UP_HIN10, 'Science': SCI10, 'Mathematics': MATH10, 'Social Science': UP_SST10}},
        '12': {'science': {'Physics': PHY12, 'Chemistry': CHEM12, 'Mathematics': MATH12, 'Biology': UP_BIO12},
               'commerce': {'Accountancy': UP_ACC12, 'Business Studies': BST12, 'Economics': ECO12},
               'arts': {'Geography': UP_GEO12, 'History': HIS12, 'Political Science': POL12, 'Economics': ECO12}}}),
 'bihar': ('Bihar Board', '🟢', {'10': {'': {'Science': BR_SCI10, 'Mathematics': BR_MATH10, 'Social Science': SST10}},
        '12': {'science': {'Physics': BR_PHY12, 'Chemistry': CHEM12, 'Mathematics': MATH12, 'Biology': BIO12},
               'commerce': {'Entrepreneurship': BR_EPS12, 'Accountancy': ACC12, 'Business Studies': BST12, 'Economics': ECO12},
               'arts': {'History': BR_HIS12, 'Political Science': POL12, 'Geography': GEO12, 'Economics': ECO12}}}),
 'maharashtra': ('Maharashtra Board', '🔵', {'10': {'': {'Science & Technology Part 1': MH_SCI1, 'Science & Technology Part 2': MH_SCI2, 'Mathematics Part 1 (Algebra)': MH_M1, 'Mathematics Part 2 (Geometry)': MH_M2}},
        '12': {'science': {'Physics': MH_PHY12, 'Chemistry': MH_CHEM12, 'Mathematics': MH_MATH12, 'Biology': MH_BIO12},
               'commerce': {'Organisation of Commerce & Management': MH_OCM12, 'Secretarial Practice': MH_SP12, 'Book-Keeping & Accountancy': MH_BK12, 'Economics': MH_ECO12},
               'arts': {'Economics': MH_ECO12}}}),
 'others': ('Other boards (NCERT-based)', '📘', CBSE),
}

idx = json.loads(Path('index.json').read_text())
ex_course = next(c for c in idx['courses'] if (c.get('id') or c.get('code')) == 'ca')
ex_level = ex_course['levels'][0]
ex_pack = json.loads(Path(ex_level['pack']).read_text())
ex_sub = ex_pack['subjects'][0]
ch_key = 'modules' if 'modules' in ex_sub else 'chapters'
ch_item = ex_sub[ch_key][0]

def chapter(name, tag):
    if isinstance(ch_item, dict):
        d = {k: copy.deepcopy(v) for k, v in ch_item.items()}
        d['name'] = name
        for k in list(d):
            if k == 'topics': d[k] = []
            elif k not in ('name',) and isinstance(d[k], (str, int, float)) and k not in ('weight', 'hours'): d.pop(k)
        d['status'] = tag
        return d
    return name

levels, made = [], 0
for bid, (bname, emoji, data) in BOARDS.items():
    for cls, streams in data.items():
        for stream, subjects in streams.items():
            lid = f'{bid}-{cls}' + (f'-{stream}' if stream else '')
            lname = f'{bname} · Class {cls}' + (f' · {stream.title()}' if stream else '')
            pack = {k: copy.deepcopy(v) for k, v in ex_pack.items() if k != 'subjects'}
            for k in ('course', 'id'):
                if k in pack: pack[k] = 'board' if k == 'course' else f'board-{lid}'
            pack['course'] = 'board'; pack['level'] = lid; pack['name'] = lname
            pack['board'] = bid; pack['class'] = cls; pack['stream'] = stream or None
            pack['subjects'] = []
            for sname, chs in subjects.items():
                s = {k: copy.deepcopy(v) for k, v in ex_sub.items() if k not in (ch_key,)}
                s['name'] = sname
                for k in list(s):
                    if k not in ('name',) and isinstance(s[k], str): s.pop(k)
                s[ch_key] = [chapter(n, t) for n, t in chs]
                pack['subjects'].append(s)
            path = f'packs/board-{lid}.v1.json'
            Path(path).write_text(json.dumps(pack, ensure_ascii=False, indent=1))
            lv = {k: copy.deepcopy(v) for k, v in ex_level.items()}
            lv.update({'id': lid, 'name': lname, 'pack': path})
            if 'code' in lv: lv['code'] = lid
            levels.append(lv); made += 1
course = {k: copy.deepcopy(v) for k, v in ex_course.items()}
course.update({'id': 'board', 'name': 'Board Exam', 'levels': levels})
if 'code' in course: course['code'] = 'board'
if 'emoji' in course: course['emoji'] = '🏫'
idx['courses'] = [c for c in idx['courses'] if (c.get('id') or c.get('code')) != 'board'] + [course]
Path('index.json').write_text(json.dumps(idx, ensure_ascii=False, indent=1))

pt = Path('exams/patterns.json')
if pt.exists():
    P = json.loads(pt.read_text())
    for lv in levels:
        pk = json.loads(Path(lv['pack']).read_text())
        cbse = lv['id'].startswith(('cbse', 'others'))
        P[f"board/{lv['id']}"] = {'total': f"{len(pk['subjects'])} theory papers", 'paper': '',
            'subjects': {s['name']: {'mode': 'written', 'duration': 180, 'marks': 80 if cbse else None,
                                     'note': 'Board theory paper (+ internal/practical marks)' + ('' if cbse else ' · check your board pattern')} for s in pk['subjects']}}
    pt.write_text(json.dumps(P, ensure_ascii=False, indent=1))
nv = sum(1 for b in BOARDS.values() for c in b[2].values() for s in c.values() for chs in s.values() for _, t in chs if t == R)
print(f'board packs: {made} | chapters to verify (from research): {nv} | course id: board | chapter key: {ch_key}')
