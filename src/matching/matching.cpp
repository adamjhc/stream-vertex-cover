// Taken from https://projects.csail.mit.edu/dnd/matching.cpp

#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <ctime>
#include <algorithm>
#include <cmath>
using namespace std;

typedef pair<int, int> joft;

vector<int> randind;

struct MaximalM
{
    int size;
    vector<joft> m;
    set<int> mv;

    MaximalM(int size = 0) : size(size)
    {
        m.resize(0);
        mv.clear();
    }

    bool update(joft e)
    {
        if ((int)m.size() < size && mv.find(e.first) == mv.end() && mv.find(e.second) == mv.end())
        {
            m.push_back(e);
            mv.insert(e.first);
            mv.insert(e.second);
            return true;
        }
        else
            return false;
    }
    int estimate() const
    {
        return m.size();
    }
};

// Assumes that randind contains a permutation of 0..n-1. A vertex is heavy, if it's degree is >=threshold+1
struct HeavySample
{
    int n;
    int threshold;
    map<int, int> deg;
    int hcount;

    HeavySample(int n = 0, int size = 0, int threshold = 0) : n(n), threshold(threshold)
    {
        deg.clear();
        hcount = 0;
        random_shuffle(randind.begin(), randind.end());

        for (int i = 0; i < size; i++)
        {
            deg[randind[i]] = 0;
        }
    }

    void update(joft e)
    {
        if (deg.find(e.first) != deg.end())
        {
            deg[e.first]++;
            if (deg[e.first] == threshold + 1)
                hcount++;
        }
        if (deg.find(e.second) != deg.end())
        {
            deg[e.second]++;
            if (deg[e.second] == threshold + 1)
                hcount++;
        }
    }

    int estimate() const
    {
        return (hcount * n) / deg.size();
    }
};

// Assumes that randind contains a permutation of 0..n-1
struct ShallowSample
{
    int n;
    int threshold;
    map<int, int> deg;
    map<int, vector<int>> mat;
    int scount;

    ShallowSample(int n = 0, int size = 0, int threshold = 0) : n(n), threshold(threshold)
    {
        deg.clear();
        mat.clear();
        scount = 0;
        random_shuffle(randind.begin(), randind.end());

        for (int i = 0; i < size; i++)
        {
            deg[randind[i]] = 0;
            mat[randind[i]] = vector<int>();
        }
    }

    void update(joft e)
    {
        if (deg.find(e.first) != deg.end())
        {
            deg[e.first]++;
            if (deg[e.first] == threshold + 1)
            {
                scount -= mat[e.first].size();
                for (int i = 0; i < (int)mat[e.first].size(); i++)
                {
                    int a = mat[e.first][i];
                    for (int j = 0; j < (int)mat[a].size(); j++)
                        if (mat[a][j] == e.first)
                        {
                            mat[a][j] = mat[a][mat[a].size() - 1];
                            mat[a].resize(mat[a].size() - 1);
                        }
                }
                mat[e.first].resize(0);
            }
        }

        if (deg.find(e.second) != deg.end())
        {
            deg[e.second]++;
            if (deg[e.second] == threshold + 1)
            {
                scount -= mat[e.second].size();
                for (int i = 0; i < (int)mat[e.second].size(); i++)
                {
                    int a = mat[e.second][i];
                    for (int j = 0; j < (int)mat[a].size(); j++)
                        if (mat[a][j] == e.second)
                        {
                            mat[a][j] = mat[a][mat[a].size() - 1];
                            mat[a].resize(mat[a].size() - 1);
                        }
                }
                mat[e.second].resize(0);
            }
        }

        if (deg.find(e.first) != deg.end() && deg[e.first] <= threshold && deg.find(e.second) != deg.end() && deg[e.second] <= threshold)
        {
            scount++;
            mat[e.first].push_back(e.second);
            mat[e.second].push_back(e.first);
        }
    }

    int estimate() const
    {
        return (scount * n * (n - 1)) / (deg.size() * (deg.size() - 1));
    }
};

MaximalM mbase;

vector<HeavySample> h;
vector<ShallowSample> s;

vector<joft> edgeSet;

int main()
{
    ios_base::sync_with_stdio(false);
    srand(time(0));
    int n; // Assuming vertices are numbered 0..n-1
    cin >> n;
    randind.resize(n);
    for (int i = 0; i < n; i++)
        randind[i] = i; // This is necessary

    int samplesize = (int)pow((long double)n, 2.0 / 3.0);
    if (samplesize > n)
        samplesize = n;

    mbase = MaximalM(samplesize);

    int Q;   //number of parallel executions
    int eta; //avg degree;

    //cin>> Q;
    //cin>>eta;
    long long m;
    Q = 100;
    cin >> m;
    eta = ((double)m) / n;
    int mu = 2 * eta; // threshold

    cerr << "samplesize=" << samplesize << endl;
    h.resize(Q);
    for (int i = 0; i < (int)h.size(); i++)
        h[i] = HeavySample(n, samplesize, mu);

    s.resize(Q);
    for (int i = 0; i < (int)s.size(); i++)
        s[i] = ShallowSample(n, samplesize, mu);

    edgeSet.resize(0);
    int a, b;
    double w;
    while (cin >> a >> b >> w)
    {
        joft t = joft(a, b);
        edgeSet.push_back(t);
        mbase.update(t);
        for (int i = 0; i < (int)h.size(); i++)
            h[i].update(t);
        for (int i = 0; i < (int)s.size(); i++)
            s[i].update(t);
    }

    if (mbase.estimate() < samplesize)
    {
        cout << mbase.estimate() << endl;
    }
    else
    {
        int M1 = mbase.estimate();
        vector<int> g;
        g.resize(Q);
        for (int i = 0; i < Q; i++)
        {
            g[i] = M1;
            if (h[i].estimate() / mu > g[i])
                g[i] = h[i].estimate() / mu;
            if (s[i].estimate() / mu > g[i])
                g[i] = s[i].estimate() / mu;
            // cerr<<"i,h,s: "<<i<<' '<<h[i].estimate()<<' '<<s[i].estimate()<<endl;
        }
        sort(g.begin(), g.end());
        cout << g[Q / 2] << endl;
    }

    return 0;
}