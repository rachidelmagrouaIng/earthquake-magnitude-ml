# Dataset

`earthquakes.csv` is the dataset supplied with the academic project. It contains 1,137 rows and 43 columns covering event dates from 2023-06-23 to 2024-09-18, with magnitudes from 3.0 to 7.6.

Event links point to USGS. Additional columns such as `continent`, `what3words` and `locationDetails` indicate enrichment. The exact upstream download URL, collection procedure and redistribution license were not documented in the supplied materials. Do not describe this enriched CSV as an unmodified official USGS export or assign it a license based on its links alone.

The file is preserved byte-for-byte after recovery from the supplied archive. Its SHA-256 appears in `results/run.json`. No live catalog update is performed.

## Field groups

| Fields | Role in this repository |
| --- | --- |
| `magnitude` | Regression target |
| `id`, `updated`, `date` | Revision handling and event-date split |
| `longitude`, `latitude`, `depth` | Primary regression inputs |
| `sig`, `mmi`, `cdi`, `alert` | Target-related/post-event fields retained only in the diagnostic comparison |
| `nst`, `rms`, `dmin`, `status`, `magType`, `continent` | Other inputs for the catalog diagnostic |
| Remaining columns | Preserved in CSV, excluded from model input |

For official field definitions see [USGS ComCat](https://earthquake.usgs.gov/data/comcat/). The earlier notebook selects 14 columns including the target; v2 follows a wider selection and drops descriptive/constant fields. The maintained script validates its own catalog feature set plus the target, event IDs and dates.
