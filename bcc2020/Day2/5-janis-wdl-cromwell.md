# BCC2020 EAST - Janis Workshop (2.5)

One of the main benefits of adding tools in Janis is the added features of generating other workflow specifications interchangeably. Janis currently only supports translation to CWL and WDL, but with future development, we'll be able to  support other upcoming workflow languages, eliminating the need to re-engineer pipelines from scratch. 


We've already demonstrated this with our inspection of the WDL translation.

[Diagram of Janis](graphics/janis_diagram.png)

## Running Janis with different execution engine

Update config (`~/.janis/janis.conf`)

```yaml
   engine: cromwell
```

```bash
    janis run 
```

## Reusing CWL & WDL 

```bash
    janis translate germline.py wdl --output 
```

We can submit this workflow to any endpoints that follow TES/WES standard from GA4GH. 

[### Publish in Dockstore]

### Run it in other system

#### HPC (cwltool)

[Petermac HPC - demonstration]

#### Cloud Cromwell 

[Launch GCP Cromwell - submit via web API]

#### Terra

[If time permits & if our trial Terra is still working]

