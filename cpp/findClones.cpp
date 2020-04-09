#include <bits/stdc++.h>

using namespace std;

const int COLS = 384;
const double THERESHOLD = 60;


struct Snippet
{
    string folder;
    string fname;
    int lineStart;
    int lineEnd;
    double array[COLS];
};


double getDistance(double *a, double *b)
{
    double result = 0;
    for(int i = 0; i < COLS; i++)
        result += (a[i] - b[i]) * (a[i] - b[i]);
    return result;
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    freopen("ClonesWithDistance", "w", stdout);
    int rows, cols=384;
    for(int folder_ = 2; folder_ < 46; folder_++)
    {
        if(folder_ == 16)
            continue;
        string ss = "../data" + to_string(folder_) + ".csv";
        char cc[15];
        strcpy(cc, ss.c_str());
        //cout << cc;
        freopen(cc, "r", stdin);
        cin >> rows >> cols;
        Snippet *data = new Snippet[rows];
        Snippet one;
        for(int i = 0; i < rows; i++)
        {
            cin >> one.folder >> one.fname;
            cin >> one.lineStart >> one.lineEnd;
            for(int j = 0; j < COLS; j++)
                cin >> one.array[j];
            data[i] = one;
        }
        double dist, subs;
        for(int i = 0; i < rows; i++)
        {
            for(int j = i + 1; j < rows; j++)
            {
                dist = 0;
                for(int k = 0; k < COLS; k++)
                {
                    subs = data[i].array[k] - data[j].array[k];
                    dist += subs * subs;
                }
                if(dist < THERESHOLD)
                {
                    cout << data[i].folder << ',' << data[i].fname << ',' << data[i].lineStart << ',' << data[i].lineEnd << ',' <<
                            data[j].folder << ',' << data[j].fname << ',' << data[j].lineStart << ',' << data[j].lineEnd << ',' << dist << '\n' ;
                }
            }
        }
    }
    return 0;
}
