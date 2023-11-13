
<div align="center">

<h1> Crystal Space 🚀 </h1>

  <p>
    <strong>Mapping Crystal Space for Binary Compounds</strong>
  </p>

</div>

## Features
- 6 Element Embeddings (magpie, mat2vec, megnet16, oliynyk, skipatom, random) provided by [ElementEmbeddings](https://github.com/WMD-group/ElementEmbeddings)
- 3 Dimensionality Reductions (PCA, TSNE, UMAP)
- Visualize 3D Interactive Plots with Crystal Strctures and a Table of Properties registed in the Materials Project

## Installation

```bash
git clone https://github.com/WMD-group/CrystalSpace.git
cd CrystalSpace
pip install -r requirements.txt
```

## Usages

- Help Command

```bash
python app.py --help
```

- Run the app with specific ip and port

```bash
python app.py --host=0.0.0.0 --port=8050
```