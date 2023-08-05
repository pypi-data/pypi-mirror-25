import os
from pathlib import Path
from Datasnakes.Orthologs.Phylogenetics.IQTree.iqtree import IQTreeCommandline
from shutil import copy
import subprocess
#TODO-ROB Make this inherit FilteredAlignment


class FilteredTree(object):

    def __init__(self, alignment, dataType='CODON', home=os.getcwd()):
        self.home = Path(home)
        self.iqtree_path = self.home / Path('IQTREE')
        self.tree_file = self.iqtree_path / Path(alignment + '.treefile')
        self.gene = alignment.replace('_P2N_na.iqtree.aln', '')

        self.aln_File = str(self.home / Path(alignment))
        outDir = self.home / Path('IQTREE')
        Path.mkdir(outDir, exist_ok=True)
        copy(self.aln_File, str(outDir))
        os.chdir(str(outDir))
        self.iqtree_best_tree(alignment, dataType)
        copy(self.tree_file, str(self.home / Path(self.gene + '_iqtree.nwk')))

    def iqtree_best_tree(self, alignment, dataType):

        IQTCmd = IQTreeCommandline(alignment=alignment, dataType=dataType)
        print(IQTCmd)
        subprocess.check_call([str(IQTCmd)], stderr=subprocess.STDOUT, shell=True)
