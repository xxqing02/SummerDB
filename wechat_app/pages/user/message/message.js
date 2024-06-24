// pages/user/message/message.js
Page({
    data: {
        username:"",
        message :[],
        statusBarHeight: wx.getStorageSync('statusBarHeight'),
        navigationBarHeight: wx.getStorageSync('navigationBarHeight'),
        menuButtonHeight: wx.getStorageSync('menuButtonHeight'),
        navigationBarAndStatusBarHeight:
                wx.getStorageSync('statusBarHeight') +
                wx.getStorageSync('navigationBarHeight'),
      },
    
      onLoad(options) {
        this.username = wx.getStorageSync('username');
        this.fetchMessage();
      },
    
      onShow() {
    
      },
      
      fetchMessage: function() {
        var that = this;
        wx.request({
            url    : 'https://app6321.acapp.acwing.com.cn/user_message/',
            method : 'GET',
            data   : {
                username: that.username,
            },
            success: function(res) {
                that.setData({
                    message: res.data
                });
            }
        });
    },

    showMessage: function(event) {
        const id = event.currentTarget.dataset.id;
        const message = this.data.message.find(item => item.id === id);
        if (message) {
          wx.showModal({
            title: message.title,
            content: message.content,
            showCancel: false
          });
        }
        
        //设置为已读
        wx.request({
            url    : 'https://app6321.acapp.acwing.com.cn/user_message/',
            method : 'GET',
            data   : {
                message_id: message.id
            },
        });
    },

    goBack: function() {
        wx.navigateBack({
            delta: 1 
        });
    }
  
})