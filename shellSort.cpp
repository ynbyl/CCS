#include <iostream>
#include <vector>
#include <chrono>

using namespace std;

void shellSort(vector<int>& arr)
{
    int n = arr.size();
    int gap = n / 2;
    
    while(gap > 0)
    {
        for(int i = gap; i < n; i++)
        {
            int temp = arr[i];
            int j = i;
            
            while (j >= gap && arr[j - gap] > temp)
            {
                arr[j] = arr[j - gap];
                j -= gap;
            }
            arr[j] = temp;
        }
         gap /= 2;
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

    shellSort(arr);

    auto stop_time = chrono::high_resolution_clock::now();
    double duration = chrono::duration_cast<chrono::millisconeds>(stop_time - start_time).count();

    cout << "Runtime: " << duration << " ms" << endl;
    return 0;
}



/*
int main()
{
    int size = 1000
    
    auto start_time = chrono::high_resolution_clock::now();
    shellSort(arr);
    auto stop_time = chrono::high_resolution_clock::now();
    double duration = chrono::duration_cast<chrono::microseconds>(stop_time - start_time).count();

    cout << "Runtime: " << duration << " us" << endl;
    return 0;
}

*/