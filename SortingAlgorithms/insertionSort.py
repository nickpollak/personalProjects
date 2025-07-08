def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        for j in range(i - 1, -1 , -1):
            if key < arr[j]:
                arr[j + 1] = arr[j]
            else:
                arr[j + 1] = key
                break      
        else:
                arr[0] = key
    return arr
#Using two for loops to get the array sorted using insertion


def insertionSort2(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
#Using a nested while loop to get the array sorted using insertion
#Takes O(n^2) at worst time
        
array = [12,51,52,1,6]
print(insertionSort(array))
print(insertionSort2(array))