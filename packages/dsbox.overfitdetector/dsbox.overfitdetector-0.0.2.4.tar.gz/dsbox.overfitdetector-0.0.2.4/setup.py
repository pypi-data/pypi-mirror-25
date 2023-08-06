from distutils.core import setup
setup(
  name = 'dsbox.overfitdetector',
  packages = ['dsbox.overfitdetector'],
  version = '0.0.2.4',
  description = 'A library for determining if a machine learning model is overfit. Used for regression and classification tasks.',
  author = 'Matt Michelson',
  author_email = 'mmichelson@inferlink.com',
  url = 'https://github.com/usc-isi-i2/dsbox-overfit-detector',
  download_url = 'https://github.com/usc-isi-i2/dsbox-overfit-detector/archive/0.0.4.tar.gz',
  keywords = ['machine learning', 'generalization', 'overfitting'],
  install_requires=["nose == 1.3.7", "numpy == 1.13.1", "pandas == 0.20.3","scikit-learn == 0.19.0",
                    "scipy == 0.19.1", "six == 1.10.0", "sklearn == 0.0"],
    python_requires='>=3',
)
