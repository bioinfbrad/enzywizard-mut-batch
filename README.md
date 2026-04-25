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

-a, --amino_acid_substitution
Required.
Input amino acid substitution in mutation format, such as A123V.

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

The program outputs the following files:

1. A mutation-integrated JSON report
   - mut_integrate_report_{wt_protein_name}_to_{mut_protein_name}.json

   This report is saved into both the wild-type and mutant output directories.

   The JSON report contains:

   - "output_type"
     A string identifying the report type:
     "enzywizard_mut_integrate"

   - "wt_integrated_graph"
     A list describing the integrated graph entries for the wild-type protein.

   - "mut_integrated_graph"
     A list describing the integrated graph entries for the mutant protein.

   Each graph entry is stored in one of the following formats:

   Node entry:
   - "node_1"
     A single integrated node record representing:
     - an amino acid residue
     - or a substrate, if substrate input is provided

   Edge entry:
   - "node_1"
     Information of the first node

   - "edge"
     Information of the relationship between nodes

   - "node_2"
     Information of the second node

   The mutation-integrated report represents:
   - wild-type residue-level features
   - mutant residue-level features
   - mutation mapping information
   - residue-residue relationships
   - intra-protein interaction networks
   - optional substrate nodes
   - optional protein-substrate docking and interaction information

2. Wild-type node-only JSON file
   - wt_integrate_nodes_{wt_protein_name}.json

   Contains all wild-type node records extracted from wt_integrated_graph.

3. Wild-type edge-only JSON file
   - wt_integrate_edges_{wt_protein_name}.json

   Contains all wild-type edge records extracted from wt_integrated_graph.

4. Mutant node-only JSON file
   - mut_integrate_nodes_{mut_protein_name}.json

   Contains all mutant node records extracted from mut_integrated_graph.

5. Mutant edge-only JSON file
   - mut_integrate_edges_{mut_protein_name}.json

   Contains all mutant edge records extracted from mut_integrated_graph.

If --save_extra_outputs is enabled, additional intermediate or side output files
may also be saved on each side, including:
- cleaned MSA STO files
- HMM profile files
- substrate SDF files
- docked substrate files
- protein-substrate complex files


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
   - Generate an enzywizard_mutclean-style report describing the wild-type to
     mutant substitution and residue mapping.

9. Optionally generate substrate structures
   - Parse substrate names or SMILES strings.
   - Retrieve or complete SMILES information.
   - Generate substrate fingerprints and 3D conformers.
   - Save substrate structure files to the wild-type output directory.
   - Copy substrate SDF files to the mutant output directory.
   - Generate one shared enzywizard_substrate report for both sides.

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
   - Run interaction analysis.
   - Build the mutant report dictionary.

12. Run mutation-aware graph integration
   - Pass the mutclean report, wild-type report dictionary, and mutant report
     dictionary into the mutation integration algorithm.
   - Use strict integration when substrate input is provided.
   - Use non-strict integration when no substrate input is provided.
   - Generate paired wild-type and mutant integrated graph representations.

13. Save mutation-integrated outputs
   - Write mut_integrate_report_{wt_protein_name}_to_{mut_protein_name}.json
     into both output directories.
   - Split wt_integrated_graph into wild-type node and edge lists.
   - Split mut_integrated_graph into mutant node and edge lists.
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
