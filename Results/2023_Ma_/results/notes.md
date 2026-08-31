### Corrections

- added ec number
- in the plasmid specidications was added the expression host and the protocoll for gene expresion
- the structure was was improved

  ```json
  "source_type": "self_produced",
        "source": {
          "source_type": "self_produced",
  ```
- notes are used to dumped all inforamtions `"notes": "Crystal structure PDB: 8J3P; space group C2221; 2.30 Å resolution; 3 molecules per asymmetric unit, 2 forming homodimer; RMSD vs WT <0.40 Å (Cα dimers). New H-bonds near 2'-O-phosphate of NADP+: Gln197, Arg198, Asn199, A372S; inter-subunit polar contact from Lys3 of partner chain (Fig S5). MD simulation: Amber 20, ff14SB force field, GAFF for NADP+/formate, RESP charges, TIP3P water, 3×50 ns. WT Arg176 blocks 2'-O-phosphate; PRS state WT 2% vs M4 0.07%. Kinetics NADP+: kcat=33.6±0.34 s-1, Km=0.71±0.03 mM, kcat/Km=47 s-1mM-1. Kinetics NAD+: kcat=7.3±0.5 s-1, Km=8.0±1.5 mM, kcat/Km=0.91 s-1mM-1."`
- deleted `- first-round cofactor switching mutant`
- The LLM stopped add purification SEC
- Incomplet informations the longer the document is comming the less infos will added
- the LLM jumps sometimes between SMIELS and and CAS. It is not consistens
- Structure has to be changed and maybe added to the substrate

```json
"results": [
    {
      "kinetics": {
        "michaelis_constant": 0.71,
        "turnover_number": 33.6,
        "catalytic_efficiency": 47.0,
        "notes": "CdFDH-M4 NADP+: kcat=33.6±0.34 s-1, Km=0.71±0.03 mM, kcat/Km=47. NAD+: kcat=7.3±0.5, Km=8.0±1.5, kcat/Km=0.91. 75-fold improvement vs WT (kcat/Km=0.63). Full series kcat/Km (s-1mM-1): WT NAD+ 439/NADP+ 0.63; M1 0.48/12; M1I 0.90/12; M1II 1.1/18; M1III 0.49/13; M2 21/21; M3 1.37/37; M4 0.91/47. Assay: Δabs340nm, UV-1900 Shimadzu, 1.4 mL quartz cuvette, 30°C, 1 min."
      },
      "yield_and_conversion": {
        "notes": "1a: CdFDH-M4 90% conv TTN 754±4, BmGDH-M6 TTN 995±1. 1b: CdFDH-M4 55% TTN 601±60, BmGDH-M6 63% TTN 589±1. 1c: CdFDH-M4 >99% TTN 911±8, BmGDH-M6 45% TTN 429±3. 1d: CdFDH-M4 99% TTN 986±1, BmGDH-M6 63% TTN 627±1. 1e: CdFDH-M4 TTN 359±2, BmGDH-M6 TTN 238±12. 1f: CdFDH-M4 TTN 135±1, BmGDH-M6 TTN 65±1. FDH outperformed GDH in all reactions except 1a; GDH terminated 22-63% due to acidification."
      },
      "activity": {
        "specific_activity": 3.2,
        "notes": "CdFDH-M4 NADP+: 3.2 U/mg. WT NAD+: 6 U/mg. M1 NADP+: 0.5 U/mg. M2 NADP+: 1.5 U/mg. 1 mL assay, 1.4 mL cuvette, 30°C, Δabs340nm 1 min."
      },
      "selectivity": {
        "notes": "High enantioselectivity inferred from chiral GC/UPLC. 1a→(R)-2a (ScIR-R3-V4); 1b→(R)-2b (PcIR-M3); 1c→(S)-2c; 1d→(S)-2d (CgKR1F92C/F94W); 1e→caprolactone (achiral); 1f→(S)-sulfoxide (AcPSMO Kagan oxidation). Quantitative ee values not reported."
      }
    }
  ],
```

### Improvemts for the model

- there is twice "source_type": "self_produced",
- activity should also have a field what substrate it is or we move it to the molecules (for me the better way)

### Thourgths

- do we add also concentration to the purification?
- Should we add how the enzyme was frozen? e.g. flash frozen
