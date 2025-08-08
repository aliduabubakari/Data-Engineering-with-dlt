import dlt
from dlt.sources.rest_api import rest_api_source

pipeline = dlt.pipeline(
    pipeline_name="rest_api_pokemon",
    destination="duckdb",
    dataset_name="rest_api_data"
)

pokemon_api = rest_api_source({
    "client": {
        "base_url": "https://pokeapi.co/api/v2/"
    },
    "resource_defaults": {
        "endpoint": {
            "params": {
                "limit": 1000,
            },
        },
        "write_disposition": "replace"
    },
    "resources": [
        {
            "name": "pokemon",
            "primary_key": "name",
            "write_disposition": "merge"
        },
        "berry",
        "location"
    ]
})

load_info = pipeline.run(pokemon_api)
print(load_info)
