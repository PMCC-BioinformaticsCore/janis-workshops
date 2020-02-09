# Workshop 1.7 - Registry 

Janis contains a registry of prebuilt tools and workflows. This information is available in the documentation:

- Tools: https://janis.readthedocs.io/en/latest/tools/index.html
- Pipelines: https://janis.readthedocs.io/en/latest/pipelines/index.html

These tools exist in separate modules to Janis, which means they can be updated independent of other janis functionality. It also means that you could create your own repository of tools independent of what Janis provides.

Let's look at the whole-genome variant calling pipeline that uses GATK to call variants: [`WGSGermlineGATK`](https://janis.readthedocs.io/en/latest/pipelines/wgsgermlinegatk.html).

We see the following table from the documentation:

|   |   |
|-- |-- |
|ID         | `WGSGermlineGATK` |
|Python:	| `janis_pipelines.wgs_germline_gatk.wgsgermlinegatk import WGSGermlineGATK` |
|Versions:	| 1.2.0 |
|Authors:	| Michael Franklin |
|Citations: | 	 |
|Created:	| None |
|Updated:	| 2019-10-16 |
|Required inputs: | fastqs: Array<FastqGzPair> <br />reference: FastaWithDict <br />\<other inputs>: \<Type>|

We note particularly the `ID: WGSGermlineGATK` row, as this is the name of the workflow that we'll use to run from the CLI, example:

```bash
janis run [...] WGSGermlineGATK
```

### Generating an inputs template

```bash
# can be directed to a file with '> germline-inputs.yml` on the end
janis inputs WGSGermlineGATK
```

