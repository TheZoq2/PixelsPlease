import random
import copy

#Picks a random element from the specified list
def pick_one(seq):
    return random.sample(seq, 1)[0]

# Possible standings of people
E_PRO_GOV = 1 # Loved by gov, hated by pop
E_NEUTRAL = 0 # Neutral to both gov and pop
E_ANTI_GOV = -1 # Hated by government, loved by people

# Consequences from an article being spread, seen from the governemnts point of view
C_GOOD = 1
C_BAD = -1
C_NEUTRAL = 0

class Entity:
    def __init__(self, name, standing):
        self.name = name
        self.standing = standing

    def get_standing_text(self):
        return {
                E_PRO_GOV: "{} should be protected from slander",
                E_NEUTRAL: "{} does not need to be protected from slander",
                E_ANTI_GOV: "Positive news about {} should be censored",
            }[self.standing].format(self.name)

ENTITIES = [
        Entity("General Vladimir", E_PRO_GOV),
        Entity("Emperor Josef", E_PRO_GOV),
        Entity("KGB leader Alexandr Blinov", E_PRO_GOV),
        Entity("President Anatoli", E_PRO_GOV),
        Entity("Empress Swetlana", E_PRO_GOV),

        Entity("Rebel general Andrei", E_ANTI_GOV),
        Entity("Opposition leader Maxim Ivanov", E_ANTI_GOV),

        Entity("Justin Bieber", E_NEUTRAL),
        Entity("Charlie Sheen", E_NEUTRAL),
        Entity("former president Obama", E_NEUTRAL),
        Entity("Hugh Hefner", E_NEUTRAL),
        Entity("Stefan Löfven", E_NEUTRAL),
        Entity("Göran Persson", E_NEUTRAL),
        Entity("Miley Cyrus", E_NEUTRAL),
    ]

def random_entity_name():
    return pick_one(ENTITIES).name


A_COOL=1
A_UNCOOL=-1

class Action:
    def __init__(self, text, change_text, coolness):
        self.text = text
        self.change_text = change_text
        self.coolness = coolness

    def get_status_text(self):
        if self.coolness == A_COOL:
            return "{} is considered cool".format(self.change_text)
        else:
            return "{} is considered uncool".format(self.change_text)


ACTIONS = [
            Action("{} has been seen wearing an ugly hat", "wearing ugly hats", A_UNCOOL),
            Action("{} was caught sneaking out of a gaybar", "going to gay bars", A_UNCOOL),
            Action("{} seen wearing dirty clothes", "wearing dirty clothes", A_UNCOOL),
            Action("{} has been begging for food in the streets", "begging", A_UNCOOL),
            Action("{} was caught smelling their own fart", "smelling your own farts", A_UNCOOL),
            Action("{} is considered a pro skateboarder", "skateboarding", A_COOL),
            Action("{} has donated a large sum to charity", "donating money", A_COOL),
            Action("{} has saved the life of {}".format("{}", random_entity_name()),
                "saving people's lives", A_COOL),
            Action("Nudes of {} have been leaked", "having your nudes leaked", A_UNCOOL),
            Action("{} has had their private emails leaked", "having your emails leaked", A_UNCOOL),
        ]


def get_random_entity(world_state):
    return random.sample(world_state.entities, 1)[0]




#Functions that generate headlines
def h_action(world_state):
    action = pick_one(world_state.actions)

    entity = get_random_entity(world_state)
    return (action.text.format(entity.name), C_BAD * entity.standing * action.coolness * -1)

def h_affair(world_state):
    scenario = "{} has had an affair with {}"

    entities = random.sample(world_state.entities, 2);

    consequence = C_BAD if E_PRO_GOV in (entities[1].standing, entities[0].standing) else C_NEUTRAL
    return (scenario.format(entities[0].name, entities[1].name), consequence)

def h_election_good(world_state):
    scenario = pick_one([
            "{} got 99.999% of the votes in the election last week",
            "{} got 129% of the votes in the election last week",
            "Latest polls show {} in the lead for the next election",
        ])

    entity = get_random_entity(world_state)

    standing = C_GOOD if entity.standing == E_PRO_GOV else C_BAD
    return (scenario.format(entity.name), standing)


def h_killing(world_state):
    scenario = pick_one([
            "{} found guilty of murdering {}",
            "{} accused of murdering {}"
        ])

    entities = random.sample(world_state.entities, 2);
    return (scenario.format(entities[0].name, entities[1].name), entities[0].standing * C_BAD)

def h_clickbait(world_state):
    return (
            pick_one([
                    "Top 5 reasons carrots cause cancer. Number 7 will shock you",
                    "Shocking news! Find out more in tomorrow's paper",
                    "Which member of the royal family are you?",
                    "You won't believe what {} said about {}".format(
                            get_random_entity(world_state).name,
                            get_random_entity(world_state).name
                        ),
                ]),
            world_state.clickbait_state
        )


def h_generic(world_state):
    return (
            pick_one([
                    "Mikhail finally got out of harbour",
                    "{} almost run over by angry australian".format(get_random_entity(world_state).name),
                    "Danish person attempted to insult {}".format(get_random_entity(world_state).name),
                ]),
            C_NEUTRAL
        )


def diversify_headline(headline_function):
    diversifiers = [
                "Population shocked, {}",
                "{} according to an annonymous source",
                "Government source says {}",
                "Breaking news: {}",
                "{}",
                "{}",
            ]

    def fun(world_state): 
        temp = headline_function(world_state)
        return (pick_one(diversifiers).format(temp[0]), temp[1])

    return fun

def check_illegal_mentions(headline_function):
    def fun(world_state): 
        temp = headline_function(world_state)

        consequence = temp[1]

        for illegal in world_state.illegal_people:
            if illegal.name in temp[0]:
                consequence = C_BAD

        return (temp[0], consequence)

    return fun


HEADLINE_TEMPLATES = [
        diversify_headline(h_action),
        diversify_headline(h_action),
        diversify_headline(h_action),
        diversify_headline(h_action),
        diversify_headline(h_action),
        diversify_headline(h_action),
        diversify_headline(h_election_good),
        diversify_headline(h_election_good),
        diversify_headline(h_killing),
        diversify_headline(h_affair),
        h_clickbait,
        h_generic
    ]

class WorldState():
    def __init__(self):
        self.entities = copy.deepcopy(ENTITIES)
        self.actions = copy.deepcopy(ACTIONS)
        self.clickbait_state = C_NEUTRAL
        self.illegal_people = []

    def get_state_text(self):
        result = "People: \n"

        for e in self.entities:
            result += e.get_standing_text() + "\n"

        result += "====================\n"
        result += "Actions: \n"

        for a in self.actions:
            result += a.get_status_text() + "\n"

        result += "====================\n"

        result += "Clickbait is: {}\n".format(("legal" if self.clickbait_state == C_NEUTRAL else "illegal"))

        result += "====================\n"
        for person in self.illegal_people:
            result += "Mentioning {} is illegal\n".format(person.name)

        return result




def generate_headline(world_state):
    return check_illegal_mentions(pick_one(HEADLINE_TEMPLATES))(world_state)


def ev_opinion_change(world_state):
    target = pick_one(world_state.entities)

    new_standing = pick_one([E_NEUTRAL, E_PRO_GOV, E_ANTI_GOV])

    if new_standing == target.standing:
        return None

    reasons = {
            E_PRO_GOV: "{} should be protected from slander",
            E_NEUTRAL: "You no longer have to care about slander against {}",
            E_ANTI_GOV: "{} is considered a threat to the government"
        }

    target.standing = new_standing
    return reasons[new_standing].format(target.name)

def ev_coolness_change(world_state):
    target = pick_one(world_state.actions)

    new_coolness = pick_one([A_UNCOOL, A_COOL])
    if new_coolness == target.coolness:
        return None

    target.coolness = new_coolness
    return "{} is now considered {}".format(target.change_text, "cool" if new_coolness == A_COOL else "uncool")

def ev_clickbait_opinion_change(world_state):
    if world_state.clickbait_state == C_NEUTRAL:
        world_state.clickbait_state = C_BAD
        return "The government has announced that publishing clickbait is now illegal"
    else:
        world_state.clickbait_state = C_NEUTRAL
        return "The government has removed the ban on clickbait"

def ev_change_mention_status(world_state):
    result = ""

    #Check if we should add someone to the list
    if random.randint(0, 1):
        person = pick_one(world_state.entities)
        world_state.illegal_people.append(person)
        result += "mentioning {} is now illegal".format(person.name)

    new_list = []

    for i in range(0, len(world_state.illegal_people)):
        if random.randint(0, 3) == 0:
            result += "\nyou are allowed to mention {} again".format(world_state.illegal_people[i].name)
        else:
            new_list.append(world_state.illegal_people[i])

    world_state.illegal_people = new_list

    return result



def random_event(world_state):
    return pick_one([
            ev_opinion_change,
            ev_opinion_change,
            ev_coolness_change,
            ev_coolness_change,
            ev_clickbait_opinion_change,
            ev_change_mention_status,
            ev_change_mention_status,
            ev_change_mention_status,
        ])(world_state)


if __name__ == "__main__":
    world_state = WorldState()
    # Run all the functions to make sure they work
    for h in HEADLINE_TEMPLATES:
        h(world_state)

    print(generate_headline(world_state))
    print(ev_opinion_change(world_state))
    print(ev_coolness_change(world_state))
    print(ev_change_mention_status(world_state))

    print(world_state.get_state_text())
