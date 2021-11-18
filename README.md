# im3-wrf

## Data Hierarchy

- `domain` is the folder to store LA county boundary data (e.g. county, city, neighborhood, census track boundaries in GeoJSON)

- `building-data` is the folder to store building footprint geojson files

- `ref_buildings` is the folder to store DOE/TITLE24 reference model and E+ simulation results.

- `bldg-wrf-mapping` is the folder to store mapping information from building to WRF grid cells in JSON format.

- `M02_EnergyPlus_Forcing_Historical` is the main working folder for each simulation rounds. 

1. `meta` is the metadata folder for WRF variables and grids information (e.g. lat & lon). 

2. `T2` (for temperature) and other variable-named folder are the WRF matrix data for each variable at each round (one .txt file for each hour). 

3. `time_series` is the intermediate result folder sorting `txt` WRF data to time series CSV.

4. `grids_csv` is the grid level weather data CSV containing all variables required for E+.

5. `wrf_epw` is the grid level EPW files converted from CSV files.

6. `eplus-results-base-csv` is the raw E+ simulation results for each grid and each building type. (e.g. `1-SSF.csv` is the results for GridID 1, Small Single Family)

7. `eplus-grid-emission-results` is the grid aggregated emission results in CSV format (unit: GJ).

8. `eplus-final-results` is the normalized emission intensity for each grid in CSV format (unit: kWh/m2).

9. `eplus-final-results-matrix` is the heat emission intensity results converted to WRF grid matrix format (one .txt file for each hour).

- `transportation-data` is the input and output folder for aggregating transportation data.

## Initialization of a new domain

1. Run `0_write_wrf_geojson` to generate WRF grid GeoJSON boundaries from raw (lat, lon) information for mapping and aggregation later.

2. Run `1_la_bldg_map` to (1) read domain-wide building footprint GeoJSON file (sorted for CityBES ready) and clean up the dataset, and (2) Map buildings to WRF grids and write the mapping info in JSON format.


## Simulation of a new forcing

1. Run `0_mv_inputs.py` to init an new working folder.

2. Run `2_wrf_to_csv_epw` to read raw input from WRF, preprocess and convert the data to EPW files.

3. Run `3_write_baseline_idf` to modify the reference E+ models with desired simulation input and emission output.

4. Run `4_post_process` to aggegregate emission results to WRF grid level.

5. Run `5_wrf_la_data_plotting` for result visualization.

6. Run `6_transportation_data` to process transportation CO2 data and aggregate the data to emission intensity at WRF grid level.
