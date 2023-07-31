#include<iostream>
#include <string>
#include <functional>
using namespace std;
std::hash<std::string> h;

struct Merkletree
{
	int left = -1;
	int right = -1;
	int parent = -1;
	int depth = -1;
	int num = -1;
	string hash_i;
};

const int num = 200000;
int r = 0;
int q = -1;
int p = -1;
int num1 = num;
int num2 = 0;
int tdepth = 0;
Merkletree arr[2 * num];

void Change_depth(Merkletree* tmp)
{
	if (tmp->left == -1 && tmp->right == -1)
	{
		tmp->depth++;
		return;
	}
	Change_depth(&(arr[tmp->left]));
	tmp->depth++;
	Change_depth(&(arr[tmp->right]));
}

string Hash(string str)
{
	size_t n = h(str);
	string Newstring = to_string(n);
	return Newstring;
}

void Merkle_tree()
{
	int num_1 = 0;
	int i = 0;
	do
	{
		int c = i;
		int d = i - num2;
		for (i; i < num1 + c; i++)
		{
			if (num1 != num)
			{
				if (p != -1)
				{
					arr[i].left = p;
					arr[p].parent = i;
					arr[i].right = d;
					arr[d].parent = i;
				}
				else
				{
					arr[i].left = d;
					arr[d].parent = i;
					arr[i].right = d + 1;
					arr[d + 1].parent = i;
				}

				d = d + 2;
				arr[i].depth = tdepth;
				arr[i].num = arr[arr[i].left].num + arr[arr[i].right].num;
				arr[i].hash_i = Hash(arr[arr[i].left].hash_i + arr[arr[i].right].hash_i);
			}
			else
			{
				arr[i].depth = tdepth;
				arr[i].num = i;
				arr[i].hash_i = Hash(to_string(i));
			}
		}
		if (num1 == 1)
		{
			num_1++;
		}
		if (num_1 == 2)
			return;
		if ((num1 + r) % 2 == 0)
		{
			num2 = num1;
			num1 = (num1 + r) / 2;
			r = 0;
			p = q;
			q = -1;
		}
		else
		{
			if (q == -1)
			{
				q = i - 1;
			}
			Change_depth(&(arr[q]));
			num2 = (num1);
			num1 = (num1 + r) / 2;
			r = 1;
		}
		tdepth++;
	} while (num1 > 0);
}

bool MT_proof(int points)
{
	if (arr[points].left != -1 && arr[points].right != -1)
	{
		return 0;
	}
	string b = Hash(to_string(arr[points].num));
	int c = points;
	do
	{
		int a = arr[c].parent;
		if (arr[a].right != c)
		{
			b = Hash(b + arr[arr[a].right].hash_i);
		}
		else b = Hash(arr[arr[a].left].hash_i + b);
		c = a;
	} while (arr[c].parent != -1);
	if (b == arr[c].hash_i)
		return 1;
	else return 0;
}

bool MT_not_proof(double points)
{
	int m = points;
	int n = m+ 1;
	bool n1 = MT_proof(m);
	bool n2 = MT_proof(n);
	if (n1 && n2)
	{
		return 1;
	}
	else return 0;
}

int main()
{
	Merkle_tree();
	if (MT_proof(4))
		cout << "Merkle_tree_proof成功!" << endl;
	else cout << "Merkle_trree_proof 失败!" << endl;

	if (MT_not_proof(5.5))
		cout << "MT_not_proof 成功" << endl;
	else cout << "MT_not_proof 失败!" << endl;
	return 0;
}