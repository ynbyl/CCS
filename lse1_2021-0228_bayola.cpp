    #include <iostream>
    using namespace std;
    
    struct Link
    {
        int value;
        Link *next;
    };
    
    int main()
    {
        int node = 20, out = 100;
 
        Link *nought = NULL;
        Link *one = NULL;
        
        for(int i=1; i<=node; i++)
        {
            Link *neww = new Link();
            neww->value = i;
            
            if(nought == NULL)
            {
                nought = neww;
            }
            
            neww->next = nought;
            
            if(one != NULL) 
            {
                one->next = neww;
            }
            
            one = neww;
        }
        
        Link* current = nought;
        for(int i=0; i<out; ++i)
        {
            cout << current->value << " ";
            if(i != out-1)
            {
                cout << "-> ";
            }
            
            current = current->next;
        }
    
    
        Link *current_del = nought;
        
        Link *temp;
        
        for (int i = 1; i <= node; i++)
        {
            temp = current_del->next;
            delete current_del;
            current_del = temp;
        }
    
        return 0;    
        
        
        
    }