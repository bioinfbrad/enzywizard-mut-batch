[![DOI](https://zenodo.org/badge/1219039494.svg)](https://doi.org/10.5281/zenodo.19709927)
# Command: enzywizard-mut-batch

EnzyWizard-Mut-Batch is a command-line tool for running paired EnzyWizard
analysis workflows for a wild-type protein and its mutant.
It takes cleaned wild-type and mutant protein structures, optional matched wild-type and
mutant MSA files, and a cleaned amino acid substitution as input. It performs the full
EnzyWizard batch workflow on both sides, including amino acid property analysis,
hydrophobic cluster detection, energy evaluation, flexibility analysis, disorder
prediction, optional conservation analysis, protein embedding generation, pocket
detection, optional substrate feature generation, optional molecular docking,
interaction network calculation, and final mutation-aware graph integration.
If substrate names or SMILES strings are provided, substrate structures are
generated and used for docking and protein-substrate interaction analysis on both sides.
If no substrate input is provided, or if substrate generation or docking fails, the program generates paired protein-only integrated
graphs based on protein-level features and intra-protein interactions. If either MSA input is omitted, the corresponding conservation workflow is skipped and final graph integration uses non-strict mode.
The final output is a paired integrated graph dataset comparing the
wild-type and mutant proteins. It can be used for graph-based analysis,
machine learning, and mutation effect studies.


# Documentation index:

- example usage
- input parameters
- output files
- output report schema
- Process
- common errors and solutions
- dependencies
- references


# example usage:

The examples below use placeholder paths such as `path/to/wt_input.cif`,
`path/to/mut_input.cif`, `path/to/wt_alignment.sto`, and
`path/to/wt_output_dir/`; replace them with your own cleaned wild-type and
mutant protein structure files, optional matched MSA files, cleaned amino acid
substitution, optional substrate input, and output directories. The input
structures must already be cleaned. MSA input is optional: providing `-wm` and
`-mm` enables conservation analysis, cleaned MSA output, and HMM profile output
on the corresponding side. Substrate input is optional: providing names or
SMILES strings enables substrate generation, docking, and protein-substrate
interaction detection on both sides. If substrate generation or docking fails,
mut-batch falls back to the paired protein-only route.

Run the default paired protein-only workflow from cleaned CIF structures.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -a A123V -wo path/to/wt_output_default/ -mo path/to/mut_output_default/
```

Run the default paired protein-only workflow from cleaned PDB structures.

```
enzywizard-mut-batch -w path/to/wt_input.pdb -m path/to/mut_input.pdb -a A123V -wo path/to/wt_output_pdb/ -mo path/to/mut_output_pdb/
```

Run a paired protein-only workflow with Stockholm MSAs.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.sto -mm path/to/mut_alignment.sto -a A123V -wo path/to/wt_output_sto/ -mo path/to/mut_output_sto/
```

Run a paired protein-only workflow with aligned FASTA MSAs.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.fasta -mm path/to/mut_alignment.fasta -a A123V -wo path/to/wt_output_fasta_msa/ -mo path/to/mut_output_fasta_msa/
```

Run a paired protein-only workflow with gzip-compressed aligned FASTA MSAs.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.fasta.gz -mm path/to/mut_alignment.fasta.gz -a A123V -wo path/to/wt_output_fasta_gz_msa/ -mo path/to/mut_output_fasta_gz_msa/
```

Run a paired protein-only workflow with A3M MSAs.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.a3m -mm path/to/mut_alignment.a3m -a A123V -wo path/to/wt_output_a3m/ -mo path/to/mut_output_a3m/
```

Run the enzyme-substrate workflow for one named substrate. Substrate names are
resolved to SMILES through external chemical databases.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -a A123V -s "glucose" -wo path/to/wt_output_glucose/ -mo path/to/mut_output_glucose/
```

Run the enzyme-substrate workflow for two named substrates.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.sto -mm path/to/mut_alignment.sto -a A123V -s "glucose;fructose" -wo path/to/wt_output_named_substrates/ -mo path/to/mut_output_named_substrates/
```

Run the full workflow with direct SMILES input. Direct SMILES skips external
name-to-SMILES lookup.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.sto -mm path/to/mut_alignment.sto -a A123V -s "CCO" -wo path/to/wt_output_smiles/ -mo path/to/mut_output_smiles/
```

Run a mixed substrate input with one name and one SMILES string.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.sto -mm path/to/mut_alignment.sto -a A123V -s "glucose;CCO" -wo path/to/wt_output_mixed_substrates/ -mo path/to/mut_output_mixed_substrates/
```

Use long option names for the same full workflow.

```
enzywizard-mut-batch --wt_cleaned_input_path path/to/wt_input.cif --mut_cleaned_input_path path/to/mut_input.cif --wt_input_msa path/to/wt_alignment.sto --mut_input_msa path/to/mut_alignment.sto --cleaned_amino_acid_substitution A123V --substrate_names "glucose;fructose" --wt_output_dir path/to/wt_output_long_options/ --mut_output_dir path/to/mut_output_long_options/
```

Run a paired workflow with multiple cleaned amino acid substitutions.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.sto -mm path/to/mut_alignment.sto -a "A123V;G456D" -wo path/to/wt_output_multi_mutation/ -mo path/to/mut_output_multi_mutation/
```

Keep intermediate files such as cleaned MSAs, HMM profiles, substrate SDF files,
docked SDF files, and protein-substrate complex files. This is useful for
debugging or inspecting downstream inputs, but writes more files to disk.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.sto -mm path/to/mut_alignment.sto -a A123V -s "glucose;fructose" -wo path/to/wt_output_with_intermediates/ -mo path/to/mut_output_with_intermediates/ --save_extra_outputs
```

Use fewer energy minimization iterations. Smaller values reduce minimization
work and leave the structures closer to the starting conformations.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.sto -mm path/to/mut_alignment.sto -a A123V -wo path/to/wt_output_energy_20/ -mo path/to/mut_output_energy_20/ --energy_minimization_iteration 20
```

Use fewer substrate synonyms during name resolution. This can reduce API
requests and runtime, but may miss difficult or ambiguous substrate names that
need synonym-expanded matching.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.sto -mm path/to/mut_alignment.sto -a A123V -s "glucose;fructose" -wo path/to/wt_output_fast_lookup/ -mo path/to/mut_output_fast_lookup/ --substrate_max_synonyms 5
```

Use a catalytic residue as the docking box center. The residue index is the
cleaned protein residue index, and the residue CA atom coordinate is used as the
center. The same cleaned residue index is applied to both wild-type and mutant
structures. This skips PyVOL pocket detection and the global docking box
fallback. A smaller box focuses the search and can run faster, but may miss
valid poses outside the box. A larger box explores a broader region, but can
increase runtime and reduce search precision at the same exhaustiveness.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.sto -mm path/to/mut_alignment.sto -a A123V -s "glucose" -wo path/to/wt_output_catalytic_residue/ -mo path/to/mut_output_catalytic_residue/ --dock_catalytic_residue 121 --dock_box_size 20,20,20
```

Use an explicit catalytic-site coordinate as the docking box center. This is
useful when the active-site coordinate is known from another analysis or a
reference structure. The same coordinate is applied to both wild-type and mutant
docking workflows.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.sto -mm path/to/mut_alignment.sto -a A123V -s "glucose" -wo path/to/wt_output_site_coord/ -mo path/to/mut_output_site_coord/ --dock_catalytic_site_coord 12.5,8.0,-3.2 --dock_box_size 18,18,18
```

Increase Vina exhaustiveness for a broader docking search. Larger values may
improve search coverage and docking robustness, but increase runtime. Smaller
values are faster but may miss better poses.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.sto -mm path/to/mut_alignment.sto -a A123V -s "glucose;fructose" -wo path/to/wt_output_high_exhaustiveness/ -mo path/to/mut_output_high_exhaustiveness/ --dock_exhaustiveness 32
```

Disable docking early stop so mut-batch continues after the first successful
docking result and searches other conformer and box combinations up to
`--dock_max_attempt_num`. This can improve the chance of finding a lower-energy
pose, but increases runtime.

```
enzywizard-mut-batch -w path/to/wt_input.cif -m path/to/mut_input.cif -wm path/to/wt_alignment.sto -mm path/to/mut_alignment.sto -a A123V -s "glucose;fructose" -wo path/to/wt_output_no_early_stop/ -mo path/to/mut_output_no_early_stop/ --dock_no_early_stop --dock_max_attempt_num 40
```


# input parameters:

-a, --cleaned_amino_acid_substitution
Required.
Input cleaned amino acid substitution in mutation format, such as A123V or A123V;G456D.
This value can be obtained from the `cleaned_amino_acid_substitution` field in
an EnzyWizard-Mut-Clean report.

-w, --wt_cleaned_input_path
Required.
Path to the input wild-type cleaned protein structure file.
Supported file extensions: .cif, .pdb.

The file must:
- already be cleaned
- contain a valid single protein chain
- match the sequence used to generate the wild-type input MSA when `--wt_input_msa` is provided

-m, --mut_cleaned_input_path
Required.
Path to the input mutant cleaned protein structure file.
Supported file extensions: .cif, .pdb.

-wm, --wt_input_msa
Optional.
Path to the input wild-type MSA file.

Supported MSA formats include:
- Stockholm (.sto)
- aligned FASTA (.fa / .fasta / .afa / .fasta.gz)
- A3M

When provided, the MSA must be generated using the wild-type cleaned protein
FASTA sequence. When omitted, wild-type conservation analysis, cleaned MSA
output, and HMM profile output are skipped.

-mm, --mut_input_msa
Optional.
Path to the input mutant MSA file.

Supported MSA formats include:
- Stockholm (.sto)
- aligned FASTA (.fa / .fasta / .afa / .fasta.gz)
- A3M

When provided, the MSA must be generated using the mutant cleaned protein FASTA
sequence. When omitted, mutant conservation analysis, cleaned MSA output, and
HMM profile output are skipped.

-s, --substrate_names
Optional.
Substrate names or SMILES strings.

Multiple substrates should be separated by ';'.

If provided, the following additional workflows will be executed on both
wild-type and mutant sides:
- substrate feature generation
- substrate 3D structure generation
- molecular docking
- protein-substrate interaction calculation
- strict mutation-aware graph integration when both MSA inputs are also provided

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

When enabled, additional files such as cleaned MSAs, HMM profiles, substrate SDF
files, docked substrate files, and protein-substrate complex files may be saved.
Cleaned MSA and HMM files are generated only for sides with MSA input.

--hydrocluster_cutoff
Optional.
Minimum contact area cutoff for hydrophobic cluster residue-residue connection.
Unit: square angstroms (A^2).
Default: 10.0.

--no_minimize_energy
Optional.
Disable energy minimization before energy evaluation.
By default, energy minimization is enabled.

--energy_minimization_iteration
Optional.
Maximum number of iterations for energy minimization.
Default: 100.

--flexibility_method
Optional.
Normal mode method for RMSF calculation.
Choices:
- ANM
- GNM
Default: ANM.

--flexibility_cutoff
Optional.
Distance cutoff used to determine residue-residue connections in ProDy.
Unit: angstroms (A).
Default: 15.0.

--flexibility_n_modes
Optional.
Number of low-frequency normal modes used for RMSF calculation.
Default: 20.

--disorder_window_size
Optional.
Sliding window size for FoldIndex-like disordered region score calculation.
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
Minimum probe radius used by PyVOL for binding pocket detection.
Unit: angstroms (A).
Default: 1.8.

--pocket_max_rad
Optional.
Maximum probe radius used by PyVOL for binding pocket detection.
Unit: angstroms (A).
Default: 6.2.

--pocket_min_volume
Optional.
Minimum binding pocket volume threshold.
Unit: cubic angstroms (A^3).
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
Unit: angstroms (A).
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
Default: 8.

--dock_cpu
Optional.
Number of CPUs used by AutoDock Vina.
Default: 0.

--dock_catalytic_residue
Optional.
Cleaned protein residue index used as the docking box center.

Example:
  121

--dock_catalytic_site_coord
Optional.
Catalytic site center coordinate separated by ','.
Unit: angstroms (A).

Example:
  12.5,8.0,-3.2

When this parameter is provided, the same coordinate is used as the docking box
center on both wild-type and mutant sides.

--dock_box_size
Optional.
Docking box size separated by ','.
Unit: angstroms (A).

Example:
  20,20,20

This parameter is required when --dock_catalytic_residue or
--dock_catalytic_site_coord is provided. All three values must be positive
numbers.

--hbond_bonded_h_min_distance
Optional.
Minimum bonded heavy atom-hydrogen distance used for hydrogen bond donor
detection.
Unit: angstroms (A).
Default: 0.8.

--hbond_bonded_h_max_distance
Optional.
Maximum bonded heavy atom-hydrogen distance used for hydrogen bond donor
detection.
Unit: angstroms (A).
Default: 1.3.

--hbond_da_max_distance
Optional.
Maximum donor-acceptor distance cutoff for hydrogen bond detection.
Unit: angstroms (A).
Default: 3.9.

--hbond_ha_max_distance
Optional.
Maximum hydrogen-acceptor distance cutoff for hydrogen bond detection.
Unit: angstroms (A).
Default: 2.5.

--hbond_angle
Optional.
Minimum donor-hydrogen-acceptor angle cutoff for hydrogen bond detection.
Unit: degrees.
Default: 90.0.

--ionic_distance_cutoff
Optional.
Maximum distance cutoff for ionic bond detection.
Unit: angstroms (A).
Default: 4.0.

--vdw_mu
Optional.
Mu parameter used in van der Waals interaction detection.
Unit: dimensionless.
Default: 0.01.

--ppstack_center_distance_cutoff
Optional.
Maximum ring-center distance cutoff for pi-pi stacking detection.
Unit: angstroms (A).
Default: 6.5.

--pication_distance_cutoff
Optional.
Maximum ring-cation distance cutoff for pi-cation interaction detection.
Unit: angstroms (A).
Default: 5.0.

--pication_angle_cutoff
Optional.
Maximum angle cutoff for pi-cation interaction detection.
Unit: degrees.
Default: 45.0.

--ssbond_max_distance
Optional.
Maximum sulfur-sulfur distance cutoff for disulfide bond detection.
Unit: angstroms (A).
Default: 2.5.


# output files:

The program always keeps the following files in the output directories:

`{wt_protein_name}` and `{mut_protein_name}` are derived from the wild-type and mutant cleaned input structure file names.

1. A mut-integrate JSON report
   - mut_integrate_report_{wt_protein_name}_to_{mut_protein_name}.json
     - Full paired report containing overall statistics, mutation-site
       properties, and wild-type / mutant integrated graph entries. This file
       is saved into both output directories.

2. A wild-type node-only JSON file
   - wt_integrate_nodes_{wt_protein_name}.json
     - Array of wild-type integrated graph node records split from the
       wild-type integrated graph. This file is saved into `wt_output_dir`.

3. A wild-type edge-only JSON file
   - wt_integrate_edges_{wt_protein_name}.json
     - Array of wild-type integrated graph edge records split from the
       wild-type integrated graph. This file is saved into `wt_output_dir`.

4. A mutant node-only JSON file
   - mut_integrate_nodes_{mut_protein_name}.json
     - Array of mutant integrated graph node records split from the mutant
       integrated graph. This file is saved into `mut_output_dir`.

5. A mutant edge-only JSON file
   - mut_integrate_edges_{mut_protein_name}.json
     - Array of mutant integrated graph edge records split from the mutant
       integrated graph. This file is saved into `mut_output_dir`.

6. A log file
   - log.txt
     - Processing log containing informational messages and errors. This file
       is saved into both output directories.

When `--save_extra_outputs` is enabled, mut-batch may also keep intermediate files
generated by the enabled workflow steps:

7. Cleaned Stockholm MSA files
   - cleaned_{wt_msa_name}.sto
     - Cleaned wild-type MSA in Stockholm format. This file is generated only
       when `--wt_input_msa` is provided.
   - cleaned_{mut_msa_name}.sto
     - Cleaned mutant MSA in Stockholm format. This file is generated only when
       `--mut_input_msa` is provided.

8. Profile HMM files
   - hmm_profile_{wt_msa_name}.hmm
     - Wild-type HMM profile generated from the cleaned Stockholm MSA. This file
       is generated only when `--wt_input_msa` is provided.
   - hmm_profile_{mut_msa_name}.hmm
     - Mutant HMM profile generated from the cleaned Stockholm MSA. This file is
       generated only when `--mut_input_msa` is provided.

9. Substrate structure files in SDF format
   - {substrate_structure_name}.sdf
     - Generated 3D substrate conformer files. These files are generated in both
       output directories only when `--substrate_names` is provided and substrate
       structure generation succeeds.

10. Docked substrate structure files in SDF format
    - docked_{substrate_name}.sdf
      - Docked SDF file for each substrate in the selected docking result. These
        files are generated only when `--substrate_names` is provided and docking
        succeeds.

11. Docked protein-substrate complex structure files
    - docked_{protein_name}_{substrate_names}.cif
      - Docked protein-substrate complex structure in CIF format.
    - docked_{protein_name}_{substrate_names}.pdb
      - Docked protein-substrate complex structure in PDB format.
      - These files are generated only when `--substrate_names` is provided and
        docking succeeds.


# output report schema:

The JSON report contains the following fields:

   - "report_type"
     - Data type: string
     - Expected value: "enzywizard_mut_integrate"
     - Description: The field 'report_type' indicates the type of report ('report': http://purl.obolibrary.org/obo/IAO_0000088) generated by the EnzyWizard-Mut-Integrate software.

   - "cleaned_amino_acid_substitution"
     - Data type: string
     - Description: The field 'cleaned_amino_acid_substitution' indicates the amino acid substitution ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) in the cleaned protein structure ('protein structure': http://edamontology.org/data_1537), using one-letter codes ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) to represent. Multiple substitutions are separated by semicolons.

   - "overall_statistics"
     - Data type: object
     - Description: The field 'overall_statistics' indicates the overall summary statistics ('statistics': http://purl.obolibrary.org/obo/STATO_0000039) comparing the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537) and the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537), integrated from EnzyWizard reports ('report': http://purl.obolibrary.org/obo/IAO_0000088).

     The "overall_statistics" object may contain:

     - "wild_type_sequence_length"
       - Data type: integer
       - Description: The field 'wild_type_sequence_length' indicates the sequence length ('sequence length': http://edamontology.org/data_1249), measured as the number of amino acid residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) in the cleaned protein sequence ('protein sequence': http://edamontology.org/data_2976) in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537).

     - "mutant_sequence_length"
       - Data type: integer
       - Description: The field 'mutant_sequence_length' indicates the sequence length ('sequence length': http://edamontology.org/data_1249), measured as the number of amino acid residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) in the cleaned protein sequence ('protein sequence': http://edamontology.org/data_2976) in the mutant protein structure ('protein structure': http://edamontology.org/data_1537).

     - "difference_sequence_length"
       - Data type: integer
       - Description: The field 'difference_sequence_length' indicates the difference between the mutant value and the wild-type value for the sequence length ('sequence length': http://edamontology.org/data_1249), measured as the number of amino acid residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) in the cleaned protein sequence ('protein sequence': http://edamontology.org/data_2976).

     - "wild_type_total_molecular_weight"
       - Data type: number
       - Description: The field 'wild_type_total_molecular_weight' indicates the total molecular weight, calculated as the sum of residue molecular weights ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) across the protein sequence ('protein sequence': http://edamontology.org/data_2976) in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: daltons (Da) ('dalton': http://qudt.org/vocab/unit/DA).

     - "mutant_total_molecular_weight"
       - Data type: number
       - Description: The field 'mutant_total_molecular_weight' indicates the total molecular weight, calculated as the sum of residue molecular weights ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) across the protein sequence ('protein sequence': http://edamontology.org/data_2976) in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: daltons (Da) ('dalton': http://qudt.org/vocab/unit/DA).

     - "difference_total_molecular_weight"
       - Data type: number
       - Description: The field 'difference_total_molecular_weight' indicates the difference between the mutant value and the wild-type value for the total molecular weight, calculated as the sum of residue molecular weights ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) across the protein sequence ('protein sequence': http://edamontology.org/data_2976). Unit: daltons (Da) ('dalton': http://qudt.org/vocab/unit/DA).

     - "wild_type_total_net_charge"
       - Data type: number
       - Description: The field 'wild_type_total_net_charge' indicates the total net charge, calculated as the sum of residue electric charges ('electric charge': https://goldbook.iupac.org/terms/view/E01923) across the protein sequence ('protein sequence': http://edamontology.org/data_2976) in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "mutant_total_net_charge"
       - Data type: number
       - Description: The field 'mutant_total_net_charge' indicates the total net charge, calculated as the sum of residue electric charges ('electric charge': https://goldbook.iupac.org/terms/view/E01923) across the protein sequence ('protein sequence': http://edamontology.org/data_2976) in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "difference_total_net_charge"
       - Data type: number
       - Description: The field 'difference_total_net_charge' indicates the difference between the mutant value and the wild-type value for the total net charge, calculated as the sum of residue electric charges ('electric charge': https://goldbook.iupac.org/terms/view/E01923) across the protein sequence ('protein sequence': http://edamontology.org/data_2976). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "wild_type_total_residue_volume"
       - Data type: number
       - Description: The field 'wild_type_total_residue_volume' indicates the total residue volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918), calculated as the sum of residue volumes across the protein sequence ('protein sequence': http://edamontology.org/data_2976) in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "mutant_total_residue_volume"
       - Data type: number
       - Description: The field 'mutant_total_residue_volume' indicates the total residue volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918), calculated as the sum of residue volumes across the protein sequence ('protein sequence': http://edamontology.org/data_2976) in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "difference_total_residue_volume"
       - Data type: number
       - Description: The field 'difference_total_residue_volume' indicates the difference between the mutant value and the wild-type value for the total residue volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918), calculated as the sum of residue volumes across the protein sequence ('protein sequence': http://edamontology.org/data_2976). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "wild_type_max_3d_diameter"
       - Data type: number
       - Description: The field 'wild_type_max_3d_diameter' indicates the maximum three-dimensional diameter ('diameter': http://purl.obolibrary.org/obo/PATO_0001334), calculated as the maximum pairwise distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) between residue alpha-carbon coordinates in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "mutant_max_3d_diameter"
       - Data type: number
       - Description: The field 'mutant_max_3d_diameter' indicates the maximum three-dimensional diameter ('diameter': http://purl.obolibrary.org/obo/PATO_0001334), calculated as the maximum pairwise distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) between residue alpha-carbon coordinates in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "difference_max_3d_diameter"
       - Data type: number
       - Description: The field 'difference_max_3d_diameter' indicates the difference between the mutant value and the wild-type value for the maximum three-dimensional diameter ('diameter': http://purl.obolibrary.org/obo/PATO_0001334), calculated as the maximum pairwise distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) between residue alpha-carbon coordinates. Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "wild_type_radius_of_gyration"
       - Data type: number
       - Description: The field 'wild_type_radius_of_gyration' indicates the radius of gyration ('radius of gyration': https://goldbook.iupac.org/terms/view/R05121) calculated from residue alpha-carbon coordinates in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "mutant_radius_of_gyration"
       - Data type: number
       - Description: The field 'mutant_radius_of_gyration' indicates the radius of gyration ('radius of gyration': https://goldbook.iupac.org/terms/view/R05121) calculated from residue alpha-carbon coordinates in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "difference_radius_of_gyration"
       - Data type: number
       - Description: The field 'difference_radius_of_gyration' indicates the difference between the mutant value and the wild-type value for the radius of gyration ('radius of gyration': https://goldbook.iupac.org/terms/view/R05121) calculated from residue alpha-carbon coordinates. Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "wild_type_asphericity"
       - Data type: number
       - Description: The field 'wild_type_asphericity' indicates the asphericity ('asphericity': https://www.rdkit.org/docs/source/rdkit.Chem.rdMolDescriptors.html) calculated from alpha-carbon coordinate covariance eigenvalues in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "mutant_asphericity"
       - Data type: number
       - Description: The field 'mutant_asphericity' indicates the asphericity ('asphericity': https://www.rdkit.org/docs/source/rdkit.Chem.rdMolDescriptors.html) calculated from alpha-carbon coordinate covariance eigenvalues in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "difference_asphericity"
       - Data type: number
       - Description: The field 'difference_asphericity' indicates the difference between the mutant value and the wild-type value for the asphericity ('asphericity': https://www.rdkit.org/docs/source/rdkit.Chem.rdMolDescriptors.html) calculated from alpha-carbon coordinate covariance eigenvalues. Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "wild_type_spherocity"
       - Data type: number
       - Description: The field 'wild_type_spherocity' indicates the spherocity ('spherocity': https://www.rdkit.org/docs/source/rdkit.Chem.rdMolDescriptors.html) calculated from alpha-carbon coordinate covariance eigenvalues in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "mutant_spherocity"
       - Data type: number
       - Description: The field 'mutant_spherocity' indicates the spherocity ('spherocity': https://www.rdkit.org/docs/source/rdkit.Chem.rdMolDescriptors.html) calculated from alpha-carbon coordinate covariance eigenvalues in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "difference_spherocity"
       - Data type: number
       - Description: The field 'difference_spherocity' indicates the difference between the mutant value and the wild-type value for the spherocity ('spherocity': https://www.rdkit.org/docs/source/rdkit.Chem.rdMolDescriptors.html) calculated from alpha-carbon coordinate covariance eigenvalues. Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "wild_type_principal_moment_ratio"
       - Data type: number
       - Description: The field 'wild_type_principal_moment_ratio' indicates the ratio of the largest to the smallest principal moments ('moment of inertia': https://goldbook.iupac.org/terms/view/M04006) calculated from alpha-carbon coordinate covariance eigenvalues in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "mutant_principal_moment_ratio"
       - Data type: number
       - Description: The field 'mutant_principal_moment_ratio' indicates the ratio of the largest to the smallest principal moments ('moment of inertia': https://goldbook.iupac.org/terms/view/M04006) calculated from alpha-carbon coordinate covariance eigenvalues in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "difference_principal_moment_ratio"
       - Data type: number
       - Description: The field 'difference_principal_moment_ratio' indicates the difference between the mutant value and the wild-type value for the ratio of the largest to the smallest principal moments ('moment of inertia': https://goldbook.iupac.org/terms/view/M04006) calculated from alpha-carbon coordinate covariance eigenvalues. Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "wild_type_bounding_box_volume"
       - Data type: number
       - Description: The field 'wild_type_bounding_box_volume' indicates the volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of the axis-aligned bounding box ('bounding box': https://developer.mozilla.org/en-US/docs/Glossary/Bounding_box) enclosing all residue alpha-carbon coordinates in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "mutant_bounding_box_volume"
       - Data type: number
       - Description: The field 'mutant_bounding_box_volume' indicates the volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of the axis-aligned bounding box ('bounding box': https://developer.mozilla.org/en-US/docs/Glossary/Bounding_box) enclosing all residue alpha-carbon coordinates in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "difference_bounding_box_volume"
       - Data type: number
       - Description: The field 'difference_bounding_box_volume' indicates the difference between the mutant value and the wild-type value for the volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of the axis-aligned bounding box ('bounding box': https://developer.mozilla.org/en-US/docs/Glossary/Bounding_box) enclosing all residue alpha-carbon coordinates. Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "wild_type_mean_pairwise_ca_distance"
       - Data type: number
       - Description: The field 'wild_type_mean_pairwise_ca_distance' indicates the mean pairwise alpha-carbon distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) between residue alpha-carbon coordinates in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "mutant_mean_pairwise_ca_distance"
       - Data type: number
       - Description: The field 'mutant_mean_pairwise_ca_distance' indicates the mean pairwise alpha-carbon distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) between residue alpha-carbon coordinates in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "difference_mean_pairwise_ca_distance"
       - Data type: number
       - Description: The field 'difference_mean_pairwise_ca_distance' indicates the difference between the mutant value and the wild-type value for the mean pairwise alpha-carbon distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) between residue alpha-carbon coordinates. Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "wild_type_std_pairwise_ca_distance"
       - Data type: number
       - Description: The field 'wild_type_std_pairwise_ca_distance' indicates the standard deviation ('standard deviation': http://purl.obolibrary.org/obo/STATO_0000237) of pairwise alpha-carbon distances ('distance': http://purl.obolibrary.org/obo/PATO_0000040) between residue alpha-carbon coordinates in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "mutant_std_pairwise_ca_distance"
       - Data type: number
       - Description: The field 'mutant_std_pairwise_ca_distance' indicates the standard deviation ('standard deviation': http://purl.obolibrary.org/obo/STATO_0000237) of pairwise alpha-carbon distances ('distance': http://purl.obolibrary.org/obo/PATO_0000040) between residue alpha-carbon coordinates in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "difference_std_pairwise_ca_distance"
       - Data type: number
       - Description: The field 'difference_std_pairwise_ca_distance' indicates the difference between the mutant value and the wild-type value for the standard deviation ('standard deviation': http://purl.obolibrary.org/obo/STATO_0000237) of pairwise alpha-carbon distances ('distance': http://purl.obolibrary.org/obo/PATO_0000040) between residue alpha-carbon coordinates. Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "wild_type_hydrophobic_cluster_count"
       - Data type: integer
       - Description: The field 'wild_type_hydrophobic_cluster_count' indicates the count of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_hydrophobic_cluster_count"
       - Data type: integer
       - Description: The field 'mutant_hydrophobic_cluster_count' indicates the count of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_hydrophobic_cluster_count"
       - Data type: integer
       - Description: The field 'difference_hydrophobic_cluster_count' indicates the difference between the mutant count and the wild-type count of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/).

     - "wild_type_max_hydrophobic_cluster_area"
       - Data type: number
       - Description: The field 'wild_type_max_hydrophobic_cluster_area' indicates the maximum area ('area': http://purl.obolibrary.org/obo/PATO_0001323) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537). Unit: square angstroms (Å^2) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "mutant_max_hydrophobic_cluster_area"
       - Data type: number
       - Description: The field 'mutant_max_hydrophobic_cluster_area' indicates the maximum area ('area': http://purl.obolibrary.org/obo/PATO_0001323) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537). Unit: square angstroms (Å^2) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "difference_max_hydrophobic_cluster_area"
       - Data type: number
       - Description: The field 'difference_max_hydrophobic_cluster_area' indicates the difference between the mutant maximum area and the wild-type maximum area ('area': http://purl.obolibrary.org/obo/PATO_0001323) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/). Unit: square angstroms (Å^2) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "wild_type_total_hydrophobic_cluster_area"
       - Data type: number
       - Description: The field 'wild_type_total_hydrophobic_cluster_area' indicates the total area ('area': http://purl.obolibrary.org/obo/PATO_0001323) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537). Unit: square angstroms (Å^2) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "mutant_total_hydrophobic_cluster_area"
       - Data type: number
       - Description: The field 'mutant_total_hydrophobic_cluster_area' indicates the total area ('area': http://purl.obolibrary.org/obo/PATO_0001323) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537). Unit: square angstroms (Å^2) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "difference_total_hydrophobic_cluster_area"
       - Data type: number
       - Description: The field 'difference_total_hydrophobic_cluster_area' indicates the difference between the mutant total area and the wild-type total area ('area': http://purl.obolibrary.org/obo/PATO_0001323) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/). Unit: square angstroms (Å^2) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "wild_type_disordered_region_count"
       - Data type: integer
       - Description: The field 'wild_type_disordered_region_count' indicates the count of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_disordered_region_count"
       - Data type: integer
       - Description: The field 'mutant_disordered_region_count' indicates the count of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_disordered_region_count"
       - Data type: integer
       - Description: The field 'difference_disordered_region_count' indicates the difference between the mutant value and the wild-type value for the count of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology).

     - "wild_type_max_disordered_region_length"
       - Data type: integer
       - Description: The field 'wild_type_max_disordered_region_length' indicates the maximum sequence length ('sequence length': http://edamontology.org/data_1249) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_max_disordered_region_length"
       - Data type: integer
       - Description: The field 'mutant_max_disordered_region_length' indicates the maximum sequence length ('sequence length': http://edamontology.org/data_1249) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_max_disordered_region_length"
       - Data type: integer
       - Description: The field 'difference_max_disordered_region_length' indicates the difference between the mutant value and the wild-type value for the maximum sequence length ('sequence length': http://edamontology.org/data_1249) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology).

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
       - Description: The field 'wild_type_binding_pocket_count' indicates the count of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/pocket_specification.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_binding_pocket_count"
       - Data type: integer
       - Description: The field 'mutant_binding_pocket_count' indicates the count of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/pocket_specification.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_binding_pocket_count"
       - Data type: integer
       - Description: The field 'difference_binding_pocket_count' indicates the difference between the mutant value and the wild-type value for the count of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/pocket_specification.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL).

     - "wild_type_max_binding_pocket_volume"
       - Data type: number
       - Description: The field 'wild_type_max_binding_pocket_volume' indicates the maximum volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "mutant_max_binding_pocket_volume"
       - Data type: number
       - Description: The field 'mutant_max_binding_pocket_volume' indicates the maximum volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "difference_max_binding_pocket_volume"
       - Data type: number
       - Description: The field 'difference_max_binding_pocket_volume' indicates the difference between the mutant value and the wild-type value for the maximum volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "wild_type_total_binding_pocket_volume"
       - Data type: number
       - Description: The field 'wild_type_total_binding_pocket_volume' indicates the total volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "mutant_total_binding_pocket_volume"
       - Data type: number
       - Description: The field 'mutant_total_binding_pocket_volume' indicates the total volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "difference_total_binding_pocket_volume"
       - Data type: number
       - Description: The field 'difference_total_binding_pocket_volume' indicates the difference between the mutant value and the wild-type value for the total volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "wild_type_total_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_total_potential_energy' indicates the total potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) calculated from the protein structure ('protein structure': http://edamontology.org/data_1537) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "mutant_total_potential_energy"
       - Data type: number
       - Description: The field 'mutant_total_potential_energy' indicates the total potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) calculated from the protein structure ('protein structure': http://edamontology.org/data_1537) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "difference_total_potential_energy"
       - Data type: number
       - Description: The field 'difference_total_potential_energy' indicates the difference between the mutant value and the wild-type value for the total potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) calculated from the protein structure ('protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "wild_type_harmonic_bond_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_harmonic_bond_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the harmonic bond force term ('harmonic bond force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#harmonicbondforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "mutant_harmonic_bond_potential_energy"
       - Data type: number
       - Description: The field 'mutant_harmonic_bond_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the harmonic bond force term ('harmonic bond force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#harmonicbondforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "difference_harmonic_bond_potential_energy"
       - Data type: number
       - Description: The field 'difference_harmonic_bond_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the harmonic bond force term ('harmonic bond force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#harmonicbondforce). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "wild_type_harmonic_angle_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_harmonic_angle_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the harmonic angle force term ('harmonic angle force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#harmonicangleforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "mutant_harmonic_angle_potential_energy"
       - Data type: number
       - Description: The field 'mutant_harmonic_angle_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the harmonic angle force term ('harmonic angle force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#harmonicangleforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "difference_harmonic_angle_potential_energy"
       - Data type: number
       - Description: The field 'difference_harmonic_angle_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the harmonic angle force term ('harmonic angle force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#harmonicangleforce). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "wild_type_custom_bond_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_custom_bond_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom bond force term ('custom bond force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#custombondforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "mutant_custom_bond_potential_energy"
       - Data type: number
       - Description: The field 'mutant_custom_bond_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom bond force term ('custom bond force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#custombondforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "difference_custom_bond_potential_energy"
       - Data type: number
       - Description: The field 'difference_custom_bond_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom bond force term ('custom bond force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#custombondforce). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "wild_type_custom_torsion_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_custom_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom torsion force term ('custom torsion force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#customtorsionforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "mutant_custom_torsion_potential_energy"
       - Data type: number
       - Description: The field 'mutant_custom_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom torsion force term ('custom torsion force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#customtorsionforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "difference_custom_torsion_potential_energy"
       - Data type: number
       - Description: The field 'difference_custom_torsion_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom torsion force term ('custom torsion force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#customtorsionforce). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "wild_type_custom_nonbonded_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_custom_nonbonded_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom nonbonded force term ('custom nonbonded force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#customnonbondedforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "mutant_custom_nonbonded_potential_energy"
       - Data type: number
       - Description: The field 'mutant_custom_nonbonded_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom nonbonded force term ('custom nonbonded force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#customnonbondedforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "difference_custom_nonbonded_potential_energy"
       - Data type: number
       - Description: The field 'difference_custom_nonbonded_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom nonbonded force term ('custom nonbonded force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#customnonbondedforce). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "wild_type_nonbonded_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_nonbonded_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the nonbonded force term ('nonbonded force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#nonbondedforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "mutant_nonbonded_potential_energy"
       - Data type: number
       - Description: The field 'mutant_nonbonded_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the nonbonded force term ('nonbonded force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#nonbondedforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "difference_nonbonded_potential_energy"
       - Data type: number
       - Description: The field 'difference_nonbonded_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the nonbonded force term ('nonbonded force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#nonbondedforce). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "wild_type_periodic_torsion_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_periodic_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the periodic torsion force term ('periodic torsion force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#periodictorsionforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "mutant_periodic_torsion_potential_energy"
       - Data type: number
       - Description: The field 'mutant_periodic_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the periodic torsion force term ('periodic torsion force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#periodictorsionforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "difference_periodic_torsion_potential_energy"
       - Data type: number
       - Description: The field 'difference_periodic_torsion_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the periodic torsion force term ('periodic torsion force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#periodictorsionforce). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "wild_type_cmap_torsion_potential_energy"
       - Data type: number
       - Description: The field 'wild_type_cmap_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the CMAP torsion force term ('CMAP torsion force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#cmaptorsionforce) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "mutant_cmap_torsion_potential_energy"
       - Data type: number
       - Description: The field 'mutant_cmap_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the CMAP torsion force term ('CMAP torsion force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#cmaptorsionforce) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "difference_cmap_torsion_potential_energy"
       - Data type: number
       - Description: The field 'difference_cmap_torsion_potential_energy' indicates the difference between the mutant value and the wild-type value for the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the CMAP torsion force term ('CMAP torsion force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#cmaptorsionforce). Unit: kilojoules per mole (kJ/mol) ('kilojoule per mole': http://qudt.org/vocab/unit/KiloJ-PER-MOL).

     - "wild_type_enzyme_substrate_binding_affinity"
       - Data type: number
       - Description: The field 'wild_type_enzyme_substrate_binding_affinity' indicates the predicted binding affinity ('binding affinity': https://vina.scripps.edu/manual/#output) calculated by AutoDock Vina software ('AutoDock Vina': https://bio.tools/autodock_vina) from docking ('docking': https://goldbook.iupac.org/terms/view/11437) of the wild-type enzyme-substrate complex ('enzyme': https://purl.dsmz.de/schema/Enzyme; 'substrate': https://purl.dsmz.de/schema/Substrate; 'complex': https://goldbook.iupac.org/terms/view/C01203). Unit: kilocalories per mole (kcal/mol) ('kilocalorie': http://qudt.org/vocab/unit/KiloCAL; 'mole': http://qudt.org/vocab/unit/MOL).

     - "mutant_enzyme_substrate_binding_affinity"
       - Data type: number
       - Description: The field 'mutant_enzyme_substrate_binding_affinity' indicates the predicted binding affinity ('binding affinity': https://vina.scripps.edu/manual/#output) calculated by AutoDock Vina software ('AutoDock Vina': https://bio.tools/autodock_vina) from docking ('docking': https://goldbook.iupac.org/terms/view/11437) of the mutant enzyme-substrate complex ('enzyme': https://purl.dsmz.de/schema/Enzyme; 'substrate': https://purl.dsmz.de/schema/Substrate; 'complex': https://goldbook.iupac.org/terms/view/C01203). Unit: kilocalories per mole (kcal/mol) ('kilocalorie': http://qudt.org/vocab/unit/KiloCAL; 'mole': http://qudt.org/vocab/unit/MOL).

     - "difference_enzyme_substrate_binding_affinity"
       - Data type: number
       - Description: The field 'difference_enzyme_substrate_binding_affinity' indicates the difference between the mutant predicted binding affinity and the wild-type predicted binding affinity ('binding affinity': https://vina.scripps.edu/manual/#output) calculated by AutoDock Vina software ('AutoDock Vina': https://bio.tools/autodock_vina) from docking ('docking': https://goldbook.iupac.org/terms/view/11437) of enzyme-substrate complexes ('enzyme': https://purl.dsmz.de/schema/Enzyme; 'substrate': https://purl.dsmz.de/schema/Substrate; 'complex': https://goldbook.iupac.org/terms/view/C01203). Unit: kilocalories per mole (kcal/mol) ('kilocalorie': http://qudt.org/vocab/unit/KiloCAL; 'mole': http://qudt.org/vocab/unit/MOL).

     - "wild_type_hydrogen_bond_count"
       - Data type: integer
       - Description: The field 'wild_type_hydrogen_bond_count' indicates the count of hydrogen bonds ('hydrogen bond': https://goldbook.iupac.org/terms/view/H02899) in the wild-type integrated graph.

     - "mutant_hydrogen_bond_count"
       - Data type: integer
       - Description: The field 'mutant_hydrogen_bond_count' indicates the count of hydrogen bonds ('hydrogen bond': https://goldbook.iupac.org/terms/view/H02899) in the mutant integrated graph.

     - "difference_hydrogen_bond_count"
       - Data type: integer
       - Description: The field 'difference_hydrogen_bond_count' indicates the difference between the mutant count and the wild-type count of hydrogen bonds ('hydrogen bond': https://goldbook.iupac.org/terms/view/H02899).

     - "wild_type_ionic_bond_count"
       - Data type: integer
       - Description: The field 'wild_type_ionic_bond_count' indicates the count of ionic bonds ('ionic bond': https://goldbook.iupac.org/terms/view/IT07058) in the wild-type integrated graph.

     - "mutant_ionic_bond_count"
       - Data type: integer
       - Description: The field 'mutant_ionic_bond_count' indicates the count of ionic bonds ('ionic bond': https://goldbook.iupac.org/terms/view/IT07058) in the mutant integrated graph.

     - "difference_ionic_bond_count"
       - Data type: integer
       - Description: The field 'difference_ionic_bond_count' indicates the difference between the mutant count and the wild-type count of ionic bonds ('ionic bond': https://goldbook.iupac.org/terms/view/IT07058).

     - "wild_type_van_der_waals_contact_count"
       - Data type: integer
       - Description: The field 'wild_type_van_der_waals_contact_count' indicates the count of van der Waals contacts ('van der Waals forces': https://goldbook.iupac.org/terms/view/V06597) in the wild-type integrated graph.

     - "mutant_van_der_waals_contact_count"
       - Data type: integer
       - Description: The field 'mutant_van_der_waals_contact_count' indicates the count of van der Waals contacts ('van der Waals forces': https://goldbook.iupac.org/terms/view/V06597) in the mutant integrated graph.

     - "difference_van_der_waals_contact_count"
       - Data type: integer
       - Description: The field 'difference_van_der_waals_contact_count' indicates the difference between the mutant count and the wild-type count of van der Waals contacts ('van der Waals forces': https://goldbook.iupac.org/terms/view/V06597).

     - "wild_type_pi_pi_stacking_count"
       - Data type: integer
       - Description: The field 'wild_type_pi_pi_stacking_count' indicates the count of pi-pi stacking interactions ('pi-pi stacking': https://goldbook.iupac.org/terms/view/13861) in the wild-type integrated graph.

     - "mutant_pi_pi_stacking_count"
       - Data type: integer
       - Description: The field 'mutant_pi_pi_stacking_count' indicates the count of pi-pi stacking interactions ('pi-pi stacking': https://goldbook.iupac.org/terms/view/13861) in the mutant integrated graph.

     - "difference_pi_pi_stacking_count"
       - Data type: integer
       - Description: The field 'difference_pi_pi_stacking_count' indicates the difference between the mutant count and the wild-type count of pi-pi stacking interactions ('pi-pi stacking': https://goldbook.iupac.org/terms/view/13861).

     - "wild_type_pi_cation_interaction_count"
       - Data type: integer
       - Description: The field 'wild_type_pi_cation_interaction_count' indicates the count of pi-cation interactions ('cation-pi interaction': https://goldbook.iupac.org/terms/view/08154) in the wild-type integrated graph.

     - "mutant_pi_cation_interaction_count"
       - Data type: integer
       - Description: The field 'mutant_pi_cation_interaction_count' indicates the count of pi-cation interactions ('cation-pi interaction': https://goldbook.iupac.org/terms/view/08154) in the mutant integrated graph.

     - "difference_pi_cation_interaction_count"
       - Data type: integer
       - Description: The field 'difference_pi_cation_interaction_count' indicates the difference between the mutant count and the wild-type count of pi-cation interactions ('cation-pi interaction': https://goldbook.iupac.org/terms/view/08154).

     - "wild_type_disulfide_bond_count"
       - Data type: integer
       - Description: The field 'wild_type_disulfide_bond_count' indicates the count of disulfide bonds ('disulfide bond': https://www.uniprot.org/help/disulfid) in the wild-type integrated graph.

     - "mutant_disulfide_bond_count"
       - Data type: integer
       - Description: The field 'mutant_disulfide_bond_count' indicates the count of disulfide bonds ('disulfide bond': https://www.uniprot.org/help/disulfid) in the mutant integrated graph.

     - "difference_disulfide_bond_count"
       - Data type: integer
       - Description: The field 'difference_disulfide_bond_count' indicates the difference between the mutant count and the wild-type count of disulfide bonds ('disulfide bond': https://www.uniprot.org/help/disulfid).

     - "wild_type_residue_name_alanine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_alanine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is alanine ('alanine': http://purl.obolibrary.org/obo/CHEBI_16977) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_alanine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_alanine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is alanine ('alanine': http://purl.obolibrary.org/obo/CHEBI_16977) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_alanine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_alanine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is alanine ('alanine': http://purl.obolibrary.org/obo/CHEBI_16977).

     - "wild_type_residue_name_cysteine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_cysteine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is cysteine ('cysteine': http://purl.obolibrary.org/obo/CHEBI_15356) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_cysteine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_cysteine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is cysteine ('cysteine': http://purl.obolibrary.org/obo/CHEBI_15356) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_cysteine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_cysteine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is cysteine ('cysteine': http://purl.obolibrary.org/obo/CHEBI_15356).

     - "wild_type_residue_name_aspartic_acid_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_aspartic_acid_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is aspartic acid ('aspartic acid': http://purl.obolibrary.org/obo/CHEBI_22660) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_aspartic_acid_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_aspartic_acid_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is aspartic acid ('aspartic acid': http://purl.obolibrary.org/obo/CHEBI_22660) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_aspartic_acid_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_aspartic_acid_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is aspartic acid ('aspartic acid': http://purl.obolibrary.org/obo/CHEBI_22660).

     - "wild_type_residue_name_glutamic_acid_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_glutamic_acid_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is glutamic acid ('glutamic acid': http://purl.obolibrary.org/obo/CHEBI_18237) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_glutamic_acid_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_glutamic_acid_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is glutamic acid ('glutamic acid': http://purl.obolibrary.org/obo/CHEBI_18237) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_glutamic_acid_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_glutamic_acid_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is glutamic acid ('glutamic acid': http://purl.obolibrary.org/obo/CHEBI_18237).

     - "wild_type_residue_name_phenylalanine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_phenylalanine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is phenylalanine ('phenylalanine': http://purl.obolibrary.org/obo/CHEBI_28044) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_phenylalanine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_phenylalanine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is phenylalanine ('phenylalanine': http://purl.obolibrary.org/obo/CHEBI_28044) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_phenylalanine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_phenylalanine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is phenylalanine ('phenylalanine': http://purl.obolibrary.org/obo/CHEBI_28044).

     - "wild_type_residue_name_glycine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_glycine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is glycine ('glycine': http://purl.obolibrary.org/obo/CHEBI_15428) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_glycine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_glycine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is glycine ('glycine': http://purl.obolibrary.org/obo/CHEBI_15428) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_glycine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_glycine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is glycine ('glycine': http://purl.obolibrary.org/obo/CHEBI_15428).

     - "wild_type_residue_name_histidine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_histidine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is histidine ('histidine': http://purl.obolibrary.org/obo/CHEBI_27570) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_histidine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_histidine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is histidine ('histidine': http://purl.obolibrary.org/obo/CHEBI_27570) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_histidine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_histidine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is histidine ('histidine': http://purl.obolibrary.org/obo/CHEBI_27570).

     - "wild_type_residue_name_isoleucine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_isoleucine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is isoleucine ('isoleucine': http://purl.obolibrary.org/obo/CHEBI_24898) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_isoleucine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_isoleucine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is isoleucine ('isoleucine': http://purl.obolibrary.org/obo/CHEBI_24898) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_isoleucine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_isoleucine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is isoleucine ('isoleucine': http://purl.obolibrary.org/obo/CHEBI_24898).

     - "wild_type_residue_name_lysine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_lysine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is lysine ('lysine': http://purl.obolibrary.org/obo/CHEBI_25094) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_lysine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_lysine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is lysine ('lysine': http://purl.obolibrary.org/obo/CHEBI_25094) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_lysine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_lysine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is lysine ('lysine': http://purl.obolibrary.org/obo/CHEBI_25094).

     - "wild_type_residue_name_leucine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_leucine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is leucine ('leucine': http://purl.obolibrary.org/obo/CHEBI_25017) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_leucine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_leucine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is leucine ('leucine': http://purl.obolibrary.org/obo/CHEBI_25017) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_leucine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_leucine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is leucine ('leucine': http://purl.obolibrary.org/obo/CHEBI_25017).

     - "wild_type_residue_name_methionine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_methionine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is methionine ('methionine': http://purl.obolibrary.org/obo/CHEBI_16811) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_methionine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_methionine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is methionine ('methionine': http://purl.obolibrary.org/obo/CHEBI_16811) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_methionine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_methionine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is methionine ('methionine': http://purl.obolibrary.org/obo/CHEBI_16811).

     - "wild_type_residue_name_asparagine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_asparagine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is asparagine ('asparagine': http://purl.obolibrary.org/obo/CHEBI_22653) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_asparagine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_asparagine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is asparagine ('asparagine': http://purl.obolibrary.org/obo/CHEBI_22653) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_asparagine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_asparagine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is asparagine ('asparagine': http://purl.obolibrary.org/obo/CHEBI_22653).

     - "wild_type_residue_name_proline_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_proline_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is proline ('proline': http://purl.obolibrary.org/obo/CHEBI_17203) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_proline_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_proline_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is proline ('proline': http://purl.obolibrary.org/obo/CHEBI_17203) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_proline_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_proline_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is proline ('proline': http://purl.obolibrary.org/obo/CHEBI_17203).

     - "wild_type_residue_name_glutamine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_glutamine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is glutamine ('glutamine': http://purl.obolibrary.org/obo/CHEBI_18050) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_glutamine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_glutamine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is glutamine ('glutamine': http://purl.obolibrary.org/obo/CHEBI_18050) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_glutamine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_glutamine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is glutamine ('glutamine': http://purl.obolibrary.org/obo/CHEBI_18050).

     - "wild_type_residue_name_arginine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_arginine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is arginine ('arginine': http://purl.obolibrary.org/obo/CHEBI_29016) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_arginine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_arginine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is arginine ('arginine': http://purl.obolibrary.org/obo/CHEBI_29016) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_arginine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_arginine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is arginine ('arginine': http://purl.obolibrary.org/obo/CHEBI_29016).

     - "wild_type_residue_name_serine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_serine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is serine ('serine': http://purl.obolibrary.org/obo/CHEBI_17822) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_serine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_serine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is serine ('serine': http://purl.obolibrary.org/obo/CHEBI_17822) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_serine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_serine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is serine ('serine': http://purl.obolibrary.org/obo/CHEBI_17822).

     - "wild_type_residue_name_threonine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_threonine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is threonine ('threonine': http://purl.obolibrary.org/obo/CHEBI_16857) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_threonine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_threonine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is threonine ('threonine': http://purl.obolibrary.org/obo/CHEBI_16857) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_threonine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_threonine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is threonine ('threonine': http://purl.obolibrary.org/obo/CHEBI_16857).

     - "wild_type_residue_name_valine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_valine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is valine ('valine': http://purl.obolibrary.org/obo/CHEBI_27266) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_valine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_valine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is valine ('valine': http://purl.obolibrary.org/obo/CHEBI_27266) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_valine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_valine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is valine ('valine': http://purl.obolibrary.org/obo/CHEBI_27266).

     - "wild_type_residue_name_tryptophan_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_tryptophan_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is tryptophan ('tryptophan': http://purl.obolibrary.org/obo/CHEBI_27897) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_tryptophan_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_tryptophan_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is tryptophan ('tryptophan': http://purl.obolibrary.org/obo/CHEBI_27897) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_tryptophan_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_tryptophan_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is tryptophan ('tryptophan': http://purl.obolibrary.org/obo/CHEBI_27897).

     - "wild_type_residue_name_tyrosine_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_name_tyrosine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is tyrosine ('tyrosine': http://purl.obolibrary.org/obo/CHEBI_18186) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_name_tyrosine_count"
       - Data type: integer
       - Description: The field 'mutant_residue_name_tyrosine_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is tyrosine ('tyrosine': http://purl.obolibrary.org/obo/CHEBI_18186) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_name_tyrosine_count"
       - Data type: integer
       - Description: The field 'difference_residue_name_tyrosine_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) whose residue name ('residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) is tyrosine ('tyrosine': http://purl.obolibrary.org/obo/CHEBI_18186).

     - "wild_type_residue_chemical_classification_uncharged_polar_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_chemical_classification_uncharged_polar_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the uncharged polar residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'uncharged polar': https://www.imgt.org/IMGTeducation/Aide-memoire/_UK/aminoacids/IMGTclasses.html) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_chemical_classification_uncharged_polar_count"
       - Data type: integer
       - Description: The field 'mutant_residue_chemical_classification_uncharged_polar_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the uncharged polar residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'uncharged polar': https://www.imgt.org/IMGTeducation/Aide-memoire/_UK/aminoacids/IMGTclasses.html) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_chemical_classification_uncharged_polar_count"
       - Data type: integer
       - Description: The field 'difference_residue_chemical_classification_uncharged_polar_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the uncharged polar residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'uncharged polar': https://www.imgt.org/IMGTeducation/Aide-memoire/_UK/aminoacids/IMGTclasses.html).

     - "wild_type_residue_chemical_classification_positively_charged_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_chemical_classification_positively_charged_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the positively charged residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'positively charged': https://www.imgt.org/IMGTeducation/Aide-memoire/_UK/aminoacids/IMGTclasses.html) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_chemical_classification_positively_charged_count"
       - Data type: integer
       - Description: The field 'mutant_residue_chemical_classification_positively_charged_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the positively charged residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'positively charged': https://www.imgt.org/IMGTeducation/Aide-memoire/_UK/aminoacids/IMGTclasses.html) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_chemical_classification_positively_charged_count"
       - Data type: integer
       - Description: The field 'difference_residue_chemical_classification_positively_charged_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the positively charged residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'positively charged': https://www.imgt.org/IMGTeducation/Aide-memoire/_UK/aminoacids/IMGTclasses.html).

     - "wild_type_residue_chemical_classification_negatively_charged_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_chemical_classification_negatively_charged_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the negatively charged residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'negatively charged': https://www.imgt.org/IMGTeducation/Aide-memoire/_UK/aminoacids/IMGTclasses.html) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_chemical_classification_negatively_charged_count"
       - Data type: integer
       - Description: The field 'mutant_residue_chemical_classification_negatively_charged_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the negatively charged residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'negatively charged': https://www.imgt.org/IMGTeducation/Aide-memoire/_UK/aminoacids/IMGTclasses.html) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_chemical_classification_negatively_charged_count"
       - Data type: integer
       - Description: The field 'difference_residue_chemical_classification_negatively_charged_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the negatively charged residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'negatively charged': https://www.imgt.org/IMGTeducation/Aide-memoire/_UK/aminoacids/IMGTclasses.html).

     - "wild_type_residue_chemical_classification_hydrophobic_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_chemical_classification_hydrophobic_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the hydrophobic residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'hydrophobic': https://goldbook.iupac.org/terms/view/HT06964) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_chemical_classification_hydrophobic_count"
       - Data type: integer
       - Description: The field 'mutant_residue_chemical_classification_hydrophobic_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the hydrophobic residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'hydrophobic': https://goldbook.iupac.org/terms/view/HT06964) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_chemical_classification_hydrophobic_count"
       - Data type: integer
       - Description: The field 'difference_residue_chemical_classification_hydrophobic_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the hydrophobic residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'hydrophobic': https://goldbook.iupac.org/terms/view/HT06964).

     - "wild_type_residue_chemical_classification_aromatic_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_chemical_classification_aromatic_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the aromatic residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'aromatic': https://goldbook.iupac.org/terms/view/A00441) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_chemical_classification_aromatic_count"
       - Data type: integer
       - Description: The field 'mutant_residue_chemical_classification_aromatic_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the aromatic residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'aromatic': https://goldbook.iupac.org/terms/view/A00441) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_chemical_classification_aromatic_count"
       - Data type: integer
       - Description: The field 'difference_residue_chemical_classification_aromatic_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the aromatic residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'aromatic': https://goldbook.iupac.org/terms/view/A00441).

     - "wild_type_residue_chemical_classification_aliphatic_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_chemical_classification_aliphatic_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the aliphatic residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'aliphatic': https://goldbook.iupac.org/terms/view/A00217) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_chemical_classification_aliphatic_count"
       - Data type: integer
       - Description: The field 'mutant_residue_chemical_classification_aliphatic_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the aliphatic residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'aliphatic': https://goldbook.iupac.org/terms/view/A00217) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_chemical_classification_aliphatic_count"
       - Data type: integer
       - Description: The field 'difference_residue_chemical_classification_aliphatic_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the aliphatic residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'aliphatic': https://goldbook.iupac.org/terms/view/A00217).

     - "wild_type_residue_chemical_classification_heterocyclic_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_chemical_classification_heterocyclic_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the heterocyclic residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'heterocyclic': https://goldbook.iupac.org/terms/view/H02798) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_chemical_classification_heterocyclic_count"
       - Data type: integer
       - Description: The field 'mutant_residue_chemical_classification_heterocyclic_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the heterocyclic residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'heterocyclic': https://goldbook.iupac.org/terms/view/H02798) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_chemical_classification_heterocyclic_count"
       - Data type: integer
       - Description: The field 'difference_residue_chemical_classification_heterocyclic_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the heterocyclic residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'heterocyclic': https://goldbook.iupac.org/terms/view/H02798).

     - "wild_type_residue_chemical_classification_sulfur_containing_count"
       - Data type: integer
       - Description: The field 'wild_type_residue_chemical_classification_sulfur_containing_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the sulfur-containing residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'sulfur': http://purl.obolibrary.org/obo/CHEBI_26833) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_residue_chemical_classification_sulfur_containing_count"
       - Data type: integer
       - Description: The field 'mutant_residue_chemical_classification_sulfur_containing_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the sulfur-containing residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'sulfur': http://purl.obolibrary.org/obo/CHEBI_26833) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_residue_chemical_classification_sulfur_containing_count"
       - Data type: integer
       - Description: The field 'difference_residue_chemical_classification_sulfur_containing_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to the sulfur-containing residue chemical classification ('chemical classification': http://purl.obolibrary.org/obo/NCIT_C25161; 'sulfur': http://purl.obolibrary.org/obo/CHEBI_26833).

     - "wild_type_secondary_structure_unassigned_count"
       - Data type: integer
       - Description: The field 'wild_type_secondary_structure_unassigned_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) without assigned residue secondary structure ('secondary structure': http://edamontology.org/operation_1847) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_secondary_structure_unassigned_count"
       - Data type: integer
       - Description: The field 'mutant_secondary_structure_unassigned_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) without assigned residue secondary structure ('secondary structure': http://edamontology.org/operation_1847) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_secondary_structure_unassigned_count"
       - Data type: integer
       - Description: The field 'difference_secondary_structure_unassigned_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) without assigned residue secondary structure ('secondary structure': http://edamontology.org/operation_1847).

     - "wild_type_secondary_structure_alpha_helix_count"
       - Data type: integer
       - Description: The field 'wild_type_secondary_structure_alpha_helix_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to alpha-helix residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'alpha helix': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_secondary_structure_alpha_helix_count"
       - Data type: integer
       - Description: The field 'mutant_secondary_structure_alpha_helix_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to alpha-helix residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'alpha helix': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_secondary_structure_alpha_helix_count"
       - Data type: integer
       - Description: The field 'difference_secondary_structure_alpha_helix_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to alpha-helix residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'alpha helix': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

     - "wild_type_secondary_structure_beta_bridge_count"
       - Data type: integer
       - Description: The field 'wild_type_secondary_structure_beta_bridge_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to beta-bridge residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'beta bridge': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_secondary_structure_beta_bridge_count"
       - Data type: integer
       - Description: The field 'mutant_secondary_structure_beta_bridge_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to beta-bridge residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'beta bridge': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_secondary_structure_beta_bridge_count"
       - Data type: integer
       - Description: The field 'difference_secondary_structure_beta_bridge_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to beta-bridge residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'beta bridge': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

     - "wild_type_secondary_structure_extended_strand_count"
       - Data type: integer
       - Description: The field 'wild_type_secondary_structure_extended_strand_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to extended-strand residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'extended strand': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_secondary_structure_extended_strand_count"
       - Data type: integer
       - Description: The field 'mutant_secondary_structure_extended_strand_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to extended-strand residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'extended strand': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_secondary_structure_extended_strand_count"
       - Data type: integer
       - Description: The field 'difference_secondary_structure_extended_strand_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to extended-strand residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'extended strand': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

     - "wild_type_secondary_structure_three_ten_helix_count"
       - Data type: integer
       - Description: The field 'wild_type_secondary_structure_three_ten_helix_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to 3-10 helix residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; '3-10 helix': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_secondary_structure_three_ten_helix_count"
       - Data type: integer
       - Description: The field 'mutant_secondary_structure_three_ten_helix_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to 3-10 helix residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; '3-10 helix': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_secondary_structure_three_ten_helix_count"
       - Data type: integer
       - Description: The field 'difference_secondary_structure_three_ten_helix_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to 3-10 helix residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; '3-10 helix': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

     - "wild_type_secondary_structure_pi_helix_count"
       - Data type: integer
       - Description: The field 'wild_type_secondary_structure_pi_helix_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to pi-helix residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'pi helix': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_secondary_structure_pi_helix_count"
       - Data type: integer
       - Description: The field 'mutant_secondary_structure_pi_helix_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to pi-helix residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'pi helix': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_secondary_structure_pi_helix_count"
       - Data type: integer
       - Description: The field 'difference_secondary_structure_pi_helix_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to pi-helix residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'pi helix': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

     - "wild_type_secondary_structure_turn_count"
       - Data type: integer
       - Description: The field 'wild_type_secondary_structure_turn_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to turn residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'turn': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_secondary_structure_turn_count"
       - Data type: integer
       - Description: The field 'mutant_secondary_structure_turn_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to turn residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'turn': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_secondary_structure_turn_count"
       - Data type: integer
       - Description: The field 'difference_secondary_structure_turn_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to turn residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'turn': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

     - "wild_type_secondary_structure_bend_count"
       - Data type: integer
       - Description: The field 'wild_type_secondary_structure_bend_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to bend residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'bend': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) in the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

     - "mutant_secondary_structure_bend_count"
       - Data type: integer
       - Description: The field 'mutant_secondary_structure_bend_count' indicates the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to bend residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'bend': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) in the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     - "difference_secondary_structure_bend_count"
       - Data type: integer
       - Description: The field 'difference_secondary_structure_bend_count' indicates the difference between the mutant count and the wild-type count for the count of residues ('residue': http://purl.obolibrary.org/obo/GENO_0000782) assigned to bend residue secondary structures ('secondary structure': http://edamontology.org/operation_1847; 'bend': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).


   - "amino_acid_substitution_properties"
     - Data type: object
     - Description: The field 'amino_acid_substitution_properties' indicates residue properties ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606), comparing the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537) and the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     The "amino_acid_substitution_properties" object may contain:

     - "wild_type_residue_name"
       - Data type: string
     - Description: The field 'wild_type_residue_name' indicates the wild-type residue name ('residue': http://purl.obolibrary.org/obo/GENO_0000782; 'residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606), using one-letter amino-acid code ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html). For multiple substitution sites, residue names are separated by semicolons in mutation-site order.

     - "mutant_residue_name"
       - Data type: string
     - Description: The field 'mutant_residue_name' indicates the mutant residue name ('residue': http://purl.obolibrary.org/obo/GENO_0000782; 'residue name': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606), using one-letter amino-acid code ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html). For multiple substitution sites, residue names are separated by semicolons in mutation-site order.

     - "wild_type_residue_name_one_hot_encoding"
       - Data type: array
       - Description: The field 'wild_type_residue_name_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the wild-type residue name ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "mutant_residue_name_one_hot_encoding"
       - Data type: array
       - Description: The field 'mutant_residue_name_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the mutant residue name ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "difference_residue_name_one_hot_encoding"
       - Data type: array
       - Description: The field 'difference_residue_name_one_hot_encoding' indicates the difference between the mutant one-hot encoding and the wild-type one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the residue name ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_chemical_classification"
       - Data type: string
       - Description: The field 'wild_type_residue_chemical_classification' indicates the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) in the wild-type protein structure. For a residue with multiple classifications, classifications are separated by slashes; for multiple substitution sites, site-level values are separated by semicolons in mutation-site order.

     - "mutant_residue_chemical_classification"
       - Data type: string
       - Description: The field 'mutant_residue_chemical_classification' indicates the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) in the mutant protein structure. For a residue with multiple classifications, classifications are separated by slashes; for multiple substitution sites, site-level values are separated by semicolons in mutation-site order.

     - "wild_type_residue_chemical_classification_multi_hot_encoding"
       - Data type: array
       - Description: The field 'wild_type_residue_chemical_classification_multi_hot_encoding' indicates the multi-hot encoding ('multi-hot encoding': https://developers.google.com/machine-learning/crash-course/categorical-data/one-hot-encoding) of the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) in the wild-type protein structure.

     - "mutant_residue_chemical_classification_multi_hot_encoding"
       - Data type: array
       - Description: The field 'mutant_residue_chemical_classification_multi_hot_encoding' indicates the multi-hot encoding ('multi-hot encoding': https://developers.google.com/machine-learning/crash-course/categorical-data/one-hot-encoding) of the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) in the mutant protein structure.

     - "difference_residue_chemical_classification_multi_hot_encoding"
       - Data type: array
       - Description: The field 'difference_residue_chemical_classification_multi_hot_encoding' indicates the difference between the mutant multi-hot encoding and the wild-type multi-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606).

     - "wild_type_residue_secondary_structure"
       - Data type: string
     - Description: The field 'wild_type_residue_secondary_structure' indicates the wild-type residue secondary-structure code ('secondary structure': http://edamontology.org/operation_1847; 'DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) assigned to the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). For multiple substitution sites, secondary-structure codes are separated by semicolons in mutation-site order.

     - "mutant_residue_secondary_structure"
       - Data type: string
     - Description: The field 'mutant_residue_secondary_structure' indicates the mutant residue secondary-structure code ('secondary structure': http://edamontology.org/operation_1847; 'DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html) assigned to the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). For multiple substitution sites, secondary-structure codes are separated by semicolons in mutation-site order.

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
       - Description: The field 'wild_type_residue_relative_solvent_accessibility' indicates the relative solvent accessibility ('solvent accessibility': http://edamontology.org/data_1542) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "mutant_residue_relative_solvent_accessibility"
       - Data type: number
       - Description: The field 'mutant_residue_relative_solvent_accessibility' indicates the relative solvent accessibility ('solvent accessibility': http://edamontology.org/data_1542) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "difference_residue_relative_solvent_accessibility"
       - Data type: number
       - Description: The field 'difference_residue_relative_solvent_accessibility' indicates the difference between the mutant value and the wild-type value for the relative solvent accessibility ('solvent accessibility': http://edamontology.org/data_1542) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "wild_type_residue_backbone_phi_angle"
       - Data type: number
       - Description: The field 'wild_type_residue_backbone_phi_angle' indicates the backbone phi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: degrees (°) ('degree': http://qudt.org/vocab/unit/DEG).

     - "mutant_residue_backbone_phi_angle"
       - Data type: number
       - Description: The field 'mutant_residue_backbone_phi_angle' indicates the backbone phi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: degrees (°) ('degree': http://qudt.org/vocab/unit/DEG).

     - "difference_residue_backbone_phi_angle"
       - Data type: number
       - Description: The field 'difference_residue_backbone_phi_angle' indicates the difference between the mutant value and the wild-type value for the backbone phi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: degrees (°) ('degree': http://qudt.org/vocab/unit/DEG).

     - "wild_type_residue_backbone_psi_angle"
       - Data type: number
       - Description: The field 'wild_type_residue_backbone_psi_angle' indicates the backbone psi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: degrees (°) ('degree': http://qudt.org/vocab/unit/DEG).

     - "mutant_residue_backbone_psi_angle"
       - Data type: number
       - Description: The field 'mutant_residue_backbone_psi_angle' indicates the backbone psi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: degrees (°) ('degree': http://qudt.org/vocab/unit/DEG).

     - "difference_residue_backbone_psi_angle"
       - Data type: number
       - Description: The field 'difference_residue_backbone_psi_angle' indicates the difference between the mutant value and the wild-type value for the backbone psi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: degrees (°) ('degree': http://qudt.org/vocab/unit/DEG).

     - "wild_type_residue_net_charge"
       - Data type: number
       - Description: The field 'wild_type_residue_net_charge' indicates the net electric charge ('net electric charge': https://goldbook.iupac.org/terms/view/N04111) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "mutant_residue_net_charge"
       - Data type: number
       - Description: The field 'mutant_residue_net_charge' indicates the net electric charge ('net electric charge': https://goldbook.iupac.org/terms/view/N04111) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "difference_residue_net_charge"
       - Data type: number
       - Description: The field 'difference_residue_net_charge' indicates the difference between the mutant value and the wild-type value for the net electric charge ('net electric charge': https://goldbook.iupac.org/terms/view/N04111) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "wild_type_residue_pka"
       - Data type: number
       - Description: The field 'wild_type_residue_pka' indicates the pKa value ('pKa': https://goldbook.iupac.org/terms/view/15441) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "mutant_residue_pka"
       - Data type: number
       - Description: The field 'mutant_residue_pka' indicates the pKa value ('pKa': https://goldbook.iupac.org/terms/view/15441) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "difference_residue_pka"
       - Data type: number
       - Description: The field 'difference_residue_pka' indicates the difference between the mutant value and the wild-type value for the pKa value ('pKa': https://goldbook.iupac.org/terms/view/15441) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "wild_type_residue_volume"
       - Data type: number
       - Description: The field 'wild_type_residue_volume' indicates the volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "mutant_residue_volume"
       - Data type: number
       - Description: The field 'mutant_residue_volume' indicates the volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "difference_residue_volume"
       - Data type: number
       - Description: The field 'difference_residue_volume' indicates the difference between the mutant value and the wild-type value for the volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "wild_type_residue_hydrophobicity"
       - Data type: number
       - Description: The field 'wild_type_residue_hydrophobicity' indicates the hydrophobicity ('hydrophobicity': https://goldbook.iupac.org/terms/view/HT06964) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "mutant_residue_hydrophobicity"
       - Data type: number
       - Description: The field 'mutant_residue_hydrophobicity' indicates the hydrophobicity ('hydrophobicity': https://goldbook.iupac.org/terms/view/HT06964) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "difference_residue_hydrophobicity"
       - Data type: number
       - Description: The field 'difference_residue_hydrophobicity' indicates the difference between the mutant value and the wild-type value for the hydrophobicity ('hydrophobicity': https://goldbook.iupac.org/terms/view/HT06964) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "wild_type_residue_molecular_weight"
       - Data type: number
       - Description: The field 'wild_type_residue_molecular_weight' indicates the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: daltons (Da) ('dalton': http://qudt.org/vocab/unit/DA).

     - "mutant_residue_molecular_weight"
       - Data type: number
       - Description: The field 'mutant_residue_molecular_weight' indicates the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: daltons (Da) ('dalton': http://qudt.org/vocab/unit/DA).

     - "difference_residue_molecular_weight"
       - Data type: number
       - Description: The field 'difference_residue_molecular_weight' indicates the difference between the mutant value and the wild-type value for the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: daltons (Da) ('dalton': http://qudt.org/vocab/unit/DA).

     - "wild_type_residue_isoelectric_point"
       - Data type: number
       - Description: The field 'wild_type_residue_isoelectric_point' indicates the isoelectric point ('isoelectric point': https://goldbook.iupac.org/terms/view/I03275) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "mutant_residue_isoelectric_point"
       - Data type: number
       - Description: The field 'mutant_residue_isoelectric_point' indicates the isoelectric point ('isoelectric point': https://goldbook.iupac.org/terms/view/I03275) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "difference_residue_isoelectric_point"
       - Data type: number
       - Description: The field 'difference_residue_isoelectric_point' indicates the difference between the mutant value and the wild-type value for the isoelectric point ('isoelectric point': https://goldbook.iupac.org/terms/view/I03275) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "wild_type_residue_root_mean_square_fluctuation"
       - Data type: number
       - Description: The field 'wild_type_residue_root_mean_square_fluctuation' indicates the root mean square fluctuation ('root mean square fluctuation': https://manual.gromacs.org/current/onlinehelp/gmx-rmsf.html) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "mutant_residue_root_mean_square_fluctuation"
       - Data type: number
       - Description: The field 'mutant_residue_root_mean_square_fluctuation' indicates the root mean square fluctuation ('root mean square fluctuation': https://manual.gromacs.org/current/onlinehelp/gmx-rmsf.html) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "difference_residue_root_mean_square_fluctuation"
       - Data type: number
       - Description: The field 'difference_residue_root_mean_square_fluctuation' indicates the difference between the mutant value and the wild-type value for the root mean square fluctuation ('root mean square fluctuation': https://manual.gromacs.org/current/onlinehelp/gmx-rmsf.html) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "wild_type_residue_sequence_conservation_score"
       - Data type: number
       - Description: The field 'wild_type_residue_sequence_conservation_score' indicates the sequence conservation score ('sequence conservation': http://edamontology.org/operation_0448) of the wild-type residue ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "mutant_residue_sequence_conservation_score"
       - Data type: number
       - Description: The field 'mutant_residue_sequence_conservation_score' indicates the sequence conservation score ('sequence conservation': http://edamontology.org/operation_0448) of the mutant residue ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "difference_residue_sequence_conservation_score"
       - Data type: number
       - Description: The field 'difference_residue_sequence_conservation_score' indicates the difference between the mutant value and the wild-type value for the sequence conservation score ('sequence conservation': http://edamontology.org/operation_0448) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) at the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "wild_type_mutation_site_distance_to_centroid"
       - Data type: number
       - Description: The field 'wild_type_mutation_site_distance_to_centroid' indicates the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the protein alpha-carbon centroid ('centroid': https://xlinux.nist.gov/dads/HTML/centroid.html) in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "mutant_mutation_site_distance_to_centroid"
       - Data type: number
       - Description: The field 'mutant_mutation_site_distance_to_centroid' indicates the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the protein alpha-carbon centroid ('centroid': https://xlinux.nist.gov/dads/HTML/centroid.html) in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "difference_mutation_site_distance_to_centroid"
       - Data type: number
       - Description: The field 'difference_mutation_site_distance_to_centroid' indicates the difference between the mutant value and the wild-type value for the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the protein alpha-carbon centroid ('centroid': https://xlinux.nist.gov/dads/HTML/centroid.html). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "wild_type_mutation_site_distance_to_nearest_binding_pocket"
       - Data type: number
       - Description: The field 'wild_type_mutation_site_distance_to_nearest_binding_pocket' indicates the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the nearest binding-pocket residue alpha-carbon coordinate ('binding pocket': https://schlessinger-lab.github.io/pyvol/pocket_specification.html) in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "mutant_mutation_site_distance_to_nearest_binding_pocket"
       - Data type: number
       - Description: The field 'mutant_mutation_site_distance_to_nearest_binding_pocket' indicates the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the nearest binding-pocket residue alpha-carbon coordinate ('binding pocket': https://schlessinger-lab.github.io/pyvol/pocket_specification.html) in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "difference_mutation_site_distance_to_nearest_binding_pocket"
       - Data type: number
       - Description: The field 'difference_mutation_site_distance_to_nearest_binding_pocket' indicates the difference between the mutant value and the wild-type value for the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the nearest binding-pocket residue alpha-carbon coordinate ('binding pocket': https://schlessinger-lab.github.io/pyvol/pocket_specification.html). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "wild_type_mutation_site_distance_to_nearest_hydrophobic_cluster"
       - Data type: number
       - Description: The field 'wild_type_mutation_site_distance_to_nearest_hydrophobic_cluster' indicates the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the nearest hydrophobic-cluster residue alpha-carbon coordinate ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/) in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "mutant_mutation_site_distance_to_nearest_hydrophobic_cluster"
       - Data type: number
       - Description: The field 'mutant_mutation_site_distance_to_nearest_hydrophobic_cluster' indicates the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the nearest hydrophobic-cluster residue alpha-carbon coordinate ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/) in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "difference_mutation_site_distance_to_nearest_hydrophobic_cluster"
       - Data type: number
       - Description: The field 'difference_mutation_site_distance_to_nearest_hydrophobic_cluster' indicates the difference between the mutant value and the wild-type value for the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the nearest hydrophobic-cluster residue alpha-carbon coordinate ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "wild_type_mutation_site_distance_to_nearest_disordered_region"
       - Data type: number
       - Description: The field 'wild_type_mutation_site_distance_to_nearest_disordered_region' indicates the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the nearest disordered-region residue alpha-carbon coordinate ('intrinsically disordered region': https://disprot.org/ontology) in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "mutant_mutation_site_distance_to_nearest_disordered_region"
       - Data type: number
       - Description: The field 'mutant_mutation_site_distance_to_nearest_disordered_region' indicates the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the nearest disordered-region residue alpha-carbon coordinate ('intrinsically disordered region': https://disprot.org/ontology) in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "difference_mutation_site_distance_to_nearest_disordered_region"
       - Data type: number
       - Description: The field 'difference_mutation_site_distance_to_nearest_disordered_region' indicates the difference between the mutant value and the wild-type value for the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the nearest disordered-region residue alpha-carbon coordinate ('intrinsically disordered region': https://disprot.org/ontology). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "wild_type_mutation_site_distance_to_nearest_substrate"
       - Data type: number
       - Description: The field 'wild_type_mutation_site_distance_to_nearest_substrate' indicates the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the nearest docked substrate center coordinate ('substrate': https://purl.dsmz.de/schema/Substrate; 'docking': https://goldbook.iupac.org/terms/view/11437) in the wild-type protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "mutant_mutation_site_distance_to_nearest_substrate"
       - Data type: number
       - Description: The field 'mutant_mutation_site_distance_to_nearest_substrate' indicates the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the nearest docked substrate center coordinate ('substrate': https://purl.dsmz.de/schema/Substrate; 'docking': https://goldbook.iupac.org/terms/view/11437) in the mutant protein structure ('protein structure': http://edamontology.org/data_1537). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "difference_mutation_site_distance_to_nearest_substrate"
       - Data type: number
       - Description: The field 'difference_mutation_site_distance_to_nearest_substrate' indicates the difference between the mutant value and the wild-type value for the distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) from the amino acid substitution site ('amino acid substitution': http://purl.obolibrary.org/obo/SO_0001606) to the nearest docked substrate center coordinate ('substrate': https://purl.dsmz.de/schema/Substrate; 'docking': https://goldbook.iupac.org/terms/view/11437). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

   - "wild_type_integrated_graph"
     - Data type: array
     - Description: The field 'wild_type_integrated_graph' indicates the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/) containing molecular interactions ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI) between source nodes and target nodes, and isolated nodes ('isolated node': https://mathworld.wolfram.com/IsolatedPoint.html), integrated from EnzyWizard reports ('report': http://purl.obolibrary.org/obo/IAO_0000088) for the wild-type protein structure ('wild-type': http://purl.obolibrary.org/obo/FBcv_0000348; 'protein structure': http://edamontology.org/data_1537).

   - "mutant_integrated_graph"
     - Data type: array
     - Description: The field 'mutant_integrated_graph' indicates the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/) containing molecular interactions ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI) between source nodes and target nodes, and isolated nodes ('isolated node': https://mathworld.wolfram.com/IsolatedPoint.html), integrated from EnzyWizard reports ('report': http://purl.obolibrary.org/obo/IAO_0000088) for the mutant protein structure ('mutant': https://ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000480; 'protein structure': http://edamontology.org/data_1537).

     Each item in "wild_type_integrated_graph" or "mutant_integrated_graph" is one of the following entry objects:

     1. Interaction graph entry object containing:

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
         - Description: The field 'interaction_count' indicates the count of molecular interactions ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI) between the source node and the target node.

     - "source_node"
       - Data type: object
       - Description: The field 'source_node' indicates the source node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) corresponding to a residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) or a substrate ('substrate': https://purl.dsmz.de/schema/Substrate) in the integrated graph.

     - "target_node"
       - Data type: object
       - Description: The field 'target_node' indicates the target node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) corresponding to a residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) or a substrate ('substrate': https://purl.dsmz.de/schema/Substrate) in the integrated graph.

     2. Isolated node graph entry object containing:

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
       - Description: The field 'node_type' indicates the type of node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node), with value 'residue' indicating a residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "node_type_one_hot_encoding"
       - Data type: array
       - Description: The field 'node_type_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the node type.

     - "residue_index"
       - Data type: integer
       - Description: The field 'residue_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_name"
       - Data type: string
       - Description: The field 'residue_name' indicates the name of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using one-letter code ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) to represent the amino acid residue.

     - "residue_name_one_hot_encoding"
       - Data type: array
       - Description: The field 'residue_name_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the residue name ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_alpha_carbon_coordinate"
       - Data type: array
       - Description: The field 'residue_alpha_carbon_coordinate' indicates the three-dimensional coordinate ('coordinate': http://purl.obolibrary.org/obo/NCIT_C44477) of the alpha carbon atom ('alpha carbon': https://www.rcsb.org/docs/general-help/glossary; 'atom': http://purl.obolibrary.org/obo/CHMO_0001075) in the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "residue_chemical_classification"
       - Data type: string
       - Description: The field 'residue_chemical_classification' indicates the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_chemical_classification_multi_hot_encoding"
       - Data type: array
       - Description: The field 'residue_chemical_classification_multi_hot_encoding' indicates the multi-hot encoding ('multi-hot encoding': https://developers.google.com/machine-learning/crash-course/categorical-data/one-hot-encoding) of the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the amino acid residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_secondary_structure"
       - Data type: string
       - Description: The field 'residue_secondary_structure' indicates the secondary structure ('secondary structure': http://edamontology.org/operation_1847) assigned to the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using DSSP secondary-structure codes ('DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

     - "residue_secondary_structure_one_hot_encoding"
       - Data type: array
       - Description: The field 'residue_secondary_structure_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the residue secondary structure ('secondary structure': http://edamontology.org/operation_1847).

     - "residue_relative_solvent_accessibility"
       - Data type: number
       - Description: The field 'residue_relative_solvent_accessibility' indicates the relative solvent accessibility ('solvent accessibility': http://edamontology.org/data_1542) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "residue_backbone_phi_angle"
       - Data type: number
       - Description: The field 'residue_backbone_phi_angle' indicates the backbone phi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825). Unit: degrees (°) ('degree': http://qudt.org/vocab/unit/DEG).

     - "residue_backbone_psi_angle"
       - Data type: number
       - Description: The field 'residue_backbone_psi_angle' indicates the backbone psi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825). Unit: degrees (°) ('degree': http://qudt.org/vocab/unit/DEG).

     - "residue_net_charge"
       - Data type: number
       - Description: The field 'residue_net_charge' indicates the net electric charge ('net electric charge': https://goldbook.iupac.org/terms/view/N04111) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "residue_pka"
       - Data type: number
       - Description: The field 'residue_pka' indicates the pKa value ('pKa': https://goldbook.iupac.org/terms/view/15441) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "residue_volume"
       - Data type: number
       - Description: The field 'residue_volume' indicates the volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782). Unit: cubic angstroms (Å^3) ('cubic angstrom': http://qudt.org/vocab/unit/ANGSTROM3).

     - "residue_hydrophobicity"
       - Data type: number
       - Description: The field 'residue_hydrophobicity' indicates the hydrophobicity ('hydrophobicity': https://goldbook.iupac.org/terms/view/HT06964) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "residue_molecular_weight"
       - Data type: number
       - Description: The field 'residue_molecular_weight' indicates the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782). Unit: daltons (Da) ('dalton': http://qudt.org/vocab/unit/DA).

     - "residue_isoelectric_point"
       - Data type: number
       - Description: The field 'residue_isoelectric_point' indicates the isoelectric point ('isoelectric point': https://goldbook.iupac.org/terms/view/I03275) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "residue_root_mean_square_fluctuation"
       - Data type: number
       - Description: The field 'residue_root_mean_square_fluctuation' indicates the root mean square fluctuation ('root mean square fluctuation': https://manual.gromacs.org/current/onlinehelp/gmx-rmsf.html) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "residue_sequence_conservation_score"
       - Data type: number
       - Description: The field 'residue_sequence_conservation_score' indicates the sequence conservation score based on normalized Shannon information content ('Shannon entropy': https://mathworld.wolfram.com/Entropy.html; 'information content': https://www.ebsco.com/research-starters/library-and-information-science/information-content) of the residue position, calculated based on the 'normalized_emission_probability'. Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "residue_embedding"
       - Data type: array
       - Item data type: number
       - Description: The field 'residue_embedding' indicates the embedding ('embedding': https://developers.google.com/machine-learning/crash-course/embeddings) generated by the ESM-2 protein language model ('ESM-2': https://docs.nvidia.com/bionemo-framework/2.0/models/esm2/; 'protein language model': https://synbiointel.com/glossary/protein-language-model/) for the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), represented as a numerical vector ('numerical vector': https://mathworld.wolfram.com/Vector.html).

       The value must be one of the following forms:

       1. Embedding length generated by esm2_t6_8M_UR50D.
          - Length: 320

       2. Embedding length generated by esm2_t12_35M_UR50D.
          - Length: 480

       3. Embedding length generated by esm2_t30_150M_UR50D.
          - Length: 640

     - "is_in_hydrophobic_cluster"
       - Data type: boolean
       - Description: The field 'is_in_hydrophobic_cluster' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in a hydrophobic cluster ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/).

     - "is_in_disordered_region"
       - Data type: boolean
       - Description: The field 'is_in_disordered_region' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in an intrinsically disordered region ('intrinsically disordered region': https://disprot.org/ontology).

     - "is_in_binding_pocket"
       - Data type: boolean
       - Description: The field 'is_in_binding_pocket' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in a binding pocket ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html).

     - "is_at_mutation_site"
       - Data type: boolean
       - Description: The field 'is_at_mutation_site' indicates whether this residue node is at an amino acid substitution site.

     Substrate node fields:

     - "node_index"
       - Data type: integer
       - Description: The field 'node_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

     - "node_type"
       - Data type: string
       - Expected value: "substrate"
       - Description: The field 'node_type' indicates the type of node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node), with value 'substrate' indicating a substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "node_type_one_hot_encoding"
       - Data type: array
       - Description: The field 'node_type_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the node type.

     - "substrate_index"
       - Data type: integer
       - Description: The field 'substrate_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_name"
       - Data type: string
       - Description: The field 'substrate_name' indicates the name of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_smiles"
       - Data type: string
       - Description: The field 'substrate_smiles' indicates the SMILES representation ('SMILES': https://opensmiles.org/opensmiles.html) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_atom_count"
       - Data type: integer
       - Description: The field 'substrate_atom_count' indicates the count of atoms ('atom': https://goldbook.iupac.org/terms/view/A00493) in the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_molecular_weight"
       - Data type: number
       - Description: The field 'substrate_molecular_weight' indicates the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate). Unit: daltons (Da) ('dalton': http://qudt.org/vocab/unit/DA).

     - "substrate_logp"
       - Data type: number
       - Description: The field 'substrate_logp' indicates the calculated logP value ('LogP': https://doktormike.gitlab.io/posts/navigating-logp-logd-pka-and-logs-a-physicists-guide/) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "substrate_tpsa"
       - Data type: number
       - Description: The field 'substrate_tpsa' indicates the topological polar surface area ('TPSA': https://www.rdkit.org/docs/GettingStartedInPython.html#descriptor-calculation) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate) calculated by RDKit software ('RDKit': https://www.rdkit.org/docs/index.html). Unit: square angstroms (Å^2) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "substrate_heavy_atom_count"
       - Data type: integer
       - Description: The field 'substrate_heavy_atom_count' indicates the count of heavy atoms ('atom': https://goldbook.iupac.org/terms/view/A00493) in the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_hbond_donor_count"
       - Data type: integer
       - Description: The field 'substrate_hbond_donor_count' indicates the count of hydrogen bond donors ('hydrogen bond': https://goldbook.iupac.org/terms/view/H02899) in the substrate ('substrate': https://purl.dsmz.de/schema/Substrate) calculated by RDKit software ('RDKit': https://www.rdkit.org/docs/index.html).

     - "substrate_hbond_acceptor_count"
       - Data type: integer
       - Description: The field 'substrate_hbond_acceptor_count' indicates the count of hydrogen bond acceptors ('hydrogen bond': https://goldbook.iupac.org/terms/view/H02899) in the substrate ('substrate': https://purl.dsmz.de/schema/Substrate) calculated by RDKit software ('RDKit': https://www.rdkit.org/docs/index.html).

     - "substrate_rotatable_bond_count"
       - Data type: integer
       - Description: The field 'substrate_rotatable_bond_count' indicates the count of rotatable bonds ('bond': https://goldbook.iupac.org/terms/view/B00701) in the substrate ('substrate': https://purl.dsmz.de/schema/Substrate) calculated by RDKit software ('RDKit': https://www.rdkit.org/docs/index.html).

     - "substrate_molar_refractivity"
       - Data type: number
       - Description: The field 'substrate_molar_refractivity' indicates the molar refractivity ('molar refractivity': https://old.iupac.org/reports/1997/6905vandewaterbeemd/glossary.html) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate) calculated by RDKit software ('RDKit': https://www.rdkit.org/docs/index.html). Unit: cubic centimeters per mole (cm^3/mol) ('cubic centimeter': http://qudt.org/vocab/unit/CentiM3; 'mole': http://qudt.org/vocab/unit/MOL).

     - "substrate_structure_energy"
       - Data type: number
       - Description: The field 'substrate_structure_energy' indicates the energy ('energy': http://purl.obolibrary.org/obo/PATO_0001021) of a possible molecular structure ('molecular structure': http://edamontology.org/data_0883) generated for the substrate ('substrate': https://purl.dsmz.de/schema/Substrate). Unit: kilocalories per mole (kcal/mol) ('kilocalorie': http://qudt.org/vocab/unit/KiloCAL; 'mole': http://qudt.org/vocab/unit/MOL).

     - "substrate_structure_max_3d_diameter"
       - Data type: number
       - Description: The field 'substrate_structure_max_3d_diameter' indicates the maximum three-dimensional diameter ('diameter': http://purl.obolibrary.org/obo/PATO_0001334) of a possible molecular structure ('molecular structure': http://edamontology.org/data_0883) generated for the substrate ('substrate': https://purl.dsmz.de/schema/Substrate). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "substrate_structure_mean_pairwise_atom_distance"
       - Data type: number
       - Description: The field 'substrate_structure_mean_pairwise_atom_distance' indicates the mean pairwise atom distance ('distance': http://purl.obolibrary.org/obo/PATO_0000040) of a possible molecular structure ('molecular structure': http://edamontology.org/data_0883) generated for the substrate ('substrate': https://purl.dsmz.de/schema/Substrate). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "substrate_structure_std_pairwise_atom_distance"
       - Data type: number
       - Description: The field 'substrate_structure_std_pairwise_atom_distance' indicates the standard deviation ('standard deviation': http://purl.obolibrary.org/obo/STATO_0000237) of pairwise atom distances ('distance': http://purl.obolibrary.org/obo/PATO_0000040) of a possible molecular structure ('molecular structure': http://edamontology.org/data_0883) generated for the substrate ('substrate': https://purl.dsmz.de/schema/Substrate). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "substrate_structure_asphericity"
       - Data type: number
       - Description: The field 'substrate_structure_asphericity' indicates the asphericity ('asphericity': https://www.rdkit.org/docs/source/rdkit.Chem.rdMolDescriptors.html) of a possible molecular structure ('molecular structure': http://edamontology.org/data_0883) generated for the substrate ('substrate': https://purl.dsmz.de/schema/Substrate) calculated by RDKit software ('RDKit': https://www.rdkit.org/docs/index.html). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "substrate_structure_spherocity"
       - Data type: number
       - Description: The field 'substrate_structure_spherocity' indicates the spherocity index ('spherocity index': https://www.rdkit.org/docs/source/rdkit.Chem.rdMolDescriptors.html) of a possible molecular structure ('molecular structure': http://edamontology.org/data_0883) generated for the substrate ('substrate': https://purl.dsmz.de/schema/Substrate) calculated by RDKit software ('RDKit': https://www.rdkit.org/docs/index.html). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "substrate_structure_principal_moment_ratio"
       - Data type: number
       - Description: The field 'substrate_structure_principal_moment_ratio' indicates the ratio of the largest to the smallest principal moments of inertia ('moment of inertia': https://goldbook.iupac.org/terms/view/M03954) of a possible molecular structure ('molecular structure': http://edamontology.org/data_0883) generated for the substrate ('substrate': https://purl.dsmz.de/schema/Substrate). Unit: dimensionless ('dimensionless': http://qudt.org/vocab/unit/UNITLESS).

     - "substrate_structure_radius_of_gyration"
       - Data type: number
       - Description: The field 'substrate_structure_radius_of_gyration' indicates the radius of gyration ('radius of gyration': https://goldbook.iupac.org/terms/view/R05121) of a possible molecular structure ('molecular structure': http://edamontology.org/data_0883) generated for the substrate ('substrate': https://purl.dsmz.de/schema/Substrate) calculated by RDKit software ('RDKit': https://www.rdkit.org/docs/index.html). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "docked_substrate_center_coordinate"
       - Data type: array
       - Description: The field 'docked_substrate_center_coordinate' indicates the center coordinate ('coordinate': https://mathworld.wolfram.com/Coordinates.html) of the docked substrate ('substrate': https://purl.dsmz.de/schema/Substrate) in the enzyme-substrate complex ('enzyme': https://purl.dsmz.de/schema/Enzyme; 'substrate': https://purl.dsmz.de/schema/Substrate; 'complex': https://goldbook.iupac.org/terms/view/C01203). Unit: angstroms (Å) ('angstrom': http://qudt.org/vocab/unit/ANGSTROM).

     - "substrate_fingerprint_encoding"
       - Data type: array
       - Description: The field 'substrate_fingerprint_encoding' indicates the molecular fingerprint encoding ('molecular fingerprint': https://www.rdkit.org/docs/GettingStartedInPython.html#fingerprinting-and-molecular-similarity) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate) calculated by RDKit software ('RDKit': https://www.rdkit.org/docs/index.html).

# Process:

This command processes the input wild-type and mutant systems as follows:

1. Validate input files
   - Check that wt_cleaned_input_path exists.
   - Check that mut_cleaned_input_path exists.
   - If wt_input_msa is provided, check that it exists.
   - If mut_input_msa is provided, check that it exists.
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
   - Extract wt_msa_name from the wild-type MSA filename when wt_input_msa is provided.
   - Extract mut_msa_name from the mutant MSA filename when mut_input_msa is provided.
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
   - If wt_input_msa is provided, run conservation analysis using the wild-type MSA.
   - Automatically decompress the wild-type MSA when the file is in .fasta.gz format.
   - If wt_input_msa is omitted, skip wild-type conservation analysis and HMM output.
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
   - If mut_input_msa is provided, run conservation analysis using the mutant MSA.
   - Automatically decompress the mutant MSA when the file is in .fasta.gz format.
   - If mut_input_msa is omitted, skip mutant conservation analysis and HMM output.
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
   - Use strict integration when substrate input is provided, substrate/docking workflows complete successfully on both sides, and both MSA inputs are provided.
   - Use non-strict integration when no substrate input is provided, either MSA input is omitted, or the workflow falls back to paired protein-only analysis.
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


# common errors and solutions:

- "the following arguments are required: -w/--wt_cleaned_input_path, -m/--mut_cleaned_input_path, -a/--cleaned_amino_acid_substitution, -wo/--wt_output_dir, -mo/--mut_output_dir"
  - Cause: One or more required inputs were not provided.
  - Solution: Provide both cleaned structure files, the cleaned amino acid substitution, and two different output directories. MSA and substrate input are optional.

- "WT cleaned input file not found"
  - Cause: The wild-type structure file passed to `-w` or `--wt_cleaned_input_path` does not exist, or the path points to the wrong location.
  - Solution: Check the wild-type structure path and use a cleaned `.cif` or `.pdb` file.

- "MUT cleaned input file not found"
  - Cause: The mutant structure file passed to `-m` or `--mut_cleaned_input_path` does not exist, or the path points to the wrong location.
  - Solution: Check the mutant structure path and use a cleaned `.cif` or `.pdb` file.

- "WT input MSA file not found"
  - Cause: `--wt_input_msa` was provided, but the wild-type MSA file does not exist.
  - Solution: Check the wild-type MSA path, or omit `--wt_input_msa` to run without wild-type conservation analysis.

- "MUT input MSA file not found"
  - Cause: `--mut_input_msa` was provided, but the mutant MSA file does not exist.
  - Solution: Check the mutant MSA path, or omit `--mut_input_msa` to run without mutant conservation analysis.

- "wt_output_dir and mut_output_dir must be different directories."
  - Cause: The same directory was used for both wild-type and mutant output.
  - Solution: Use two different output directories so side-specific node and edge files cannot overwrite each other.

- "Wild-type and mutant protein names are the same"
  - Cause: The wild-type and mutant cleaned structure filenames produce the same protein name.
  - Solution: Rename one input structure so the wild-type and mutant output filenames are distinct.

- "Filename too long"
  - Cause: The structure or MSA filename without extension is longer than the supported filename limit.
  - Solution: Rename the input file to a shorter name and run the command again.

- "Unsupported format"
  - Cause: The input structure extension is not `.cif` or `.pdb`, or an optional MSA file uses an unsupported format.
  - Solution: Use a supported cleaned structure format and, when MSA is provided, use Stockholm, aligned FASTA, gzip-compressed aligned FASTA, or A3M.

- "Exception while loading WT structure"
  - Cause: The wild-type structure file could not be parsed as a usable protein structure, or the file is empty, corrupted, or inconsistent with its extension.
  - Solution: Check that the wild-type file is valid and non-empty, then rerun with a cleaned CIF or PDB structure.

- "Exception while loading MUT structure"
  - Cause: The mutant structure file could not be parsed as a usable protein structure, or the file is empty, corrupted, or inconsistent with its extension.
  - Solution: Check that the mutant file is valid and non-empty, then rerun with a cleaned CIF or PDB structure.

- "Input structure is not a valid cleaned structure."
  - Cause: One of the inputs is not a valid cleaned single-chain protein structure. Common causes include multiple chains, non-chain-A input, heterogens, insertion codes, non-standard residues, missing atoms, unexpected atoms, invalid occupancies, or non-continuous numbering.
  - Solution: Review the specific validation error above this summary in `log.txt`, run `enzywizard-clean` on the original structure, and use its cleaned output.

- "Input cleaned structure does not contain hydrogen atoms."
  - Cause: Hydrogen atoms are missing from one of the cleaned protein structures.
  - Solution: Regenerate the cleaned structure with hydrogen addition enabled, then rerun mut-batch.

- "Invalid amino acid substitution format"
  - Cause: The value passed to `-a` or `--cleaned_amino_acid_substitution` does not match the supported mutation format.
  - Solution: Use one-letter mutation notation such as `A123V`; separate multiple substitutions with semicolons.

- "Mutation position out of wild-type range"
  - Cause: The mutation position is outside the wild-type cleaned sequence length.
  - Solution: Check that the mutation uses cleaned residue numbering and that the wild-type structure matches the intended sequence.

- "Mutation position out of mutant range"
  - Cause: The mutation position is outside the mutant cleaned sequence length.
  - Solution: Check that the mutation uses cleaned residue numbering and that the mutant structure matches the intended sequence.

- "Mutation position missing in WT cleaned residue list"
  - Cause: The mutation position cannot be found in the wild-type cleaned residue list during mutation-aware integration.
  - Solution: Check residue numbering in the wild-type cleaned structure and regenerate the cleaned inputs if numbering is inconsistent.

- "Mutation position missing in MUT cleaned residue list"
  - Cause: The mutation position cannot be found in the mutant cleaned residue list during mutation-aware integration.
  - Solution: Check residue numbering in the mutant cleaned structure and regenerate the cleaned inputs if numbering is inconsistent.

- "Exception in loading dssp"
  - Cause: DSSP failed to run or failed to parse one of the cleaned structures.
  - Solution: Confirm that DSSP or `mkdssp` is installed and available, and check that both cleaned input structures are valid.

- "Failed to load OpenMM force field"
  - Cause: OpenMM could not load the force field used for energy calculation.
  - Solution: Check the OpenMM installation and force-field availability in the running environment.

- "Failed to create OpenMM system"
  - Cause: OpenMM could not build a molecular system from a cleaned topology and coordinates, often because the structure contains residues, atoms, or connectivity that the force field cannot parameterize.
  - Solution: Rerun structure cleaning, check both cleaned structures, and review the detailed OpenMM error in `log.txt`.

- "Failed to calculate RMSF by ProDy"
  - Cause: ProDy failed while building the elastic network or solving normal modes, often because of unsuitable coordinates, an extreme cutoff value, or an environment issue.
  - Solution: Review the detailed ProDy error in `log.txt`, check the cleaned structures, and try a standard cutoff such as `15.0`.

- "The first Stockholm MSA sequence does not match query_sequence after gap removal."
  - Cause: The first sequence in a Stockholm MSA is not the same as the corresponding cleaned input structure sequence after gaps are removed.
  - Solution: Put the matching cleaned protein sequence as the first MSA record and make sure the MSA is paired with the correct wild-type or mutant structure.

- "The first aligned FASTA MSA sequence does not match query_sequence after gap removal."
  - Cause: The first sequence in an aligned FASTA MSA is not the same as the corresponding cleaned input structure sequence after gaps are removed.
  - Solution: Put the matching cleaned protein sequence as the first MSA record and make sure all aligned sequences have consistent length.

- "The first A3M MSA sequence does not match query_sequence after removing lowercase insertions and gaps."
  - Cause: The first sequence in an A3M MSA is not the same as the corresponding cleaned input structure sequence after lowercase insertions and gaps are removed.
  - Solution: Put the matching cleaned protein sequence as the first A3M record and regenerate the alignment if needed.

- "hmmbuild failed"
  - Cause: HMMER `hmmbuild` failed while building an HMM profile from the cleaned Stockholm MSA.
  - Solution: Confirm that HMMER is installed and available, then check the cleaned MSA and earlier messages in `log.txt`.

- "HMM length"
  - Cause: The number of match emission rows parsed from the HMM profile does not match the corresponding cleaned protein sequence length.
  - Solution: Regenerate the MSA from the same cleaned protein sequence as the structure, or omit the corresponding MSA if conservation scores are not needed.

- "Failed to load ESM2 model"
  - Cause: The selected ESM-2 model cannot be loaded, often because model files or dependencies are unavailable in the runtime environment.
  - Solution: Check the ESM installation and model cache, or use the default smaller model if a larger model is not available.

- "Failed to compute pockets."
  - Cause: PyVOL pocket detection failed on one of the cleaned structures or with the selected pocket parameters.
  - Solution: Check that PyVOL is installed and try standard pocket parameters before adjusting radius or volume thresholds.

- "Failed to obtain SMILES for substrate"
  - Cause: A substrate name could not be resolved to a SMILES string through the supported chemical lookup route.
  - Solution: Check the spelling, use a more specific substrate name, increase `--substrate_max_synonyms`, or provide the SMILES string directly with `-s`.

- "Invalid SMILES"
  - Cause: A direct SMILES input cannot be parsed by RDKit.
  - Solution: Check the SMILES syntax and use a valid canonical or isomeric SMILES string.

- "Failed to convert SMILES to Mol(2D)"
  - Cause: RDKit could not convert the resolved SMILES into a valid 2D molecular object.
  - Solution: Check whether the SMILES string represents a supported small molecule and try a corrected substrate name or direct SMILES input.

- "Substrate input parsing failed. Falling back to protein-only workflow on both sides."
  - Cause: Substrate input could not be parsed into valid substrate names or SMILES strings.
  - Solution: Check the value passed to `-s`; separate multiple substrates with semicolons and avoid empty substrate entries.

- "Substrate feature or 3D structure generation failed. Falling back to protein-only workflow on both sides."
  - Cause: Substrate feature generation, conformer generation, or SDF writing failed.
  - Solution: Check the substrate name or SMILES string, RDKit availability, and output directory write permissions.

- "Copying substrate SDF files to MUT side failed. Falling back to protein-only workflow on both sides."
  - Cause: Generated substrate SDF files could not be copied from the wild-type output directory to the mutant output directory.
  - Solution: Check that both output directories are writable and that there is enough disk space.

- "mk_prepare_receptor.py failed."
  - Cause: Meeko receptor preparation started but failed while converting a cleaned protein structure to PDBQT.
  - Solution: Review the output tail in `log.txt`, confirm Meeko is installed correctly, and check that the cleaned protein input is valid.

- "Vina docking failed for"
  - Cause: AutoDock Vina failed for a substrate combination and docking box, often because of receptor or ligand preparation issues, unsuitable docking box settings, or an unavailable Vina executable.
  - Solution: Confirm Vina is installed, review the docking error in `log.txt`, and try default docking settings or a manually defined box around the active site.

- "No valid docking results were found for any substrate combination and docking box."
  - Cause: Docking completed attempts but no valid pose could be parsed and accepted.
  - Solution: Check substrate SDF generation, box center and size, Vina installation, and consider increasing `--dock_max_attempt_num` or disabling early stop.

- "Failed to save integrate JSON"
  - Cause: Mut-batch could not write the mutation-integrated report, node-only JSON file, or edge-only JSON file because of a filesystem, permission, path, or disk-space problem.
  - Solution: Check that both output directories are writable and that there is enough disk space.

- "wild_type_integrated_graph missing in mut_batch integrate report."
  - Cause: The mutation integration step returned an invalid report without the wild-type graph field expected by mut-batch.
  - Solution: Check `log.txt` for the first earlier error, because this is usually caused by an upstream report-generation or integration failure.

- "mutant_integrated_graph missing in mut_batch integrate report."
  - Cause: The mutation integration step returned an invalid report without the mutant graph field expected by mut-batch.
  - Solution: Check `log.txt` for the first earlier error, because this is usually caused by an upstream report-generation or integration failure.

- Substrate, docked SDF, or complex output files are missing even though `--substrate_names` was provided.
  - Cause: Mut-batch intentionally falls back to paired protein-only analysis when substrate parsing, SMILES completion, substrate 3D generation, SDF copying, docking, dock report generation, or docked substrate validation fails.
  - Solution: Check `log.txt` for the first warning ending with `Falling back to protein-only workflow on both sides.` or `Falling back to protein-only workflow`, verify substrate names or SMILES strings, and rerun with corrected substrate input or more suitable docking settings.

- Conservation scores are missing from residue nodes.
  - Cause: The corresponding side has no MSA input, or MSA/HMM processing failed before conservation scores were generated.
  - Solution: Provide a matched wild-type and/or mutant MSA, ensure each MSA was generated from the matching cleaned protein sequence, and check `log.txt` for MSA/HMM errors.

- Output files are missing or fewer than expected.
  - Cause: The command failed before final integration files were written, or optional intermediate files were not requested with `--save_extra_outputs`.
  - Solution: Check `log.txt`, confirm both output directories, and remember that cleaned MSA/HMM files require the corresponding MSA input, while substrate, docked SDF, and complex files require successful substrate and docking workflows plus `--save_extra_outputs`.

- Output files are saved in a different directory than expected.
  - Cause: Wild-type node and edge JSON files are saved only in `wt_output_dir`, mutant node and edge JSON files are saved only in `mut_output_dir`, while the paired report and `log.txt` are saved in both output directories.
  - Solution: Check both output directories before treating a file as missing.

- Output file names do not match the expected protein names.
  - Cause: Final output file names use protein names derived from the cleaned input structure filenames, after filename shortening if needed.
  - Solution: Check the wild-type and mutant cleaned input structure filenames and look for the paired report, side-specific node files, side-specific edge files, and `log.txt` in the corresponding output directories.

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
