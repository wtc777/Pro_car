#include <unistd.h>
#include "CarOperW.h"
#include "ui_CarOperW.h"
#include <QHostAddress>
#include <QHostInfo>
#include <QDebug>
#include <QMessageBox>
#include <QKeyEvent>
CarOperW::CarOperW(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::CarOperW),
    keypressflag(false),
    traceon(false)
{
    ui->setupUi(this);
    //创建客户端套接字
    this->m_tcpsocket = new QTcpSocket(this);
    //连接服务器
    this->m_tcpsocket->connectToHost(QHostAddress("192.168.137.42"),8800);
    /*
    QString hostaddrname = "raspberrypi.local";
    QHostInfo info = QHostInfo::fromName(hostaddrname);
    if(info.addresses().size()<=0){
        qDebug()<<"IP address:"<<info.addresses().size();
    }else{
        qDebug()<<hostaddrname<<info.addresses().at(1).toString();
        QString hostip = info.addresses().at(1).toString();
        this->m_tcpsocket->connectToHost(hostip,8800);
    }*/
}

CarOperW::~CarOperW()
{
    delete ui;
}

void CarOperW::on_pb_sendmsg_clicked()
{
    QString text = ui->line_msg->text();
    if(text.isEmpty()){
        QMessageBox::warning(this,"send","发送的信息不能为空");
    }else{
        this->m_tcpsocket->write(text.toStdString().c_str(),text.size());
    }
}

void CarOperW::forward_clicked()
{
    QString text = "forward=1";
    this->m_tcpsocket->write(text.toStdString().c_str(),text.size());
}

void CarOperW::left_clicked()
{
    QString text = "turnleft=1";
    this->m_tcpsocket->write(text.toStdString().c_str(),text.size());
}

void CarOperW::right_clicked()
{
    QString text = "turnright=1";
    this->m_tcpsocket->write(text.toStdString().c_str(),text.size());
}

void CarOperW::back_clicked()
{
    QString text = "back=1";
    this->m_tcpsocket->write(text.toStdString().c_str(),text.size());
}

void CarOperW::on_pb_maxspeed_clicked()
{
    QString text = "maxspeed";
    this->m_tcpsocket->write(text.toStdString().c_str(),text.size());
}

void CarOperW::on_pb_midspeed_clicked()
{
    QString text = "midspeed";
    this->m_tcpsocket->write(text.toStdString().c_str(),text.size());
}

void CarOperW::on_pb_minspeed_clicked()
{
    QString text = "minspeed";
    this->m_tcpsocket->write(text.toStdString().c_str(),text.size());
}

void CarOperW::stopCar()
{
    QString text = "stopcar=1";
    this->m_tcpsocket->write(text.toStdString().c_str(),text.size());
}

void CarOperW::keyPressEvent(QKeyEvent *ev)
{
    if(ev->key() == Qt::Key_W){
        forward_clicked();
        qDebug()<<"up"<<keypressflag;
    }else if(ev->key() == Qt::Key_S){
        back_clicked();
        qDebug()<<"down"<<keypressflag;
    }else if(ev->key() == Qt::Key_A){
        left_clicked();
        qDebug()<<"left"<<keypressflag;
    }else if(ev->key() == Qt::Key_D){
        right_clicked();
        qDebug()<<"right"<<keypressflag;
    }
}

void CarOperW::keyReleaseEvent(QKeyEvent *ev)
{
    stopCar();
    qDebug()<<"release";
}

bool CarOperW::eventFilter(QObject *ob, QEvent *ev)
{
    return QWidget::eventFilter(ob, ev);
}

void CarOperW::on_pb_automode_clicked()
{
    if(this->automode == false){
        this->automode = true;
        QString text = "automode=1";
        ui->pb_automode->setText("自动模式");
        this->m_tcpsocket->write(text.toStdString().c_str(),text.size());
        qDebug()<<text;
    }else{
        if(this->traceon == true){
            on_pb_traceon_clicked();
        }
        usleep(500);
        this->automode = false;
        QString text = "automode=0";
        ui->pb_automode->setText("手动模式");
        this->m_tcpsocket->write(text.toStdString().c_str(),text.size());
        qDebug()<<text;

    }

}

void CarOperW::on_pb_traceon_clicked()
{
    if(this->traceon == false){
        this->traceon = true;
        QString text = "traceon=1";
        ui->pb_traceon->setText("禁用寻迹模式");
        this->m_tcpsocket->write(text.toStdString().c_str(),text.size());
        qDebug()<<text;
    }else{
        this->traceon = false;
        QString text = "traceon=0";
        ui->pb_traceon->setText("开启寻迹模式");
        this->m_tcpsocket->write(text.toStdString().c_str(),text.size());
        qDebug()<<text;
    }
}
