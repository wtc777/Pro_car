//index.js
//获取应用实例
const app = getApp()

Page({
  /*全局变量*/
  data: {
    ip : "http://192.168.43.37",
    autoMode:false,//手自动模式标志，True 自动，false 手动
    traceon:false,//寻迹模式开启状态，True 开启中，false 禁用中
    //手自动按钮透明度，文本变量
    opacityMode:0.3,/*透明度*/
    ModeText:'手动模式',
    //寻迹按钮透明度，文本变量
    opacityTrace:0.3,/*透明度*/
    TraceText:'开寻迹',
    //连接按钮透明度，点击次数变量
    opacityCon:0.3,/*透明度*/
    counterCon:0,/*连接按钮点击计数*/
    connectText:'未连接',
    //红灯按钮透明度，点击次数变量
    opacityRed:0.3,
    counterRed:0,
    RedText:'开红灯',
    //绿灯按钮透明度，点击次数变量
    opacityGreen:0.3,
    counterGreen:0,
    GreenText:'开绿灯',
    //蓝灯按钮透明度，点击次数变量
    opacityBlue:0.3,
    counterBlue:0,
    BlueText:'开蓝灯',
    //蜂鸣器按钮透明度，点击次数变量
    opacityBeep:0.3,
    counterBeep:0,
    BeepText:'开蜂鸣',
    //小车前进按钮透明度，点击次数，文本
    opacityForward:0.3,
    counterForward:0,
    ForwardText:'小车前进',
    //小车后退按钮透明度，点击次数，文本
    opacityBack:0.3,
    counterBack:0,
    BackText:'小车后退',
    //小车右转按钮透明度，点击次数，文本
    opacityRight:0.3,
    counterRight:0,
    RightText:'小车右转',
    //小车左转按钮透明度，点击次数，文本
    opacityLeft:0.3,
    counterLeft:0,
    LeftText:'小车左转',
    //小车高速按钮透明度，点击次数，文本
    opacityMaxspeed:0.3,
    counterMaxspeed:0,
    MaxspeedText:'高速',
    //小车中速按钮透明度，点击次数，文本
    opacityMidspeed:0.3,
    counterMidspeed:0,
    MidspeedText:'中速',
    //小车低速按钮透明度，点击次数，文本
    opacityMinspeed:0.3,
    counterMinspeed:0,
    MinspeedText:'低速',
  },
  connectPi:function(){
    this.data.counterCon++
    console.log('counterCon:',this.data.counterCon)
    if(this.data.counterCon%2){
      //连接树莓派服务器
      wx.request({
        url: this.data.ip + ':8800?connect=1', //树莓派服务器地址端口及发送的数据
        success (res) {
          console.log(res.data)
        }
      })
      this.setData({
        opacityCon:1,  //设置透明度为1---100%
        connectText:'已连接'
      })
    }else{
      //连接树莓派服务器发送信息
      wx.request({
        url: this.data.ip + ':8800?connect=0', //树莓派服务器地址端口及发送的数据
        success (res) {
          console.log(res.data)
        }
      })
      this.setData({
        opacityCon:0.3,  //设置透明度为0.3---30%
        connectText:'未连接'
      })
    }
  },
  RedLed:function(){
    this.data.counterRed++
    if(this.data.counterRed%2){   
      wx.request({
        url: this.data.ip + ':8800?Redon=1', //树莓派服务器地址端口及发送的数据
        success (res) {
          console.log(res.data)
        }
      })   
      this.setData({//连接成功显示亮色
        opacityRed:1,  //设置透明度为1---100%
        RedText:'关红灯'
      })
    }else{
      wx.request({
        url: this.data.ip + ':8800?Redon=0', //树莓派服务器地址端口及发送的数据
        success (res) {
          console.log(res.data)
        }
      })
      this.setData({//断开连接显示暗色
        opacityRed:0.3,  //设置透明度为0.3---30%
        RedText:'开红灯'
      })
    }
  },
  GreenLed:function(){
    this.data.counterGreen++
    if(this.data.counterGreen%2){
      wx.request({
        url: this.data.ip + ':8800?Greenon=1', //树莓派服务器地址端口及发送的数据
        success (res) {
          console.log(res.data)
        }
      })
      this.setData({
        opacityGreen:1,  //设置透明度为1---100%
        GreenText:'关绿灯'
      })
    }else{
      wx.request({
        url: this.data.ip + ':8800?Greenon=0', //树莓派服务器地址端口及发送的数据
        success (res) {
          console.log(res.data)
        }
      })
      this.setData({
        opacityGreen:0.3,  //设置透明度为0.3---30%
        GreenText:'开绿灯'
      })
    }
  },
  BlueLed:function(){
    this.data.counterBlue++
    if(this.data.counterBlue%2){
      wx.request({
        url: this.data.ip + ':8800?Blueon=1', //树莓派服务器地址端口及发送的数据
        success (res) {
          console.log(res.data)
        }
      })
      this.setData({
        opacityBlue:1,  //设置透明度为1---100%
        BlueText:'关蓝灯'
      })
    }else{
      wx.request({
        url: this.data.ip + ':8800?Blueon=0', //树莓派服务器地址端口及发送的数据
        success (res) {
          console.log(res.data)
        }
      })
      this.setData({
        opacityBlue:0.3,  //设置透明度为0.3---30%
        BlueText:'开蓝灯'
      })
    }
  },
  Beep:function(){
    this.data.counterBeep++
    if(this.data.counterBeep%2){
      wx.request({
        url: this.data.ip + ':8800?Beepon=1', //树莓派服务器地址端口及发送的数据
        success (res) {
          console.log(res.data)
        }
      })
      this.setData({
        opacityBeep:1,  //设置透明度为1---100%
        BeepText:'关蜂鸣'
      })
    }else{
      wx.request({
        url: this.data.ip + ':8800?Beepon=0', //树莓派服务器地址端口及发送的数据
        success (res) {
          console.log(res.data)
        }
      })
      this.setData({
        opacityBeep:0.3,  //设置透明度为0.3---30%
        BeepText:'开蜂鸣'
      })
    }
  },
  //小车马达控制函数 
  Forward:function(){
    if (this.data.autoMode == true){//自动模式，禁用该函数
      return
    }
    wx.request({
      url: this.data.ip + ':8800?forward=1', //树莓派服务器地址端口及发送的数据
      success (res) {
        console.log(res.data)
      }
    })
      this.setData({
        opacityForward:1,  //设置透明度为1---100%
        ForwardText:'小车前进中'
      })
  },  
  Back:function(){
    if (this.data.autoMode == true){//自动模式，禁用该函数
      return
    }
    wx.request({
      url: this.data.ip + ':8800?back=1', //树莓派服务器地址端口及发送的数据
      success (res) {
        console.log(res.data)
      }
    })
      this.setData({
        opacityBack:1,  //设置透明度为1---100%
        BackText:'小车后退中'
      })
  },  
  Left:function(){
    if (this.data.autoMode == true){//自动模式，禁用该函数
      return
    }
    wx.request({
      url: this.data.ip + ':8800?turnleft=1', //树莓派服务器地址端口及发送的数据
      success (res) {
        console.log(res.data)
      }
    })
      this.setData({
        opacityLeft:1,  //设置透明度为1---100%
        LeftText:'小车左转中'
      })
  },  
  Right:function(){
    if (this.data.autoMode == true){//自动模式，禁用该函数
      return
    }
    wx.request({
      url: this.data.ip + ':8800?turnright=1', //树莓派服务器地址端口及发送的数据
      success (res) {
        console.log(res.data)
      }
    })
      this.setData({
        opacityRight:1,  //设置透明度为1---100%
        RightText:'小车右转中'
      })
  },  
  StopCar:function(){
    if (this.data.autoMode == true){
      return
    }
    wx.request({
      url: this.data.ip + ':8800?stopcar=1', //树莓派服务器地址端口及发送的数据
      success (res) {
        console.log(res.data)
      }
    }) 
    this.setData({
      opacityForward:0.3,  //设置透明度为1---100%
      ForwardText:'小车前进',
      opacityBack:0.3,  //设置透明度为1---100%
      BackText:'小车后退',
      opacityLeft:0.3,  //设置透明度为1---100%
      LeftText:'小车左转',
      opacityRight:0.3,  //设置透明度为1---100%
      RightText:'小车右转',
    })   
  },
  Maxspeed:function(){
    wx.request({
      url: this.data.ip + ':8800?maxspeed', //树莓派服务器地址端口及发送的数据
      success (res) {
        console.log(res.data)
      }
    }) 
    this.setData({
      opacityMaxspeed:1,
      opacityMidspeed:0.3,  
      opacityMinspeed:0.3,  
    })   
  },
  Midspeed:function(){
    wx.request({
      url: this.data.ip + ':8800?midspeed', //树莓派服务器地址端口及发送的数据
      success (res) {
        console.log(res.data)
      }
    }) 
    this.setData({
      opacityMaxspeed:0.3,
      opacityMidspeed:1,  
      opacityMinspeed:0.3,  
    })   
  },
  Minspeed:function(){
    wx.request({
      url: this.data.ip + ':8800?minspeed', //树莓派服务器地址端口及发送的数据
      success (res) {
        console.log(res.data)
      }
    }) 
    this.setData({
      opacityMaxspeed:0.3,
      opacityMidspeed:0.3,  
      opacityMinspeed:1,  
    })   
  },
  SetMode:function(){
    if(this.data.autoMode == true){//自动模式下切换为手动模式
      //如果寻迹开启中则先关闭寻迹
      if(this.data.traceon == true){
        this.Trace()
        setTimeout(this.SetModeoff, 500)
      }else{
        this.SetModeoff()
      }
      
    }else{
      wx.request({
        url: this.data.ip + ':8800?automode=1', //树莓派服务器地址端口及发送的数据
        success (res) {
          console.log(res.data)
        }
      }) 
      this.setData({
        opacityMode:1,
        ModeText:"自动模式",
        autoMode:true
      })
    }    
  },
  SetModeoff: function(){
    wx.request({
      url: this.data.ip + ':8800?automode=0', //树莓派服务器地址端口及发送的数据
      success (res) {
        console.log(res.data)
      }
    }) 
    this.setData({
      opacityMode:0.3,
      ModeText:"手动模式",
      autoMode:false
    })
  },
  Trace:function(){
    if(this.data.autoMode == false){//手动模式下禁用该按钮
      return
    }
    if(this.data.traceon == true){//开启中则关闭寻迹模式
      wx.request({
        url: this.data.ip + ':8800?traceon=0', //树莓派服务器地址端口及发送的数据
        success (res) {
          console.log(res.data)
        }
      }) 
      this.setData({
        opacityTrace:0.3,
        TraceText:"开寻迹",
        traceon:false
      })
    }else{//关闭中则开启寻迹模式
      wx.request({
        url: this.data.ip + ':8800?traceon=1', //树莓派服务器地址端口及发送的数据
        success (res) {
          console.log(res.data)
        }
      }) 
      this.setData({
        opacityTrace:1,
        TraceText:"关寻迹",
        traceon:true
      })
    }  
  },
})

