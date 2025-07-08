def mergeSort(arr):
    if len(arr) <= 1:
        return arr
    pivot = len(arr) // 2
    left = arr[0:pivot]
    right = arr[pivot:len(arr)]
    sortedLeft = mergeSort(left)
    sortedRight = mergeSort(right)
    return merge2lists(sortedLeft, sortedRight)

#two pointer sort
def merge2lists(left, right):
    pointerL = 0
    pointerR = 0
    sorted = []

    while pointerL < len(left) and pointerR < len(right):
        if left[pointerL] < right[pointerR]:
            sorted.append(left[pointerL])
            pointerL += 1
        else:
            sorted.append(right[pointerR])
            pointerR += 1
    sorted.extend(left[pointerL:])
    sorted.extend(right[pointerR:])
    return sorted

array = [1,2,115,23,4,115, 5]
print(mergeSort(array))

#Merge Sort taking O(nlogn) time always