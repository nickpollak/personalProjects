def selectionSort(arr):
    for i in range(len(arr)):
        minIndex = i
        for j in range(i + 1, len(arr)):
            if arr[minIndex] > arr[j]:
                minIndex = j
        temp = arr[minIndex]
        arr[minIndex] = arr[i]
        arr[i] = temp
    return arr

array = [12,51,52,1,6]
print(selectionSort(array))

#This is a slow sort going in O(n^2) time due to the nested loops