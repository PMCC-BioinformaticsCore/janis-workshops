# Workshop 1 - Conclusion

## Resetting your config

At the start of the workshop, we set the template to submit to the `debug` partition with a `max_cpu` of 1. Let's reset that with:

```bash
vim ~/.janis/janis.conf
# OR
janis init --force pmac
```

## Summary

Thanks for taking part of the Introduction to Janis workshop!

To summarise, in this workflow you've learnt:

- What is Janis, 
    - How Janis is different from seqliner
- How to load a Janis environment,
- How to run a simple workflow,
- How to align some samples.
- How to debug if something goes wrong (check logs)
- How to override amount of resources
- How to batch run same pipeline on cohort of samples.


## Advanced functionality

Here's some additional functionality that Janis supports:

- Scattering by multiple fields (dot + cross product)
- Naming output files
- Python Tool for arbitrary code execution
- Cloud execution of workflows
