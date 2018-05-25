from distutils.core import setup


setup(name="WebCrawler",
      version="1.0",
      description="Application focused on scraping a domain looking for pages following a specific pattern",
      author="Carlos Monteiro",
      author_email="carlos_monteiro@poli.ufrj.br",
      packages=["crawler"],
      package_dir={"crawler": "crawler"}
)
