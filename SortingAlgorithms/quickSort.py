def quickSort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    right = []
    left = []
    for i in range(len(arr) - 1):
        if arr[i] > pivot:
            right.append(arr[i])
        else:
            left.append(arr[i])
    sorted = quickSort(left) + [pivot] + quickSort(right)
    return sorted

#quick sort implemented with recursion and works in O(nlogn) time

array = [12,51,52,1,6]
print(quickSort(array))
