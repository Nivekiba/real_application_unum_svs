This MapReduce example consists of four functions: `Split`, `Map`, `Shuffle`, and `Reduce`.

The workflow processes text data through the following steps:
1. **Split**: Divides input data into chunks for parallel processing
2. **Map**: Processes each chunk and counts word frequencies
3. **Shuffle**: Organizes the mapped data for the reduce phase
4. **Reduce**: Aggregates the results from all map operations

This workflow requires input data with the following structure:
- `benchmark_bucket`: S3 bucket name for data storage
- `words_bucket`: S3 bucket containing the input text file
- `words`: Name of the text file to process
- `n_mappers`: Number of parallel map operations
- `output_bucket`: S3 bucket for intermediate and final results

Alternatively, you can specify a SQS queue and the `Reduce` function will write its final
output to the SQS queue. See `events/sqs.json` for an example.

`events` directory contains example inputs to the application.
