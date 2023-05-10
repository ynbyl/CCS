#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <chrono>

using namespace std;

void randomSort(vector<int>& arr)
{
    srand(time(NULL)); 
    int n = arr.size();
    bool sorted = false;
    while (!sorted) 
    {
        sorted = true;
        for (int i = 0; i < n-1; i++) 
        {
            int j = rand() % n; 
            if (i < j && arr[i] > arr[j]) 
            {
                swap(arr[i], arr[j]);
                sorted = false;
            }
        }
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
    randomSort(arr);
    auto stop_time = chrono::high_resolution_clock::now();
    double duration = chrono::duration_cast<chrono::microseconds>(stop_time - start_time).count();

    cout << "Runtime: " << duration << " us" << endl;
    return 0;
}
