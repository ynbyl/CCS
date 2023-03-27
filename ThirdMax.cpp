#include <iostream>
#include <algorithm>
using namespace std;



/*
 sort the array in ascending order and 
 then iterate over it backwards to find 
 the third maximum value
 */
int ThirdMax1(int arr[], int size)
{
    // Sorts in ascending order
    sort(arr, arr + size);

    // Count the number of elements
    int count = 1;
    for (int i = size - 2; i >= 0; i--)
    {
        if (arr[i] != arr[i + 1])
            {
            count++;
        }
        if (count == 3)
        {
            return arr[i];
        }
    }
    return arr[size - 1];
}



/*
An algorithm that finds the first, second, and third 
maximum elements in the array, looping to replace 
the smallest element if a larger one is found
*/
int ThirdMax2(int arr[], int size)
{
    int firstMax = arr[0];
    int secondMax = arr[0];
    int thirdMax = arr[0];

    // Find the first, second, and third maximum values
    for (int i = 1; i < size; i++)
    {
        if (arr[i] > firstMax)
        {
            thirdMax = secondMax;
            secondMax = firstMax;
            firstMax = arr[i];
        }
        else if (arr[i] > secondMax && arr[i] < firstMax)
        {
            thirdMax = secondMax;
            secondMax = arr[i];
        }
        else if (arr[i] > thirdMax && arr[i] < secondMax)
        {
            thirdMax = arr[i];
        }
    }

    // Loop and replace
    for (int i = 3; i < size; i++)
    {
        if (arr[i] > thirdMax && arr[i] < secondMax)
        {
            thirdMax = arr[i];
        }
        else if (arr[i] > secondMax && arr[i] < firstMax)
        {
            thirdMax = secondMax;
            secondMax = arr[i];
        }
        else if (arr[i] > firstMax)
        {
            thirdMax = secondMax;
            secondMax = firstMax;
            firstMax = arr[i];
        }
    }
    return thirdMax;
}



/*
Another sorting but uses the bubble sort
*/

// Bubble sort implementation
void bubbleSort(int arr[], int size) {
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

// FFinding the third max element with bub sort
int ThirdMax3(int arr[], int size) {
    bubbleSort(arr, size);
    if (size < 3) {
        return arr[0];
    }
    return arr[size - 3];
}







int main()
{
    // first algo
    int arr[] = {1, 5, 2, 7, 3, 9, 8};
    int size = sizeof(arr) / sizeof(arr[0]);
    int thirdMax = ThirdMax1(arr, size);

    cout << "First ThirdMax is: " << thirdMax << endl;


    // second algo
    int arr[] = {1, 8, 12, 4, 5, 3, 10};
    int size = sizeof(arr) / sizeof(arr[0]);
    int thirdMax = ThirdMax2(arr, size);

    cout << "Second ThirdMax is: " << thirdMax << endl; 


    // third algo
    int arr[] = { 5, 9, 1, 3, 8, 4, 7, 6, 2 };
    int size = sizeof(arr) / sizeof(arr[0]);
    int thirdMax = ThirdMax3(arr, size);

    cout << "Third Thirdmax is: " << thirdMax << endl;

    return 0;
}
