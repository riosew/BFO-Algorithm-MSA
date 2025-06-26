BFOAdtp – Bacterial Foraging Optimization for Multiple Sequence Alignment
===================================================================

BFOAdtp is a Python implementation of a Bacterial Foraging Optimization Algorithm (BFOA) designed to create high-quality multiple sequence alignments (MSA) for DNA, RNA or protein sequences.
The core logic lives in `parallel_BFOA.py`, supported by

- `bacteria.py`         – agent (bacterium) definition and chemotactic operators
- `fastaReader.py`    – simple FASTA parser & utilities
- `evaluadorBlosum.py` – fitness evaluation using BLOSUM (or PAM) scoring

The code is fully parallelizable (multiprocessing) and produces a fitness, NFE and time log for convergence analysis.

--------------------------------------------------------------------
Table of Contents
--------------------------------------------------------------------
1. Features
2. Installation
3. Quick Start
4. Command-line Options
5. Output Files & Their Meaning
6. Internal Workflow
7. Extending / Customizing
8. Troubleshooting & Support
9. License & Citation
10. Usage example
11. List of genetic and protein sequences

--------------------------------------------------------------------
1. Features
--------------------------------------------------------------------
- Heuristic global MSA via Bacterial Foraging with swarming, reproduction & elimination–dispersal phases
- Support for protein, DNA and RNA sequences (any alphabet)
- Gap-open / gap-extension penalties configurable
- Scoring via BLOSUM-62 (default) – easily switchable to other matrices
- CPU-parallel evaluation 
- Automatic FASTA reading & preprocessing
- Detailed log of normalized fitness, NFE (number of function evaluations) and processing time

--------------------------------------------------------------------
2. Installation
--------------------------------------------------------------------
Prerequisites:
- Python ≥ 3.8
- NumPy, Biopython, tqdm (install via pip)

Quick install:
```bash
python -m venv msa-env
source msa-env/bin/activate  # Windows: msa-env\Scripts\activate
pip install -r requirements.txt
```

--------------------------------------------------------------------
3. Quick Start
--------------------------------------------------------------------
```bash
python parallel_BFOA.py --in sequences.fasta --out result.aln --iterations 500 --pop 64 --cores 8
```

--------------------------------------------------------------------
4. Command-line Options
--------------------------------------------------------------------
--in <file>            Input FASTA
--out <file>           Output alignment (Clustal format)
--iterations <int>     Total chemotactic steps (default 300)
--pop <int>            Bacteria population size (default 32)
--matrix <name>        Scoring matrix (BLOSUM62, PAM250 …)
--Ataction <float>     Atraction parameters
--Repulsion <float>    Repulsion parameters
--------------------------------------------------------------------
5. Output Files & Their Meaning
--------------------------------------------------------------------
BFOA.out  – CSV with iteration, best_score, avg_score, NFE

--------------------------------------------------------------------
6. Internal Workflow (high-level)
--------------------------------------------------------------------
1. Read FASTA & pad sequences.
2. Initialize random alignment population.
3. Chemotaxis: tumble/roll updates (shifts, insertions, deletions).
4. Swarming: collective attraction to elite.
5. Reproduction: best 50 % split, worst die.
6. Elimination–Dispersal: random reset with prob P.
7. Terminate when iterations reached 

Fitness (evaluadorBlosum):
$$
Score = \sum_{i<j} \sum_{k} igl( M_{a_{ik},\,a_{jk}} - (g_o\,gap_{open} + g_e\,gap_{ext}) igr)
$$

--------------------------------------------------------------------
7. Extending / Customizing
--------------------------------------------------------------------
- Modify `bacteria.py` for custom mutation operators.
- Replace `evaluadorBlosum.py` to optimize a different objective.

--------------------------------------------------------------------
8. Troubleshooting & Support
--------------------------------------------------------------------
- Queue errors: lower --cores or raise --pop.
- No improvement: increase population or iterations, tweak gaps.
- FASTA header issues: keep headers simple (A-Z, 0-9, _).

Email: ***

--------------------------------------------------------------------
9. License & Citation
--------------------------------------------------------------------
***

--------------------------------------------------------------------
10. Usage Example
--------------------------------------------------------------------
when using the BFOAdtp algorithm, parameters can be adjusted. For instance, consider the values:
Sequence Set : Set B 
numeroDeBacterias = 8
numRandomBacteria = 0
iteraciones = 200
tumbo = 100                                             
nado = 1
secuencias = list()
#path de salida csv
outPath = "C:\\secuenciasBFOA\\out.csv"
dAttr= 0.1 #0.1
wAttr= 0.002 #0.2
hRep=dAttr
wRep= 1    #10 default   phase 1: 0.001 phase 2: 0.002

The result provided a 200 iterations log. The first 30 are presented next:
fitness  	NFE	tiempo Acumulativo	corrida	iteracion
5.761956878	8	9.409359932	corrida1	1
76.00551929	16	19.02449632	corrida1	2
127.6318601	24	28.77755451	corrida1	3
173.0800685	32	38.32812929	corrida1	4
173.0800685	40	47.99365449	corrida1	5
173.0800685	48	57.76775742	corrida1	6
174.2770092	56	67.50014472	corrida1	7
201.4678214	64	77.21003914	corrida1	8
537.3576431	72	86.9033432	corrida1	9
537.3576431	80	96.55619121	corrida1	10
537.3576431	88	106.5656242	corrida1	11
537.3576431	96	116.3720353	corrida1	12
537.3576431	104	126.4280398	corrida1	13
537.3576431	112	136.2847221	corrida1	14
537.3576431	120	146.0804908	corrida1	15
537.3576431	128	156.1240482	corrida1	16
537.3576431	136	165.9862518	corrida1	17
537.3576431	144	176.0197294	corrida1	18
537.3576431	152	186.1158144	corrida1	19
537.3576431	160	196.1428504	corrida1	20
5486.38225	168	206.0743604	corrida1	21
13684.65093	176	216.1346855	corrida1	22
16628.81887	184	226.0191472	corrida1	23
16628.81887	192	236.1444917	corrida1	24
16628.86817	200	246.207093	corrida1	25
16628.86817	208	256.267226	corrida1	26
207126.4349	216	266.1206183	corrida1	27
207126.4349	224	276.2318618	corrida1	28
207126.4349	232	286.1812506	corrida1	29
217485.8112	240	296.3442483	corrida1	30
--The complete log file in BFOA_30Corridas.csv




--------------------------------------------------------------------
11. Sequences Report
--------------------------------------------------------------------
Set A
- Description: Sequences of the APP gene in various organisms (AD-related).
- Number of sequences: 4
- Minimum length: 2217
- Maximum length: 3583
- Mean length: 2964.0
- Mean length: 3028.0
- Sequence type: Nucleotide
- GC content: 50.75 %
- Identifiers:
  * NM_000484.4
  * NM_001198823.1
  * NM_001259804.2
  * AF389401.1

Set B
- Description: Protein sequences of ABCA7 in various organisms.
- Number of sequences: 5
- Minimum length: 1710
- Maximum length: 2244
- Mean length: 1946.2
- Mean length: 1820.0
- Sequence type: Protein
- Identifiers:
  * NP_061985.2
  * XP_044943956.1
  * XP_063575887.1
  * XP_070321384.1
  * XP_053906274.1

Set C
- Description: Protein sequences of EphA1 in various organisms.
- Number of sequences: 3
- Minimum length: 839
- Maximum length: 977
- Mean length: 930.67
- Mean length: 976.0
- Sequence type: Protein
- Identifiers:
  * EAL23789.1
  * NP_076069.2
  * XP_009452691.2

Set D
- Description: Protein sequences of TREM2 in various organisms.
- Number of sequences: 4
- Minimum length: 221
- Maximum length: 229
- Mean length: 224.75
- Mean length: 224.5
- Sequence type: Protein
- Identifiers:
  * AAH32362.1
  * sp|Q99NH8.1|TREM2_MOUSE
  * NP_001418899.1
  * XP_011842060.1


--------------------------------------------------------------------







Happy aligning!
