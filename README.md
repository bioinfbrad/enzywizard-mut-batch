[![DOI](https://zenodo.org/badge/1219039494.svg)](https://doi.org/10.5281/zenodo.19709927)
# Command: enzywizard-mut-batch

EnzyWizard-Mut-Batch is a command-line tool for running paired EnzyWizard
analysis workflows for a wild-type protein and its mutant.
It takes cleaned wild-type and mutant protein structures, matched wild-type and
mutant MSA files, and a cleaned amino acid substitution as input. It performs the full
EnzyWizard batch workflow on both sides, including amino acid property analysis,
hydrophobic cluster detection, energy evaluation, flexibility analysis, disorder
prediction, conservation analysis, protein embedding generation, pocket
detection, optional substrate feature generation, optional molecular docking,
interaction network calculation, and final mutation-aware graph integration.
If substrate names or SMILES strings are provided, substrate structures are
generated and used for docking and protein-substrate interaction analysis on both sides.
If no substrate input is provided, the program generates paired protein-only integrated 
graphs based on protein-level features and intra-protein interactions.
The final output is a paired integrated graph dataset comparing the
wild-type and mutant proteins. It can be used for graph-based analysis,
machine learning, and mutation effect studies.


# example usage:

Example command:

enzywizard-mut-batch -w examples/input/cleaned_1ZG4_WT.cif -m examples/input/cleaned_1ZG6_S70G.cif -wm examples/input/jhmm_1ZG4_WT.sto -mm examples/input/jhmm_1ZG6_S70G.sto -a S45G -s glucose,fructose -wo examples/wt_output/ -mo examples/mut_output/


# input parameters:

-w, --wt_cleaned_input_path
Required.
Path to the input wild-type cleaned protein structure file in CIF or PDB format.

The file must:
- already be cleaned
- contain a valid single protein chain
- contain hydrogen atoms
- match the sequence used to generate the wild-type input MSA

-m, --mut_cleaned_input_path
Required.
Path to the input mutant cleaned protein structure file in CIF or PDB format.

-wm, --wt_input_msa
Required.
Path to the input wild-type MSA file.

Supported MSA formats include:
- Stockholm (.sto)
- aligned FASTA
- A3M

The MSA must be generated using the wild-type cleaned protein FASTA sequence.

-mm, --mut_input_msa
Required.
Path to the input mutant MSA file.

-a, --cleaned_amino_acid_substitution
Required.
Input cleaned amino acid substitution in mutation format, such as A123V.

-s, --substrate_names
Optional.
Substrate names or SMILES strings.

Multiple substrates should be separated by ','.

If provided, the following additional workflows will be executed on both
wild-type and mutant sides:
- substrate feature generation
- substrate 3D structure generation
- molecular docking
- protein-substrate interaction calculation
- strict mutation-aware graph integration

If substrate generation or docking fails on either side, these additional workflows
are skipped and the program continues with paired protein-only analysis.

If not provided, substrate, docking, and protein-substrate interaction steps
will be skipped on both sides.

-wo, --wt_output_dir
Required.
Directory to save wild-type-side outputs.

-mo, --mut_output_dir
Required.
Directory to save mutant-side outputs.

The wild-type and mutant output directories must be different.

--save_extra_outputs
Optional.
Enable keeping intermediate and side output files.

By default, this option is disabled, and only the final mutation-integrated JSON
outputs and log.txt are kept.

--hydrocluster_cutoff
Optional.
Minimum contact area cutoff for hydrophobic cluster residue-residue connection.
Default: 10.0.

--no_minimize_energy
Optional.
Disable energy minimization before energy evaluation.
By default, energy minimization is enabled.

--energy_minimization_iteration
Optional.
Maximum number of iterations for energy minimization.
Default: 1000.

--flexibility_method
Optional.
Normal mode method for RMSF calculation.
Choices:
- ANM
- GNM
Default: ANM.

--flexibility_cutoff
Optional.
Distance cutoff used to determine residue connections in ProDy.
Default: 15.0.

--flexibility_n_modes
Optional.
Number of low-frequency normal modes used for RMSF calculation.
Default: 20.

--disorder_window_size
Optional.
Sliding window size for FoldIndex-like disorder score calculation.
Default: 11.

--disorder_min_region_length
Optional.
Minimum number of consecutive residues required to define a disordered region.
Default: 5.

--embedding_model_name
Optional.
ESM2 model used for residue embedding generation.

Choices:
- esm2_t6_8M_UR50D
- esm2_t12_35M_UR50D
- esm2_t30_150M_UR50D

Default: esm2_t6_8M_UR50D.

--pocket_min_rad
Optional.
Minimum probe radius used by PyVOL for cavity detection.
Default: 1.8.

--pocket_max_rad
Optional.
Maximum probe radius used by PyVOL for cavity detection.
Default: 6.2.

--pocket_min_volume
Optional.
Minimum pocket volume threshold.
Default: 50.

--substrate_max_synonyms
Optional.
Maximum number of substrate synonyms retried when fetching SMILES from a
substrate name.
Default: 20.

--substrate_fp_radius
Optional.
Radius used for Morgan fingerprint generation.
Default: 2.

--substrate_n_bits
Optional.
Bit size of the Morgan fingerprint vector.
Default: 512.

--substrate_num_confs
Optional.
Maximum number of 3D conformers generated for each substrate.
Default: 5.

--substrate_prune_rms
Optional.
RMS threshold used to prune highly similar conformers during 3D conformer
generation.
Default: 0.5.

--dock_max_attempt_num
Optional.
Maximum number of docking attempts for each side.
Default: 20.

--dock_no_early_stop
Optional.
Disable stopping immediately after the first successful docking result.

By default, early stopping is enabled.

--dock_exhaustiveness
Optional.
Exhaustiveness of AutoDock Vina search.
Default: 16.

--dock_cpu
Optional.
Number of CPUs used by AutoDock Vina.
Default: 0.

--dock_catalytic_residue
Optional.
Cleaned protein residue index used as the docking box center.

Example:
  121

This parameter is an integer residue index from the cleaned single-chain protein
structure. The CA atom coordinate of this residue is used as the docking box
center. When this parameter is provided, --dock_box_size is required.
This parameter cannot be used together with --dock_catalytic_site_coord.
When this parameter is provided, the docking step does not use PyVOL pocket
detection or the global docking box fallback to build Vina docking boxes.

--dock_catalytic_site_coord
Optional.
Catalytic site center coordinate separated by ','.

Example:
  12.5,8.0,-3.2

When this parameter is provided, the same coordinate is used as the docking box
center on both wild-type and mutant sides, and --dock_box_size is required.
This parameter cannot be used together with --dock_catalytic_residue.
When this parameter is provided, the docking step does not use PyVOL pocket
detection or the global docking box fallback to build Vina docking boxes.

--dock_box_size
Optional.
Docking box size separated by ','.

Example:
  20,20,20

This parameter is required when --dock_catalytic_residue or
--dock_catalytic_site_coord is provided. All three values must be positive
numbers.

--hbond_bonded_h_min_distance
Optional.
Minimum bonded heavy atom-hydrogen distance used for hydrogen bond donor
detection.
Default: 0.8.

--hbond_bonded_h_max_distance
Optional.
Maximum bonded heavy atom-hydrogen distance used for hydrogen bond donor
detection.
Default: 1.3.

--hbond_da_max_distance
Optional.
Maximum donor-acceptor distance cutoff for hydrogen bond detection.
Default: 3.9.

--hbond_ha_max_distance
Optional.
Maximum hydrogen-acceptor distance cutoff for hydrogen bond detection.
Default: 2.5.

--hbond_angle
Optional.
Minimum donor-hydrogen-acceptor angle cutoff for hydrogen bond detection.
Default: 90.0.

--ionic_distance_cutoff
Optional.
Maximum distance cutoff for ionic bond detection.
Default: 4.0.

--vdw_mu
Optional.
Mu parameter used in van der Waals interaction detection.
Default: 0.01.

--ppstack_center_distance_cutoff
Optional.
Maximum ring-center distance cutoff for pi-pi stacking detection.
Default: 6.5.

--pication_distance_cutoff
Optional.
Maximum ring-cation distance cutoff for pi-cation interaction detection.
Default: 5.0.

--pication_angle_cutoff
Optional.
Maximum angle cutoff for pi-cation interaction detection.
Default: 45.0.

--ssbond_max_distance
Optional.
Maximum sulfur-sulfur distance cutoff for disulfide bond detection.
Default: 2.5.


# output content:

The program outputs the following files into the output directories:

1. A shared mut-integrate JSON report
   - mut_integrate_report_{wt_protein_name}_to_{mut_protein_name}.json

   This file is saved into both wt_output_dir and mut_output_dir.

   The report follows the JSON schema file:
   - resources/enzywizard_mut_integrate_report_schema.json

   The JSON report contains the following fields:

   - "report_type"
     - Data type: string
     - Expected value: "enzywizard_mut_integrate"
     - Description: The field 'report_type' indicates the type ('type': http://purl.org/dc/terms/type) of report ('report': http://purl.obolibrary.org/obo/IAO_0000088) generated by the EnzyWizard-Mut-Integrate software ('software': https://schema.org/SoftwareApplication).

   - "cleaned_amino_acid_substitution"
     - Data type: string
     - Description: The field 'cleaned_amino_acid_substitution' indicates the amino acid substitution ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) in the cleaned protein structure ('protein structure': http://edamontology.org/data_1537), using one-letter codes ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) to represent.

   - "overall_statistics"
     - Data type: object
     - Description: The field 'overall_statistics' indicates the overall summary statistics ('statistics': http://purl.obolibrary.org/obo/STATO_0000039) comparing the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537) and the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537), integrated from EnzyWizard reports ('report': http://purl.obolibrary.org/obo/IAO_0000088).

     The "overall_statistics" object may contain:

     - "wild_type_residue_name_count"
       - Data type: array
       - Description: The field 'wild_type_residue_name_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of residue names ('residue': http://purl.obolibrary.org/obo/GENO_0000782; 'name': http://xmlns.com/foaf/0.1/name) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537), represented in the order of one-letter codes ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html).

     - "mutant_residue_name_count"
       - Data type: array
       - Description: The field 'mutant_residue_name_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of residue names ('residue': http://purl.obolibrary.org/obo/GENO_0000782; 'name': http://xmlns.com/foaf/0.1/name) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537), represented in the order of one-letter codes ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html).

     - "difference_residue_name_count"
       - Data type: array
       - Description: The field 'difference_residue_name_count' indicates the difference between the mutant count and the wild-type count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of residue names ('residue': http://purl.obolibrary.org/obo/GENO_0000782; 'name': http://xmlns.com/foaf/0.1/name), represented in the order of one-letter codes ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html).

     - "wild_type_residue_chemical_classification_count"
       - Data type: array
       - Description: The field 'wild_type_residue_chemical_classification_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of residue chemical classifications ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_chemical_classification_count"
       - Data type: array
       - Description: The field 'mutant_residue_chemical_classification_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of residue chemical classifications ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_chemical_classification_count"
       - Data type: array
       - Description: The field 'difference_residue_chemical_classification_count' indicates the difference between the mutant count and the wild-type count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of residue chemical classifications ('classification': http://purl.obolibrary.org/obo/NCIT_C25161).

     - "wild_type_residue_secondary_structure_count"
       - Data type: array
       - Description: The field 'wild_type_residue_secondary_structure_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of residue secondary structures ('secondary structure': http://edamontology.org/operation_1847) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537), represented using DSSP secondary-structure codes ('DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

     - "mutant_residue_secondary_structure_count"
       - Data type: array
       - Description: The field 'mutant_residue_secondary_structure_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of residue secondary structures ('secondary structure': http://edamontology.org/operation_1847) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537), represented using DSSP secondary-structure codes ('DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

     - "difference_residue_secondary_structure_count"
       - Data type: array
       - Description: The field 'difference_residue_secondary_structure_count' indicates the difference between the mutant count and the wild-type count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of residue secondary structures ('secondary structure': http://edamontology.org/operation_1847), represented using DSSP secondary-structure codes ('DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

     - "wild_type_hydrophobic_cluster_count"
       - Data type: integer
       - Description: The field 'wild_type_hydrophobic_cluster_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_hydrophobic_cluster_count"
       - Data type: integer
       - Description: The field 'mutant_hydrophobic_cluster_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_hydrophobic_cluster_count"
       - Data type: integer
       - Description: The field 'difference_hydrophobic_cluster_count' indicates the difference between the mutant count and the wild-type count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/).

     - "wild_type_max_hydrophobic_cluster_area"
       - Data type: number
       - Description: The field 'wild_type_max_hydrophobic_cluster_area' indicates the maximum area ('maximum': http://purl.obolibrary.org/obo/STATO_0000150; 'area': http://purl.obolibrary.org/obo/PATO_0001323) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_max_hydrophobic_cluster_area"
       - Data type: number
       - Description: The field 'mutant_max_hydrophobic_cluster_area' indicates the maximum area ('maximum': http://purl.obolibrary.org/obo/STATO_0000150; 'area': http://purl.obolibrary.org/obo/PATO_0001323) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_max_hydrophobic_cluster_area"
       - Data type: number
       - Description: The field 'difference_max_hydrophobic_cluster_area' indicates the difference between the mutant maximum area and the wild-type maximum area ('maximum': http://purl.obolibrary.org/obo/STATO_0000150; 'area': http://purl.obolibrary.org/obo/PATO_0001323) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/).

     - "wild_type_total_hydrophobic_cluster_area"
       - Data type: number
       - Description: The field 'wild_type_total_hydrophobic_cluster_area' indicates the total area ('area': http://purl.obolibrary.org/obo/PATO_0001323) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_total_hydrophobic_cluster_area"
       - Data type: number
       - Description: The field 'mutant_total_hydrophobic_cluster_area' indicates the total area ('area': http://purl.obolibrary.org/obo/PATO_0001323) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_total_hydrophobic_cluster_area"
       - Data type: number
       - Description: The field 'difference_total_hydrophobic_cluster_area' indicates the difference between the mutant total area and the wild-type total area ('area': http://purl.obolibrary.org/obo/PATO_0001323) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/).

     - "wild_type_disordered_region_count"
       - Data type: integer
       - Description: The field 'wild_type_disordered_region_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_disordered_region_count"
       - Data type: integer
       - Description: The field 'mutant_disordered_region_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_disordered_region_count"
       - Data type: integer
       - Description: The field 'difference_disordered_region_count' indicates the difference between the mutant value and the wild-type value for the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology).

     - "wild_type_max_disordered_region_length"
       - Data type: integer
       - Description: The field 'wild_type_max_disordered_region_length' indicates the maximum sequence length ('maximum': http://purl.obolibrary.org/obo/STATO_0000150; 'sequence length': http://edamontology.org/data_1249) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_max_disordered_region_length"
       - Data type: integer
       - Description: The field 'mutant_max_disordered_region_length' indicates the maximum sequence length ('maximum': http://purl.obolibrary.org/obo/STATO_0000150; 'sequence length': http://edamontology.org/data_1249) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_max_disordered_region_length"
       - Data type: integer
       - Description: The field 'difference_max_disordered_region_length' indicates the difference between the mutant value and the wild-type value for the maximum sequence length ('maximum': http://purl.obolibrary.org/obo/STATO_0000150; 'sequence length': http://edamontology.org/data_1249) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology).

     - "wild_type_total_disordered_region_length"
       - Data type: integer
       - Description: The field 'wild_type_total_disordered_region_length' indicates the total sequence length ('sequence length': http://edamontology.org/data_1249) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_total_disordered_region_length"
       - Data type: integer
       - Description: The field 'mutant_total_disordered_region_length' indicates the total sequence length ('sequence length': http://edamontology.org/data_1249) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_total_disordered_region_length"
       - Data type: integer
       - Description: The field 'difference_total_disordered_region_length' indicates the difference between the mutant value and the wild-type value for the total sequence length ('sequence length': http://edamontology.org/data_1249) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology).

     - "wild_type_binding_pocket_count"
       - Data type: integer
       - Description: The field 'wild_type_binding_pocket_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/pocket_specification.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_binding_pocket_count"
       - Data type: integer
       - Description: The field 'mutant_binding_pocket_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/pocket_specification.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_binding_pocket_count"
       - Data type: integer
       - Description: The field 'difference_binding_pocket_count' indicates the difference between the mutant value and the wild-type value for the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/pocket_specification.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL).

     - "wild_type_max_binding_pocket_volume"
       - Data type: number
       - Description: The field 'wild_type_max_binding_pocket_volume' indicates the maximum volume ('maximum': http://purl.obolibrary.org/obo/STATO_0000150; 'volume': http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_max_binding_pocket_volume"
       - Data type: number
       - Description: The field 'mutant_max_binding_pocket_volume' indicates the maximum volume ('maximum': http://purl.obolibrary.org/obo/STATO_0000150; 'volume': http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_max_binding_pocket_volume"
       - Data type: number
       - Description: The field 'difference_max_binding_pocket_volume' indicates the difference between the mutant value and the wild-type value for the maximum volume ('maximum': http://purl.obolibrary.org/obo/STATO_0000150; 'volume': http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL).

     - "wild_type_total_binding_pocket_volume"
       - Data type: number
       - Description: The field 'wild_type_total_binding_pocket_volume' indicates the total volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_total_binding_pocket_volume"
       - Data type: number
       - Description: The field 'mutant_total_binding_pocket_volume' indicates the total volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_total_binding_pocket_volume"
       - Data type: number
       - Description: The field 'difference_total_binding_pocket_volume' indicates the difference between the mutant value and the wild-type value for the total volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL).

     - "wild_type_total_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_total_potential_energy' indicates the total potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) calculated from the protein structure ('protein structure': http://edamontology.org/data_1537) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_total_potential_energy"
       - Data type: number
       - Description: The field 'mutant_total_potential_energy' indicates the total potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) calculated from the protein structure ('protein structure': http://edamontology.org/data_1537) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_total_potential_energy"
       - Data type: number
       - Description: The field 'difference_total_potential_energy' indicates the difference between the mutant value and the wild-type value for the total potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) calculated from the protein structure ('protein structure': http://edamontology.org/data_1537).

     - "wild_type_harmonic_bond_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_harmonic_bond_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the harmonic bond force term ('harmonic bond force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#harmonicbondforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_harmonic_bond_potential_energy"
       - Data type: number
       - Description: The field 'mutant_harmonic_bond_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the harmonic bond force term ('harmonic bond force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#harmonicbondforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_harmonic_bond_potential_energy"
       - Data type: number
       - Description: The field 'difference_harmonic_bond_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the harmonic bond force term ('harmonic bond force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#harmonicbondforce).

     - "wild_type_harmonic_angle_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_harmonic_angle_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the harmonic angle force term ('harmonic angle force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#harmonicangleforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_harmonic_angle_potential_energy"
       - Data type: number
       - Description: The field 'mutant_harmonic_angle_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the harmonic angle force term ('harmonic angle force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#harmonicangleforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_harmonic_angle_potential_energy"
       - Data type: number
       - Description: The field 'difference_harmonic_angle_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the harmonic angle force term ('harmonic angle force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#harmonicangleforce).

     - "wild_type_custom_bond_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_custom_bond_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom bond force term ('custom bond force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#custombondforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_custom_bond_potential_energy"
       - Data type: number
       - Description: The field 'mutant_custom_bond_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom bond force term ('custom bond force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#custombondforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_custom_bond_potential_energy"
       - Data type: number
       - Description: The field 'difference_custom_bond_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom bond force term ('custom bond force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#custombondforce).

     - "wild_type_custom_torsion_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_custom_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom torsion force term ('custom torsion force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#customtorsionforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_custom_torsion_potential_energy"
       - Data type: number
       - Description: The field 'mutant_custom_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom torsion force term ('custom torsion force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#customtorsionforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_custom_torsion_potential_energy"
       - Data type: number
       - Description: The field 'difference_custom_torsion_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom torsion force term ('custom torsion force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#customtorsionforce).

     - "wild_type_custom_nonbonded_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_custom_nonbonded_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom nonbonded force term ('custom nonbonded force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#customnonbondedforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_custom_nonbonded_potential_energy"
       - Data type: number
       - Description: The field 'mutant_custom_nonbonded_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom nonbonded force term ('custom nonbonded force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#customnonbondedforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_custom_nonbonded_potential_energy"
       - Data type: number
       - Description: The field 'difference_custom_nonbonded_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom nonbonded force term ('custom nonbonded force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#customnonbondedforce).

     - "wild_type_nonbonded_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_nonbonded_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the nonbonded force term ('nonbonded force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#nonbondedforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_nonbonded_potential_energy"
       - Data type: number
       - Description: The field 'mutant_nonbonded_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the nonbonded force term ('nonbonded force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#nonbondedforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_nonbonded_potential_energy"
       - Data type: number
       - Description: The field 'difference_nonbonded_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the nonbonded force term ('nonbonded force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#nonbondedforce).

     - "wild_type_periodic_torsion_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_periodic_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the periodic torsion force term ('periodic torsion force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#periodictorsionforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_periodic_torsion_potential_energy"
       - Data type: number
       - Description: The field 'mutant_periodic_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the periodic torsion force term ('periodic torsion force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#periodictorsionforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_periodic_torsion_potential_energy"
       - Data type: number
       - Description: The field 'difference_periodic_torsion_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the periodic torsion force term ('periodic torsion force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#periodictorsionforce).

     - "wild_type_cmap_torsion_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_cmap_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the CMAP torsion force term ('CMAP torsion force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#cmaptorsionforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_cmap_torsion_potential_energy"
       - Data type: number
       - Description: The field 'mutant_cmap_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the CMAP torsion force term ('CMAP torsion force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#cmaptorsionforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_cmap_torsion_potential_energy"
       - Data type: number
       - Description: The field 'difference_cmap_torsion_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the CMAP torsion force term ('CMAP torsion force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#cmaptorsionforce).

     - "wild_type_enzyme_substrate_binding_affinity"
       - Data type: number
       - Description: The field 'wild_type_enzyme_substrate_binding_affinity' indicates the predicted binding affinity ('binding affinity': https://vina.scripps.edu/manual/#output) calculated by AutoDock Vina software ('AutoDock Vina': https://bio.tools/autodock_vina) from docking ('docking': https://goldbook.iupac.org/terms/view/11437) of the wild-type enzyme-substrate complex ('enzyme': https://purl.dsmz.de/schema/Enzyme; 'substrate': https://purl.dsmz.de/schema/Substrate; 'complex': https://goldbook.iupac.org/terms/view/C01203).

     - "mutant_enzyme_substrate_binding_affinity"
       - Data type: number
       - Description: The field 'mutant_enzyme_substrate_binding_affinity' indicates the predicted binding affinity ('binding affinity': https://vina.scripps.edu/manual/#output) calculated by AutoDock Vina software ('AutoDock Vina': https://bio.tools/autodock_vina) from docking ('docking': https://goldbook.iupac.org/terms/view/11437) of the mutant enzyme-substrate complex ('enzyme': https://purl.dsmz.de/schema/Enzyme; 'substrate': https://purl.dsmz.de/schema/Substrate; 'complex': https://goldbook.iupac.org/terms/view/C01203).

     - "difference_enzyme_substrate_binding_affinity"
       - Data type: number
       - Description: The field 'difference_enzyme_substrate_binding_affinity' indicates the difference between the mutant predicted binding affinity and the wild-type predicted binding affinity ('binding affinity': https://vina.scripps.edu/manual/#output) calculated by AutoDock Vina software ('AutoDock Vina': https://bio.tools/autodock_vina) from docking ('docking': https://goldbook.iupac.org/terms/view/11437) of enzyme-substrate complexes ('enzyme': https://purl.dsmz.de/schema/Enzyme; 'substrate': https://purl.dsmz.de/schema/Substrate; 'complex': https://goldbook.iupac.org/terms/view/C01203).

     - "wild_type_hydrogen_bond_count"
       - Data type: integer
       - Description: The field 'wild_type_hydrogen_bond_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of hydrogen bonds ('hydrogen bond': https://goldbook.iupac.org/terms/view/H02899) in the wild-type integrated graph.

     - "mutant_hydrogen_bond_count"
       - Data type: integer
       - Description: The field 'mutant_hydrogen_bond_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of hydrogen bonds ('hydrogen bond': https://goldbook.iupac.org/terms/view/H02899) in the mutant integrated graph.

     - "difference_hydrogen_bond_count"
       - Data type: integer
       - Description: The field 'difference_hydrogen_bond_count' indicates the difference between the mutant count and the wild-type count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of hydrogen bonds ('hydrogen bond': https://goldbook.iupac.org/terms/view/H02899).

     - "wild_type_ionic_bond_count"
       - Data type: integer
       - Description: The field 'wild_type_ionic_bond_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of ionic bonds ('ionic bond': https://goldbook.iupac.org/terms/view/IT07058) in the wild-type integrated graph.

     - "mutant_ionic_bond_count"
       - Data type: integer
       - Description: The field 'mutant_ionic_bond_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of ionic bonds ('ionic bond': https://goldbook.iupac.org/terms/view/IT07058) in the mutant integrated graph.

     - "difference_ionic_bond_count"
       - Data type: integer
       - Description: The field 'difference_ionic_bond_count' indicates the difference between the mutant count and the wild-type count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of ionic bonds ('ionic bond': https://goldbook.iupac.org/terms/view/IT07058).

     - "wild_type_van_der_waals_contact_count"
       - Data type: integer
       - Description: The field 'wild_type_van_der_waals_contact_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of van der Waals contacts ('van der Waals forces': https://goldbook.iupac.org/terms/view/V06597) in the wild-type integrated graph.

     - "mutant_van_der_waals_contact_count"
       - Data type: integer
       - Description: The field 'mutant_van_der_waals_contact_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of van der Waals contacts ('van der Waals forces': https://goldbook.iupac.org/terms/view/V06597) in the mutant integrated graph.

     - "difference_van_der_waals_contact_count"
       - Data type: integer
       - Description: The field 'difference_van_der_waals_contact_count' indicates the difference between the mutant count and the wild-type count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of van der Waals contacts ('van der Waals forces': https://goldbook.iupac.org/terms/view/V06597).

     - "wild_type_pi_pi_stacking_count"
       - Data type: integer
       - Description: The field 'wild_type_pi_pi_stacking_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of pi-pi stacking interactions ('pi-pi stacking': https://goldbook.iupac.org/terms/view/13861) in the wild-type integrated graph.

     - "mutant_pi_pi_stacking_count"
       - Data type: integer
       - Description: The field 'mutant_pi_pi_stacking_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of pi-pi stacking interactions ('pi-pi stacking': https://goldbook.iupac.org/terms/view/13861) in the mutant integrated graph.

     - "difference_pi_pi_stacking_count"
       - Data type: integer
       - Description: The field 'difference_pi_pi_stacking_count' indicates the difference between the mutant count and the wild-type count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of pi-pi stacking interactions ('pi-pi stacking': https://goldbook.iupac.org/terms/view/13861).

     - "wild_type_pi_cation_interaction_count"
       - Data type: integer
       - Description: The field 'wild_type_pi_cation_interaction_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of pi-cation interactions ('cation-pi interaction': https://goldbook.iupac.org/terms/view/08154) in the wild-type integrated graph.

     - "mutant_pi_cation_interaction_count"
       - Data type: integer
       - Description: The field 'mutant_pi_cation_interaction_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of pi-cation interactions ('cation-pi interaction': https://goldbook.iupac.org/terms/view/08154) in the mutant integrated graph.

     - "difference_pi_cation_interaction_count"
       - Data type: integer
       - Description: The field 'difference_pi_cation_interaction_count' indicates the difference between the mutant count and the wild-type count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of pi-cation interactions ('cation-pi interaction': https://goldbook.iupac.org/terms/view/08154).

     - "wild_type_disulfide_bond_count"
       - Data type: integer
       - Description: The field 'wild_type_disulfide_bond_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of disulfide bonds ('disulfide bond': https://www.uniprot.org/help/disulfid) in the wild-type integrated graph.

     - "mutant_disulfide_bond_count"
       - Data type: integer
       - Description: The field 'mutant_disulfide_bond_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of disulfide bonds ('disulfide bond': https://www.uniprot.org/help/disulfid) in the mutant integrated graph.

     - "difference_disulfide_bond_count"
       - Data type: integer
       - Description: The field 'difference_disulfide_bond_count' indicates the difference between the mutant count and the wild-type count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of disulfide bonds ('disulfide bond': https://www.uniprot.org/help/disulfid).

   - "amino_acid_substitution_properties"
     - Data type: object
     - Description: The field 'amino_acid_substitution_properties' indicates residue properties ('residue': http://purl.obolibrary.org/obo/GENO_0000782; 'property': http://purl.obolibrary.org/obo/IAO_0000030) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606), comparing the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537) and the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     The "amino_acid_substitution_properties" object may contain:

     - "wild_type_residue_name"
       - Data type: string
       - Description: The field 'wild_type_residue_name' indicates the name ('name': http://xmlns.com/foaf/0.1/name) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606), using one-letter code ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) to represent.

     - "mutant_residue_name"
       - Data type: string
       - Description: The field 'mutant_residue_name' indicates the name ('name': http://xmlns.com/foaf/0.1/name) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606), using one-letter code ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) to represent.

     - "wild_type_residue_name_one_hot_encoding"
       - Data type: array
       - Description: The field 'wild_type_residue_name_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the wild-type residue name ('residue': http://purl.obolibrary.org/obo/GENO_0000782; 'name': http://xmlns.com/foaf/0.1/name) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "mutant_residue_name_one_hot_encoding"
       - Data type: array
       - Description: The field 'mutant_residue_name_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the mutant residue name ('residue': http://purl.obolibrary.org/obo/GENO_0000782; 'name': http://xmlns.com/foaf/0.1/name) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "difference_residue_name_one_hot_encoding"
       - Data type: array
       - Description: The field 'difference_residue_name_one_hot_encoding' indicates the difference between the mutant one-hot encoding and the wild-type one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the residue name ('residue': http://purl.obolibrary.org/obo/GENO_0000782; 'name': http://xmlns.com/foaf/0.1/name) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_chemical_classification"
       - Data type: string
       - Description: The field 'wild_type_residue_chemical_classification' indicates the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) in the wild-type protein structure.

     - "mutant_residue_chemical_classification"
       - Data type: string
       - Description: The field 'mutant_residue_chemical_classification' indicates the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) in the mutant protein structure.

     - "wild_type_residue_chemical_classification_one_hot_encoding"
       - Data type: array
       - Description: The field 'wild_type_residue_chemical_classification_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) in the wild-type protein structure.

     - "mutant_residue_chemical_classification_one_hot_encoding"
       - Data type: array
       - Description: The field 'mutant_residue_chemical_classification_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) in the mutant protein structure.

     - "difference_residue_chemical_classification_one_hot_encoding"
       - Data type: array
       - Description: The field 'difference_residue_chemical_classification_one_hot_encoding' indicates the difference between the mutant one-hot encoding and the wild-type one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_secondary_structure"
       - Data type: string
       - Description: The field 'wild_type_residue_secondary_structure' indicates the secondary structure ('secondary structure': http://edamontology.org/operation_1847) assigned to the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using DSSP secondary-structure codes ('DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) in the wild-type protein structure.

     - "mutant_residue_secondary_structure"
       - Data type: string
       - Description: The field 'mutant_residue_secondary_structure' indicates the secondary structure ('secondary structure': http://edamontology.org/operation_1847) assigned to the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using DSSP secondary-structure codes ('DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) in the mutant protein structure.

     - "wild_type_residue_secondary_structure_one_hot_encoding"
       - Data type: array
       - Description: The field 'wild_type_residue_secondary_structure_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the secondary structure ('secondary structure': http://edamontology.org/operation_1847) assigned to the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using DSSP secondary-structure codes ('DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) in the wild-type protein structure.

     - "mutant_residue_secondary_structure_one_hot_encoding"
       - Data type: array
       - Description: The field 'mutant_residue_secondary_structure_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the secondary structure ('secondary structure': http://edamontology.org/operation_1847) assigned to the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using DSSP secondary-structure codes ('DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) in the mutant protein structure.

     - "difference_residue_secondary_structure_one_hot_encoding"
       - Data type: array
       - Description: The field 'difference_residue_secondary_structure_one_hot_encoding' indicates the difference between the mutant one-hot encoding and the wild-type one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the secondary structure ('secondary structure': http://edamontology.org/operation_1847) assigned to the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using DSSP secondary-structure codes ('DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_relative_solvent_accessibility"
       - Data type: number
       - Description: The field 'wild_type_residue_relative_solvent_accessibility' indicates the relative solvent accessibility ('solvent accessibility': http://edamontology.org/data_1542) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "mutant_residue_relative_solvent_accessibility"
       - Data type: number
       - Description: The field 'mutant_residue_relative_solvent_accessibility' indicates the relative solvent accessibility ('solvent accessibility': http://edamontology.org/data_1542) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "difference_residue_relative_solvent_accessibility"
       - Data type: number
       - Description: The field 'difference_residue_relative_solvent_accessibility' indicates the difference between the mutant value and the wild-type value for the relative solvent accessibility ('solvent accessibility': http://edamontology.org/data_1542) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_backbone_phi_angle"
       - Data type: number
       - Description: The field 'wild_type_residue_backbone_phi_angle' indicates the backbone phi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "mutant_residue_backbone_phi_angle"
       - Data type: number
       - Description: The field 'mutant_residue_backbone_phi_angle' indicates the backbone phi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "difference_residue_backbone_phi_angle"
       - Data type: number
       - Description: The field 'difference_residue_backbone_phi_angle' indicates the difference between the mutant value and the wild-type value for the backbone phi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_backbone_psi_angle"
       - Data type: number
       - Description: The field 'wild_type_residue_backbone_psi_angle' indicates the backbone psi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "mutant_residue_backbone_psi_angle"
       - Data type: number
       - Description: The field 'mutant_residue_backbone_psi_angle' indicates the backbone psi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "difference_residue_backbone_psi_angle"
       - Data type: number
       - Description: The field 'difference_residue_backbone_psi_angle' indicates the difference between the mutant value and the wild-type value for the backbone psi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_net_charge"
       - Data type: number
       - Description: The field 'wild_type_residue_net_charge' indicates the net electric charge ('net electric charge': https://goldbook.iupac.org/terms/view/N04111) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "mutant_residue_net_charge"
       - Data type: number
       - Description: The field 'mutant_residue_net_charge' indicates the net electric charge ('net electric charge': https://goldbook.iupac.org/terms/view/N04111) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "difference_residue_net_charge"
       - Data type: number
       - Description: The field 'difference_residue_net_charge' indicates the difference between the mutant value and the wild-type value for the net electric charge ('net electric charge': https://goldbook.iupac.org/terms/view/N04111) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_pka"
       - Data type: number
       - Description: The field 'wild_type_residue_pka' indicates the pKa value ('pKa': https://goldbook.iupac.org/terms/view/15441) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "mutant_residue_pka"
       - Data type: number
       - Description: The field 'mutant_residue_pka' indicates the pKa value ('pKa': https://goldbook.iupac.org/terms/view/15441) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "difference_residue_pka"
       - Data type: number
       - Description: The field 'difference_residue_pka' indicates the difference between the mutant value and the wild-type value for the pKa value ('pKa': https://goldbook.iupac.org/terms/view/15441) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_volume"
       - Data type: number
       - Description: The field 'wild_type_residue_volume' indicates the volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "mutant_residue_volume"
       - Data type: number
       - Description: The field 'mutant_residue_volume' indicates the volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "difference_residue_volume"
       - Data type: number
       - Description: The field 'difference_residue_volume' indicates the difference between the mutant value and the wild-type value for the volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_hydrophobicity"
       - Data type: number
       - Description: The field 'wild_type_residue_hydrophobicity' indicates the hydrophobicity ('hydrophobicity': https://goldbook.iupac.org/terms/view/HT06964) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "mutant_residue_hydrophobicity"
       - Data type: number
       - Description: The field 'mutant_residue_hydrophobicity' indicates the hydrophobicity ('hydrophobicity': https://goldbook.iupac.org/terms/view/HT06964) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "difference_residue_hydrophobicity"
       - Data type: number
       - Description: The field 'difference_residue_hydrophobicity' indicates the difference between the mutant value and the wild-type value for the hydrophobicity ('hydrophobicity': https://goldbook.iupac.org/terms/view/HT06964) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_molecular_weight"
       - Data type: number
       - Description: The field 'wild_type_residue_molecular_weight' indicates the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "mutant_residue_molecular_weight"
       - Data type: number
       - Description: The field 'mutant_residue_molecular_weight' indicates the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "difference_residue_molecular_weight"
       - Data type: number
       - Description: The field 'difference_residue_molecular_weight' indicates the difference between the mutant value and the wild-type value for the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_isoelectric_point"
       - Data type: number
       - Description: The field 'wild_type_residue_isoelectric_point' indicates the isoelectric point ('isoelectric point': https://goldbook.iupac.org/terms/view/I03275) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "mutant_residue_isoelectric_point"
       - Data type: number
       - Description: The field 'mutant_residue_isoelectric_point' indicates the isoelectric point ('isoelectric point': https://goldbook.iupac.org/terms/view/I03275) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "difference_residue_isoelectric_point"
       - Data type: number
       - Description: The field 'difference_residue_isoelectric_point' indicates the difference between the mutant value and the wild-type value for the isoelectric point ('isoelectric point': https://goldbook.iupac.org/terms/view/I03275) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_root_mean_square_fluctuation"
       - Data type: number
       - Description: The field 'wild_type_residue_root_mean_square_fluctuation' indicates the root mean square fluctuation ('root mean square fluctuation': https://manual.gromacs.org/current/onlinehelp/gmx-rmsf.html) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "mutant_residue_root_mean_square_fluctuation"
       - Data type: number
       - Description: The field 'mutant_residue_root_mean_square_fluctuation' indicates the root mean square fluctuation ('root mean square fluctuation': https://manual.gromacs.org/current/onlinehelp/gmx-rmsf.html) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "difference_residue_root_mean_square_fluctuation"
       - Data type: number
       - Description: The field 'difference_residue_root_mean_square_fluctuation' indicates the difference between the mutant value and the wild-type value for the root mean square fluctuation ('root mean square fluctuation': https://manual.gromacs.org/current/onlinehelp/gmx-rmsf.html) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_sequence_conservation_score"
       - Data type: number
       - Description: The field 'wild_type_residue_sequence_conservation_score' indicates the sequence conservation score ('sequence conservation': http://edamontology.org/operation_0448; 'score': http://edamontology.org/data_1772) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "mutant_residue_sequence_conservation_score"
       - Data type: number
       - Description: The field 'mutant_residue_sequence_conservation_score' indicates the sequence conservation score ('sequence conservation': http://edamontology.org/operation_0448; 'score': http://edamontology.org/data_1772) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "difference_residue_sequence_conservation_score"
       - Data type: number
       - Description: The field 'difference_residue_sequence_conservation_score' indicates the difference between the mutant value and the wild-type value for the sequence conservation score ('sequence conservation': http://edamontology.org/operation_0448; 'score': http://edamontology.org/data_1772) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

   - "wild_type_integrated_graph"
     - Data type: array
     - Description: The field 'wild_type_integrated_graph' indicates the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/) containing molecular interactions ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI) between source nodes and target nodes, and isolated nodes ('isolated node': https://mathworld.wolfram.com/IsolatedPoint.html), integrated from EnzyWizard reports ('report': http://purl.obolibrary.org/obo/IAO_0000088) for the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

   - "mutant_integrated_graph"
     - Data type: array
     - Description: The field 'mutant_integrated_graph' indicates the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/) containing molecular interactions ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI) between source nodes and target nodes, and isolated nodes ('isolated node': https://mathworld.wolfram.com/IsolatedPoint.html), integrated from EnzyWizard reports ('report': http://purl.obolibrary.org/obo/IAO_0000088) for the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     Each item in "wild_type_integrated_graph" or "mutant_integrated_graph" is one of the following entry objects:

     Interaction graph entry:

     - "molecular_interaction"
       - Data type: object
       - Description: The field 'molecular_interaction' indicates a molecular interaction ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI) between the source node and the target node in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

     - "source_node"
       - Data type: object
       - Description: The field 'source_node' indicates the source node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) corresponding to a residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) or a substrate ('substrate': https://purl.dsmz.de/schema/Substrate) in the integrated graph.

     - "target_node"
       - Data type: object
       - Description: The field 'target_node' indicates the target node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) corresponding to a residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) or a substrate ('substrate': https://purl.dsmz.de/schema/Substrate) in the integrated graph.

       The "molecular_interaction" object contains:

       - "molecular_interaction_type"
         - Data type: string
         - Description: The field 'molecular_interaction_type' indicates the type ('interaction type': http://purl.obolibrary.org/obo/MI_0190) of molecular interaction ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI), using RING interaction codes ('RING interaction type': https://ring.biocomputingup.it/help/interactions): hydrogen bond ('hydrogen bond': https://goldbook.iupac.org/terms/view/H02899; value: HBOND), ionic bond ('ionic bond': https://goldbook.iupac.org/terms/view/IT07058; value: IONIC), van der Waals contact ('van der Waals forces': https://goldbook.iupac.org/terms/view/V06597; value: VDW), pi-pi stacking ('pi-pi stacking': https://goldbook.iupac.org/terms/view/13861; value: PIPISTACK), pi-cation interaction ('cation-pi interaction': https://goldbook.iupac.org/terms/view/08154; value: PICATION), and disulfide bond ('disulfide bond': https://www.uniprot.org/help/disulfid; value: SSBOND).

       - "molecular_interaction_one_hot_encoding"
         - Data type: array
         - Description: The field 'molecular_interaction_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the molecular interaction type ('interaction type': http://purl.obolibrary.org/obo/MI_0190).

       - "interaction_count"
         - Data type: integer
         - Description: The field 'interaction_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of molecular interactions ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI) between the source node and the target node.

     Isolated node graph entry:

     - "isolated_node"
       - Data type: object
       - Description: The field 'isolated_node' indicates an isolated residue node ('isolated point': https://mathworld.wolfram.com/IsolatedPoint.html; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) or a substrate node ('substrate': https://purl.dsmz.de/schema/Substrate) in the integrated graph.

     Node objects used in "source_node", "target_node", and "isolated_node" may contain residue node fields or substrate node fields.

     Residue node fields:

     - "node_index"
       - Data type: integer
       - Description: The field 'node_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

     - "node_type"
       - Data type: string
       - Expected value: "residue"
       - Description: The field 'node_type' indicates the type ('type': http://purl.org/dc/terms/type) of node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node), with value 'residue' indicating a residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "node_type_one_hot_encoding"
       - Data type: array
       - Description: The field 'node_type_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the node type ('type': http://purl.org/dc/terms/type).

     - "residue_index"
       - Data type: integer
       - Description: The field 'residue_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_name"
       - Data type: string
       - Description: The field 'residue_name' indicates the name ('name': http://xmlns.com/foaf/0.1/name) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using one-letter code ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) to represent.

     - "residue_name_one_hot_encoding"
       - Data type: array
       - Description: The field 'residue_name_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the residue name ('residue': http://purl.obolibrary.org/obo/GENO_0000782; 'name': http://xmlns.com/foaf/0.1/name).

     - "residue_alpha_carbon_coordinate"
       - Data type: array
       - Description: The field 'residue_alpha_carbon_coordinate' indicates the three-dimensional coordinate ('coordinate': http://purl.obolibrary.org/obo/NCIT_C44477) of the alpha carbon atom ('alpha carbon': https://www.rcsb.org/docs/general-help/glossary; 'atom': http://purl.obolibrary.org/obo/CHMO_0001075) in the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_chemical_classification"
       - Data type: string
       - Description: The field 'residue_chemical_classification' indicates the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_chemical_classification_one_hot_encoding"
       - Data type: array
       - Description: The field 'residue_chemical_classification_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_secondary_structure"
       - Data type: string
       - Description: The field 'residue_secondary_structure' indicates the secondary structure ('secondary structure': http://edamontology.org/operation_1847) assigned to the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using DSSP secondary-structure codes ('DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

     - "residue_secondary_structure_one_hot_encoding"
       - Data type: array
       - Description: The field 'residue_secondary_structure_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the residue secondary structure ('secondary structure': http://edamontology.org/operation_1847).

     - "residue_relative_solvent_accessibility"
       - Data type: number
       - Description: The field 'residue_relative_solvent_accessibility' indicates the relative solvent accessibility ('solvent accessibility': http://edamontology.org/data_1542) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_backbone_phi_angle"
       - Data type: number
       - Description: The field 'residue_backbone_phi_angle' indicates the backbone phi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825).

     - "residue_backbone_psi_angle"
       - Data type: number
       - Description: The field 'residue_backbone_psi_angle' indicates the backbone psi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825).

     - "residue_net_charge"
       - Data type: number
       - Description: The field 'residue_net_charge' indicates the net electric charge ('net electric charge': https://goldbook.iupac.org/terms/view/N04111) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_pka"
       - Data type: number
       - Description: The field 'residue_pka' indicates the pKa value ('pKa': https://goldbook.iupac.org/terms/view/15441) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_volume"
       - Data type: number
       - Description: The field 'residue_volume' indicates the volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_hydrophobicity"
       - Data type: number
       - Description: The field 'residue_hydrophobicity' indicates the hydrophobicity ('hydrophobicity': https://goldbook.iupac.org/terms/view/HT06964) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_molecular_weight"
       - Data type: number
       - Description: The field 'residue_molecular_weight' indicates the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_isoelectric_point"
       - Data type: number
       - Description: The field 'residue_isoelectric_point' indicates the isoelectric point ('isoelectric point': https://goldbook.iupac.org/terms/view/I03275) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_root_mean_square_fluctuation"
       - Data type: number
       - Description: The field 'residue_root_mean_square_fluctuation' indicates the root mean square fluctuation ('root mean square fluctuation': https://manual.gromacs.org/current/onlinehelp/gmx-rmsf.html) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_sequence_conservation_score"
       - Data type: number
       - Description: The field 'residue_sequence_conservation_score' indicates the sequence conservation score ('sequence conservation': http://edamontology.org/operation_0448; 'score': http://edamontology.org/data_1772) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_embedding"
       - Data type: array
       - Description: The field 'residue_embedding' indicates the embedding ('embedding': https://developers.google.com/machine-learning/crash-course/embeddings) generated by the ESM-2 protein language model ('ESM-2': https://docs.nvidia.com/bionemo-framework/2.0/models/esm2/; 'protein language model': https://synbiointel.com/glossary/protein-language-model/) for the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), represented as a numerical vector ('numerical vector': https://mathworld.wolfram.com/Vector.html).

     - "is_in_hydrophobic_cluster"
       - Data type: boolean
       - Description: The field 'is_in_hydrophobic_cluster' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in a hydrophobic cluster ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/).

     - "is_in_disordered_region"
       - Data type: boolean
       - Description: The field 'is_in_disordered_region' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in an intrinsically disordered region ('intrinsically disordered region': https://disprot.org/ontology).

     - "is_in_binding_pocket"
       - Data type: boolean
       - Description: The field 'is_in_binding_pocket' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in a binding pocket ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html).

     Substrate node fields:

     - "node_index"
       - Data type: integer
       - Description: The field 'node_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

     - "node_type"
       - Data type: string
       - Expected value: "substrate"
       - Description: The field 'node_type' indicates the type ('type': http://purl.org/dc/terms/type) of node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node), with value 'substrate' indicating a substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "node_type_one_hot_encoding"
       - Data type: array
       - Description: The field 'node_type_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the node type ('type': http://purl.org/dc/terms/type).

     - "substrate_index"
       - Data type: integer
       - Description: The field 'substrate_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_name"
       - Data type: string
       - Description: The field 'substrate_name' indicates the name ('name': http://xmlns.com/foaf/0.1/name) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_smiles"
       - Data type: string
       - Description: The field 'substrate_smiles' indicates the SMILES representation ('SMILES': https://opensmiles.org/opensmiles.html) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_atom_count"
       - Data type: integer
       - Description: The field 'substrate_atom_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of atoms ('atom': https://goldbook.iupac.org/terms/view/A00493) in the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_molecular_weight"
       - Data type: number
       - Description: The field 'substrate_molecular_weight' indicates the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_logp"
       - Data type: number
       - Description: The field 'substrate_logp' indicates the calculated logP value ('LogP': https://doktormike.gitlab.io/posts/navigating-logp-logd-pka-and-logs-a-physicists-guide/) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "docked_substrate_center_coordinate"
       - Data type: array
       - Description: The field 'docked_substrate_center_coordinate' indicates the center coordinate ('coordinate': https://mathworld.wolfram.com/Coordinates.html) of the docked substrate ('substrate': https://purl.dsmz.de/schema/Substrate) in the enzyme-substrate complex ('enzyme': https://purl.dsmz.de/schema/Enzyme; 'substrate': https://purl.dsmz.de/schema/Substrate; 'complex': https://goldbook.iupac.org/terms/view/C01203).

     - "substrate_fingerprint_encoding"
       - Data type: array
       - Description: The field 'substrate_fingerprint_encoding' indicates the molecular fingerprint encoding ('molecular fingerprint': https://www.rdkit.org/docs/GettingStartedInPython.html#fingerprinting-and-molecular-similarity) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate) calculated by RDKit software ('RDKit': https://www.rdkit.org/docs/index.html).

2. Wild-type node-only JSON file
   - wt_integrate_nodes_{wt_protein_name}.json

   The node-only JSON file follows the JSON schema file:
   - resources/integrated_graph_nodes_schema.json

   This file contains all wild-type node records extracted from "wild_type_integrated_graph". The node objects are the same residue or substrate node objects used in the shared mut-integrate JSON report.

   Each item is one of the following node objects:

   Residue node object:

   The residue node object contains:

   - "node_index"
     - Data type: integer
     - Description: The field 'node_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

   - "node_type"
     - Data type: string
     - Expected value: "residue"
     - Description: The field 'node_type' indicates the type ('type': http://purl.org/dc/terms/type) of node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node), with value 'residue' indicating a residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "node_type_one_hot_encoding"
     - Data type: array
     - Description: The field 'node_type_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the node type ('type': http://purl.org/dc/terms/type).

   - "residue_index"
     - Data type: integer
     - Description: The field 'residue_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_name"
     - Data type: string
     - Description: The field 'residue_name' indicates the name ('name': http://xmlns.com/foaf/0.1/name) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using one-letter code ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) to represent.

   - "residue_name_one_hot_encoding"
     - Data type: array
     - Description: The field 'residue_name_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the residue name ('residue': http://purl.obolibrary.org/obo/GENO_0000782; 'name': http://xmlns.com/foaf/0.1/name).

   - "residue_alpha_carbon_coordinate"
     - Data type: array
     - Description: The field 'residue_alpha_carbon_coordinate' indicates the three-dimensional coordinate ('coordinate': http://purl.obolibrary.org/obo/NCIT_C44477) of the alpha carbon atom ('alpha carbon': https://www.rcsb.org/docs/general-help/glossary; 'atom': http://purl.obolibrary.org/obo/CHMO_0001075) in the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_chemical_classification"
     - Data type: string
     - Description: The field 'residue_chemical_classification' indicates the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_chemical_classification_one_hot_encoding"
     - Data type: array
     - Description: The field 'residue_chemical_classification_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_secondary_structure"
     - Data type: string
     - Description: The field 'residue_secondary_structure' indicates the secondary structure ('secondary structure': http://edamontology.org/operation_1847) assigned to the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using DSSP secondary-structure codes ('DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

   - "residue_secondary_structure_one_hot_encoding"
     - Data type: array
     - Description: The field 'residue_secondary_structure_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the residue secondary structure ('secondary structure': http://edamontology.org/operation_1847).

   - "residue_relative_solvent_accessibility"
     - Data type: number
     - Description: The field 'residue_relative_solvent_accessibility' indicates the relative solvent accessibility ('solvent accessibility': http://edamontology.org/data_1542) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_backbone_phi_angle"
     - Data type: number
     - Description: The field 'residue_backbone_phi_angle' indicates the backbone phi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825).

   - "residue_backbone_psi_angle"
     - Data type: number
     - Description: The field 'residue_backbone_psi_angle' indicates the backbone psi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825).

   - "residue_net_charge"
     - Data type: number
     - Description: The field 'residue_net_charge' indicates the net electric charge ('net electric charge': https://goldbook.iupac.org/terms/view/N04111) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_pka"
     - Data type: number
     - Description: The field 'residue_pka' indicates the pKa value ('pKa': https://goldbook.iupac.org/terms/view/15441) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_volume"
     - Data type: number
     - Description: The field 'residue_volume' indicates the volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_hydrophobicity"
     - Data type: number
     - Description: The field 'residue_hydrophobicity' indicates the hydrophobicity ('hydrophobicity': https://goldbook.iupac.org/terms/view/HT06964) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_molecular_weight"
     - Data type: number
     - Description: The field 'residue_molecular_weight' indicates the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_isoelectric_point"
     - Data type: number
     - Description: The field 'residue_isoelectric_point' indicates the isoelectric point ('isoelectric point': https://goldbook.iupac.org/terms/view/I03275) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_root_mean_square_fluctuation"
     - Data type: number
     - Description: The field 'residue_root_mean_square_fluctuation' indicates the root mean square fluctuation ('root mean square fluctuation': https://manual.gromacs.org/current/onlinehelp/gmx-rmsf.html) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_sequence_conservation_score"
     - Data type: number
     - Description: The field 'residue_sequence_conservation_score' indicates the sequence conservation score ('sequence conservation': http://edamontology.org/operation_0448; 'score': http://edamontology.org/data_1772) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_embedding"
     - Data type: array
     - Description: The field 'residue_embedding' indicates the embedding ('embedding': https://developers.google.com/machine-learning/crash-course/embeddings) generated by the ESM-2 protein language model ('ESM-2': https://docs.nvidia.com/bionemo-framework/2.0/models/esm2/; 'protein language model': https://synbiointel.com/glossary/protein-language-model/) for the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), represented as a numerical vector ('numerical vector': https://mathworld.wolfram.com/Vector.html).

   - "is_in_hydrophobic_cluster"
     - Data type: boolean
     - Description: The field 'is_in_hydrophobic_cluster' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in a hydrophobic cluster ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/).

   - "is_in_disordered_region"
     - Data type: boolean
     - Description: The field 'is_in_disordered_region' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in an intrinsically disordered region ('intrinsically disordered region': https://disprot.org/ontology).

   - "is_in_binding_pocket"
     - Data type: boolean
     - Description: The field 'is_in_binding_pocket' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in a binding pocket ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html).

   Substrate node object:

   The substrate node object contains:

   - "node_index"
     - Data type: integer
     - Description: The field 'node_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

   - "node_type"
     - Data type: string
     - Expected value: "substrate"
     - Description: The field 'node_type' indicates the type ('type': http://purl.org/dc/terms/type) of node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node), with value 'substrate' indicating a substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

   - "node_type_one_hot_encoding"
     - Data type: array
     - Description: The field 'node_type_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the node type ('type': http://purl.org/dc/terms/type).

   - "substrate_index"
     - Data type: integer
     - Description: The field 'substrate_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

   - "substrate_name"
     - Data type: string
     - Description: The field 'substrate_name' indicates the name ('name': http://xmlns.com/foaf/0.1/name) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

   - "substrate_smiles"
     - Data type: string
     - Description: The field 'substrate_smiles' indicates the SMILES representation ('SMILES': https://opensmiles.org/opensmiles.html) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

   - "substrate_atom_count"
     - Data type: integer
     - Description: The field 'substrate_atom_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of atoms ('atom': https://goldbook.iupac.org/terms/view/A00493) in the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

   - "substrate_molecular_weight"
     - Data type: number
     - Description: The field 'substrate_molecular_weight' indicates the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

   - "substrate_logp"
     - Data type: number
     - Description: The field 'substrate_logp' indicates the calculated logP value ('LogP': https://doktormike.gitlab.io/posts/navigating-logp-logd-pka-and-logs-a-physicists-guide/) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

   - "docked_substrate_center_coordinate"
     - Data type: array
     - Description: The field 'docked_substrate_center_coordinate' indicates the center coordinate ('coordinate': https://mathworld.wolfram.com/Coordinates.html) of the docked substrate ('substrate': https://purl.dsmz.de/schema/Substrate) in the enzyme-substrate complex ('enzyme': https://purl.dsmz.de/schema/Enzyme; 'substrate': https://purl.dsmz.de/schema/Substrate; 'complex': https://goldbook.iupac.org/terms/view/C01203).

   - "substrate_fingerprint_encoding"
     - Data type: array
     - Description: The field 'substrate_fingerprint_encoding' indicates the molecular fingerprint encoding ('molecular fingerprint': https://www.rdkit.org/docs/GettingStartedInPython.html#fingerprinting-and-molecular-similarity) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate) calculated by RDKit software ('RDKit': https://www.rdkit.org/docs/index.html).

3. Wild-type edge-only JSON file
   - wt_integrate_edges_{wt_protein_name}.json

   The edge-only JSON file follows the JSON schema file:
   - resources/integrated_graph_edges_schema.json

   This file contains all wild-type edge records extracted from "wild_type_integrated_graph".

   Each item is an object containing:

   - "molecular_interaction"
     - Data type: object
     - Description: The field 'molecular_interaction' indicates a molecular interaction ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI) between the source node and the target node in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

     The "molecular_interaction" object contains:

     - "molecular_interaction_type"
       - Data type: string
       - Description: The field 'molecular_interaction_type' indicates the type ('interaction type': http://purl.obolibrary.org/obo/MI_0190) of molecular interaction ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI), using RING interaction codes ('RING interaction type': https://ring.biocomputingup.it/help/interactions): hydrogen bond ('hydrogen bond': https://goldbook.iupac.org/terms/view/H02899; value: HBOND), ionic bond ('ionic bond': https://goldbook.iupac.org/terms/view/IT07058; value: IONIC), van der Waals contact ('van der Waals forces': https://goldbook.iupac.org/terms/view/V06597; value: VDW), pi-pi stacking ('pi-pi stacking': https://goldbook.iupac.org/terms/view/13861; value: PIPISTACK), pi-cation interaction ('cation-pi interaction': https://goldbook.iupac.org/terms/view/08154; value: PICATION), and disulfide bond ('disulfide bond': https://www.uniprot.org/help/disulfid; value: SSBOND).

     - "molecular_interaction_one_hot_encoding"
       - Data type: array
       - Description: The field 'molecular_interaction_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the molecular interaction type ('interaction type': http://purl.obolibrary.org/obo/MI_0190).

     - "interaction_count"
       - Data type: integer
       - Description: The field 'interaction_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of molecular interactions ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI) between the source node and the target node.

   - "source_node"
     - Data type: object
     - Description: The field 'source_node' indicates the source node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph.

     The "source_node" object contains:

     - "node_index"
       - Data type: integer
       - Description: The field 'node_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

   - "target_node"
     - Data type: object
     - Description: The field 'target_node' indicates the target node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph.

     The "target_node" object contains:

     - "node_index"
       - Data type: integer
       - Description: The field 'node_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

4. Mutant node-only JSON file
   - mut_integrate_nodes_{mut_protein_name}.json

   The node-only JSON file follows the JSON schema file:
   - resources/integrated_graph_nodes_schema.json

   This file contains all mutant node records extracted from "mutant_integrated_graph". The node objects have the same schema and content structure as the wild-type node-only JSON file.

5. Mutant edge-only JSON file
   - mut_integrate_edges_{mut_protein_name}.json

   The edge-only JSON file follows the JSON schema file:
   - resources/integrated_graph_edges_schema.json

   This file contains all mutant edge records extracted from "mutant_integrated_graph". The edge objects have the same schema and content structure as the wild-type edge-only JSON file.

# Process:

This command processes the input wild-type and mutant systems as follows:

1. Validate input files
   - Check that wt_cleaned_input_path exists.
   - Check that mut_cleaned_input_path exists.
   - Check that wt_input_msa exists.
   - Check that mut_input_msa exists.
   - Create wt_output_dir and mut_output_dir if needed.
   - Check that wt_output_dir and mut_output_dir are different directories.

2. Validate mutation input
   - Check that amino_acid_substitution is not empty.
   - Validate the mutation format, such as A123V.
   - Check that the mutation position is within the wild-type and mutant
     sequence length.

3. Resolve names
   - Extract wt_protein_name from the wild-type cleaned structure filename.
   - Extract mut_protein_name from the mutant cleaned structure filename.
   - Extract wt_msa_name from the wild-type MSA filename.
   - Extract mut_msa_name from the mutant MSA filename.
   - Validate filename length.
   - Reject input if wild-type and mutant protein names are the same.

4. Validate parameters
   - Check parameter ranges for hydrophobic cluster detection.
   - Check energy minimization parameters.
   - Check flexibility and disorder parameters.
   - Check pocket detection parameters.
   - Check substrate generation parameters.
   - Check docking parameters.
   - Check interaction detection parameters.

5. Prepare output mode
   - If --save_extra_outputs is enabled, run directly in wt_output_dir and
     mut_output_dir.
   - If disabled, run in temporary wild-type and mutant directories and only
     copy final outputs.

6. Load wild-type and mutant structures
   - Read the wild-type cleaned CIF or PDB file.
   - Read the mutant cleaned CIF or PDB file.
   - Validate that both are valid cleaned protein structures.
   - Check that both structures contain hydrogen atoms.
   - Check that both structures contain a valid single protein chain.
   - Check that wild-type and mutant sequence lengths are equal.

7. Build identity clean reports
   - Treat both input structures as already cleaned.
   - Build identity residue mappings for wild-type and mutant structures.
   - Generate enzywizard_clean-style reports for both sides.

8. Build mutation clean report
   - Map the input amino acid substitution onto cleaned residue indexing.
   - Generate an enzywizard_mut_clean-style report describing the wild-type to
     mutant substitution and residue mapping.

9. Optionally generate substrate structures
   - Parse substrate names or SMILES strings.
   - Retrieve or complete SMILES information.
   - Generate substrate fingerprints and 3D conformers.
   - Save substrate structure files to the wild-type output directory.
   - Copy substrate SDF files to the mutant output directory.
   - Generate one shared enzywizard_substrate report for both sides.
   - If substrate parsing, SMILES completion, conformer generation, structure saving,
     SDF copying, or report generation fails, log a warning and continue with paired
     protein-only analysis.

10. Run wild-type side workflow
   - Prepare OpenMM and sequence objects.
   - Run amino acid property analysis.
   - Run hydrophobic cluster analysis.
   - Run energy analysis.
   - Run flexibility analysis.
   - Run disorder analysis.
   - Run conservation analysis using the wild-type MSA.
   - Run embedding analysis.
   - Run pocket analysis.
   - Optionally run docking analysis using wild-type substrate SDF files.
   - In manual docking box mode, use --dock_catalytic_residue or --dock_catalytic_site_coord with --dock_box_size and skip docking-specific PyVOL pocket detection and the global docking box fallback.
   - In automatic docking box mode, use automatically generated pocket and global fallback docking boxes.
   - If wild-type docking cannot complete, continue this side as protein-only and
     run the mutant side as protein-only.
   - Run interaction analysis.
   - Build the wild-type report dictionary.

11. Run mutant side workflow
   - Prepare OpenMM and sequence objects.
   - Run amino acid property analysis.
   - Run hydrophobic cluster analysis.
   - Run energy analysis.
   - Run flexibility analysis.
   - Run disorder analysis.
   - Run conservation analysis using the mutant MSA.
   - Run embedding analysis.
   - Run pocket analysis.
   - Optionally run docking analysis using mutant substrate SDF files.
   - In manual docking box mode, use --dock_catalytic_residue or --dock_catalytic_site_coord with --dock_box_size and skip docking-specific PyVOL pocket detection and the global docking box fallback.
   - In automatic docking box mode, use automatically generated pocket and global fallback docking boxes.
   - If mutant docking cannot complete after wild-type docking succeeded, re-run the
     wild-type side as protein-only so both sides are integrated consistently.
   - Run interaction analysis.
   - Build the mutant report dictionary.

12. Run mutation-aware graph integration
   - Pass the enzywizard_mut_clean report, wild-type report dictionary, and mutant report
     dictionary into the mutation integration algorithm.
   - Use strict integration when substrate input is provided and substrate/docking
     workflows complete successfully on both sides.
   - Use non-strict integration when no substrate input is provided or the workflow
     falls back to paired protein-only analysis.
   - Generate paired wild-type and mutant integrated graph representations.

13. Save mutation-integrated outputs
   - Write mut_integrate_report_{wt_protein_name}_to_{mut_protein_name}.json
     into both output directories.
   - Split wild_type_integrated_graph into wild-type node and edge lists.
   - Split mutant_integrated_graph into mutant node and edge lists.
   - Write wt_integrate_nodes_{wt_protein_name}.json.
   - Write wt_integrate_edges_{wt_protein_name}.json.
   - Write mut_integrate_nodes_{mut_protein_name}.json.
   - Write mut_integrate_edges_{mut_protein_name}.json.

14. Finalize outputs
   - If --save_extra_outputs is disabled, copy only the final mutation-integrated
     JSON outputs and log.txt from temporary directories to the requested output
     directories.
   - Copy log.txt to the mutant output directory when available.
   - Finish the mut-batch workflow.


# dependencies:

- Biopython
- NumPy
- OpenMM
- DSSP
- ProDy
- ESM
- HMMER
- PyVOL
- RDKit
- AutoDock Vina
- Meeko
- JSON


# references:

- Biopython:
  https://biopython.org/

- OpenMM:
  https://openmm.org/

- DSSP:
  https://github.com/PDB-REDO/dssp

- ProDy:
  http://prody.csb.pitt.edu/

- ESM:
  https://github.com/facebookresearch/esm

- HMMER:
  http://hmmer.org/

- PyVOL:
  https://github.com/schlessinger-lab/pyvol

- RDKit:
  https://www.rdkit.org/

- AutoDock Vina:
  https://vina.scripps.edu/

- Meeko:
  https://github.com/forlilab/Meeko

- JSON:
  https://www.json.org/