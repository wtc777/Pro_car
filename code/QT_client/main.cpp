#include "CarOperW.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    CarOperW w;
    w.show();

    return a.exec();
}
