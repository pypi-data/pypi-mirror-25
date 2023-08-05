import itertools

class Reaction(object):
    kegg_id = None
    substrates = None
    products = None
    reversible = None
    orthologs = None
    pathway = None

    def __init__(self, kegg_id, substrates, products, reversible, orthologs, pathways):
        self.kegg_id = kegg_id
        self.substrates = set(substrates)
        self.products = set(products)
        self.reversible = reversible
        self.orthologs = set(orthologs)
        if isinstance(pathways, str):
            self.pathways = set(pathways)

    def cmp_compounds(self, other):
        if (self.substrates != other.substrates) and (self.products != other.products):
            if self.reversible:
                return (self.substrates == other.products) and (self.products == other.substrates)
            else:
                return False
        else:
            return True

    def to_edges(self):
        edges = [
            itertools.product(self.substrates, [self.kegg_id]),
            itertools.product([self.kegg_id], self.products)
        ]
        if self.reversible:
            edges.extend(
                [
                    itertools.product(self.products, [self.kegg_id]),
                    itertools.product([self.kegg_id], self.substrates)
                ]
            )
        return itertools.chain(*edges)

    def __eq__(self, other):
        if (self.kegg_id == other.kegg_id) and (self.reversible == other.reversible) and (self.orthologs == other.orthologs):
            return self.cmp_compounds(other)
    def __ne__(self, other):
        return not (self == other)
    def __repr__(self):
        return "{}: s {} {} p {} - ({} - {})".format(
            self.kegg_id,
            ','.join(self.substrates),
            '<=>' if self.reversible else '=>',
            ','.join(self.products),
            ','.join(self.orthologs),
            self.pathway
        )
    def __str__(self):
        return repr(self)

from xml.etree import ElementTree
def merge_kgmls(kgmls, kegg_data=None, cpd_only=True):
    if isinstance(kgmls, str):
        kgmls = [kgmls]

    data = {}

    for kgml in kgmls:
        pathway = ElementTree.fromstring(kgml)
        pathway_name = pathway.attrib['name'].replace('path:', '')
        print pathway_name, pathway.attrib['title']
        for entry in pathway.findall('reaction'):
            orthologs = tuple(
                sorted(
                    ortholog.replace('ko:', '')
                    for ortholog in pathway.find("entry/[@id='{}']".format(entry.attrib['id'])).attrib['name'].split(' ')
                )
            )
            # the "reaction" defined is equivalent to a EC number, meaning multiple
            # reactions IDs in kegg may belong to it. They are stored in the name
            # attribute, separated by space
            reactions = entry.attrib['name'].split(' ')

            # definition of the reaction direction, by manual either reversible
            # or irreversible
            if entry.attrib['type'] == 'irreversible':
                reversible = False
            else:
                reversible = True

            substrates = []
            products = []

            for compound in entry:
                cpd_id = compound.attrib['name'].split(':')[1]
                if not cpd_id.startswith('C'):
                    continue
                if compound.tag == 'substrate':
                    substrates.append(cpd_id)
                else:
                    products.append(cpd_id)

            for reaction in reactions:
                # Each reaction ID is (as usual) prepended by the type "rn", which
                # we don't need
                reaction = reaction.split(':')[1]

                definition = Reaction(reaction, substrates, products, reversible, orthologs, pathway_name)
                # if it's already in the dictionary then check that they're equal
                key = (reaction, orthologs)
                if key in data:
                    if definition != data[key]:
#                         print 'Duplicate reaction NEW[{}] != OLD[{}]'.format(
#                                 data[key],
#                                 definition,
#                             )
                        # Defaults to Reversible
                        definition.reversible = True
                        if not definition.cmp_compounds(data[key]):
                            # Fails checks even if reversible enabled
                            # If not found, it may be a glycan reaction -> duplicate of another one
                            kd_compounds = set(kegg_data.get(reaction, []))
                            if not kd_compounds & (definition.substrates.union(definition.substrates)):
                                print 'Invalid reaction NEW[{}] != OLD[{}] CPDS[{}]'.format(
                                    data[key],
                                    definition,
                                    ','.join(kd_compounds)
                                )
                                continue
                            else:
                                definition.reversible = reversible

                data[key] = definition
    return data


def find_reactions(reactions, orthologs):
    if isinstance(orthologs, str):
        orthologs = [orthologs]
    orthologs = set(orthologs)
    for reaction in reactions:
        if reaction.orthologs & orthologs:
            yield reaction, reaction.orthologs & orthologs
