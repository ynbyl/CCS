#include <iostream>
#include <vector>
#include <chrono>

using namespace std;

void merge(vector<int>& arr, int a, int b, int c)
{
    int n1 = b - a + 1;
    int n2 = c - b;

    vector<int> L(n1), R(n2); //creat tempo

    //tempo
    for (int x = 0; x < n1; x++)
    {
        L[x] = arr[a + x];
    }

    //tempo
    for (int y = 0; y < n2; y++)
    {
        R[y] = arr[b + 1 +y];
    }

    //merge 
    int x = 0, y = 0, z = a;
    while (x < n1 && y < n2)
    {
        if (L[x] <= R[y])
        {
            arr[z] = L[x];
            x++;
        }
        else
        {
            arr[z] = R[y];
            y++;
        }
        z++;
    }

    while (x < n1)
    {
        arr[z] = L[x];
        x++;
        z++;
    }

    while (y < n2)
    {
        arr[z] = R[y];
        y++;
        z++;
    }
}

void mergeSort(vector<int>& arr, int a, int c)
{
    if (a >= c)
    {
        return;
    }

    int b = a + (c - a) / 2;

    mergeSort(arr, a, b);
    mergeSort(arr, b + 1, c);

    merge(arr, a, b, c);
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
    
    mergeSort(arr, 0, arr.size() - 1);
        
    auto stop_time = chrono::high_resolution_clock::now();
    double duration = chrono::duration_cast<chrono::milliseconds>(stop_time - start_time).count();

    cout << "Runtime: " << duration << " ms" << endl;
    return 0;
}