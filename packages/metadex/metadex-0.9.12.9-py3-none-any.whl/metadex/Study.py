
from .preprocessing import *
from .analysis import *
from pkg_resources import resource_string

class Study:

    def __init__(self, name=None, counts=None, groups=None, iDs=None, geneMatrix=None):
        self.name = name

    def read_annotations(self):
        self.counts = get_group_counts_API(self.name)
        filenames = glob.glob(self.name +'/*.csv')
        self.groups = [filename.split('/')[1].split('_')[0] for filename in filenames]
        self.iDs = [filename.split('/')[1].split('_')[1] for filename in filenames]



    def normalise_counts(self):
        normalise_rnr(self.name)
        normalisedList = glob.glob(os.path.join('normalised_counts/*.csv'))
        normalisedDFList = [pd.read_csv(norm) for norm in normalisedList]
        self.counts = normalisedDFList

    def load_counts(self, folder):
        filenames = glob.glob(folder +'/*.csv')
        self.counts = [pd.read_csv(filename) for filename in filenames]
        self.groups = [filename.split('/')[1].split('_')[0] for filename in filenames]
        self.iDs = [filename.split('/')[1].split('_')[1] for filename in filenames]

    def add_lineage_info(self):
        self.counts = annotate_all_counts(self.name)


    def load_gene_matrix(self, filename):
        self.geneMatrix = pd.read_table(filename, header=0)

    def determine_genes_of_interest(self, lvl1pct=70, lvl2pct=70, lvl3pct=60, fxnpct=40):
        find_genes_of_interest(self.name, self.groups, self.geneMatrix, lvl1pct, lvl2pct, lvl3pct, fxnpct)
        return [pd.read_csv(i) for i in glob.glob('*tentative*.csv')]

    def determine_organisms_of_interest(self, lvl1pct=70, lvl2pct=70, lvl3pct=60, lvl4pct=40):
        find_organisms_of_interest(self.name, self.groups, lvl1pct, lvl2pct, lvl3pct, lvl4pct)
        return [pd.read_csv(i) for i in glob.glob('*tentative*.csv')]


    def focus_on_gene(self, searchString):
        mergedCounts = merge_all_counts(self.name)
        mergedCounts = mergedCounts.fillna(0)
        geneDF = subset_by_gene(self.name, searchString, mergedCounts)
        return geneDF

    def visualise_diversity_for_gene(self, geneName, searchString):
        get_diversity_measures(geneName, searchString, self.name)

    def focus_on_organisms(self, level, query):
        mergedCounts = merge_all_counts(self.name)
        mergedCounts = mergedCounts.fillna(0)
        orgDF = subset_by_taxa(self.name, level, query, mergedCounts)
        return orgDF
