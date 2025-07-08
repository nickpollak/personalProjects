def bubbleSort(arr):
    for i in range(len(arr)):
        for j in range(0, len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
    return arr
#Bubble sort takes O(n^2) time and makes the largest element "bubble" to the end of the array
#thats why we can subtract i from the j loop and still sort things

array = [12,51,52,1,6]
print(bubbleSort(array))