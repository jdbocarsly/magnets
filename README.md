A website for visualizing data from:

 J.D. Bocarsly, E.E. Levin, C.A.C. Garcia, K. Schwennicke, S.D. Wilson, R. Seshadri, A Simple Computational Proxy for Screening Magnetocaloric Compounds, *Chem. Mater.* **29** (2017) 1613−1622. [doi](https://doi.org/10.1021/acs.chemmater.6b04729)


To install, clone the directory and use [`uv`](https://astral.sh/uv) to run 

```
uv sync --python=3.10
```

Then run the server locally with:

```
uv run python magnet_main.py
```

after which you can access the site at `http://localhost:5001`.

Alternatively, you can use the Dockerfile to build a container:

```
docker build -t bocarsly-magnets .
```

and then launch it with:

```
docker run -p 5001:5001 bocarsly-magnets
```

after which you can access the site at `http://localhost:5001`.
