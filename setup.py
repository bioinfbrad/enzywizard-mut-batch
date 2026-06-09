#!/usr/bin/env python
from setuptools import setup, find_packages
import os

# Read the version from version.py without importing the package
version_file = os.path.join(os.path.dirname(__file__), 'src', 'enzywizard_mut_batch', 'version.py')
with open(version_file) as f:
    exec(f.read())  # defines __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="enzywizard-mut-batch",
    version=__version__,                     # dynamically read from version.py (1.0.1)
    author="bioinfbrad",
    description=(
        "Run paired EnzyWizard analysis workflows for a wild-type protein and its mutant, "
        "including property analysis, cluster detection, energy evaluation, flexibility, disorder, "
        "conservation, embeddings, pocket detection, optional docking, interaction networks, "
        "and mutation-aware graph integration."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bioinfbrad/enzywizard-mut-batch",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    # Core runtime dependencies based on the tool's functionality
    install_requires=[
        "biopython>=1.86",          # Protein structure I/O, sequence handling
        "numpy>=1.23.5",            # Numerical operations
        "rdkit>=2026.3.1",          # Cheminformatics for substrates
        "openmm>=8.5.0",            # Molecular mechanics (energy, minimization)
        "prody>=2.6.1",             # Elastic network models (flexibility)
        "fair-esm>=2.0.0",          # Residue embeddings
        "bio-pyvol>=1.7.8",         # Binding pocket detection
        "meeko>=0.7.1",             # Ligand preparation for docking
        "pdbfixer>=1.12",           # Structure cleaning
        "requests>=2.33.0",         # HTTP requests (API calls)
        "packaging>=26.1",          # Version handling
        # External binaries are NOT listed here – they must be added in the Conda
        # recipe's run dependencies: hmmer, msms, dssp, vina.
    ],
    entry_points={
        "console_scripts": [
            "enzywizard-mut-batch = enzywizard_mut_batch.cli:main",
        ],
    },
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
    ],
)
