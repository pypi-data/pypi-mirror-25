# coding: utf-8
import argparse
# from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio import SeqIO
import datetime
import glob
import itertools
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import numpy as np
import os
import pandas as pd
import re
from scipy.cluster import hierarchy
from scipy.spatial import distance
import seaborn as sns
import sys
import wolfeutils.base

# # Venn private functions
# from matplotlib_venn._venn3 import compute_venn3_subsets, compute_venn3_colors
# from matplotlib.colors import ColorConverter


def basicAnalysis(pgap_dir, annotated_gbk_pat=None):
    '''Standard Analysis of PGAP run with figures and Core/Pan breakdown

    This workflow started as a Jupyter notebook for investigating the core and
    pan genomes of strains. It **needs** refactoring.

    Inputs:
    * Path to PGAP dir

    Outputs:
    * Returns None; creates a dated figures_tables directory in the PGAP dir
    '''
    # figdir = 'figures_tables_%s' % datetime.date.today()
    figdir = os.path.join(pgap_dir,
                          'figures_tables_%s' % datetime.date.today())

    if not os.path.exists(figdir):
        os.makedirs(figdir)

    # ## 1. Orthologs clusters identification
    #
    # First, show how many genes are shared between each pair of genomes.
    # Load list of genes shared between each genome
    gene_Distribution_By_Conservation = pd.read_table(
        os.path.join(pgap_dir, '1.Gene_Distribution_By_Conservation.txt'),
        header=0,
        index_col='SharedBy_Strains')

    # Load the full list of which genes belong to which ortholog groups.
    orthologs_cluster = pd.read_table(
        os.path.join(pgap_dir, '1.Orthologs_Cluster.txt'), index_col=0)
    orthologs_cluster.index.name = 'ClusterID'

    # Show a heatmap for gene conservation. 24 (core) is much larger than the
    # rest, so limit the max.
    sns.heatmap(gene_Distribution_By_Conservation, )
    plt.savefig(
        os.path.join(figdir, '1.gene_Distribution_By_Conservation.png'))
    plt.clf()

    # # Optionally, show the distribution for each geneome:
    # for l, col in gene_Distribution_By_Conservation.iteritems():
    #     sns.distplot(col)
    #     # # Or show them on individual plots
    #     # plt.show()

    # Load the full list of which genes belong to which ortholog groups.
    orthologs_presence = orthologs_cluster.copy()
    orthologs_presence = orthologs_presence != '-'
    conservation_level = orthologs_presence.sum(axis=1)

    n_strains = orthologs_cluster.shape[1]  # Total of strains
    n_clusters = len(orthologs_cluster)  # Total of identified clusters

    # Number of clusters present in all clusters
    n_core = conservation_level.value_counts()[n_strains]

    # Number of clusters present in some but not all strains
    n_accessory = n_clusters - n_core
    n_single = conservation_level.value_counts()[1]

    # Position of accessory clusters (present in at least two but not all samples)
    accessory_index = (conservation_level < n_strains) & (
        conservation_level > 1)
    accessory = orthologs_presence[accessory_index].T

    # Drop any entire strains that are NAs (included in strains table but not
    # in PGAP run)
    accessory.dropna(axis='rows')

    print("Number of strains included in analysis: %d" % n_strains)
    print("Total number of clusters: %d" % n_clusters)
    print("Core Clusters: %d" % n_core)
    print("Accessory Clusters: %d" % n_accessory)
    print("Single clusters (only 1 gene in cluster): %d" % n_single)

    # ## 2. PanGenome
    #
    # PGAP does automatic bootstrapping and will show the trends for Pan and
    # Core genome as genomes are added:
    # cat 2.PanGenome.Profile.txt
    pan_pat = re.compile(
        'y = (?P<A>[0-9\.-]+) \*x\*\*(?P<B>[0-9\.-]+) \+ (?P<C>[0-9\.-]+)')
    core_pat = re.compile(
        'y = (?P<A>[0-9\.-]+) \*exp\((?P<B>[0-9\.-]+) \* x\) \+ (?P<C>[0-9\.-]+)')
    with open(os.path.join(pgap_dir, '2.PanGenome.Profile.txt'), 'r') as f:
        pangenome_profile = f.readlines()

    match = pan_pat.search(''.join(pangenome_profile))
    pan_params = match.groupdict()

    match = core_pat.search(''.join(pangenome_profile))
    core_params = match.groupdict()

    pangenome_data = pd.read_table(
        os.path.join(pgap_dir, '2.PanGenome.Data.txt'))

    # pangenome_data.plot()
    # plt.show()
    # for l, col in pangenome_data[['PanGenome', 'CoreGenome']].iteritems():
    #     col.plot()
    #     plt.title(l)
    #     plt.show()

    sns.set_style("whitegrid")

    g = sns.violinplot(
        x="ClusterConservation",
        y="PanGenome",
        data=pangenome_data,
        palette="YlGnBu_d")

    x = np.linspace(0, n_strains, 200)
    y = pan_size(x, float(pan_params['A']), float(pan_params['B']),
                 float(pan_params['C']))
    plt.plot(x, y, label='model')
    plt.legend()
    plt.savefig(os.path.join(figdir, '2.GenomeSize_Pan.png'))
    plt.clf()

    sns.violinplot(
        x="ClusterConservation",
        y="CoreGenome",
        data=pangenome_data,
        palette="YlGnBu_d")
    y = core_size(x, float(core_params['A']), float(core_params['B']),
                  float(core_params['C']))
    plt.plot(x, y, label='model')
    plt.legend()

    plt.savefig(os.path.join(figdir, '2.GenomeSize_Core.png'))
    plt.clf()

    sns.set_style('darkgrid')

    if pan_params['B'] > 0:
        print("Pan-geneome x**B exponent is positive, ∴ the species' "
              "Pan genome is open")
    else:
        print("Pan-geneome x**B exponent is negative, ∴ the species' "
              "Pan genome is closed")

    # > The curve for the pan-genome size can be represented by the following
    # > mathematical function of Y = 2735.2287 X0.5 + 544.4458 (R2 = 0.99)
    # > where, Y represents pan-genome size, while X represents number of
    # > sequenced genomes (Pan-genome size = infinite when X → ∞). Positive
    # > value for exponent of X indicates an open pan-genome whereas a negative
    # > value indicates a closed pan-genome, meaning no new gene to be found
    # > when a new genome is sequenced.
    #
    # http://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-015-1959-5
    # DOI: 10.1186/s12864-015-1959-5

    # ## 3. Gene Variation & SNP Calling
    #
    # ## 4. SNP and Genome Trees
    #
    # The quick thing to show here (besides looking at the trees) is that the
    # species distance clusters in a similar manner to the ortholog clustering
    # we did before:
    species_distance = pd.read_table(
        os.path.join(pgap_dir, '4.Species_Distance_Clusters_Based.txt'),
        skiprows=[0],
        sep='\ *',
        engine='python',
        header=None,
        index_col=0)
    # species_distance.head()
    species_distance['strain'] = species_distance.index
    species_distance.index = species_distance['strain']
    species_distance.drop('strain', axis=1, inplace=True)
    species_distance.columns = species_distance.index.T

    clustergrid = sns.clustermap(species_distance)
    plt.setp(clustergrid.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
    plt.setp(clustergrid.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
    clustergrid.savefig(
        os.path.join(figdir, 'PGAP-Species_Distance_Clusters_Based.png'))

    # ## 5. Function

    # b = '#434FA2'  # sns.xkcd_rgb['blue'] # (xkcd_rgb returns *hex*, not rgb)
    # y = '#F2ED29'  # sns.xkcd_rgb['yellow']

    # # 'DarkYlw'
    # color_dark = '#01031D'  # sns.xkcd_rgb['dark grey blue']  # '#000000'
    # color_light = '#F2EC6A'  # sns.xkcd_rgb['light lavender']
    # cmap = discrete_cmap('DarkYlw', [color_dark, color_light])

    color_dark = sns.xkcd_rgb['grey']
    color_light = sns.xkcd_rgb['light grey']
    cmap = discrete_cmap('GreyLightGrey', [color_dark, color_light])

    # http://stackoverflow.com/questions/27924813/extracting-clusters-from-seaborn-clustermap
    # http://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.dendrogram.html

    # correlations = df.corr()
    # correlations_array = np.asarray(df.corr())

    # In[ ]:
    (row_linkage, reordered_row_indices, col_linkage,
     reordered_col_indices) = get_linkages(accessory)

    filebase = os.path.join(figdir, 'AccessoryPresenceAbsence_low_jaccard')
    if not os.path.exists(filebase + '.pdf'):
        # cgrid_hi = sns.clustermap(accessory, cmap=cmap, row_cluster=True, # col_cluster=False,
        #                           col_linkage=col_linkage, figsize=(250, 4))
        # filebase = os.path.join(figdir, 'AccessoryPresenceAbsence_hi_jaccard')
        # for ext in ['pdf', 'png']:  # '.svg'
        #     cgrid_hi.savefig('%s.%s' % (filebase, ext))
        # plt.show()

        # row_cluster=False,  # col_cluster=False,
        cgrid_low = sns.clustermap(
            accessory,
            cmap=cmap,
            row_linkage=row_linkage,
            col_linkage=col_linkage,
            figsize=(25, 4), xticklabels=False)

        for ext in ['pdf', 'png']:  # '.svg'
            cgrid_low.savefig('%s.%s' % (filebase, ext))
        # plt.show()

    rowtree = hierarchy.to_tree(row_linkage, False)
    row_newick = getNewick(rowtree, "", rowtree.dist, accessory.index)
    with open(os.path.join(figdir, 'StrainUPGMAJaccard.newick'), 'w') as f:
        f.write(row_newick)

    # ### Cleaner version of the UPGMA Strain Tree
    cg = sns.clustermap(
        accessory,
        cmap=cmap,
        row_cluster=True,
        col_cluster=False,
        method='average',
        metric='jaccard',
        figsize=(4, 15))
    plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)

    filebase = os.path.join(figdir, 'AccessoryPresenceAbsence_strainUPGMA')
    for ext in ['pdf', 'png']:  # '.svg'
        cg.savefig('%s.%s' % (filebase, ext))
    plt.clf()

    # Create a dataframe of all the annotations so that we can look up peg
    # descriptions from peg id's by reading the gbk files:
    if annotated_gbk_pat:
        seq_df_cache = os.path.join(pgap_dir, 'seq_df_cache.csv.bz2')
        if os.path.exists(seq_df_cache):
            seq_df = pd.read_csv(seq_df_cache, index_col=0)
            print("Using cached reads from %s" % seq_df_cache)
        else:
            # gbk_pat = 'SAP_Genomes_NCBIGBFF/refseq/bacteria/*/*.gbff*'
            # gbk_path = os.path.expanduser(gbk_pat)

            files = glob.glob(annotated_gbk_pat)
            print('Found %d files at %s' % (len(files), annotated_gbk_pat))
            seqs = []
            for fname in files:
                # Split Filename
                # pth = os.path.dirname(fname)
                fbase = os.path.basename(fname)
                base, ext = os.path.splitext(fbase)

                for i, seq_record in enumerate(
                        SeqIO.parse(wolfeutils.base.openFunc(fname),
                                    "genbank")):
                    cds_features = [feat for feat in seq_record.features
                                    if feat.type == 'CDS']
                    for j, feature in enumerate(cds_features):
                        nuc = feature.extract(seq_record).seq
                        description = feature.qualifiers['product'][0]
                        if 'protein_id' in feature.qualifiers:
                            seed_xref = feature.qualifiers['protein_id'][0]
                            pep_str = feature.qualifiers['translation'][0]
                            if not pep_str.endswith('*'):
                                pep_str += '*'
                            pep = Seq(pep_str)
                        elif 'db_xref' in feature.qualifiers:
                            seed_xref = feature.qualifiers['db_xref'][0]
                            # seed_xref = feature.qualifiers['locus_tag'][0]
                            pep = nuc.translate()
                        else:
                            seed_xref = '%s_%d_%d' % (base, i, j)

                        seqs.append(
                            dict(
                                nuc=str(nuc),
                                pep=str(pep),
                                description=description,
                                cog='-',
                                seed_xref=seed_xref,
                                fname=fbase, ))
                sys.stdout.write('.')
                sys.stdout.flush()

            # Concatenate Records
            seq_df = pd.DataFrame(seqs)
            seq_df.index = seq_df['seed_xref']
            seq_df.to_csv(seq_df_cache, compression='bz2')

        # import pdb; pdb.set_trace()
        ortho_desc = orthologs_cluster.copy()
        ortho_nuc = orthologs_cluster.copy()
        ortho_pep = orthologs_cluster.copy()
        for name, col in ortho_desc.iteritems():
            ortho_nuc.loc[:, name] = col.apply(
                lookup_desc, seq_df=seq_df, key='nuc')
            ortho_pep.loc[:, name] = col.apply(
                lookup_desc, seq_df=seq_df, key='pep')
            ortho_desc.loc[:, name] = col.apply(
                lookup_desc, seq_df=seq_df, key='description')
        accessory_desc = ortho_desc[accessory_index].T
        accessory_nuc = ortho_nuc[accessory_index].T
        accessory_pep = ortho_pep[accessory_index].T

        writer = pd.ExcelWriter(
            os.path.join(figdir, 'AccessoryPresenceAbsence_jaccard.xlsx'))

        ordered_desc = accessory_desc.iloc[:, reordered_col_indices]
        ordered_nuc = accessory_nuc.iloc[:, reordered_col_indices]
        ordered_pep = accessory_pep.iloc[:, reordered_col_indices]

        ordered_desc.to_excel(writer, 'Descriptions')
        ordered_nuc.to_excel(writer, 'Nuc')
        ordered_pep.to_excel(writer, 'Pep')

        # http://stackoverflow.com/questions/14627380/pandas-html-output-with-conditional-formatting

        table_html = accessory.iloc[
            reordered_row_indices, reordered_col_indices].to_html(
                formatters=[bool2html] * accessory.shape[1], escape=False)

        html_args = (color_light, color_light, color_dark, color_dark,
                     table_html)

        with open(
                os.path.join(figdir,
                             '6.AccessoryPresenceAbsence_jaccard.html'),
                'w') as f:
            f.write(html_template() % html_args)

        # # In[ ]:
        #
        # # accessory_desc_wconsensus = accessory_desc.copy()
        # # accessory_desc_wconsensus.loc['desc', :] = accessory_desc.apply(lambda row: row[row != '-'].value_counts().index[0], axis=0)
        # # # accessory_desc.iloc[:,0].value_counts().index[0]
        # # accessory_desc_wconsensus.tail()
        #
        # # # pd.concat([accessory_desc, accessory_desc.apply(lambda row: row[row != '-'].value_counts().index[0], axis=0)], axis=0).tail()
        #
        # # print pd.DataFrame(accessory_desc.iloc[reordered_row_indices, reordered_col_indices].apply(lambda row: row[row != '-'].value_counts().index[0], axis=0)).T.to_html()
        # # # accessory_desc.apply(lambda row: row[row != '-'].value_counts().index[0], axis=0)
        # # # accessory_desc_wconsensus
        #
        # if strains:
        #     cluster_by_group(strains, orthologs_presence)


def cluster_by_group(strains, orthologs_presence):
    '''Extra analysis using sequence metadata to look at group association'''

    # ## Cluster Identification by Group
    #
    # Interesting clusters are those that are differentially distributed amongst the phylogenetic groups - i.e. which clusters are found only in UTI strains? Only in cheese strains?
    #
    # To answer this, we can look at the overlap - for each cluster, figure out how likely it is (penetrance?) to be found in that group. We can then identify clusters that are promiscuous (found in all groups equally) or unbalanced - likely to be found in one instead of the others, or shared between two.
    #
    # First, parse the strains df to get a list of columns that each group belongs to:

    # In[ ]:

    group_cols = {grp: [s for s in strains.index
                        if s in strains[strains['group'] == grp].index]
                  for grp in [1, 2, 3]}
    # species_cols = {sp: [col for col in annotated_clusters.columns if col.startswith(sp)] for sp in ['EQ', 'EQSAP', 'SAP', 'SUC', 'XYL']}
    group_cols

    # Then, we want to create a long dataframe containing the percent penetrance of each cluster in each group. This is done by counting the presence / absence of each cluster within the strains of each group, and concatenating them together.

    # In[ ]:

    cluster_grp_counts_list = []
    # How many columns/fastas are present for each species? Needed for "all", "some", "none"
    n_cols = {grp: float(len(group_cols[grp])) for grp in group_cols.keys()}

    # For each species, sum the presence of the family, and calculate whether the family was in
    # all, some or none of the columns for that species.
    for grp in group_cols.keys():
        count = pd.DataFrame(
            orthologs_presence[group_cols[grp]].sum(axis=1), columns=['count'])
        count['clusterid'] = count.index
        count.reset_index()
        count['group'] = grp
        count['presence_pct'] = count['count'] / n_cols[grp]
        count['all'] = count['count'] == n_cols[grp]
        count['some'] = (count['count'] < n_cols[grp]) & (count['count'] > 0)
        count['none'] = count['count'] == 0

        cluster_grp_counts_list.append(count)

    # Put all the species together in a long table.
    cluster_grp_counts = pd.concat(cluster_grp_counts_list, ignore_index=True)
    sns.distplot(
        cluster_grp_counts[(cluster_grp_counts['presence_pct'] < 1) & (
            cluster_grp_counts['presence_pct'] > 0)]['presence_pct'], rug=True)
    plt.title(
        'Distribution of species presence within clusters\n(percent of species with a sequence with this cluster)')
    cluster_grp_counts.head()

    # In[ ]:
    """Also pivot this frame so we can see them side by side for visualzation.
    This is similar to the simpler method where we simply broke up the
    groups and counted."""
    cluster_grp_counts_pvt = cluster_grp_counts.pivot(
        index='clusterid', columns='group', values='presence_pct')
    cluster_grp_counts_pvt.head()

    # In[ ]:

    # Now that we have a list of counts, we can identify clusters for each group that fall within a certain percent.
    #
    # The most interesting percent is 1 - what clusters are present in *all* strains of one group and absent in *all* others?
    #
    # Alternatively, what clusters are absent in *all* strains of one group but present in others?

    # In[ ]:

    overlapset_counts = {}
    # pcts = linspace(0, 1, n_steps)
    pcts = [1]
    n_steps = float(len(pcts))
    print n_steps
    for pct in pcts:
        pct_counts_1 = cluster_grp_counts[(cluster_grp_counts[
            'group'] == 1) & (cluster_grp_counts['presence_pct'] == pct)]

        pct_counts_2 = cluster_grp_counts[(cluster_grp_counts[
            'group'] == 2) & (cluster_grp_counts['presence_pct'] == pct)]

        pct_counts_3 = cluster_grp_counts[(cluster_grp_counts[
            'group'] == 3) & (cluster_grp_counts['presence_pct'] == pct)]

        #     print 'EQ', set(pct_counts_EQ.index)
        #     print 'SAP', set(pct_counts_SAP.index)

        venn3([
            set(pct_counts_1['clusterid']), set(pct_counts_2['clusterid']),
            set(pct_counts_3['clusterid'])
        ], ('G1', 'G2', 'G3'))
        plt.title('Overlap for pct %.02f' % pct)
        # plt.show()
        overlapset_counts[pct] = compute_venn3_subsets(
            set(pct_counts_1['clusterid']), set(pct_counts_2['clusterid']),
            set(pct_counts_3['clusterid']))
        overlapsets = compute_subsets(
            set(pct_counts_1['clusterid']), set(pct_counts_2['clusterid']),
            set(pct_counts_3['clusterid']))
    overlaps = pd.DataFrame(overlapset_counts).T
    # subsets = (Abc, aBc, ABc, abC, AbC, aBC, ABC)
    overlap_columns = ['G1_g2_g3', 'g1_G2_g3', 'G1_G2_g3', 'g1_g2_G3',
                       'G1_g2_G3', 'g1_G2_G3', 'G1_G2_G3']
    overlaps.columns = overlap_columns
    # Reorder Columns
    overlaps = overlaps[['G1_g2_g3', 'g1_G2_g3', 'g1_g2_G3', 'G1_G2_g3',
                         'g1_G2_G3', 'G1_g2_G3', 'G1_G2_G3']]

    sns.heatmap(overlaps, vmax=100, annot=True, fmt='d')
    plt.clf()
    # plt.show()
    # with sns.color_palette(compute_venn3_colors(['r','g','b']), desat=.8):
    # ccv = ColorConverter()
    # colors = [ccv.to_rgba(c, .4) for c in compute_venn3_colors(['r','g','b'])]
    overlaps.plot(kind='bar', stacked=True, cmap='Set2')
    overlaps

    # In[ ]:

    #     pct_counts_1 = cluster_grp_counts[(cluster_grp_counts['group'] == 1) &
    #                                       (cluster_grp_counts['presence_pct'] >= pct) &
    #                                       (cluster_grp_counts['presence_pct'] < pct + 1/n_steps)]

    #     pct_counts_2 = cluster_grp_counts[(cluster_grp_counts['group'] == 2) &
    #                                        (cluster_grp_counts['presence_pct'] >= pct) &
    #                                        (cluster_grp_counts['presence_pct'] < pct + 1/n_steps)]

    #     pct_counts_3 = cluster_grp_counts[(cluster_grp_counts['group'] == 3) &
    #                                        (cluster_grp_counts['presence_pct'] >= pct) &
    #                                        (cluster_grp_counts['presence_pct'] < pct + 1/n_steps)]

    # In[ ]:

    ordered_strains = list(flatten([v for v in group_cols.itervalues()]))

    # overlapsets[1]
    # cluster_grp_counts_pvt.loc[overlapsets[5]]

    high = 1
    low = 1 - high

    set_indices = [
        # Abc
        cluster_grp_counts_pvt[(cluster_grp_counts_pvt[1] >= high) & (
            cluster_grp_counts_pvt[2] <= low) & (cluster_grp_counts_pvt[3] <=
                                                 low)].index,

        # aBc
        cluster_grp_counts_pvt[(cluster_grp_counts_pvt[1] <= low) & (
            cluster_grp_counts_pvt[2] >= high) & (cluster_grp_counts_pvt[3] <=
                                                  low)].index,

        # abC
        cluster_grp_counts_pvt[(cluster_grp_counts_pvt[1] <= low) & (
            cluster_grp_counts_pvt[2] <= low) & (cluster_grp_counts_pvt[3] >=
                                                 high)].index,

        # ABc
        cluster_grp_counts_pvt[(cluster_grp_counts_pvt[1] >= high) & (
            cluster_grp_counts_pvt[2] >= high) & (cluster_grp_counts_pvt[3] <=
                                                  low)].index,

        # aBC
        cluster_grp_counts_pvt[(cluster_grp_counts_pvt[1] <= low) & (
            cluster_grp_counts_pvt[2] >= high) & (cluster_grp_counts_pvt[3] >=
                                                  high)].index,
        # AbC
        cluster_grp_counts_pvt[(cluster_grp_counts_pvt[1] >= high) & (
            cluster_grp_counts_pvt[2] <= low) & (cluster_grp_counts_pvt[3] >=
                                                 high)].index,

        #     # ABC - This is just Core
        #     cluster_grp_counts_pvt[(cluster_grp_counts_pvt[1] == 1) &
        #                            (cluster_grp_counts_pvt[2] == 1) &
        #                            (cluster_grp_counts_pvt[3] == 1)].index,
    ]

    # ortho_desc.loc[Abc+ABc, ordered_strains]
    penetrance_sets = ortho_desc.loc[list(
        flatten([s.tolist() for s in set_indices])), ordered_strains].copy()

    set_labels = ('Abc', 'aBc', 'abC', 'ABc', 'aBC', 'AbC')  # , 'ABC')
    for (i, s), label in zip(enumerate(set_indices), set_labels):
        penetrance_sets.loc[set_indices[i], 'SetID'] = label

    print penetrance_sets['SetID'].value_counts()
    penetrance_sets

    hm = sns.heatmap(
        (penetrance_sets.loc[:, ordered_strains] != '-').T,
        xticklabels=False,
        cmap=cmap)
    penetrance_sets.loc[:, ordered_strains].T.to_csv(
        os.path.join(figdir, 'AccessoryPenetrance_75.csv'))
    plt.savefig(os.path.join(figdir, 'AccessoryPenetrance_75.png'))
    plt.clf()
    penetrance_sets.loc[:, ordered_strains].T

    # ### Alternative Manual Method w/o dict comprehensions

    # In[ ]:

    # group1 = accessory.loc['BWH2':'9325']
    # group2 = accessory.loc['396A':'BC4']
    # group3 = accessory.loc['3751':'3201']
    g1_idx = strains[strains['group'] == 1]['strain']
    group1 = accessory.loc[g1_idx]

    g2_idx = strains[strains['group'] == 2]['strain']
    group2 = accessory.loc[g2_idx]

    g3_idx = strains[strains['group'] == 3]['strain']
    group3 = accessory.loc[g3_idx]

    group_pcts = pd.DataFrame(
        [g.sum() / g.shape[0] for g in [group1, group2, group3]],
        index=['g1', 'g2', 'g3']).T

    group_pcts.plot(figsize=(20, 5))

    group_pcts.head()

    # In[ ]:

    # Group Percents
    only_g1 = group_pcts[(group_pcts['g1'] == 1) & (group_pcts['g2'] == 0) & (
        group_pcts['g3'] == 0)]
    accessory_desc.loc[g1_idx, only_g1.index]

    # In[ ]:

    only_g2 = group_pcts[(group_pcts['g1'] == 0) & (group_pcts['g2'] == 1) & (
        group_pcts['g3'] == 0)]
    accessory_desc.loc[g2_idx, only_g2.index]

    # In[ ]:

    only_g3 = group_pcts[(group_pcts['g1'] == 0) & (group_pcts['g2'] == 0) & (
        group_pcts['g3'] == 1)]
    accessory_desc.loc[g3_idx, only_g3.index]

    # In[ ]:

    accessory_desc[only_g1.index.tolist() + only_g2.index.tolist() +
                   only_g3.index.tolist()].to_csv(
                       os.path.join(figdir, 'GroupSpecificGenes.csv'))

    # In[ ]:

    # In[ ]:

    cheese_idx = strains[strains['source'] == 'cheese']['strain']
    cheese = accessory.loc[cheese_idx]

    uti_idx = strains[strains['source'] == 'UTI']['strain']
    uti = accessory.loc[uti_idx]

    mammal_idx = strains[strains['source'] == 'mammal']['strain']
    mammal = accessory.loc[mammal_idx]

    group_pcts = pd.DataFrame(
        [g.sum() / g.shape[0] for g in [cheese, uti, mammal]],
        index=['cheese', 'uti', 'mammal']).T

    group_pcts.plot(figsize=(20, 5))

    # In[ ]:

    # Group Percents
    only_cheese = group_pcts[(group_pcts['cheese'] == 1) & (group_pcts[
        'uti'] == 0) & (group_pcts['mammal'] == 0)]
    accessory_desc.loc[cheese_idx, only_cheese.index]

    # In[ ]:

    # Group Percents
    only_uti = group_pcts[(group_pcts['cheese'] == 0) & (group_pcts[
        'uti'] == 1) & (group_pcts['mammal'] == 0)]
    accessory_desc.loc[uti_idx, only_uti.index]

    # In[ ]:

    # Group Percents
    only_mammal = group_pcts[(group_pcts['cheese'] == 0) & (group_pcts[
        'uti'] == 0) & (group_pcts['mammal'] == 1)]
    accessory_desc.loc[mammal_idx, only_mammal.index]


def pan_size(x, A, B, C):
    return A * x**B + C


def core_size(x, A, B, C):
    return A * np.exp(B * x) + C


def discrete_cmap(name, colors):
    '''Take a list of rgb or hex colors and build a cmap. Only takes 2 colors now.
       http://matplotlib.org/1.4.1/api/colors_api.html'''
    if colors[0].startswith('#'):  # Just call this a hex value
        colors = [mpl.colors.hex2color(c) for c in colors]

    color1, color2 = colors  # Assume there are only two colors!

    cdict = dict(
        red=[(0, 0, color1[0]), (1, color2[0], 1)],
        green=[(0, 0, color1[1]), (1, color2[1], 1)],
        blue=[(0, 0, color1[2]), (1, color2[2], 1)])
    cmap = mpl.colors.LinearSegmentedColormap(name, cdict)

    return cmap


def get_linkages(df):
    sys.setrecursionlimit(10000)

    df.dropna(inplace=True)
    row_distance = distance.pdist(df, metric='jaccard')
    row_linkage = hierarchy.linkage(row_distance, method='average')
    row_dendrogram = hierarchy.dendrogram(
        row_linkage, no_plot=True, color_threshold=-np.inf)
    reordered_row_indices = row_dendrogram['leaves']

    col_distance = distance.pdist(df.T, metric='jaccard')
    col_linkage = hierarchy.linkage(
        col_distance, metric='jaccard', method='average')
    col_dendrogram = hierarchy.dendrogram(
        col_linkage, no_plot=True, color_threshold=-np.inf, no_labels=True)
    reordered_col_indices = col_dendrogram['leaves']

    return (row_linkage, reordered_row_indices, col_linkage,
            reordered_col_indices)


def bool2html(v):
    if v:
        return '<div class="present">+</div>'
    else:
        return '<div class="absent">-</div>'


def lookup_desc(label, seq_df, key='description'):
    '''Look up a description from a reference df.

    Inputs:
    * s : ID item to look up
    * seq_df : Reference data frame of which has a "description" column
    '''
    desc = []
    if label == '-':
        desc.append('-')
    else:
        try:
            for seq_id in label.split(','):
                desc.append(seq_df.loc[seq_id, key])
        except KeyError:
            # import pdb; pdb.set_trace()
            desc.append('????????')
    return ','.join(desc)


def html_template():
    return """<!DOCTYPE html>
        <html>
        <head>
        <style>
        .present {background-color:%s; color:%s}
        .absent {background-color:%s; color:%s}
        .main {padding: 15px;}
        table, th, td {border: thin solid gray; border-spacing: 0; border-collapse: collapse}
        thead th {padding: .5em;}
        tr th {padding-left: .5em; padding-right: .5em;}
        #legend {margin-bottom: .5em;}
        #legend tr td {color: black; padding: .5em;}
        </style>

        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">

        <!-- Optional theme -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">

        <!-- Latest compiled and minified JavaScript -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
        </head>
        <body>
        <div class="main">
        <h1>Accessory Genome Presence / Absence by Protein Cluster Family</h1>
        <table id="legend">
          <tr>
            <td class="present">Present</td>
            <td class="absent">Absent</td>
          </tr>
        </trable>
        %s
        </div>
        </body>
        </html>
        """


def flatten(lists):
    chain = itertools.chain(*lists)
    return list(chain)


def getNewick(node, newick, parentdist, leaf_names):
    '''http://stackoverflow.com/a/31878514'''
    if node.is_leaf():
        return "%s:%.2f%s" % (leaf_names[node.id], parentdist - node.dist,
                              newick)
    else:
        if len(newick) > 0:
            newick = "):%.2f%s" % (parentdist - node.dist, newick)
        else:
            newick = ");"
        newick = getNewick(node.get_left(), newick, node.dist, leaf_names)
        newick = getNewick(node.get_right(), ",%s" % (newick), node.dist,
                           leaf_names)
        newick = "(%s" % (newick)
        return newick


def compute_subsets(a, b, c):
    '''
    This method is taken from matplotlib-venn3, excpet that instead of returning lengths
    of the subsets it returns the subsetes themselves.

    Given three set objects, computes the sizes of (a & ~b & ~c, ~a & b & ~c, a & b & ~c, ....),
    as needed by the subsets parameter of venn3 and venn3_circles.
    Returns the result as a tuple.

    subsets = (Abc, aBc, ABc, abC, AbC, aBC, ABC)

    >>> compute_venn3_subsets(set([1,2,3]), set([2,3,4]), set([3,4,5,6]))
    (1, 0, 1, 2, 0, 1, 1)
    >>> compute_venn3_subsets(set([]), set([]), set([]))
    (0, 0, 0, 0, 0, 0, 0)
    >>> compute_venn3_subsets(set([1]), set([]), set([]))
    (1, 0, 0, 0, 0, 0, 0)
    >>> compute_venn3_subsets(set([]), set([1]), set([]))
    (0, 1, 0, 0, 0, 0, 0)
    >>> compute_venn3_subsets(set([]), set([]), set([1]))
    (0, 0, 0, 1, 0, 0, 0)
    >>> compute_venn3_subsets(set([1]), set([1]), set([1]))
    (0, 0, 0, 0, 0, 0, 1)
    >>> compute_venn3_subsets(set([1,3,5,7]), set([2,3,6,7]), set([4,5,6,7]))
    (1, 1, 1, 1, 1, 1, 1)
    '''
    return ((a - (b.union(c))), (b - (a.union(c))), (a.intersection(b) - c),
            (c - (a.union(b))), (a.intersection(c) - b),
            (b.intersection(c) - a), (a.intersection(b).intersection(c)))


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('pgap_dir', help='Path to PGAP output directory')
    parser.add_argument(
        '--annotated-genbank-pat', default=None, help='Pattern to match genbank files')
    return parser.parse_args(args)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    print(dir(args))
    pgap_dir = os.path.abspath(args.pgap_dir)

    basicAnalysis(pgap_dir, args.genbank_pat)
