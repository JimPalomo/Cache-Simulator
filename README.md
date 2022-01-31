# Cache-Simulator

### Description
The Cache Simulator is developed in Python. Four different cache configurations were simulated to output detailed step-by-step information and hit or missed targets.

### Cache Configurations:
- A. (N=1, S=1, b=64) a simplest cache, with only 1 block, size of 64 B
- B. (N=1, S=4, b=16) a Direct Map cache with 4 sets, block size of 16 B
- C. (N=4, S=1, b=16) a 4-way Fully Associative cache, cache, block size of 8 B [LRU]
- D. (N=2, S=4, b=8) a 2-way 4-set, Set Associative cache, block size of 8 B [LRU]

### Program Includes:
- Detailed step-by step information of memory breakdown (tag, valid bit, offset), LRU (least recently used) information, and hit/miss results
- Two modes: Fast Mode (output only hit/miss results), Detailed Mode (output step-by-step cache attempt information and hit/miss results

### Example of Detailed Mode
![alt text]()
![alt text]()
![alt text]()
### Example of Fast Mode
![alt text]()
![alt text]()