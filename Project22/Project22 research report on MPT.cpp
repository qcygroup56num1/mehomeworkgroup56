#include<iostream>
#include<string.h>
using namespace std;

int char_to_int(const char*);
int check(string);
void MPT();

int char_to_int(const char* m)
{
	if ((m[0] >= 'a') && (m[0] <= 'z'))
	{
		return m[0] - 'a' + 10;
	}

	else if ((m[0] >= '0') && (m[0] <= '9'))
	{
		return m[0] - '0';
	}
}

struct inode
{
	int wealth = -1;
	bool leaf = 0;
	int pre=0;
	string publictitle;
	inode* next_node[16];
};

inode* testMPT = new inode();

int check(string m)
{
	inode* temp;
	string str_temp = "";
	temp = testMPT;
	int getlength = m.length();
	while (temp->leaf == 0 && getlength > 0)
	{
		str_temp = str_temp + temp->publictitle;
		if (m.substr(0, str_temp.length()) == str_temp)
		{
			string p = m.substr(str_temp.length(), 1);
			str_temp += p;
			temp = temp->next_node[char_to_int(p.c_str())];
		}
		else
		{
			return 0;
		}
	}

	getlength = getlength-str_temp.length();

	if (getlength != temp->publictitle.length())
		return 0;
	str_temp = str_temp + temp->publictitle;
	if (m.substr(0, str_temp.length()) == str_temp)
	{
		return 1;
	}
	else
	{
		return 0;
	}


}

void MPT()
{
	inode* temp = NULL;

	testMPT->publictitle = "46";
	testMPT->next_node[1] = new inode();
	testMPT->next_node[1]->pre = 2;
	testMPT->next_node[1]->leaf = 1;
	testMPT->next_node[1]->publictitle = "1355";
	testMPT->next_node[1]->wealth = 28;
	testMPT->next_node[15] = new inode();
	testMPT->next_node[15]->pre = 2;
	testMPT->next_node[15]->leaf = 9;
	testMPT->next_node[15]->publictitle = "8245";
	testMPT->next_node[15]->wealth = 2;
	testMPT->next_node[7] = new inode();
	temp = testMPT->next_node[7];

	temp->publictitle = "25";
	temp->next_node[3] = new inode();
	temp->next_node[3]->pre = 3;
	temp->next_node[3]->leaf = 9;
	temp->next_node[3]->publictitle = "7";
	temp->next_node[3]->wealth = 9;
	temp->next_node[9] = new inode();
	temp->next_node[9]->pre = 3;
	temp->next_node[9]->leaf = 9;
	temp->next_node[9]->publictitle = "7";
	temp->next_node[9]->wealth = 5;

	delete temp;
}

int main()
{
	MPT();
//测试结点为46f8245 2
	cout << "46f8245,";

	if (check("46f8245") != 0 ) {
		cout << "成功";
	}
	else cout << "失败";

	return 0;
}