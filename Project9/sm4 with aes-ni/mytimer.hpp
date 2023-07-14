#ifndef MY_TIMER_H_
#define MY_TIMER_H_

#include<chrono>

class mytimer
{
private:
    std::chrono::steady_clock::time_point _begin;
    std::chrono::steady_clock::time_point _end;
public:
    mytimer()
    {
        _begin = std::chrono::steady_clock::time_point();
        _end = std::chrono::steady_clock::time_point();
    }

    virtual ~mytimer() {};


    void UpDate()
    {
        _begin = std::chrono::steady_clock::now();
    }

    double GetSecond()
    {
        _end = std::chrono::steady_clock::now();

        std::chrono::duration<double> temp = std::chrono::duration_cast<std::chrono::duration<double>>(_end - _begin);
        return temp.count();
    }
};

#endif