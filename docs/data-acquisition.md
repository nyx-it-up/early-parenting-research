# Data Acquisition Log

This log records every raw data file used in the project: source, release, download date and checksums. Raw files live in `data/raw/` and are **not** under version control (see `.gitignore`). To reproduce the analysis, re-download from the URLs below and check the SHA-256 checksums.

Checksums are SHA-256. "Last-Modified" is the server header at download time and shows which release of a file was retrieved.

---

## NSCH: National Survey of Children's Health (topical files, Stata)

- **Source:** U.S. Census Bureau, NSCH datasets: https://www.census.gov/programs-surveys/nsch/data/datasets.html
- **Downloaded:** 2026-10-30 (completed 20:02:57 UTC)
- **Location:** `data/raw/nsch/{year}/`
- **Format:** Each zip contains one Stata data file (`.dta`) and one Stata label script (`.do`). All three data files are the "enhanced" (`e`) releases.
- **Purpose:** NSCH feasibility check (research plan Section 11). 2023–2025 are the years with the detailed employment variable `A1_EMPLOYED_R`.

### Downloaded archives

| Year | URL | Bytes | Last-Modified | SHA-256 |
|---|---|---|---|---|
| 2025 | https://www2.census.gov/programs-surveys/nsch/datasets/2025/nsch_2025_topical_Stata.zip | 5,507,296 | Mon, 05 Oct 2026 13:15:24 GMT | `e7ffdc758bc0c2ac8ed7bd666176c292ceb2f38bf6b019bcbc0000767b1d6720` |
| 2024 | https://www2.census.gov/programs-surveys/nsch/datasets/2024/nsch_2024_topical_Stata.zip | 6,252,225 | Tue, 02 Dec 2025 14:00:23 GMT | `a12d1839cae8b843884e7fb5b520835844ee6304c496ba7873d7f8a4152fe2e0` |
| 2023 | https://www2.census.gov/programs-surveys/nsch/datasets/2023/nsch_2023e_topical_Stata.zip | 6,583,004 | Wed, 03 Dec 2025 15:00:26 GMT | `61c8cc0366e7ef07e934dba290b99895b86e39c493d06ab09081a42948d5be1a` |

### Extracted files

| Year | File | SHA-256 |
|---|---|---|
| 2025 | `nsch_2025e_topical.dta` | `2a1570249f9e9506428d841c7bc12b7a7320d2462a986adf84098de90cb9881f` |
| 2025 | `nsch_2025_topical.do` | `321c670db5ba189873b1f8d5115968da2f40513f3c73bb941fa176155dd45263` |
| 2024 | `nsch_2024e_topical.dta` | `0b03ecb3a6f905c6c90961b089e1efbc9fbf64da77716729ad31f950ab7d682e` |
| 2024 | `nsch_2024_topical.do` | `c5690cd25056414ce97a6943c256280ce932f6e57ed6ffcb5af1a9842227faf7` |
| 2023 | `nsch_2023e_topical.dta` | `9ff72c95d8f6cf341d159d957c254360152f2701bb8b6504dacb05d39754d1e3` |
| 2023 | `nsch_2023_topical.do` | `7ca650d9e5335d370375d6800fc629d3ed3105aad054e8a6342af4fed4e13cd0` |

### Integrity checks performed

| Year | Rows | Columns | Core variables present* | Notes |
|---|---|---|---|---|
| 2025 | 45,139 | 458 | All | Row count matches the 45,139 completed topical questionnaires reported in the 2025 NSCH FAQs |
| 2024 | 51,375 | 457 | All | |
| 2023 | 55,162 | 456 | All | |

\*Checked: `HHID`, `FWC`, `FIPSST`, `STRATUM`, `SC_AGE_YEARS`, `A1_SEX`, `A1_RELATION`, `A1_EMPLOYED_R`, `A1_MENTHEALTH`, `K8Q31`, `K8Q35`, `HOURSLEEP05`, `TENURE`, `FPL_I1`.

**Not downloaded:** the SAS versions; the 2024 screener file (the screener public file was discontinued after 2024 and is not needed); the "Title V Code" files.
