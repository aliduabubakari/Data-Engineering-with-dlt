from typing import Any, Iterator
import dlt
from dlt.sources import TDataItems
from dlt.sources.filesystem import FileItemDict
from dlt.sources.filesystem import filesystem

@dlt.transformer()
def read_csv_custom(items: Iterator[FileItemDict], chunksize: int = 10000, **pandas_kwargs: Any) -> Iterator[TDataItems]:
    import pandas as pd
    import uuid

    kwargs = {**{"header": "infer", "chunksize": chunksize}, **pandas_kwargs}

    for file_obj in items:
        with file_obj.open() as file:
            for df in pd.read_csv(file, **kwargs):
                df["file_name"] = file_obj["file_name"]
                df["id"] = [str(uuid.uuid4()) for _ in range(len(df))]  # Generate unique ID
                yield df.to_dict(orient="records")

# Select JSON or CSV files
files = filesystem(file_glob="encounters*.csv")
files.apply_hints(incremental=dlt.sources.incremental("modification_date"))

reader = (files | read_csv_custom()).with_name("encounters")
reader.apply_hints(primary_key="id", incremental=dlt.sources.incremental("STOP"))

pipeline = dlt.pipeline(
    pipeline_name="filesystem_pipeline",  # or match with `hospital_data_pipeline` if using that name
    dataset_name="hospital_data",
    destination="duckdb",
    dev_mode=False  # recommended instead of deprecated full_refresh
)

info = pipeline.run(reader, write_disposition="merge")
print(info)