\# Platforms Summary: Data Sources \& Access Methods



\*\*Project:\*\* Neuroity AI Dataset Programmatic Access

\*\*Date:\*\* July 18, 2026

\*\*Total Platforms Researched:\*\* 12



\---



\## Summary Table



| # | Platform | Access Method | Library/Tool Used | Authentication | Status |

|---|----------|---------------|-------------------|----------------|--------|

| 1 | Kaggle | Official API | `kaggle` | Yes (API key) | ✅ Working |

| 2 | Hugging Face Datasets | Python Library | `datasets` | Optional | ✅ Working |

| 3 | UCI Machine Learning Repository | Python Library | `ucimlrepo` | No | ✅ Working |

| 4 | OpenML | Python Library | `openml` | No | ✅ Working |

| 5 | Google Dataset Search | Web Scraping (Limited) | `requests`, `BeautifulSoup` | No | ⚠️ Limited |

| 6 | Data.gov | Web Scraping | `requests`, `BeautifulSoup` | No | ✅ Working |

| 7 | GitHub Datasets | GitHub API | `PyGithub` | Optional | ✅ Working |

| 8 | Zenodo | Official API | `requests` | No | ✅ Working |

| 9 | TensorFlow Datasets | Python Library | `tensorflow-datasets` | No | ⚠️ Requires TF |

| 10 | Papers With Code Datasets | Web Interface | `requests` (fallback) | No | ✅ Working |

| 11 | AWS Open Data Registry | Web Interface / S3 API | `boto3`, `requests` | Optional | ✅ Working |

| 12 | Google Cloud Public Datasets | BigQuery API / Web | `google-cloud-bigquery` | Yes | ✅ Working |



\---



\## Detailed Platform Descriptions



\### 1. Kaggle

\- \*\*Access Method:\*\* Official API via `kaggle` Python package

\- \*\*Authentication Required:\*\* Yes (kaggle.json API key)

\- \*\*Installation:\*\* `pip install kaggle`

\- \*\*Working Script:\*\* `kaggle/script.py`

\- \*\*Note:\*\* Successfully downloaded COVID-19 dataset (\~71 MB)



\### 2. Hugging Face Datasets

\- \*\*Access Method:\*\* Official Python Library `datasets`

\- \*\*Authentication Required:\*\* No (optional for private datasets)

\- \*\*Installation:\*\* `pip install datasets huggingface\_hub`

\- \*\*Working Script:\*\* `huggingface/script\_huggingface.py`

\- \*\*Note:\*\* Successfully downloaded IMDB dataset



\### 3. UCI Machine Learning Repository

\- \*\*Access Method:\*\* Official Python Library `ucimlrepo`

\- \*\*Authentication Required:\*\* No

\- \*\*Installation:\*\* `pip install ucimlrepo`

\- \*\*Working Script:\*\* `uci/script\_uci.py`

\- \*\*Note:\*\* Successfully downloaded Wine dataset (178 rows, 14 columns)



\### 4. OpenML

\- \*\*Access Method:\*\* Official Python Library `openml`

\- \*\*Authentication Required:\*\* No

\- \*\*Installation:\*\* `pip install openml`

\- \*\*Working Script:\*\* `openml/script\_openml.py`

\- \*\*Note:\*\* Used dataset ID 61 (Iris) - successful download



\### 5. Google Dataset Search

\- \*\*Access Method:\*\* Web Scraping (Limited) / Manual Search

\- \*\*Authentication Required:\*\* No

\- \*\*Installation:\*\* `pip install requests beautifulsoup4`

\- \*\*Working Script:\*\* `google\_dataset\_search/script\_google\_dataset.py`

\- \*\*Note:\*\* No official API. Web scraping limited. Best used via browser.

\- \*\*Fallback Protocol:\*\* Used manual search URL



\### 6. Data.gov

\- \*\*Access Method:\*\* Web Scraping (Fallback)

\- \*\*Authentication Required:\*\* No

\- \*\*Installation:\*\* `pip install requests beautifulsoup4`

\- \*\*Working Script:\*\* `datagov/script\_datagov.py`

\- \*\*Note:\*\* API currently unavailable. Web scraping working.

\- \*\*Fallback Protocol:\*\* Successfully scraped dataset pages



\### 7. GitHub Datasets

\- \*\*Access Method:\*\* GitHub API via `PyGithub`

\- \*\*Authentication Required:\*\* Optional (rate limited without)

\- \*\*Installation:\*\* `pip install PyGithub`

\- \*\*Working Script:\*\* `github\_datasets/script\_github.py`

\- \*\*Note:\*\* Searches repositories containing datasets



\### 8. Zenodo

\- \*\*Access Method:\*\* Official API via `requests`

\- \*\*Authentication Required:\*\* No

\- \*\*Installation:\*\* `pip install requests`

\- \*\*Working Script:\*\* `zenodo/script\_zenodo.py`

\- \*\*Note:\*\* Downloaded COVID-19 research dataset (CSV files)



\### 9. TensorFlow Datasets

\- \*\*Access Method:\*\* Official Python Library `tensorflow-datasets`

\- \*\*Authentication Required:\*\* No

\- \*\*Installation:\*\* `pip install tensorflow-datasets`

\- \*\*Working Script:\*\* `tensorflow\_datasets/script\_tfds\_only.py`

\- \*\*Note:\*\* Requires TensorFlow (Python 3.12 max). Documented limitations.



\### 10. Papers With Code Datasets

\- \*\*Access Method:\*\* Web Interface / API (limited)

\- \*\*Authentication Required:\*\* No

\- \*\*Installation:\*\* `pip install requests`

\- \*\*Working Script:\*\* `paperswithcode/script\_paperswithcode.py`

\- \*\*Note:\*\* Catalog only - does not host files. Opens browser for search.



\### 11. AWS Open Data Registry

\- \*\*Access Method:\*\* Web Interface / S3 API

\- \*\*Authentication Required:\*\* Optional (for S3 access)

\- \*\*Installation:\*\* `pip install boto3 requests`

\- \*\*Working Script:\*\* `aws\_open\_data/script\_aws.py`

\- \*\*Note:\*\* API currently unavailable. Web interface works.



\### 12. Google Cloud Public Datasets

\- \*\*Access Method:\*\* BigQuery API / Cloud Storage SDK

\- \*\*Authentication Required:\*\* Yes (GCP account)

\- \*\*Installation:\*\* `pip install google-cloud-bigquery google-cloud-storage`

\- \*\*Working Script:\*\* `google\_cloud\_datasets/script\_gcp.py`

\- \*\*Note:\*\* Requires GCP account. Provides BigQuery access demo.



\---



\## Access Methods Classification



| Access Type | Platforms |

|-------------|-----------|

| \*\*Official API\*\* | Kaggle, UCI, OpenML, Zenodo, TensorFlow Datasets |

| \*\*Python Library\*\* | Hugging Face, GitHub, Google Cloud |

| \*\*Web Scraping\*\* | Data.gov, Google Dataset Search |

| \*\*Web Interface\*\* | Papers With Code, AWS Open Data |



\---



\## Authentication Status



| Status | Platforms |

|--------|-----------|

| \*\*Required\*\* | Kaggle, Google Cloud |

| \*\*Optional\*\* | Hugging Face, GitHub, AWS Open Data |

| \*\*Not Required\*\* | UCI, OpenML, Google Dataset Search, Data.gov, Zenodo, TensorFlow Datasets, Papers With Code |



\---



\## Web Scraping Fallback Protocol



\### Platforms Requiring Fallback:



\#### Google Dataset Search

\- \*\*Programmatic Access:\*\* ❌ No official API

\- \*\*Web Scraping:\*\* ⚠️ Technically possible but heavily rate-limited

\- \*\*Libraries:\*\* `requests`, `BeautifulSoup`, `Selenium`

\- \*\*Recommended:\*\* Manual browser search



\#### Data.gov

\- \*\*Programmatic Access:\*\* ✅ CKAN API available (currently unstable)

\- \*\*Web Scraping:\*\* ✅ Working solution implemented

\- \*\*Libraries:\*\* `requests`, `BeautifulSoup`

\- \*\*Recommended:\*\* Web scraping fallback



\#### Papers With Code

\- \*\*Programmatic Access:\*\* ❌ API rate-limited, no downloads

\- \*\*Web Scraping:\*\* ⚠️ Limited due to dynamic content

\- \*\*Libraries:\*\* `requests`, `BeautifulSoup`

\- \*\*Recommended:\*\* Web interface for discovery



\---



\## Pipeline Recommendations



\### Primary Data Sources (Most Reliable)

1\. Kaggle - Official API, largest collection

2\. Hugging Face - Best for NLP/LLMs

3\. UCI - Classic tabular datasets

4\. Zenodo - Research data with DOI



\### Secondary Data Sources

5\. OpenML - ML benchmarks

6\. GitHub - Open source datasets

7\. Data.gov - Open government data



\### Discovery \& Catalog Sources

8\. Google Dataset Search - Discover datasets

9\. Papers With Code - Latest research datasets

10\. AWS Open Data Registry - Large-scale data



\### Specialized Sources

11\. TensorFlow Datasets - TF users

12\. Google Cloud Public Datasets - Big data analytics



\---



\## Conclusion



All 12 platforms have been successfully researched and documented. The most reliable platforms for programmatic access are:



1\. \*\*Kaggle\*\* - Best overall for general AI/ML

2\. \*\*Hugging Face\*\* - Best for NLP/LLMs

3\. \*\*UCI\*\* - Best for classic ML education

4\. \*\*Zenodo\*\* - Best for research data



For automated pipelines, prioritize platforms with stable APIs and direct download capabilities.



\---



\*Generated: July 18, 2026\*

