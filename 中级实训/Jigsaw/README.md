## Jigsaw
See [N Puzzle](https://se-2018.github.io/Stage3--NPuzzle).

**Please make sure that you can pass `test.sh` before submission.**

#### Demo
```shell
# compile
mkdir -p build
javac -encoding UTF-8 -d build -cp src src/Runners/*.java

# run
java -cp build Runners.RunnerDemo
java -cp build Runners.RunnerPart1
java -cp build Runners.RunnerPart2
```


#### Test

##### Constraints

| Item | Limit | Notes |
| :--: | :--: | :--: |
| Time | < 1 secs | guarantee shortest path length no more than 11 in `BFSearch` |
| Memory | < 32 MB | / |
| Code length | < 1MB | / |
| Sensitive operation | forbid | / |

##### Description
Finish class `Solution`.
 - `BFSearch`
 - `estimateValue`

##### Input
You don't need to handle input.

##### Ouput
You don't need to handle output.


##### Sample Input
```
Score Runtime
11
22 1 2 3 4 5 6 7 8 9 10 11 18 12 14 15 21 16 13 19 20 17 0 22 23 24
16 1 2 3 4 5 6 7 8 9 10 11 18 12 14 15 0 16 13 19 20 21 17 22 23 24
1 0 1 8 23 24 16 4 9 7 20 12 3 10 15 17 6 22 5 19 14 21 2 18 11 13
24 8 2 13 9 3 15 22 5 6 21 12 4 14 11 1 18 20 19 7 17 23 24 16 0 10
```

##### Sample Output
```
Jigsaw AStar Search Result:
Begin state:{16,1,2,3,4,5,6,7,8,9,10,11,18,12,14,15,0,16,13,19,20,21,17,22,23,24}
End state:{25,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,0}
Total number of searched nodes:169
Depth of the current node is:9

Runtime:20ms
Jigsaw AStar Search Result:
Begin state:{1,0,1,8,23,24,16,4,9,7,20,12,3,10,15,17,6,22,5,19,14,21,2,18,11,13}
End state:{25,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,0}
Total number of searched nodes:29000
Depth of the current node is:210

Runtime:433ms
Jigsaw AStar Search Result:
Begin state:{24,8,2,13,9,3,15,22,5,6,21,12,4,14,11,1,18,20,19,7,17,23,24,16,0,10}
End state:{25,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,0}
Total number of searched nodes:29000
Depth of the current node is:289

Runtime:470ms

Total Runtime:924ms
Average Runtime:308ms

Score:0

```

##### Run
See `test.sh`.

