# Spectralizer

A Streamlit app to redshift and visualise template galaxy spectra.

Clone the repo, then install the dependencies:

`pip install -r requirements.txt`

Then `streamlit run app.py` and browse to http://localhost:5901 .

The templates are from [EAZY](https://github.com/gbrammer/eazy-photoz) [Brammer, van Dokkum & Coppi (2008)](http://adsabs.harvard.edu/abs/2008ApJ...686.1503B).
Todo:

- Log lambda axis
- Tweak plot axes and labels
- Photometry
- Fonts of labels
- Expand default line set, check absorption lines
- Choose proper templates, e.g. AGN, dusty
- Normalize the templates and filters for optimal appearance
- Mouseovers tweak (line, filter etc has better info)


