# 包烟复习：C +    +

1. 二维数组的申请和释放（我选择 `vector<vector<int>>`）

   ``` c++
   int** mat = new int* [N];
   for(int i = 0; i < N; i++){
       mat[i] = new int [M];
   }
   
   for(int i = 0; i < N; i++){
       delete [] mat[i];
   }
   delete [] mat;
   ```

2. 输入输出运算符的重载

   ```c++
   // 类内声明，friend
   class Date{
   public:
       Date(int y, int m, int d);
       friend ostream& operator << (ostream& out, const Date& x);
   	friend istream& operator >> (istream& in, Date& x);
   private:
       int year, month, day;  
   };
   
   
   // 类外实现，**不用加 Date::**
   ostream& operator << (ostream& out, const Date& x){
       out<<x.year<<"."<<x.month<<"."<<x.day;
       return out;
   }
   istream& operator >> (istream& in, const Date& x){
       in>>x.year>>x.month>>x.day;
       return in;
   }
   ```

3. a++ 和 ++a 的重载：

   ``` c++
   // ++a 参数为空，返回引用
   Date& Date::operator ++(){
       r += 1;
       return *this;
   }
   // a++ 参数为int
   Date Date::operator ++(int){
       Date before = *this;
       r += 1;
       return before;
   }
   ```

4. 类的继承：

   ``` c++
   class Rectangle: public Point{
       Rectangle(int a,int b,int c,int d): Point(a,b)
       { // 向基类构造函数传参
           length = c;
           width = d;
       }
   };
   ```

   1. 多继承 - 虚继承，使得在派生类中只保留一份间接基类的成员：`class C: public virtual A, B{};`

5. 函数重载、重写（覆盖）、隐藏之间的关系

   1. 重载：在一个类内，相同的函数名字，不同的参数列表  
   2. 重写：在派生类内重写基类的同名虚函数
   3. 隐藏：在派生类内隐藏基类的同名非虚函数

6. 多态：动态绑定，虚函数

   1. 使用虚函数实现动态绑定的关键：使用基类指针或基类引用来访问虚函数

7. 模板：函数模板和类模板

   ```c++
   template <typename T>
   void swap（T& v1,T& v2){
       T temp = v1;
       v1 = v2;
       v2 = temp;
   }
   ```

   ``` c++
   template <typename T, std::size_t N>
   class Stack{
       public:
       void push(T obj);
       private:
       T elements[N];
   }
   
   template <typename T, std::size_t N>
   void Stack<T>::push(T obj){
       
   }
   ```

8. **STL**
   
   1. `pair<int, string>`
   
      ```c++
      #include <iostream>
      #include <string>
      
      pair<int, string> p = make_pair(1, "Fu");
      cout<<p.first<<" "<<p.second<<endl;
      ```
   
   2. `list<int>`
   
      ``` c++
      #include <list>
      
      list<int> l;
      l.push_front(1);
      
      list<int>:: iterator i;
      for(i = l.begin(); i != l.end(); i++){
          int c = (*iter);
      }
      ```
   
   3. `deque<int>`
   
      ``` c++
      #include <deque>
      
      int iarr[] = {1, 2, 3, 4, 5};
      deque<int> deq(iarr, iarr + 5);
      deque<int>::iterator iter;
      
      deq.pop_back();
      deq.pop_front();
      
      iter = ideq.begin() 1 
      ideq.erase(iter, iter + 2);
      
      if(!deq.empty()){
          ideq.clear();
      }
      ```
   
   4. `map<char, int>`
   
      ``` c++
      #include <map>
      
      map<char, int> m;
      m.insert(make_pair('a', 0));
      
      map<char, int>::iterator p = m.find('b');
      if(p != m.end){
          cout<<"find"<<endl;
      }
      ```
   
   5. `set<int>`
   
      ``` c++
      #include <set>
      
      set<int> s;
      s.insert(1);
      s.insert(2);
      s.insert(3);
      
      s.erase(s.find(2), s.find(3));
      ```
   
   6. `priority_queue<int>`
   
      ``` c++
      #include <queue>
      
      priority_queue <int> q;
      priority_queue <int, vector<int>, greater<int>> qq;
      priority_queue <int, vector<int>, less<int>> ql;
      
      q.push(1);
      while(!q.empty()){
          int t = q.top;
          q.pop();
      }
      ```
   

## Liitcode [Done!]

* 水果类：输入输出重载 https://matrix.sysu.edu.cn/course/private/214/assignment/10324

* 分数类：运算符重载 https://matrix.sysu.edu.cn/course/private/214/assignment/10359
* 圆和长方体类：继承 https://matrix.sysu.edu.cn/course/private/214/assignment/12197
* 园、三角和长方体类：虚函数 https://matrix.sysu.edu.cn/course/private/214/assignment/12278
* 栈类：类模板 https://matrix.sysu.edu.cn/course/private/214/assignment/12397

```c++
#include "fraction.h"
#include <iostream>
 
#define _num _numerator
#define _den _denominator
 
int fraction::gcd(const int & a, const int & b) const {
    if (b != 0)
        return gcd(b, a % b);
    return a;
}
 
void fraction::simp() {
    if (_den != 0) {
        if (_num == 0) {
            _den = 1;
        } else {
            int g = gcd(_num, _den);
            _num /= g;
            _den /= g;
            if (_den < 0) {
                _num *= -1;
                _den *= -1;
            }
        }
    }
}
 
fraction::fraction(const int & num, const int & den)
    : _num(num), _den(den) {
    simp();
}
 
fraction::fraction(const fraction &another)
    : _num(another._num), _den(another._den) {}
 
void fraction::operator=(const fraction & another) {
    _num = another._num;
    _den = another._den;
}
 
fraction fraction::operator+(const fraction & right) const {
    if (_den == 0 || right._den == 0)
        return fraction(0, 0);
    int lcm = _den / gcd(_den, right._den) * right._den;
    int l = lcm / _den, r = lcm / right._den;
    return fraction(_num * l + right._num * r, lcm);
}
 
fraction fraction::operator-(const fraction & right) const {
    return *this + fraction(-1 * right._num, right._den);
}
 
fraction fraction::operator*(const fraction & right) const {
    if (_den == 0 || right._den == 0)
        return fraction(0, 0);
    int g1 = gcd(_num, right._den), g2 = gcd(_den, right._num);
    return fraction((_num / g1) * (right._num / g2),
                    (_den / g2) * (right._den / g1));
}
 
fraction fraction::operator/(const fraction & right) const {
    return *this * fraction(right._den, right._num);
}
 
void fraction::operator+=(const fraction & right) {
    *this = *this + right;
}
 
void fraction::operator-=(const fraction & right) {
    *this = *this - right;
}
 
void fraction::operator*=(const fraction & right) {
    *this = *this * right;
}
 
void fraction::operator/=(const fraction & right) {
    *this = *this / right;
}
 
bool fraction::operator==(const fraction & right) const {
    return _den == 0 && right._den == 0 ||
           _den == right._den && _num == right._num;
}
 
bool fraction::operator!=(const fraction & right) const {
    return !(*this == right);
}
 
bool fraction::operator<(const fraction & right) const {
    return _num * right._den < _den * right._num;
}
 
bool fraction::operator>(const fraction & right) const {
    return _num * right._den > _den * right._num;
}
 
bool fraction::operator<=(const fraction & right) const {
    return !(*this > right);
}
 
bool fraction::operator>=(const fraction & right) const {
    return !(*this < right);
}
 
std::istream & operator>>(std::istream & is, fraction & f) {
    int n, d;
    is >> n >> d;
    f = fraction(n, d);
    return is;
}
 
std::ostream & operator<<(std::ostream & os, const fraction & f) {
    if (f._den == 0)
        os << "NaN";
    else if (f._den == 1)
        os << f._num;
    else
        os << f._num << '/' << f._den;
    return os;
}

```

```c++
#ifndef FRACTION_H
#define FRACTION_H

#include <iostream>

class fraction {
    private:
        int _numerator, _denominator;
        int gcd(const int &, const int &) const;
            // If you don't need this method, just ignore it.
        void simp();
            // To get the lowest terms.
    public:
        fraction(const int & = 0, const int & = 1);
            // The numerator and the denominator
            // fraction(5) = 5/1 = 5 :)
        fraction(const fraction &);
            // copy constructor

        void operator=(const fraction &);

        // You must know the meaning of +-*/, don't you ?
        fraction operator+(const fraction &) const;
        fraction operator-(const fraction &) const;
        fraction operator*(const fraction &) const;
        fraction operator/(const fraction &) const;

        void operator+=(const fraction &);
        void operator-=(const fraction &);
        void operator*=(const fraction &);
        void operator/=(const fraction &);

        // Comparison operators
        bool operator==(const fraction &) const;
        bool operator!=(const fraction &) const;
        bool operator<(const fraction &) const;
        bool operator>(const fraction &) const;
        bool operator<=(const fraction &) const;
        bool operator>=(const fraction &) const;

        friend std::istream & operator>>(std::istream &, fraction &);
            // Input Format: two integers with a space in it
            // "a b" is correct. Not "a/b"
        friend std::ostream & operator<<(std::ostream &, const fraction &);
            // Normally you should output "a/b" without any space and LF
            // Sometims you may output a single integer (Why? Guess XD)
            // If it is not a number (den = 0), output "NaN"
};

#endif


```



## Lmmtcode 

* 辗转相除求最大公约数

  ```c++
  int gcd(int a, int b){
      if (b != 0)
          return gcd(b, a % b);
      return a;
  }
  ```

* **二分算法**

* **排序算法**

* **搜索算法**：广搜 + 深搜

* **括号匹配** 

  * https://www.noobdream.com/DreamJudge/Issue/page/1067/

* **组合排列** 

  * https://www.noobdream.com/DreamJudge/Issue/page/1726/

* **拓扑排序** 

  * https://www.noobdream.com/DreamJudge/Issue/page/1566/