#ifndef MY_TIMER_H_
#define MY_TIMER_H_

#include<chrono>

class mytimer
{
private:
    std::chrono::steady_clock::time_point _begin;//��ʼʱ��
    std::chrono::steady_clock::time_point _end;//��ֹʱ��
public:
    mytimer()
    {
        _begin = std::chrono::steady_clock::time_point();
        _end = std::chrono::steady_clock::time_point();
    }

    virtual ~mytimer() {};

    //����updateʱ��ʹ��ʼʱ����ڵ�ǰʱ��
    void UpDate()
    {
        _begin = std::chrono::steady_clock::now();
    }

    //����getsecond����ʱ��������ʱ��Ϊ��ǰʱ���ȥ֮ǰͳ�ƹ�����ʼʱ�䡣
    double GetSecond()
    {
        _end = std::chrono::steady_clock::now();
        //ʹ��duration���ͱ�������ʱ��Ĵ���   duration_cast������ת������
        std::chrono::duration<double> temp = std::chrono::duration_cast<std::chrono::duration<double>>(_end - _begin);
        return temp.count();//count() ��ȡ��ǰʱ��ļ�������
    }
};

#endif