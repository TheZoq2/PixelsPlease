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

ENTITIES = [
        Entity("The prince", E_PRO_GOV),
        Entity("The queen", E_PRO_GOV),
        Entity("The king", E_PRO_GOV),
        Entity("The emperor", E_PRO_GOV),
        Entity("The opposition", E_ANTI_GOV),
        Entity("The capitalist", E_ANTI_GOV),
        Entity("Justin Bieber", E_NEUTRAL),
        Entity("A child", E_NEUTRAL),
    ]




def get_random_entity(world_state):
    return random.sample(world_state.entities, 1)[0]




#Functions that generate headlines
def h_embarasing(world_state):
    scenario = pick_one([
                "{} seen wearing dirty clothes",
                "{} has been begging for food in the streets",
                "{} seen wearing 'unmanly' clothes",
                "{} was caught smelling their own fart",
                "{} was caught sneaking out of a gaybar",
            ])

    entity = get_random_entity(world_state)
    return (scenario.format(entity.name), C_BAD * entity.standing)

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

    standing = C_GOOD if entity == E_PRO_GOV else C_BAD
    return (scenario.format(entity.name), standing)


def h_killing(world_state):
    scenario = pick_one([
            "{} found guilty of murdering {}",
            "{} accused of murdering {}"
        ])

    entities = random.sample(world_state.entities, 2);
    return (scenario.format(entities[0].name, entities[1].name), entities[0].standing * C_BAD)

HEADLINE_TEMPLATES = [
        h_embarasing,
        h_election_good,
        h_killing,
        h_affair
    ]

class WorldState():
    def __init__(self):
        self.entities = copy.deepcopy(ENTITIES)



def generate_headline(world_state):
    return pick_one(HEADLINE_TEMPLATES)(world_state)


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

def random_event(world_state):
    pass

if __name__ == "__main__":
    world_state = WorldState()
    # Run all the functions to make sure they work
    for h in HEADLINE_TEMPLATES:
        h(world_state)

    print(generate_headline(world_state))
    print(ev_opinion_change(world_state))
