import statistics

arr = [
0.0,
15.0,
23.0,
0.0,
18.0,
19.0,
24.0,
24.0,
1.0,
14.0,
0.0,
27.0,
23.0,
1.0,
10.0,
0.0,
23.0,
26.0,
22.0,
29.0,
27.0,
20.0,
15.0,
24.0,
17.0,
30.0,
25.0,
30.0,
30.0,
27.0,
20.0,
30.0,
14.0,
29.0,
16.0,
30.0,
30.0,
20.0,
30.0,
30.0,
17.0,
1.0,
22.0,
25.0
]


average = sum(arr) / len(arr)
mean = statistics.mean(arr)
median = statistics.median(arr)
mode = statistics.mode(arr)
std_dev = statistics.stdev(arr)

print("Average:", average)
print("Mean:", mean)
print("Median:", median)
print("Mode:", mode)
print("Standard Deviation:", std_dev)