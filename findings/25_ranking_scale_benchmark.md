# 25 - Ranking Scale Benchmark

## Executive Summary

The personalized ranking pipeline was benchmarked locally using chunked inference across increasingly large candidate sets.

| Candidates | Runtime | Throughput |
|---:|---:|---:|
| 100,000 | 0.32 s | 314K rows/s |
| 500,000 | 1.14 s | 440K rows/s |
| 1,000,000 | 3.03 s | 330K rows/s |

## Conclusion

The ranking pipeline successfully scored **1 million candidate rows in 3.03 seconds** on a local machine.

Throughput remained above approximately **300K candidates/second** across all tested scales.

Chunked inference allowed large candidate sets to be processed without materializing a separate million-row dataset in memory.

## Engineering Interpretation

The benchmark demonstrates that the current implementation can efficiently perform batch candidate scoring at moderate scale.

This is a **local single-machine benchmark** and should not be interpreted as distributed-system or production-serving throughput.