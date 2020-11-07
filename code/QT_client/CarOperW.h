#ifndef CAROPERW_H
#define CAROPERW_H

#include <QMainWindow>
#include <QTcpSocket>
class QEvent;
namespace Ui {
class CarOperW;
}

class CarOperW : public QMainWindow
{
    Q_OBJECT

public:
    explicit CarOperW(QWidget *parent = nullptr);
    ~CarOperW();

private slots:
    void on_pb_sendmsg_clicked();

    void forward_clicked();

    void left_clicked();

    void right_clicked();

    void back_clicked();

    void on_pb_maxspeed_clicked();

    void on_pb_midspeed_clicked();

    void on_pb_minspeed_clicked();

    void stopCar();
    void on_pb_automode_clicked();

    void on_pb_traceon_clicked();

protected:
    void keyPressEvent(QKeyEvent* ev);
    void keyReleaseEvent(QKeyEvent* ev);
    bool eventFilter(QObject* ob, QEvent* ev);
private:
    Ui::CarOperW *ui;
    QTcpSocket* m_tcpsocket;
    bool keypressflag;
    bool traceon;
    bool automode;
};

#endif // CAROPERW_H
