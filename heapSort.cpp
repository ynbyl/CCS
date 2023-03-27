#include <iostream>
#include <vector>
#include <chrono>

using namespace std;

void swap(int& a, int& b)
{
    int temp = a;
    a = b;
    b = temp;
}

void heapify(vector<int>& arr, int x, int y)
{
    int largest = y; 
    int left = 2 * y + 1;
    int right = 2 * y + 2;

    if (left < x && arr[left] > arr[largest])
        largest = left;

    if (right < x && arr[right] > arr[largest])
        largest = right;

    if (largest != y)
    {
        swap(arr[y], arr[largest]);
        heapify(arr, x, largest);
    }
}


void heapsort(vector<int>& arr)
{
    int x = arr.size();

    for (int y = x / 2 - 1; y >= 0; y--)
        heapify(arr, x, y);

    for (int y = x -1; y >= 0; y--)
    {
        swap(arr[0], arr[y]);
        heapify(arr, y, 0);
    }
}




int main() 
{
    int size = n; //to a size you prefer
    vector<int> arr(size);
    srand(time(NULL));
    for (int i = 0; i < size; i++) 
    {
        arr[i] = rand() % size;
    }
    
    auto start_time = chrono::high_resolution_clock::now();

    heapSort(arr);

    auto stop_time = chrono::high_resolution_clock::now();
    double duration = chrono::duration_cast<chrono::milliseconds>(stop_time - start_time).count();

    cout << "Runtime: " << duration << " ms" << endl;
    return 0;
}